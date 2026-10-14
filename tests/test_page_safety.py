"""Security and failure-path regression coverage of the first-use executor."""
import json
import tempfile
import unittest
from typing import Any, cast
from test_onboarding import RegisteredHost
from test_expansion import plugin, snapshot, URL

TARGET = 'https://qaqc.newtecons.vn/#/nhat-ky-thi-cong/1/fixture/fixturegs'
GRANTS = {'allow_open_page': True, 'allow_new_tab': True}


class PageSafety(unittest.TestCase):
    def args(self, **kwargs):
        return dict(action='open_page',url=TARGET,mode='new',expected_project='Fixture Project',operation_id='safety',**kwargs)
    def test_unsafe_urls_never_call_browser(self):
        for url in ('http://qaqc.newtecons.vn/#/nhat-ky-thi-cong/1/fixture',
                    'https://qaqc.newtecons.vn.evil.test/#/nhat-ky-thi-cong/1/fixture',
                    'https://user:pass@qaqc.newtecons.vn/#/nhat-ky-thi-cong/1/fixture',
                    'https://qaqc.newtecons.vn/?token=fixture',
                    'https://qaqc.newtecons.vn/#/unmapped/fixture'):
            with self.subTest(url=url), tempfile.TemporaryDirectory() as root:
                h=RegisteredHost(root,settings=GRANTS);plugin.register(h)
                r=h.invoke(**{**self.args(),'url':url})
                self.assertFalse(r['ok']);self.assertEqual(h.calls,[])
    def test_binding_project_and_grants_fail_before_browser(self):
        cases=[({'expected_user_display_name':''},{},'pending_user_binding'),
               ({},{'expected_project':''},'pending_project_selection'),
               ({'allow_open_page':False},{},'page_open_not_authorized'),
               ({'allow_new_tab':False},{},'new_tab_not_authorized')]
        for settings,args,status in cases:
            with self.subTest(status=status),tempfile.TemporaryDirectory() as root:
                h=RegisteredHost(root,settings={**GRANTS,**settings});plugin.register(h)
                r=h.invoke(**{**self.args(),**args})
                self.assertEqual(r['status'],status);self.assertEqual(h.calls,[])
    def test_invalid_ids_fields_and_modes_fail_before_browser(self):
        cases=[{'operation_id':'../fixture'}, {'mode':'unknown'}, {'page_id':1}, {'extra':'not-in-schema'}, {'expected_discipline':'UNKNOWN'}]
        for args in cases:
            with self.subTest(args=args),tempfile.TemporaryDirectory() as root:
                h=RegisteredHost(root,settings=GRANTS);plugin.register(h)
                r=h.invoke(**{**self.args(),**args})
                self.assertFalse(r['ok']);self.assertEqual(h.calls,[])
    def test_wrong_source_account_or_project_blocks_reuse_before_navigation(self):
        for text in (snapshot(project='Different Project'),snapshot().replace('Fixture User','Different User')):
            with self.subTest(text=text),tempfile.TemporaryDirectory() as root:
                h=RegisteredHost(root,['4: Fixture ('+URL+')',text],GRANTS);plugin.register(h)
                r=h.invoke(**{**self.args(),'mode':'reuse','page_id':4})
                self.assertFalse(r['ok']);self.assertNotIn('navigate_page',[x[0] for x in h.calls])
    def test_post_open_mismatch_or_denial_is_not_success_and_blocks_new_attempt(self):
        texts=[snapshot(project='Different Project').replace(URL,TARGET),
               snapshot().replace('Fixture User','Different User').replace(URL,TARGET),
               snapshot('  uid=8_0 StaticText "Không có quyền truy cập"\n').replace(URL,TARGET),
               snapshot().replace(URL,'https://qaqc.newtecons.vn/#/nhat-ky-thi-cong/1/other/other')]
        for text in texts:
            with self.subTest(text=text),tempfile.TemporaryDirectory() as root:
                h=RegisteredHost(root,['1: Fixture ('+URL+')','Created','1: Fixture ('+URL+')\n6: Diary ('+TARGET+')',text],GRANTS);plugin.register(h)
                r=h.invoke(**self.args());self.assertFalse(r['ok'])
                calls=len(h.calls);again=h.invoke(**{**self.args(),'operation_id':'another'})
                self.assertEqual(again['status'],'open_page_pending_no_replay');self.assertEqual(len(h.calls),calls)
    def test_concurrent_tabs_are_not_guessed(self):
        with tempfile.TemporaryDirectory() as root:
            h=RegisteredHost(root,['1: Fixture ('+URL+')','Created','1: Fixture ('+URL+')\n6: Diary ('+TARGET+')\n7: Diary ('+TARGET+')'],GRANTS);plugin.register(h)
            r=h.invoke(**self.args());self.assertEqual(r['status'],'new_page_identity_unverified')
            self.assertNotIn('take_snapshot',[x[0] for x in h.calls])
    def test_transport_refusal_never_retries_creation(self):
        with tempfile.TemporaryDirectory() as root:
            h=RegisteredHost(root,['1: Fixture ('+URL+')'],GRANTS);base=h.call_mcp
            def call(server,tool,arguments,timeout=15):
                if tool=='new_page':
                    h.calls.append((tool,arguments));return {'ok':False,'error':'fixture refusal'}
                return base(server,tool,arguments,timeout)
            h.call_mcp=call;plugin.register(h)
            r=h.invoke(**self.args());self.assertEqual(r['status'],'host_mcp_blocked_or_failed')
            again=h.invoke(**{**self.args(),'operation_id':'another'});self.assertEqual(again['mcp_calls'],0)
            self.assertEqual([x[0] for x in h.calls].count('new_page'),1)
    def test_status_scope_mismatch_never_calls_browser(self):
        with tempfile.TemporaryDirectory() as root:
            h=RegisteredHost(root,settings=GRANTS);plugin.register(h)
            r=h.invoke(action='open_page_status',operation_id='missing',expected_project='Fixture Project')
            self.assertEqual(r['status'],'page_open_scope_mismatch');self.assertEqual(h.calls,[])
    def test_old_status_cannot_clear_another_pending_attempt(self):
        with tempfile.TemporaryDirectory() as root:
            final=snapshot().replace(URL,TARGET)
            h=RegisteredHost(root,['1: Fixture ('+URL+')','Created','1: Fixture ('+URL+')\n6: Diary ('+TARGET+')',final,final],GRANTS);plugin.register(h)
            self.assertTrue(h.invoke(**self.args())['ok'])
            h.state.set('page_open_active',{'status':'pending_no_replay','operation_id':'other'})
            r=h.invoke(action='open_page_status',operation_id='safety',expected_project='Fixture Project')
            self.assertTrue(r['ok']);self.assertEqual(cast(dict,h.state.get('page_open_active'))['operation_id'],'other')
    def test_successful_operation_id_is_not_reused(self):
        with tempfile.TemporaryDirectory() as root:
            h=RegisteredHost(root,['1: Fixture ('+URL+')','Created','1: Fixture ('+URL+')\n6: Diary ('+TARGET+')',snapshot().replace(URL,TARGET)],GRANTS);plugin.register(h)
            self.assertTrue(h.invoke(**self.args())['ok'])
            again=h.invoke(**self.args());self.assertEqual(again['status'],'operation_id_already_used_no_replay');self.assertEqual(again['mcp_calls'],0)
    def test_legacy_host_without_prompt_sections_keeps_hook_and_skills(self):
        with tempfile.TemporaryDirectory() as root:
            h=RegisteredHost(root);cast(Any,h).register_system_prompt_section=None;plugin.register(h)
            self.assertEqual(set(h.skills),{'setup','operations','tasks'})
            self.assertIn('prepare',h.hooks['pre_llm_call']()['context'])
            self.assertEqual(h.calls,[])


if __name__=='__main__':
    unittest.main()

"""Recipient first-use contracts; browser replies are synthetic, never live records."""
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any, cast
from test_expansion import plugin, Host, snapshot, URL


class RegisteredHost(Host):
    def __init__(self, root, outputs=(), settings=None):
        super().__init__(root, outputs)
        self.settings = settings or {}
        self.tools, self.hooks, self.skills, self.sections = {}, {}, {}, {}
    def get_config(self, key, default=None):
        return self.settings.get(key, super().get_config(key, default))
    def register_tool(self, **kwargs):
        self.tools[kwargs['name']] = kwargs
    def register_hook(self, name, fn):
        self.hooks[name] = fn
    def register_skill(self, name, path, **kwargs):
        self.skills[name] = path
    def register_system_prompt_section(self, name, content, **kwargs):
        self.sections[name] = content
    def invoke(self, **args):
        return json.loads(self.tools['qaqc_fast_session']['handler'](args, session_id='recipient-fixture'))


class FirstUse(unittest.TestCase):
    def test_failed_mcp_is_attempted_not_claimed_browser_checked(self):
        with tempfile.TemporaryDirectory() as root:
            host=RegisteredHost(root)
            host.call_mcp=lambda *a,**kw:{'ok':False,'error':'fixture refusal'}
            plugin.register(host)
            result=host.invoke(action='pages')
            self.assertFalse(result['guidance']['browser_checked'])
            self.assertTrue(result['guidance'].get('browser_call_attempted'))

    def test_reuse_already_at_target_is_verified_without_navigation(self):
        target = 'https://qaqc.newtecons.vn/#/nhat-ky-thi-cong/1/fixture/fixturegs'
        final = snapshot().replace(URL,target)
        with tempfile.TemporaryDirectory() as root:
            host = RegisteredHost(root,['4: Diary ('+target+')',final],{'allow_open_page':True})
            plugin.register(host)
            result = host.invoke(action='open_page',url=target,mode='reuse',page_id=4,expected_project='Fixture Project',operation_id='no-op')
            self.assertTrue(result['ok'],result)
            self.assertTrue(result.get('navigation_noop'),result)
            self.assertNotIn('navigate_page',[c[0] for c in host.calls])

    def test_pending_state_is_rechecked_after_acquiring_controller_lock(self):
        target = 'https://qaqc.newtecons.vn/#/nhat-ky-thi-cong/1/fixture/fixturegs'
        with tempfile.TemporaryDirectory() as root:
            host = RegisteredHost(root, (), {'allow_open_page': True, 'allow_new_tab': True})
            class Lock:
                def acquire(self, **kw):
                    host.state.set('page_open_active', {'status':'pending_no_replay','operation_id':'other'})
                    return True
                def release(self):
                    pass
            saved = cast(Any,plugin)._LOCK
            cast(Any,plugin)._LOCK = Lock()
            try:
                plugin.register(host)
                result = host.invoke(action='open_page',url=target,mode='new',expected_project='Fixture Project',operation_id='race')
                self.assertEqual(result['status'], 'open_page_pending_no_replay', result)
                self.assertEqual(host.calls, [])
            finally:
                cast(Any,plugin)._LOCK = saved

    def test_reuse_timeout_retains_owned_page_id_for_read_only_reconciliation(self):
        target = 'https://qaqc.newtecons.vn/#/nhat-ky-thi-cong/1/fixture/fixturegs'
        with tempfile.TemporaryDirectory() as root:
            host = RegisteredHost(root, ['4: Fixture ('+URL+')', snapshot(), snapshot().replace(URL,target)], {'allow_open_page': True})
            base = host.call_mcp
            def call(server, tool, arguments, timeout=15):
                if tool=='navigate_page':
                    host.calls.append((tool,arguments))
                    return {'ok':False,'error':'synthetic uncertain transport'}
                return base(server,tool,arguments,timeout)
            host.call_mcp = call
            plugin.register(host)
            result = host.invoke(action='open_page', url=target, mode='reuse', page_id=4, expected_project='Fixture Project', operation_id='reuse-timeout')
            self.assertEqual(result['status'], 'host_mcp_blocked_or_failed', result)
            checked = host.invoke(action='open_page_status', operation_id='reuse-timeout', expected_project='Fixture Project')
            self.assertTrue(checked['ok'], checked)
            self.assertEqual(checked['page_id'], 4)
            self.assertEqual([c[0] for c in host.calls].count('navigate_page'), 1)

    def test_open_grants_and_schema_are_consistent_with_safe_defaults(self):
        text = (Path(__file__).parents[1]/'plugin.yaml').read_text(encoding='utf-8')
        self.assertIn('version: 0.2.0-rc.3', text)
        self.assertIn('allow_open_page:', text)
        self.assertIn('allow_new_tab:', text)
        example = json.loads((Path(__file__).parents[1]/'connector.example.json').read_text(encoding='utf-8'))
        self.assertIn('new_page', example['mcp_servers']['chrome_qaqc']['tools']['include'])
        self.assertFalse(example['plugins']['entries']['qaqc-fast']['settings']['allow_open_page'])
        self.assertFalse(example['plugins']['entries']['qaqc-fast']['settings']['allow_new_tab'])
        with tempfile.TemporaryDirectory() as root:
            host = RegisteredHost(root)
            plugin.register(host)
            decision = host.hooks['pre_tool_call'](tool_name='qaqc_fast_session',args={'action':'open_page'})
            self.assertEqual(decision['action'], 'approve')
            self.assertIn('tab', decision['message'])
            self.assertNotIn('Only plugin-owned', decision['message'])

    def test_login_pending_is_reconciled_read_only_without_second_open(self):
        target = 'https://qaqc.newtecons.vn/#/nhat-ky-thi-cong/1/fixture/fixturegs'
        login = 'uid=1_0 RootWebArea "Login" url="https://qaqc.newtecons.vn/"\n  uid=1_1 textbox "Password"\n'
        final = snapshot().replace(URL, target)
        with tempfile.TemporaryDirectory() as root:
            host = RegisteredHost(root, ['1: Fixture ('+URL+')', 'Created', '1: Fixture ('+URL+')\n6: Login (https://qaqc.newtecons.vn/)', login, final],
                                  {'allow_open_page': True, 'allow_new_tab': True})
            plugin.register(host)
            args = dict(url=target, mode='new', expected_project='Fixture Project', operation_id='login-fixture')
            result = host.invoke(action='open_page', **args)
            self.assertEqual(result['status'], 'pending_login', result)
            replay = host.invoke(action='open_page', **{**args, 'operation_id': 'do-not-replay'})
            self.assertEqual(replay['status'], 'open_page_pending_no_replay', replay)
            checked = host.invoke(action='open_page_status', operation_id='login-fixture', expected_project='Fixture Project')
            self.assertTrue(checked['ok'], checked)
            self.assertEqual(checked['page_id'], 6)
            self.assertEqual([x[0] for x in host.calls].count('new_page'), 1)
            self.assertEqual(host.calls[-1][0], 'take_snapshot')

    def test_bootstrap_root_is_separate_from_business_route_and_pages_exposes_it(self):
        site = 'https://qaqc.newtecons.vn/'
        with tempfile.TemporaryDirectory() as root:
            host = RegisteredHost(root, ['1: Home ('+site+')'])
            plugin.register(host)
            result = host.invoke(action='pages')
            self.assertEqual(result.get('bootstrap_pages'), [{'page_id': 1, 'url': site}], result)
            self.assertEqual(result['pages'], [])
        with tempfile.TemporaryDirectory() as root:
            host = RegisteredHost(root, ['1: Home ('+site+')', 'Created', '1: Home ('+site+')\n6: Home ('+site+')'],
                                  {'allow_open_page': True, 'allow_new_tab': True})
            plugin.register(host)
            result = host.invoke(action='open_page', url=site, mode='new', operation_id='bootstrap-fixture')
            self.assertEqual(result['status'], 'bootstrap_page_opened', result)
            self.assertFalse(result['business_verified'])
            self.assertFalse(result['project_verified'])
            self.assertEqual(result['page_id'], 6)

    def test_reuse_verifies_original_tab_and_never_overwrites_unrelated_origin(self):
        target = 'https://qaqc.newtecons.vn/#/nhat-ky-thi-cong/1/fixture/fixturegs'
        final = snapshot().replace(URL, target)
        with tempfile.TemporaryDirectory() as root:
            host = RegisteredHost(root, ['4: Fixture ('+URL+')', snapshot(), 'Navigated', final], {'allow_open_page': True})
            plugin.register(host)
            result = host.invoke(action='open_page', url=target, mode='reuse', page_id=4, expected_project='Fixture Project', operation_id='reuse-fixture')
            self.assertTrue(result['ok'], result)
            self.assertEqual(host.calls[2], ('navigate_page', {'pageId': 4, 'type': 'url', 'url': target, 'handleBeforeUnload': 'dismiss', 'timeout': 10000}))
        with tempfile.TemporaryDirectory() as root:
            host = RegisteredHost(root, ['4: Other (https://example.org/)'], {'allow_open_page': True})
            plugin.register(host)
            result = host.invoke(action='open_page', url=target, mode='reuse', page_id=4, expected_project='Fixture Project', operation_id='foreign-tab')
            self.assertEqual(result['status'], 'page_source_unverified', result)
            self.assertEqual([c[0] for c in host.calls], ['list_pages'])

    def test_new_diary_tab_preserves_literal_url_and_verifies_project(self):
        target = 'https://qaqc.newtecons.vn/#/nhat-ky-thi-cong/1/fixture/fixturegs'
        text = snapshot('  uid=8_0 heading "NHẬT KÝ THI CÔNG"\n').replace(URL, target)
        with tempfile.TemporaryDirectory() as root:
            host = RegisteredHost(root, ['1: Fixture ('+URL+')', 'Created page', '1: Fixture ('+URL+')\n9: Diary ('+target+') [selected]', text],
                                  {'allow_open_page': True, 'allow_new_tab': True})
            plugin.register(host)
            result = host.invoke(action='open_page', url=target, mode='new', expected_project='Fixture Project',
                                 destination_heading='NHẬT KÝ THI CÔNG', operation_id='open-fixture')
            self.assertTrue(result['ok'], result)
            self.assertEqual(result['page_id'], 9)
            self.assertTrue(result['project_verified'])
            self.assertTrue(result['heading_verified'])
            self.assertFalse(result['data_ready_verified'])
            self.assertEqual(host.calls[1], ('new_page', {'url': target, 'background': True, 'timeout': 10000}))
            self.assertEqual(host.calls[-1][1]['pageId'], 9)

    def test_fresh_registration_supplies_purpose_task_skill_and_frozen_context(self):
        with tempfile.TemporaryDirectory() as root:
            host = RegisteredHost(root)
            plugin.register(host)
            self.assertIn('tasks', host.skills)
            self.assertTrue(host.skills['tasks'].is_file())
            context = '\n'.join(host.sections.values())
            self.assertIn('nhật ký', context.lower())
            self.assertIn('prepare', context)
            self.assertIn('open_page', context)
            self.assertIn('qaqc-fast:tasks', context)
            self.assertIn('prepare', host.tools['qaqc_fast_session']['schema']['description'])
            self.assertEqual(host.calls, [])

    def test_prepare_reports_missing_binding_without_browser_and_without_inventing_destination_failure(self):
        with tempfile.TemporaryDirectory() as root:
            host = RegisteredHost(root, settings={'expected_user_display_name': ''})
            plugin.register(host)
            result = host.invoke(action='prepare')
            self.assertEqual(result['status'], 'pending_user_binding', result)
            self.assertEqual(host.calls, [])
            self.assertEqual(result['mcp_calls'], 0)
            self.assertFalse(result['browser_checked'])
            self.assertFalse(result['destination_checked'])
            self.assertIn('qaqc-fast:setup', result['guidance']['load_skills'])
            self.assertIn('expected_user_display_name', result['missing'])


if __name__ == '__main__':
    unittest.main()

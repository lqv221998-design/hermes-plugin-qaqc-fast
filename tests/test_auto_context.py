"""Automatic observed context: no manual name or project for basic QAQC use."""
import tempfile
import unittest
from test_onboarding import RegisteredHost
from test_expansion import plugin, snapshot, URL


class AutoHost(RegisteredHost):
    def get_config(self,key,default=None):
        return self.settings.get(key,default)


class AutoContext(unittest.TestCase):
    def test_auto_native_uses_only_same_session_owned_handoff_scope(self):
        import time
        with tempfile.TemporaryDirectory() as root:
            h=AutoHost(root);plugin.register(h)
            h.state.set('native_handoff',{'token':'owned','session_id':'recipient-fixture','project':'Fixture Project','user':'Fixture User','captured_at':time.time(),'sha256':'a'*64})
            args=dict(action='native_step',page_id=1,handoff_token='owned',reviewed_capture_sha256='b'*64)
            self.assertEqual(h.invoke(**args)['status'],'native_capture_review_required')
            h.state.values['native_handoff']['session_id']='someone-else'
            self.assertEqual(h.invoke(**args)['status'],'native_handoff_scope_mismatch')
            self.assertEqual(h.calls,[])

    def test_prepare_reports_real_import_failure_not_only_present_specs(self):
        from unittest.mock import patch
        import sys
        module=sys.modules[plugin.prepare.__module__]
        with tempfile.TemporaryDirectory() as root,patch.object(module,'import_module',side_effect=ImportError('synthetic missing native dependency'),create=True):
            h=AutoHost(root);plugin.register(h)
            r=h.invoke(action='prepare')
            self.assertFalse(r.get('dependency_imports',{}).get('openpyxl',{}).get('ok',True),r)
            self.assertEqual(r['dependency_imports']['openpyxl']['error_type'],'ImportError')
            self.assertEqual(h.calls,[])

    def test_default_manifest_and_example_have_no_required_identity(self):
        import json
        from pathlib import Path
        root=Path(__file__).resolve().parents[1]
        manifest=(root/'plugin.yaml').read_text(encoding='utf-8')
        self.assertIn('context_policy:',manifest)
        self.assertNotIn('required: true',manifest)
        settings=json.loads((root/'connector.example.json').read_text(encoding='utf-8'))['plugins']['entries']['qaqc-fast']['settings']
        self.assertEqual(settings['context_policy'],'auto')
        self.assertNotIn('expected_user_display_name',settings)
        self.assertEqual(settings['write_project'],'')

    def test_old_author_name_does_not_bind_other_users_in_auto_mode(self):
        for name in ('Recipient A','Recipient B'):
            with self.subTest(name=name),tempfile.TemporaryDirectory() as root:
                text=snapshot().replace('Fixture User',name)
                h=AutoHost(root,[text,text],{'expected_user_display_name':'Old author binding'})
                plugin.register(h)
                r=h.invoke(action='read_view',page_id=1)
                self.assertTrue(r['ok'],r)
                self.assertFalse(r['source']['unique_principal_verified'])

    def test_auto_context_still_stops_on_login_or_backend_denial(self):
        for status,text in [('permission_denied',snapshot(body='  uid=7_0 StaticText "Access denied"\n')),
                            ('pending_login',snapshot(body='  uid=7_0 textbox "Password"\n'))]:
            with self.subTest(status=status),tempfile.TemporaryDirectory() as root:
                h=AutoHost(root,[text]);plugin.register(h)
                r=h.invoke(action='read_view',page_id=1)
                self.assertEqual(r['status'],status)
                self.assertEqual([x[0] for x in h.calls],['take_snapshot'])

    def test_auto_context_does_not_follow_drift_mid_read(self):
        for second,status in [(snapshot(project='Other project'),'project_mismatch'),
                              (snapshot().replace('Fixture User','Different user'),'user_mismatch')]:
            with self.subTest(status=status),tempfile.TemporaryDirectory() as root:
                h=AutoHost(root,[snapshot(),second]);plugin.register(h)
                self.assertEqual(h.invoke(action='read_view',page_id=1)['status'],status)

    def test_explicit_target_still_checked_and_record_writes_not_auto_granted(self):
        with tempfile.TemporaryDirectory() as root:
            h=AutoHost(root,[snapshot(),snapshot()]);plugin.register(h)
            self.assertEqual(h.invoke(action='read_view',page_id=1,expected_project='Other project')['status'],'project_mismatch')
            r=h.invoke(action='write_record',page_id=1,record_id='QAQC-PLUGIN-TEST-auto',intent='create',operation_id='auto-write',fields={'Mã hồ sơ':'QAQC-PLUGIN-TEST-auto'},create_label='Thêm mới',submit_label='Lưu',expected_status='Draft')
            self.assertFalse(r['ok'],r)
            self.assertNotIn('click',[x[0] for x in h.calls])

    def test_pages_and_legacy_inspect_need_no_names(self):
        with tempfile.TemporaryDirectory() as root:
            h=AutoHost(root,['1: Fixture ('+URL+')',snapshot()])
            plugin.register(h)
            self.assertTrue(h.invoke(action='pages')['ok'])
            r=h.invoke(action='inspect',page_id=1)
            self.assertTrue(r['ok'],r)
            self.assertEqual(r['page']['project'],'Fixture Project')

    def test_open_and_status_need_no_typed_names_or_project(self):
        target='https://qaqc.newtecons.vn/#/nhat-ky-thi-cong/1/fixture/fixturegs'
        final=snapshot().replace(URL,target)
        with tempfile.TemporaryDirectory() as root:
            h=AutoHost(root,['1: Existing ('+URL+')','created','1: Existing ('+URL+')\n4: Diary ('+target+')',final,final],{'allow_open_page':True,'allow_new_tab':True})
            plugin.register(h)
            r=h.invoke(action='open_page',url=target,mode='new',operation_id='auto-open')
            self.assertTrue(r['ok'],r)
            self.assertEqual(r['source']['project'],'Fixture Project')
            r=h.invoke(action='open_page_status',operation_id='auto-open')
            self.assertTrue(r['ok'],r)
            self.assertEqual([x[0] for x in h.calls].count('new_page'),1)

    def test_read_observes_context_without_typed_names_or_project(self):
        with tempfile.TemporaryDirectory() as root:
            h=AutoHost(root,[snapshot(),snapshot()])
            plugin.register(h)
            r=h.invoke(action='read_view',page_id=1)
            self.assertTrue(r['ok'],r)
            self.assertEqual(r['source']['project'],'Fixture Project')
            self.assertEqual(r['source']['account_check'],'observed_session_context_not_unique_principal')
            self.assertNotIn('expected_user_display_name',h.state.values)

    def test_prepare_requires_no_manual_name_or_project(self):
        with tempfile.TemporaryDirectory() as root:
            h=AutoHost(root)
            plugin.register(h)
            r=h.invoke(action='prepare')
            self.assertTrue(r['ok'],r)
            self.assertEqual(r.get('context_policy'),'auto')
            self.assertEqual(h.calls,[])


if __name__=='__main__':unittest.main()

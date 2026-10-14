"""QAQC read-only contract tests; synthetic fixtures, not live data."""
import importlib.util
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('qaqc_fast_contract', ROOT / '__init__.py', submodule_search_locations=[str(ROOT)])
plugin = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = plugin
if spec.origin and pathlib.Path(spec.origin).exists():
    spec.loader.exec_module(plugin)

URL = 'https://qaqc.newtecons.vn/#/ProjectList/503/examplegs'

def snapshot(project='Công trình A', body='', user='Người A'):
    return ('## Latest page snapshot\n'
            f'uid=1_0 RootWebArea "Danh sách dự án" url="{URL}"\n'
            f'  uid=1_90 StaticText "{user}"\n'
            '  uid=1_1 link "QAQC" url="unsafe:javascript:;"\n'
            '  uid=1_2 StaticText "DANH SÁCH DỰ ÁN"\n'
            f'  uid=1_3 StaticText "{project}"\n'
            '  uid=1_4 StaticText "XÂY DỰNG"\n'
            '  uid=1_5 StaticText "CƠ ĐIỆN"\n'
            '  uid=1_6 StaticText "HỆ THỐNG"\n'
            '  uid=1_7 StaticText "PHÁP CHẾ"\n' + body)

class Host:
    def __init__(self, outputs):
        self.outputs = iter(outputs)
        self.calls = []
    def get_config(self, key, default=None):
        return 'Người A' if key=='expected_user_display_name' else default
    def call_mcp(self, server, tool, arguments, timeout=15):
        self.calls.append((server, tool, arguments))
        return {'ok':True, 'result':next(self.outputs)}

class Contract(unittest.TestCase):
    def test_unstructured_business_text_is_preserved_without_inventing_records(self):
        nodes=plugin.parse_snapshot(snapshot(body='  uid=3_0 StaticText "CÔNG VIỆC"\n  uid=3_1 StaticText "Trình duyệt vật liệu"\n'))
        data=plugin.list_data(nodes)
        self.assertEqual(data['visible_text'],['CÔNG VIỆC','Trình duyệt vật liệu'])
        self.assertEqual(data['view_structure'],'unstructured_accessibility_text')
        self.assertEqual(data['rows'],[])
        self.assertFalse(data['empty_view_proves_zero_records'])
        self.assertFalse(data['data_ready_verified'])

    def test_iframe_business_content_is_not_attributed_to_the_verified_top_page(self):
        nodes=plugin.parse_snapshot(snapshot(body='  uid=3_0 StaticText "Nội dung chính"\n  uid=3_1 Iframe\n    uid=3_2 RootWebArea "Other" url="https://example.com/"\n      uid=3_3 row\n        uid=3_4 cell "OTHER RECORD"\n'))
        data=plugin.list_data(nodes)
        self.assertEqual(data['rows'],[])
        self.assertEqual(data['visible_text'],['Nội dung chính'])

    def test_unbound_user_is_blocked_before_browser_access(self):
        host = Host([])
        host.get_config = lambda key,default=None: '' if key=='expected_user_display_name' else default
        for action in ('pages','inspect'):
            args={'action':action}
            if action=='inspect':
                args.update(page_id=1,expected_project='Công trình A')
            result=plugin.run(host,args)
            self.assertEqual(result['status'],'pending_user_binding')
            self.assertEqual(result['mcp_calls'],0)

    def test_each_recipient_uses_their_own_bound_browser_account(self):
        for user in ('Người A','Người B'):
            host=Host([snapshot(user=user)])
            host.get_config=lambda key,default=None,u=user: u if key=='expected_user_display_name' else default
            result=plugin.run(host,{'action':'inspect','page_id':1,'expected_project':'Công trình A'})
            self.assertTrue(result['ok'],result)
            self.assertEqual(result['page']['account_check'],'display_name_matches_local_binding')

    def test_wrong_or_switched_account_cannot_navigate(self):
        host=Host([snapshot(user='Người B')])
        result=plugin.run(host,{'action':'open_module','page_id':1,'expected_project':'Công trình A','module':'photos'})
        self.assertEqual(result['status'],'user_mismatch')
        self.assertEqual([c[1] for c in host.calls],['take_snapshot'])
        target='https://qaqc.newtecons.vn/#/AlbumThiCong/1/x'
        host=Host([snapshot(body=f'  uid=1_9 link "Hình ảnh thi công" url="{target}"\n'),snapshot(user='Người B').replace(URL,target)])
        result=plugin.run(host,{'action':'open_module','page_id':1,'expected_project':'Công trình A','module':'photos'})
        self.assertEqual(result['status'],'user_mismatch')
        self.assertEqual([c[1] for c in host.calls],['take_snapshot','click'])

    def test_invalid_arguments_stop_before_mcp(self):
        bad = [None,{}, {'action':'click'}, {'action':'read_list','page_id':True,'expected_project':'A','module':'photos'},
               {'action':'inspect','page_id':1,'expected_project':''}, {'action':'inspect','page_id':-1,'expected_project':'A'},
               {'action':'inspect','page_id':1,'expected_project':'A','url':URL},
               {'action':'inspect','page_id':1,'expected_project':'A','uid':'1_3'},
               {'action':'open_module','page_id':1,'expected_project':'A','module':'approve'},
               {'action':'capabilities','page_id':1}, {'action':'pages','expected_project':'A'}]
        for args in bad:
            with self.subTest(args=args):
                host = Host([])
                result = plugin.run(host,args)
                self.assertFalse(result['ok'])
                self.assertEqual(result['mcp_calls'],0)
                self.assertEqual(host.calls,[])

    def test_dms_connector_configuration_is_rejected(self):
        host = Host([])
        host.get_config = lambda key,default=None: 'chrome_dms'
        result = plugin.run(host, {'action':'inspect','page_id':1,'expected_project':'Công trình A'})
        self.assertEqual(result['status'],'invalid_mcp_settings')
        self.assertEqual(host.calls,[])

    def test_unsafe_origins_routes_and_embedded_credentials_stop(self):
        bad_urls = ['https://dms.newtecons.vn/document/list','https://qaqc.newtecons.vn.evil/#/AlbumThiCong/1/x',
                    'https://user:pass@qaqc.newtecons.vn/#/AlbumThiCong/1/x','http://qaqc.newtecons.vn/#/AlbumThiCong/1/x',
                    'https://qaqc.newtecons.vn/?token=secret#/AlbumThiCong/1/x','https://qaqc.newtecons.vn/#/approve/1/x',
                    'https://qaqc.newtecons.vn/#/AlbumThiCong/../x']
        for url in bad_urls:
            with self.subTest(url=url):
                result = plugin.run(Host([snapshot().replace(URL,url)]),{'action':'inspect','page_id':1,'expected_project':'Công trình A'})
                self.assertFalse(result['ok'])
                self.assertEqual(result['mcp_calls'],1)
                self.assertNotIn('secret',str(result))

    def test_project_name_in_card_does_not_satisfy_header(self):
        text = snapshot(project='Công trình B',body='  uid=2_0 heading "Công trình A" level="5"\n')
        result = plugin.run(Host([text]),{'action':'open_module','page_id':1,'expected_project':'Công trình A','module':'photos'})
        self.assertEqual(result['status'],'project_mismatch')
        self.assertEqual(result['mcp_calls'],1)

    def test_project_drift_after_click_stops_before_wait(self):
        target='https://qaqc.newtecons.vn/#/AlbumThiCong/1/x'
        host=Host([snapshot(body=f'  uid=1_9 link "Hình ảnh thi công" url="{target}"\n'),snapshot(project='Công trình B').replace(URL,target)])
        result=plugin.run(host,{'action':'open_module','page_id':1,'expected_project':'Công trình A','module':'photos'})
        self.assertEqual(result['status'],'project_mismatch')
        self.assertEqual([x[1] for x in host.calls],['take_snapshot','click'])

    def test_ambiguous_live_menu_never_clicks(self):
        body=''.join(f'  uid=2_{i} link "Hình ảnh thi công" url="https://qaqc.newtecons.vn/#/AlbumThiCong/1/x"\n' for i in range(2))
        host=Host([snapshot(body=body)])
        result=plugin.run(host,{'action':'open_module','page_id':1,'expected_project':'Công trình A','module':'photos'})
        self.assertEqual(result['status'],'ambiguous_navigation')
        self.assertEqual(len(host.calls),1)

    def test_destination_heading_alone_does_not_verify_wrong_route(self):
        target='https://qaqc.newtecons.vn/#/AlbumThiCong/1/x'
        wrong=snapshot(body='  uid=2_0 StaticText "QUẢN LÝ HÌNH ẢNH THI CÔNG"\n')
        host=Host([snapshot(body=f'  uid=1_9 link "Hình ảnh thi công" url="{target}"\n'),wrong,wrong])
        result=plugin.run(host,{'action':'open_module','page_id':1,'expected_project':'Công trình A','module':'photos'})
        self.assertEqual(result['status'],'destination_not_verified')
        self.assertEqual(result['mcp_calls'],3)

    def test_transport_failure_or_truncation_never_retries_or_leaks(self):
        for envelope in [{'ok':False,'error':'token=secret'},{'ok':True,'result':snapshot(),'truncated':True}]:
            host=Host([])
            host.call_mcp=lambda *args,**kwargs: envelope
            result=plugin.run(host,{'action':'inspect','page_id':1,'expected_project':'Công trình A'})
            self.assertFalse(result['ok'])
            self.assertFalse(result['retried'])
            self.assertEqual(result['mcp_calls'],1)
            self.assertNotIn('secret',str(result))

    def test_controller_busy_has_no_browser_calls(self):
        plugin._LOCK.acquire()
        try:
            result=plugin.run(Host([]),{'action':'inspect','page_id':1,'expected_project':'Công trình A'})
            self.assertEqual(result['status'],'controller_busy')
            self.assertEqual(result['mcp_calls'],0)
        finally:
            plugin._LOCK.release()

    def test_registration_blocks_raw_qaqc_but_not_dms(self):
        class RegistrationHost(Host):
            def __init__(self):
                super().__init__([])
                self.tools, self.hooks, self.skills = {},{},{}
            def register_tool(self, **kwargs):
                self.tools[kwargs['name']] = kwargs
            def register_hook(self, name, callback):
                self.hooks[name] = callback
            def register_skill(self, name, path, **kwargs):
                self.skills[name] = path
        ctx = RegistrationHost()
        register = getattr(plugin,'register',None)
        self.assertTrue(callable(register),'Missing native plugin registration')
        register(ctx)
        self.assertEqual(set(ctx.tools),{'qaqc_fast_session'})
        self.assertTrue(ctx.skills['operations'].name=='SKILL.md')
        guard = ctx.hooks['pre_tool_call']
        self.assertEqual(guard(tool_name='mcp__chrome_qaqc__click',args={})['action'],'block')
        self.assertEqual(guard(tool_name='tool_call',args={'calls':[{'name':'mcp__chrome_qaqc__take_snapshot','arguments':{}}]})['action'],'block')
        self.assertIsNone(guard(tool_name='dms_fast_session',args={}))
        result = json.loads(ctx.tools['qaqc_fast_session']['handler']({'action':'capabilities'}))
        self.assertTrue(result['ok'])

    def test_capabilities_and_pages_do_not_guess_current_page(self):
        host = Host([])
        caps = plugin.run(host, {'action':'capabilities'})
        self.assertTrue(caps['ok'],caps)
        self.assertEqual(caps['mcp_calls'],0)
        self.assertEqual(set(caps['modules']),{'photos','work_acceptance','quality_risks'})
        pages = plugin.run(Host(['## Pages\n1: QAQC ('+URL+') [selected]\n2: Other (https://example.com/)']), {'action':'pages'})
        self.assertTrue(pages['ok'],pages)
        self.assertEqual([p['page_id'] for p in pages['pages']], [1])
        self.assertFalse(pages['project_verified'])

    def test_login_and_denial_are_pending_without_navigation(self):
        for text, status in [
            ('uid=1_0 RootWebArea "Login" url="https://login.microsoftonline.com/"\n  uid=1_1 textbox "Password"', 'pending_login'),
            (snapshot(body='  uid=9_0 StaticText "Không có quyền truy cập"\n'), 'permission_denied')
        ]:
            with self.subTest(status=status):
                host = Host([text])
                result = plugin.run(host, {'action':'open_module','page_id':1,'expected_project':'Công trình A','module':'photos'})
                self.assertEqual(result['status'], status)
                self.assertEqual(len(host.calls),1)
                self.assertFalse(result['retried'])

    def test_read_list_preserves_rows_filters_and_partial_coverage(self):
        text = snapshot(body=(
            '  uid=3_0 StaticText "DANH SÁCH RỦI RO CHẤT LƯỢNG"\n'
            '  uid=3_1 combobox "Loại hồ sơ" value="THI CÔNG"\n'
            '  uid=3_2 row\n'
            '    uid=3_3 columnheader "Mã"\n'
            '    uid=3_4 columnheader "Nội dung"\n'
            '  uid=3_5 row\n'
            '    uid=3_6 cell "R-001"\n'
            '    uid=3_7 cell "Lỗi lớp bảo vệ"\n'
            '  uid=3_8 link "2" url="https://qaqc.newtecons.vn/"\n'
        )).replace(URL,'https://qaqc.newtecons.vn/#/hosochatluong/2/554/livegs')
        result = plugin.run(Host([text]), {'action':'read_list','page_id':1,'expected_project':'Công trình A','module':'quality_risks'})
        self.assertTrue(result['ok'],result)
        data = result['page']['list_data']
        self.assertEqual(data['columns'], ['Mã','Nội dung'])
        self.assertEqual(data['rows'][0]['cells'], ['R-001','Lỗi lớp bảo vệ'])
        self.assertEqual(data['filters'][0]['value'], 'THI CÔNG')
        self.assertEqual(data['pagination']['coverage'], 'current_page_only')
        self.assertEqual(data['pagination']['available_page_labels'], ['2'])
        self.assertFalse(result['page']['inventory_complete'])

    def test_open_module_batches_live_link_and_verified_destination(self):
        target = 'https://qaqc.newtecons.vn/#/AlbumThiCong/514/livegs'
        before = snapshot(body=f'  uid=1_9 link "Hình ảnh thi công" url="{target}"\n')
        after = snapshot(body='  uid=2_9 StaticText "QUẢN LÝ HÌNH ẢNH THI CÔNG"\n').replace(URL,target)
        host = Host([before, after])
        result = plugin.run(host, {'action':'open_module','page_id':1,'expected_project':'Công trình A','module':'photos'})
        self.assertTrue(result['ok'], result)
        self.assertEqual(result['page']['url'], target)
        self.assertEqual([x[1] for x in host.calls], ['take_snapshot','click'])
        self.assertEqual(host.calls[1][2]['uid'], '1_9')
        self.assertEqual(result['verification'], 'project_route_and_heading_read_back')

    def test_inspect_verifies_header_project_not_card_or_url_segment(self):
        host = Host([snapshot(body='  uid=1_8 heading "Công trình B" level="5"\n')])
        run = getattr(plugin, 'run', None)
        self.assertTrue(callable(run), 'Missing executable QAQC reader')
        result = run(host, {'action':'inspect', 'page_id':1, 'expected_project':'Công trình A'})
        self.assertTrue(result['ok'], result)
        self.assertEqual(result['page']['project'], 'Công trình A')
        self.assertEqual(result['verification'], 'header_project_and_source_read_back')
        self.assertFalse(result['page']['inventory_complete'])
        self.assertEqual(host.calls[0][0], 'chrome_qaqc')
        self.assertNotIn('1_3', str(result))
        other = run(Host([snapshot()]), {'action':'inspect','page_id':1,'expected_project':'503'})
        self.assertEqual(other['status'], 'project_mismatch')

if __name__ == '__main__':
    unittest.main()

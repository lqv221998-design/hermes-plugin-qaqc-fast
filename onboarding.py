"""Self-contained recipient guidance. No configuration writes or browser bootstrap."""
from importlib.util import find_spec
from importlib import import_module
from importlib.metadata import version
import sys

VERSION = '0.2.0-rc.3'
START_CONTEXT = (
    'QAQC Fast hỗ trợ mở/đọc website QAQC, nhật ký thi công, hồ sơ nghiệm thu, ảnh và rủi ro; '
    'không thay kỹ sư, không nâng ACL. Dùng qaqc_fast_session, không raw chrome_qaqc. '
    'Nạp qaqc-fast:tasks để ánh xạ yêu cầu thành thao tác, qaqc-fast:setup khi thiếu prerequisite, '
    'qaqc-fast:operations trước thao tác. capabilities kiểm runtime/actions, prepare kiểm local '
    'prerequisite không gọi browser; pages chỉ tìm tab đã có. open_page nhận URL QAQC do người dùng '
    'chọn và mode new/reuse, cần grant mở trang/tab, operation_id và xác minh đích; không tự chạy Chrome. '
    'Mặc định context_policy=auto: không bắt nhập tên tài khoản hoặc dự án trước kết nối; '
    'tự quan sát ngữ cảnh trang hiện tại. expected_project chỉ là assertion tùy chọn khi có đích cụ thể. '
    'Quyền do QAQC backend theo phiên đăng nhập của người dùng, không dùng quyền/cookie tác giả. '
    'Không đổi account/project giữa thao tác, không nâng quyền. Ba module legacy là recipes. Đọc '
    'trang workflow không đồng nghĩa gửi/duyệt. Login/ACL/denial/mismatch là pending, không '
    'fallback/replay. Ghi chỉ hồ sơ thử mới do plugin sở hữu ở TEST được grant; workflow riêng. '
    'Không suy project từ URL, không copy cookies/profile. Current-page không là toàn inventory. '
    'Nếu skills/schema/version chưa khớp, kiểm installed build và mở phiên mới; không sửa cache '
    'chat đang chạy. Với nhật ký: đúng row → Chỉnh sửa → kiểm template; chưa template không '
    'tạo thêm hay sửa cấu hình global. Browser/MCP local của từng người vẫn cần setup/consent.'
)


def guidance(status, mcp_calls=0):
    reasons = {
        'pending_user_binding': 'Ask the recipient to confirm their own displayed QAQC name; configure only with consent. No browser call occurred: no conclusion about connection, route or ACL.',
        'pending_login': 'Recipient completes login/SSO/2FA manually in their own Chrome. Keep the chosen tab/attempt; no credentials in chat or plugin.',
        'project_mismatch': 'Stop. Confirm exact requested header project; do not adopt the current project or URL segments.',
        'pending_project_selection': 'Ask for the exact requested displayed project. Route parameters are not project identity.',
        'page_open_not_authorized': 'Request separate permission for QAQC page navigation; apply allow_open_page only after consent.',
        'new_tab_not_authorized': 'Request separate new-tab permission and native new_page tool allowlist; do not repoint another connector.',
        'host_mcp_blocked_or_failed': 'Inspect native connector/approval/transport through setup. No controller fallback or blind retry.',
        'open_page_pending_no_replay': 'An earlier page-open attempt is unresolved. Observe the owned attempt with open_page_status; never create a fresh operation ID to replay.',
        'unsupported_read_route': 'The route is not accepted by this build. This is distinct from ACL denial; do not synthesize a supported URL.',
    }
    return {'load_skills': ['qaqc-fast:setup', 'qaqc-fast:operations', 'qaqc-fast:tasks'],
            'next_step': reasons.get(status, 'Use the observed status and active schema; read task-recipes before selecting an action.'),
            'browser_checked': False, 'browser_call_attempted': mcp_calls > 0,
            'warning': 'Capabilities describe code support, not access grants. A prerequisite block is not proof that the destination is unsupported.'}


def prepare(ctx, args):
    from . import Stop, context_policy
    if set(args) != {'action'}:
        raise Stop('invalid_input')
    value = ctx.get_config('expected_user_display_name', default='')
    missing = []
    policy = context_policy(ctx)
    if policy=='manual' and (not isinstance(value, str) or not value.strip() or len(value) > 200):
        missing.append('expected_user_display_name')
    if ctx.get_config('mcp_server', default='chrome_qaqc') != 'chrome_qaqc':
        missing.append('mcp_server=chrome_qaqc')
    dependencies = {name: find_spec(name) is not None for name in ('openpyxl', 'pypdf', 'PIL')}
    imports = {}
    for name,module,distribution in [('openpyxl','openpyxl','openpyxl'),('pypdf','pypdf','pypdf'),('Pillow','PIL.Image','Pillow')]:
        try:
            import_module(module)
            imports[name] = {'ok':True,'version':version(distribution)}
        except Exception as exc:
            imports[name] = {'ok':False,'error_type':type(exc).__name__}
    status = 'pending_user_binding' if 'expected_user_display_name' in missing else 'local_prerequisites_observed'
    return {'ok': not missing, 'version': VERSION, 'status': status, 'missing': missing,
            'context_policy':policy,'manual_context_required':policy=='manual',
            'dependency_import_specs': dependencies, 'mcp_calls': 0,
            'dependency_imports':imports,'python_runtime':{'executable':sys.executable,'version':sys.version.split()[0]},
            'dependency_installation':'not_attempted; use native PM after consent; see PREREQUISITES.md',
            'browser_checked': False, 'destination_checked': False, 'business_verified': False,
            'mcp_handshake': 'not_checked', 'browser_login_acl': 'not_checked',
            'grants': {key: ctx.get_config(key, default=False) is True for key in ('allow_open_page', 'allow_new_tab')},
            'guidance': guidance(status)}

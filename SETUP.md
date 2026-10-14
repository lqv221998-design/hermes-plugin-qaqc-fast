# Cài QAQC Fast 0.2.0-rc.3 theo từng người sử dụng

Hướng dẫn chính: [START-HERE-HERMES.md](START-HERE-HERMES.md). Đây là root-layout Git repository/Agent component; setup và operations bundled, không cần #subdir, không có Desktop pane. Native repository install/review là primary path.

Load `qaqc-fast:setup`; dependencies openpyxl/pypdf/Pillow được khai báo và provisioning là consent/gate riêng qua native manager. Doctor warning missing deps không là runtime ready; CLI đã kiểm không có plugins deps. Không pip chèn managed venv, không CLI dispatch né approval, không kill turn hay restart DMS để activate.

## Ranh giới quyền
- Mỗi người dùng phải có Windows/Hermes/Chrome profile và phiên QAQC riêng. Không dùng trình duyệt, cookie, tài khoản hoặc kết nối của người xây plugin.
- Quyền dự án/hồ sơ/thao tác do QAQC backend kiểm tra với phiên đó. Các module có recipe trong plugin KHÔNG phải danh sách quyền được cấp.
- RC có ghi scoped TEST/new QAQC-PLUGIN-TEST owned records, write_project mặc định trống. Quyền create/edit/upload/delete không cấp send/approve/reject/close; workflow_transitions=[] nếu chưa có grant riêng. Restore/OCR bindings local/grant riêng.
- Đây là plugin desktop cá nhân, không phải lớp xác thực cho một dịch vụ nhiều người dùng chung Chrome. Không triển khai theo mô hình đó.

## Điều kiện
Thiếu runtime/thư viện: theo [PREREQUISITES.md](PREREQUISITES.md); prompt điều phối [PROMPT-HERMES.md](PROMPT-HERMES.md). Đọc từng actual dependency_imports, không chỉ prepare.ok/find_spec.
Hermes có native MCP SDK và API PluginContext.call_mcp; Node.js và Chrome trên máy của người nhận. Connector đã nghiệm thu với chrome-devtools-mcp 1.10.1 của GoogleChromeLabs. Không cần Jev, BrowserPaw, service account hoặc API key QAQC.

## Thiết lập trên máy người nhận
1. Native Desktop Review repository hoặc `hermes plugins install <URL-repo> --no-enable` theo START-HERE. Pin bằng exact commit đã kiểm nếu cần; không dùng author profile/paths. Doctor absolute installed directory, enable riêng --no-allow-tool-override. Cài code không là MCP/login/ACL/business ready; không force overwrite.
2. Chuẩn bị Chrome chuyên dụng bằng profile mới thuộc người nhận, không sao chép profile/cookie của người khác. Người nhận tự đăng nhập QAQC. Chrome DevTools chỉ bind loopback trên máy mình; không công khai cổng ra LAN/Internet. DevTools có quyền rộng trên profile, vì vậy không dùng profile có đăng nhập các hệ thống không liên quan.
3. Cài phiên bản cố định `chrome-devtools-mcp@1.10.1` từ nguồn GoogleChromeLabs. Trong Hermes tạo native STDIO MCP server tên **chrome_qaqc**. Dùng Node và entrypoint `build/src/bin/chrome-devtools-mcp.js` của bản đã cài trên máy người nhận. Browser URL phải là loopback endpoint của Chrome riêng ở bước 2, KHÔNG lấy endpoint/đường dẫn máy người xây.
4. Giới hạn tool native đúng tên: list_pages,take_snapshot,click,wait_for,fill_form,upload_file,navigate_page; thêm new_page sau consent tạo tab. allow_open_page/allow_new_tab mặc định false, bật từng key chỉ khi grant. Tắt resources/prompts/sampling/elicitation, usage statistics, CrUX, JavaScript evaluation và category không cần. Không generic script/API; giữ DMS nguyên trạng và approval/trust.
5. Người nhận tự quyết định trust/approval. Không sao chép chấp thuận của tác giả. Nếu chọn untrusted, các bước điều hướng có thể cần approval của chính người nhận; không đổi trust để né một từ chối.
6. Chỉ cấp MCP allowlist **chrome_qaqc**; settings.mcp_server phải cùng key. context_policy mặc định **auto**, không cấu hình tên người dùng. Config thay đổi qua native UI/hermes config set sau consent, không thay nguyên YAML.
7. Không cần tên tài khoản hoặc dự án trước kết nối. Plugin dùng own login/session người nhận và quan sát context của tab được chọn, không lưu binding tên tĩnh. expected_project tùy chọn khi có một đích cụ thể. Manual policy cũ chỉ là opt-in assertion, không quyền QAQC.
8. Mở phiên chat mới để native MCP dùng cấu hình đã lưu. Không reload toàn bộ MCP hay restart DMS đang làm việc chỉ để kích hoạt QAQC.

## Nghiệm thu cho từng người nhận
- Nạp `qaqc-fast:tasks` và `qaqc-fast:operations`; chạy capabilities, prepare, pages/open_page; lấy page ID quan sát thực tế, không mặc định 1. Root/bootstrap khác business; xem ví dụ request trong tasks. Không tìm thấy skill/action/version thì activation pending, không kết luận chỉ ba module.
- Chạy inspect/read_view với page_id; project/account tự quan sát. Nếu người dùng đã chỉ định đích khác thì truyền expected_project và phải kiểm khớp. Không tự dùng Dự án TEST cho mọi người.
- Nếu website từ chối hoặc menu thiếu, dừng; không đổi tài khoản, đoán URL/ID hoặc dò API để vượt quyền.
- Thử module mà người nhận có quyền đọc. Kết quả kiểm riêng người này không chứng minh người khác có cùng quyền.
- Tên tài khoản không khớp, đổi tài khoản hoặc header không rõ phải dừng. Kiểm chuyển tài khoản chỉ thực hiện với tài khoản do chính người nhận được phép sử dụng.

## Giới hạn dữ liệu
Public read_list/read_view dùng native snapshot file, lossless current-page rows/text/links, readiness hai snapshot + completion evidence; false stays partial. 8 MiB overflow stops, không clipping. Iframe subtree excluded, later siblings kept. Discipline requires selected state; expected_discipline mismatch stops. read_all cần identity/terminal pager/total reconciliation. Reader local/OCR/vision không chứng minh SharePoint/revision/full scan/normative rules. Native/print và caller/model/chat baseline benchmark còn cần live acceptance riêng; không suy speed từ fixture.

Tài liệu: https://hermes-agent.nousresearch.com/docs/developer-guide/plugins ; https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference ; https://github.com/GoogleChromeLabs/chrome-devtools-mcp .

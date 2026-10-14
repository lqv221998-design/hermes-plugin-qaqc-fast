# Cài QAQC Fast 0.2.0-rc.1 theo từng người sử dụng

Hướng dẫn chính: [START-HERE-HERMES.md](START-HERE-HERMES.md). Đây là root-layout Git repository/Agent component; setup và operations bundled, không cần #subdir, không có Desktop pane. Native repository install/review là primary path.

Load `qaqc-fast:setup`; dependencies openpyxl/pypdf/Pillow được khai báo và provisioning là consent/gate riêng qua native manager. Doctor warning missing deps không là runtime ready; CLI đã kiểm không có plugins deps. Không pip chèn managed venv, không CLI dispatch né approval, không kill turn hay restart DMS để activate.

## Ranh giới quyền
- Mỗi người dùng phải có Windows/Hermes/Chrome profile và phiên QAQC riêng. Không dùng trình duyệt, cookie, tài khoản hoặc kết nối của người xây plugin.
- Quyền dự án/hồ sơ/thao tác do QAQC backend kiểm tra với phiên đó. Các module có recipe trong plugin KHÔNG phải danh sách quyền được cấp.
- RC có ghi scoped TEST/new QAQC-PLUGIN-TEST owned records, write_project mặc định trống. Quyền create/edit/upload/delete không cấp send/approve/reject/close; workflow_transitions=[] nếu chưa có grant riêng. Restore/OCR bindings local/grant riêng.
- Đây là plugin desktop cá nhân, không phải lớp xác thực cho một dịch vụ nhiều người dùng chung Chrome. Không triển khai theo mô hình đó.

## Điều kiện
Hermes có native MCP SDK và API PluginContext.call_mcp; Node.js và Chrome trên máy của người nhận. Connector đã nghiệm thu với chrome-devtools-mcp 1.10.1 của GoogleChromeLabs. Không cần Jev, BrowserPaw, service account hoặc API key QAQC.

## Thiết lập trên máy người nhận
1. Native Desktop Review repository hoặc `hermes plugins install <URL-repo> --no-enable` theo START-HERE. Pin bằng exact commit đã kiểm nếu cần; không dùng author profile/paths. Doctor absolute installed directory, enable riêng --no-allow-tool-override. Cài code không là MCP/login/ACL/business ready; không force overwrite.
2. Chuẩn bị Chrome chuyên dụng bằng profile mới thuộc người nhận, không sao chép profile/cookie của người khác. Người nhận tự đăng nhập QAQC. Chrome DevTools chỉ bind loopback trên máy mình; không công khai cổng ra LAN/Internet. DevTools có quyền rộng trên profile, vì vậy không dùng profile có đăng nhập các hệ thống không liên quan.
3. Cài phiên bản cố định `chrome-devtools-mcp@1.10.1` từ nguồn GoogleChromeLabs. Trong Hermes tạo native STDIO MCP server tên **chrome_qaqc**. Dùng Node và entrypoint `build/src/bin/chrome-devtools-mcp.js` của bản đã cài trên máy người nhận. Browser URL phải là loopback endpoint của Chrome riêng ở bước 2, KHÔNG lấy endpoint/đường dẫn máy người xây.
4. Giới hạn tool native đúng tên: list_pages,take_snapshot,click,wait_for,fill_form,upload_file,navigate_page. Tắt resources/prompts/sampling/elicitation, usage statistics, CrUX, JavaScript evaluation và category không cần. Không generic script/API/new_page; giữ DMS nguyên trạng và approval/trust.
5. Người nhận tự quyết định trust/approval. Không sao chép chấp thuận của tác giả. Nếu chọn untrusted, các bước điều hướng có thể cần approval của chính người nhận; không đổi trust để né một từ chối.
6. Chỉ cấp MCP allowlist **chrome_qaqc** cho `plugins.entries.qaqc-fast`. Cấu hình `settings.mcp_server` là chuỗi **chrome_qaqc**, và `settings.expected_user_display_name` là chính xác tên tài khoản QAQC do người nhận xác nhận. Dùng giao diện Hermes hoặc `hermes config set`, không sửa YAML toàn file. Với CLI, truyền string nguyên văn; JSON chỉ dành cho object/list, tránh thêm dấu nháy vào giá trị string.
7. Tên mặc định trong manifest là rỗng: plugin phải trả `pending_user_binding` trước khi đọc Chrome. Không tự bind theo tài khoản tình cờ đang mở. Binding tên hiển thị chỉ chống dùng nhầm thông thường; tên trùng nhau không xác minh được principal duy nhất.
8. Mở phiên chat mới để native MCP dùng cấu hình đã lưu. Không reload toàn bộ MCP hay restart DMS đang làm việc chỉ để kích hoạt QAQC.

## Nghiệm thu cho từng người nhận
- Nạp `qaqc-fast:operations`; chạy capabilities, pages; lấy page ID quan sát thực tế, không mặc định 1.
- Chạy inspect với tên dự án chính xác mà chính người nhận yêu cầu. Phải kiểm được account/header/source; đừng dùng dự án đang mở hoặc Dự án TEST làm mặc định.
- Nếu website từ chối hoặc menu thiếu, dừng; không đổi tài khoản, đoán URL/ID hoặc dò API để vượt quyền.
- Thử module mà người nhận có quyền đọc. Kết quả kiểm riêng người này không chứng minh người khác có cùng quyền.
- Tên tài khoản không khớp, đổi tài khoản hoặc header không rõ phải dừng. Kiểm chuyển tài khoản chỉ thực hiện với tài khoản do chính người nhận được phép sử dụng.

## Giới hạn dữ liệu
Public read_list/read_view dùng native snapshot file, lossless current-page rows/text/links, readiness hai snapshot + completion evidence; false stays partial. 8 MiB overflow stops, không clipping. Iframe subtree excluded, later siblings kept. Discipline requires selected state; expected_discipline mismatch stops. read_all cần identity/terminal pager/total reconciliation. Reader local/OCR/vision không chứng minh SharePoint/revision/full scan/normative rules. Native/print và caller/model/chat baseline benchmark còn cần live acceptance riêng; không suy speed từ fixture.

Tài liệu: https://hermes-agent.nousresearch.com/docs/developer-guide/plugins ; https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference ; https://github.com/GoogleChromeLabs/chrome-devtools-mcp .

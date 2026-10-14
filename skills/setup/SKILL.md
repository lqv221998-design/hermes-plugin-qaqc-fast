---
name: setup
description: Use when setting up QAQC Fast. Verify each runtime gate.
version: 0.2.0-rc.2
license: MIT
platforms: [windows]
---
# QAQC Fast — thiết lập độc lập
Đích: giúp một Hermes chưa có session/skills tác giả nhận ra mục đích, kiểm gate và mở/đọc đúng QAQC. Nạp `qaqc-fast:tasks` để hiểu yêu cầu và ví dụ. Trước browser gọi capabilities và prepare; runtime phải 0.2.0-rc.2 với open_page/open_page_status. Skills bundled không tự vào available_skills; bản này cung cấp schema + hook + frozen prompt section nếu host hỗ trợ. Không tìm thấy setup/tasks hoặc capabilities cũ → activation/discovery pending, không kết luận “plugin chỉ ba module”.

Mở URL/tab là quyền riêng: allow_open_page/allow_new_tab mặc định false. Sau consent, apply đúng hai keys và include native new_page khi cần; không thay nguyên config/allowlist hoặc trust để né refusal. Mode new mở background, không launcher Chrome; mode reuse chỉ tab QAQC đã xác minh project nguồn. Vẫn cần người nhận tự chuẩn bị Chrome/endpoint/login và xác nhận binding. Browser/MCP/root login/ACL và read/record effects là các gate riêng.

Bản RC có code/fixture proof, không là nghiệm thu mọi website/role. Hướng dẫn này và START-HERE-HERMES.md tự chứa, không yêu cầu thư viện skills riêng của tác giả. Nếu có skill hermes-agent phù hợp thì nạp thêm; đối chiếu tài liệu chính thức Hermes trước cấu hình. Dùng public CLI của bản đang chạy; không chèn package vào managed venv bằng pip và không dùng CLI dispatch để vượt approval.

Hai native Windows CLI installs thử riêng đã clone đúng source nhưng gặp WinError 5 khi publish/rename staged tree. Nguyên nhân host/PM chưa xác định; tests/Doctor/probe không là install PASS. Giữ error/state và pending host gate; không force/manual-copy/sửa core hoặc registry để giả nghiệm thu. Native Desktop physical review/install và máy nhận khác vẫn kiểm riêng.

1. Xác minh OS, Hermes home/profile, bản cài và nguồn. Máy người nhận dùng Chrome/profile/tài khoản của chính họ, không copy endpoint, cookie, cấu hình, state hay chấp thuận tác giả.
2. Đọc START-HERE-HERMES.md tại repo root (từ thư mục skill đi ../../). Native Desktop: Capabilities → Plugins → Install plugin → Repository → URL → Review repository; repo root chứa Agent plugin, không #subdir/Desktop pane. CLI đã kiểm: hermes plugins install <URL> --no-enable, pin actual full 40-hex SHA bằng --ref nếu cần, enable riêng --no-allow-tool-override. Không force overwrite. Mọi provisioning/config/browser grant riêng; không tự sửa trust/profile từ repo.
3. Đọc dependencies trong `plugin.yaml`: openpyxl, pypdf, Pillow. Consent provisioning riêng; dependency manager của Hermes giữ selection cũ nếu admission thất bại. `hermes plugins deps` không có trong CLI đã kiểm: đừng tự dựng lệnh này. Doctor/import đúng interpreter không thay live business acceptance.
4. Connector QAQC là native Google Chrome DevTools MCP 1.10.1, browser riêng thuộc người nhận, bind loopback. Cấp `list_pages,take_snapshot,click,wait_for,fill_form,upload_file,navigate_page`; bổ sung `new_page` sau consent tạo tab. resources/prompts/sampling/elicitation false. Không JavaScript evaluation, không API/cookie/storage, không server DMS. Tools filter là tên native, không tên mcp đã sanitize.
5. Consent riêng cấu hình, plugin mcp_allowlist chỉ `chrome_qaqc`, enablement và browser attachment. Giữ trust/approval; không đổi trust để chữa một từ chối. Cấu hình bằng public `hermes config set`, không sửa cả YAML. Giữ tất cả connector khác nguyên trạng.
6. Người nhận xác nhận `expected_user_display_name` tại UI. Trống hoặc khác tên thì dừng; tên hiển thị không là principal duy nhất hay ACL. `write_project` mặc định trống; chỉ cấu hình TEST theo grant riêng. `workflow_transitions=[]` cho đến grant send/approve/reject/close riêng. Không bật restore/OCR theo endpoint máy tác giả: cấu hình đúng binding local nếu được phép.
7. Mở chat mới sau activation, không sửa prefix/toolset giữa turn hoặc kill/restart DMS. Load `qaqc-fast:operations`, gọi capabilities → pages → inspect đúng dự án yêu cầu → read_view/read_list với expected_discipline khi cần. Phân biệt code installed, dependency-ready, MCP handshake, browser/account/project/discipline verified và live acceptance.
8. Chưa login/quota/denial/mismatch/transport failure thì pending/stop, không controller fallback hoặc replay. Chỉ hồ sơ thử mới mang tiền tố QAQC-PLUGIN-TEST do plugin tạo mới được sửa/upload/xóa. Send/approve/reject/close không thuộc quyền tạo hồ sơ.

Đầu ra runtime nằm trong dữ liệu riêng của plugin. Không đưa vào gói chia sẻ. Native Computer Use qua executor giữ session/approval, capture trước, review ảnh đúng cửa sổ/URL/account/project rồi mới input. Bàn giao source, báo cáo và hash riêng; không báo toàn site đã nghiệm thu từ Doctor/unit tests.

Nguồn: https://hermes-agent.nousresearch.com/docs/developer-guide/plugins ; https://hermes-agent.nousresearch.com/docs/reference/package-management ; https://github.com/ChromeDevTools/chrome-devtools-mcp .

# Prompt gửi Hermes máy nhận — QAQC Fast 0.2.0-rc.3

Copy phần dưới; chỉ thay URL và nhiệm vụ, **không cần tên tài khoản/tên dự án** cho mở/đọc cơ bản. Tên dự án chỉ cần khi chủ động chọn chuyển sang dự án khác hoặc muốn một target assertion. Đây là prompt điều phối, không tự cấp quyền/cài mọi thứ.

---

Hãy khảo sát, thiết lập những phần còn thiếu và sử dụng QAQC Fast trên máy/backend/profile của tôi để mở và đọc URL QAQC tôi chọn: **<URL_QAQC>**.

Phạm vi ban đầu: mở trang/tab và chỉ đọc. Không tạo/sửa/xóa/upload/gửi/duyệt hồ sơ hoặc sửa template/config trên QAQC. Không dùng quyền, tài khoản, cookie, browser profile, endpoint, binding hoặc grant của người xây plugin cho tôi.

Nguồn: https://github.com/lqv221998-design/hermes-plugin-qaqc-fast . Chọn release RC3 `0.2.0-rc.3`, kiểm actual full commit của release qua GitHub, không đoán SHA. Nếu bản đó chưa có trên remote, báo nguồn còn pending, không gọi RC2 là RC3.

1. Đọc START-HERE-HERMES.md, PREREQUISITES.md và SETUP.md tại source được chọn. Sau discovery, nạp qaqc-fast:setup, qaqc-fast:tasks, qaqc-fast:operations. Không có skill/tool không đồng nghĩa plugin chỉ ba module; kiểm installed/profile/activation.

2. Khảo sát read-only: OS/architecture, backend host, installation owner, active Hermes profile, native SDK, selected Python, Git, Node.js/npm, Chrome và Google Chrome DevTools MCP. Không cài lại thứ đã có. Kiểm PATH/PM tool lookup trước kết luận command not found là chưa cài. Không dùng Python/pip alias hệ thống để sửa managed Hermes.

3. Nếu thiếu, trình bày phần thiếu, scope/path/version, tải ngoài và thay đổi dự kiến; xin consent trước cài/enable/config/browser attachment. Sau consent, bổ sung bằng owner workflow chính thức theo PREREQUISITES.md:
- Hermes/Python thiếu hoặc hỏng: đúng installer/PM owner, không sửa signed payload/core.
- Git/Node/npm: native PM named tools-only nếu receiving build hỗ trợ; kiểm version/path.
- Python plugin dependencies: openpyxl==3.1.5, pypdf>=6,<7, Pillow>=11,<13 qua native plugin admission/PM union, không bare pip/uv pip.
- Google MCP: reuse hoặc scoped npm install chrome-devtools-mcp@1.10.1; kiểm Node engine ^20.19.0 || ^22.12.0 || >=23, package/binary.
- CUA/MinerU chỉ khi nhiệm vụ cần và có consent riêng; không kéo toàn bộ optional stack.
Mọi install phải có read-back/import thật. Missing spec, import lỗi native subdependency, wrong interpreter, install refused và browser login là các gate khác nhau.

4. Native plugin review/install trên đúng profile; nếu đã installed thì dùng update workflow, không force reinstall. Enablement/dependency admission/MCP grants là riêng. Giữ DMS/connector khác và working runtime. WinError 5 publication/rename → giữ log/attempt, installation pending; không manual-copy/core patch để báo install PASS.

5. Native chrome_qaqc chỉ kết nối Chrome của tôi, loopback, own login. Mẫu connector là DATA, không copy nguyên config. Consent riêng config/allowlist/enablement/open-page/new-tab. Không tự login, không nhận password/OTP/token trong chat, không copy cookies. Không sửa trust để vượt refusal.

6. Phiên mới phải thấy capabilities version 0.2.0-rc.3. Gọi prepare; mặc định context_policy=auto, manual_context_required=false. Đọc dependency_imports và Python path/version, không chỉ find_spec hoặc prepare.ok. Không yêu cầu nhập tên tài khoản hay dự án để binding. expected_user_display_name cũ bị bỏ qua trong auto mode.

7. Website work chỉ qua qaqc_fast_session. Dùng pages để chọn tab hiện có hoặc open_page với URL nguyên văn/mode theo yêu cầu/operation_id. Plugin tự quan sát account/project của tab; backend QAQC quyết định quyền theo phiên của tôi. Nếu tôi đã chọn explicit target thì kiểm expected_project; không suy project từ IDs URL. Không đổi account/project giữa các bước hoặc áp project tác giả.

8. Sau mở, inspect/read_view kiểm source/context/readiness/artifact. Current page không là whole inventory. Login/denial/drift/transport uncertainty giữ pending; không raw chrome_qaqc/DMS/JS/API/controller fallback. open_page_status chỉ đối soát same session/attempt, không mint ID mới để replay.

9. Template Nhật ký/Hồ sơ thiếu trên QAQC là server/project/discipline configuration blocker, không chữa bằng pip/npm/Jinja2/docxtpl. Báo đúng admin quyền, không tự sửa template global, bấm Lưu hay tạo lặp. Thư viện/template generator chưa có trong manifest/code không tự cài để hứa feature.

Báo cáo ngắn: nguồn/commit và runtime thực tế; phần bổ sung và import/version read-back; MCP handshake vs browser/login/ACL; URL/context/readiness/coverage; blockers cụ thể và next step nhỏ nhất. Chỉ gọi kết nối/nghiệp vụ hoàn tất sau terminal read-back, không từ installer/Doctor/click/toast. Không hứa mọi máy/mọi role chạy ngay khi còn gate chưa đạt.

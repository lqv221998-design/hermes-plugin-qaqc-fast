# QAQC Fast 0.2.0-rc.2 — mở QAQC có ngữ cảnh, chưa full-site acceptance

## Plugin dùng để làm gì và bắt đầu thế nào?
Giúp Hermes mở đúng link/tab **QAQC**, đọc nhật ký thi công/hồ sơ nghiệm thu/ảnh/rủi ro, tra cứu và xử lý **hồ sơ thử được grant** có read-back. Không điều khiển website khác, không nâng ACL, không thay kỹ sư hoặc tự login.

1. Nạp **qaqc-fast:tasks** để chọn action theo yêu cầu; **qaqc-fast:setup** khi thiếu prerequisite; **qaqc-fast:operations** trước browser work.
2. Gọi **capabilities → prepare**. Phải nhận version 0.2.0-rc.2 với prepare/open_page/open_page_status. prepare không truy cập browser. Thiếu binding với mcp_calls=0 không chứng minh trang không hỗ trợ.
3. Người nhận có own Chrome/MCP/login/binding và grant local; lấy exact requested project, không suy từ URL.
4. **open_page** nhận literal QAQC URL mode new/reuse; new mở background và kiểm duy nhất tab, reuse kiểm account/project nguồn. **open_page_status** chỉ đối soát attempt, không replay. Sau mở dùng read_view để kiểm readiness/coverage.

Đọc [ví dụ request hợp schema](skills/tasks/references/examples.md) và [recipe Nhật ký thi công](skills/tasks/references/construction-diary.md). Ví dụ synthetic, không là chứng nhận mọi live UI. Skills không tự vào available_skills của Hermes; bản này có schema guidance, hook ngữ cảnh và frozen prompt section cho host hỗ trợ. Không sửa cache/prompt phiên cũ.

## Cài trực tiếp từ GitHub trên Hermes khác
Repository: https://github.com/lqv221998-design/hermes-plugin-qaqc-fast

CLI: `hermes plugins install https://github.com/lqv221998-design/hermes-plugin-qaqc-fast --no-enable`.

**Host gate đã tái hiện:** native Agent installer trong hai Hermes home Windows thử riêng clone đúng repo nhưng thất bại với **WinError 5 / Access is denied** ở bước publish/rename staged plugin. Anonymous clone/byte verification, tests và Doctor/validator đạt không thay thế install PASS. Nguyên nhân host/PM chưa được xác định; không force/manual-copy/sửa core để gọi native install đạt. Physical máy nhận và Desktop UI review/install còn phải kiểm riêng. Nếu gặp lỗi này, giữ log/state và báo pending; không coi cài code đã hoàn tất.

**Đọc [START-HERE-HERMES.md](START-HERE-HERMES.md)**: hướng dẫn native Desktop/CLI, điều kiện cần và các phép kiểm đủ cho từng phạm vi. Repo có Agent plugin ở gốc, không cần #subdir; không có Desktop pane. Skills setup, operations và tasks tự đi cùng plugin. Public GitHub chỉ cung cấp code, không browser/login/QAQC permissions.

Đọc `qaqc-fast:setup`/SETUP.md và skill operations mới. RC sửa readiness theo bằng chứng, artifact lossless bỏ cap 100/250/100, subtree iframe, selected discipline và thêm benchmark handler. Có generic verified context/query/all-pages/detail/docs/OCR/vision, owned TEST write/workflow/transfer, Computer Use và recovery/checkpoint. Fixtures là code proof, không là live TEST/mọi role acceptance. Benchmark handler không gồm model/chat hay baseline, chưa kết luận nhanh hơn.

Native capture/input giữ session/approval, scope exact window, review SHA, fresh matching pixels/elements, consume một lần; dialog refresh chỉ cached verified handoff. MCP failure/context drift invalidate, uncertain không replay. Dependencies trong plugin.yaml cần native provisioning riêng. Send/approve/reject/close không thuộc quyền tạo TEST; write_project mặc định trống và workflow_transitions=[].

Plugin Python độc lập cho Hermes; tool `qaqc_fast_session`, skill `qaqc-fast:operations`. Dùng native Chrome DevTools MCP của Google, không sửa Hermes core hoặc DMS.

## Quyền theo người dùng
- Plugin chạy bằng phiên QAQC của **người cài/sử dụng**, không bằng quyền tác giả hoặc người nghiên cứu.
- Mỗi người dùng có OS/Hermes/Chrome profile riêng và tự đăng nhập QAQC. Backend QAQC quyết định dự án/hồ sơ họ được truy cập. Plugin không nâng quyền, gọi service account hoặc tái sử dụng tài khoản nghiên cứu.
- `expected_user_display_name` phải được người nhận xác nhận và cấu hình cục bộ. Mặc định trống; thiếu ràng buộc chặn browser. Sai tài khoản/dự án dừng trước điều hướng; kiểm lại sau mỗi click.
- Tên hiển thị chỉ là kiểm tra chống đổi nhầm account, không phải định danh đăng nhập duy nhất. Hai tài khoản trùng tên chưa được phân biệt bởi v0.1. Không dùng plugin desktop này làm lớp auth cho một dịch vụ nhiều người dùng.
- Đồng ý trust/allowlist trên máy tác giả không chuyển sang máy người nhận. Người nhận tự cấp quyền kết nối theo chính sách của họ.
- Gói không chứa config máy tác giả, tài khoản, mật khẩu, cookie, browser profile, endpoint, token, session/state hoặc dữ liệu dự án thật. Fixtures trong tests là dữ liệu tổng hợp để kiểm code, không phải dữ liệu nghiệm thu website.

## Chức năng hiện có
`capabilities` liệt kê verbs RC; ba recipe legacy: work_acceptance/photos/quality_risks. Expanded navigation dùng menu/heading sống có kiểm. Code support không phải quyền account; thiếu/denial dừng.

Một lần gọi gom UI steps có kiểm account/project/route; open_page chỉ nhận URL QAQC được người dùng chọn, không arbitrary-domain UID/script/API. Ghi chỉ scoped approved plugin-owned TEST records; các workflow grant riêng.

read_view/read_list current-page lossless; read_all có pagination/dedupe/total reconciliation. Local workbook/PDF readers không chứng minh SharePoint link/revision. OCR/vision unreviewed/non-normative; XLSX không tính công thức, PDF scan/text-layer gaps explicit. DOCX/CSV/ZIP content reader chưa có. Không suy full inventory/site từ snapshot.

## Cài cho người nhận
1. Đọc chính sách tổ chức; dùng máy/profile và tài khoản QAQC của người nhận. Đọc docs chính thức Hermes và DevTools trước cấu hình.
2. Native Desktop: Capabilities → Plugins → Install plugin → Repository → URL repo → Review repository; kiểm Agent/profile/commit/dependencies rồi consent. CLI: `hermes plugins install <URL-repo> --no-enable`, optional `--ref <actual-full-40-hex-SHA>`; enable riêng `hermes plugins enable qaqc-fast --no-allow-tool-override`. Root layout không dùng fragment hoặc helper copy. Doctor dùng absolute installed directory. Không force reinstall hoặc tự grant MCP từ installation.
3. Tạo kết nối Chrome QAQC **riêng của người nhận**, chạy Google `chrome-devtools-mcp@1.10.1`. Không copy kết nối/CDP endpoint hoặc Chrome profile của tác giả. Tắt JavaScript evaluation, usage statistics và CrUX. Khi Chrome khởi động lại, phát hiện lại endpoint cục bộ; không dùng port mẫu của máy khác.
4. Native chrome_qaqc include list_pages,take_snapshot,click,wait_for,fill_form,upload_file,navigate_page; new_page chỉ sau consent tạo tab. allow_open_page/allow_new_tab mặc định false; resources/prompts/sampling/elicitation false, parallel false. Trust theo consent riêng; không đổi DMS hoặc credentials. DevTools rộng, policy không là sandbox.
5. Dùng public `hermes config set` để cấp `plugins.entries.qaqc-fast.mcp_allowlist` chỉ cho server trên; cấu hình `plugins.entries.qaqc-fast.settings.expected_user_display_name` bằng đúng tên của người nhận đã tự xác nhận ở UI. Không có tên mặc định. Không ghi mật khẩu vào config.
6. Mở chat mới; load `qaqc-fast:tasks` và `qaqc-fast:operations`, chạy capabilities → prepare → pages/open_page → inspect/read_view với đúng dự án yêu cầu. Không nhận `pages` success làm xác nhận account/dự án. Nếu pending_login, người nhận tự đăng nhập hoặc dùng host vault đúng origin; plugin không nhập credentials.
7. Không profile-wide reload/restart DMS chỉ để dùng QAQC. Nếu connection chưa xuất hiện, nghiệm thu trong phiên mới trước; không thay server DMS.

## Kiểm thử
`python -m unittest discover -s tests -v` bằng interpreter đúng của Hermes. Python hệ thống/venv alias cũ có thể khác managed generation; kiểm `sys.executable`, phiên bản và import SDK trước chẩn đoán.

## Chưa nghiệm thu ở tài khoản khác
Fixture không là QAQC account/role live acceptance. Mỗi người kiểm riêng login/ACL/project/discipline, các luồng expanded/native/print/SharePoint và benchmark caller/model/chat. Không cam kết toàn site, cold login, OS khác hoặc tăng tốc model từ unit/Doctor. Approval và workflow grants vẫn riêng.

## Nguồn
- https://hermes-agent.nousresearch.com/docs/developer-guide/plugins
- https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference
- https://github.com/ChromeDevTools/chrome-devtools-mcp
- Hướng dẫn vận hành/module có sẵn trong skill đóng gói. `qaqc-site-map` và `qaqc-business-map` chỉ là phần bổ sung nếu người nhận đã cài, không bắt buộc.

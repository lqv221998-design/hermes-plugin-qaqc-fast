# Bắt đầu trên Hermes máy nhận — QAQC Fast 0.2.0-rc.1

## Link GitHub cài cái gì?
Repo có `plugin.yaml` + `__init__.py` ở **gốc**, nên native Hermes dùng URL repo trực tiếp, không `#subdir`. Đây là **Agent plugin**, không có Desktop pane: Review repository phải nhận Agent; không hứa Agent + Desktop UI như plugin Cognee tham chiếu. Enable đăng ký tool `qaqc_fast_session` và skills `qaqc-fast:setup`, `qaqc-fast:operations`.

Cài code từ Public GitHub không cần tài khoản GitHub của tác giả. **Không phải kết nối vào máy tác giả hoặc tự có phiên QAQC.** Mỗi máy giữ browser/profile/login/quyền/consent của chính mình. Chưa nghiệm thu mọi OS/role/UI; đây là prerelease, không tự nâng cấp khi clone.

## Cách cài native
**Kết quả kiểm Windows:** source clone public khớp đủ bytes, tests/Doctor/validator đạt; nhưng hai native CLI installs thử độc lập gặp WinError 5 ở staged publish/rename. Vì vậy flow bên dưới là workflow được hỗ trợ, **chưa là proof cài thành công cả plugin trên máy này/mọi máy**. Lỗi không tự chứng minh repo sai hoặc login thiếu; nguyên nhân chưa xác định. Không force overwrite, copy để che native failure, thay registry/core hoặc đổi credentials. Giữ log/state, xử lý host/PM gate qua workflow chính thức rồi nghiệm thu lại. Desktop physical UI/second-machine acceptance còn pending.

### Hermes Desktop
Capabilities → Plugins → Install plugin → Repository → dán URL repo → Review repository. Kiểm tên `qaqc-fast`, Agent component, exact source/commit, backend/profile đích và dependencies. Xác nhận cài/enable riêng theo UI; cài code không tự cấu hình MCP. Không Force reinstall lên bản đang làm việc.

### CLI
Từ đúng profile/backend, đọc `hermes plugins install --help` của phiên bản nhận trước. Với CLI đã kiểm, `hermes plugins install <URL-repo> --no-enable` cài disabled; pin immutable bằng `--ref <full-40-hex-commit-SHA>` lấy từ GitHub/tag đã kiểm, không đoán SHA. Sau consent riêng, enable `hermes plugins enable qaqc-fast --no-allow-tool-override`. Không cấp core tool override. Private/removed catalog/unsupported SDK/dependency refusal phải dừng, không force/bypass.

Sau cài, nạp `qaqc-fast:setup` để Hermes trên máy đó khảo sát và hướng dẫn. Hướng dẫn bên dưới cũng dùng được trước enable khi đọc README của repo.

## Điều kiện cần — code, backend và môi trường
| Gate | Điều kiện | Bằng chứng cần kiểm |
|---|---|---|
| Nguồn | Repo/commit/tag được lựa chọn và đủ authored files | Native review, exact commit SHA; không cài ZIP không rõ nguồn |
| Hermes SDK | Có register_tool/register_hook/register_skill, state/data-dir, native call_mcp; dispatch_tool giữ parent session/approval cho native/vision | Doctor trên **absolute installed directory**, thực tế tool/skill discovery; số version không tự chứng minh contract |
| Python | Dependencies native PM từ plugin.yaml: openpyxl==3.1.5, pypdf>=6,<7, Pillow>=11,<13 | Import trong **selected runtime interpreter**; alias venv cũ có thể khác. Không pip chèn managed generation |
| OS | Windows là host đã kiểm; điều khiển desktop cần interactive user session | Không dùng Session 0/headless/cloud như thể có GUI; macOS/Linux chưa full acceptance, restore helper hiện Windows |
| Browser/Node | Chrome/Node thuộc máy/backend được chọn, native Google chrome-devtools-mcp **1.10.1** | Source chính thức, CLI flags/version/Node engine thực tế; không thay latest chưa kiểm |
| Filesystem | MCP browser host và plugin host dùng được đúng file paths cho snapshot/upload/download | Native file capture/read-back; remote/WSL/container không chung filesystem phải dừng, không giả file local |
| Mạng | QAQC truy cập được theo mạng/VPN chính sách của người nhận; DevTools chỉ loopback | Không mở DevTools ra LAN/Internet; GitHub public không vượt QAQC ACL |

## Điều kiện cần — kết nối và quyền độc lập
1. **Consent từng bước:** provisioning dependencies, tạo/cấu hình connector, plugin mcp_allowlist, enablement và gắn browser. Link repo/cài code không là tất cả các consent đó.
2. Chrome riêng của người nhận. Người nhận tự login QAQC; không copy cookie/profile/token/password/OTP hoặc source account của tác giả. Login/SSO/2FA/permission do người nhận xử lý; secret chỉ qua vault hỗ trợ đúng origin hoặc nhập thủ công, không qua plugin/chat.
3. Native MCP key **chrome_qaqc**, settings.mcp_server và plugin mcp_allowlist phải khớp đúng key. Dùng native `mcp_servers` của Hermes, không shape `mcpServers` vendor. Mẫu [connector.example.json](connector.example.json) là **DATA**, enabled=false, trust=untrusted, binding trống. Không áp cả file để thay config hiện có.
4. Tools include đúng **list_pages,take_snapshot,click,wait_for,fill_form,upload_file,navigate_page**. Tắt resources/prompts/sampling/elicitation, usage statistics/CrUX/JavaScript evaluation và category không cần. Giữ DMS/connector khác nguyên trạng. Nếu filesystem guard cần roots, chỉ grant thư mục artifacts của plugin/selected file scope trên host thực, không --allowUnrestrictedPaths.
5. Tạo endpoint Chrome local của người nhận theo docs Chrome/Hermes; không dùng port/path của tác giả. Browser restore cần own executable/profile/debug_port được chọn, grant riêng; không tự đóng/restart Chrome để giải quyết quyền.
6. Cấu hình bằng native UI/public `hermes config set`, không thay toàn YAML. `expected_user_display_name` phải do người nhận xác nhận trên UI, mặc định trống phải block. Tên hiển thị không là unique principal; **backend QAQC ACL** là thẩm quyền.
7. Đúng dự án nguyên văn ở **header** cho mỗi call, không menuId/card/current project fallback. Nếu cần bộ môn, expected_discipline phải có selected/checked/pressed=true được quan sát, không label-only.
8. Read-only trước. Ghi chỉ có write_project TEST được grant và **hồ sơ mới QAQC-PLUGIN-TEST do plugin tạo/ghi ownership**. Không hỗ trợ ghi tùy ý vào hồ sơ production. Send/approve/reject/close có grant riêng và approval riêng; giữ workflow_transitions=[] nếu chưa được cấp.
9. Snapshot/controller errors, quota/login/denial/mismatch/uncertain effects là stop/pending, không controller khác/raw Chrome/hidden APIs/reset quota/replay. Plugin policy không là OS sandbox hoặc dịch vụ multi-user auth.

## Điều kiện đủ — chỉ cho phạm vi đã nghiệm thu
Cài + Doctor + MCP handshake **chưa đủ**. Để gọi kết nối đọc dùng được, cần **đồng thời**:
- Backend/profile/tool/skills mới thực sự nạp: mở chat mới, capabilities báo **0.2.0-rc.1** và expanded verbs; không sửa prompt/toolset chat cũ để né cache.
- pages quan sát page ID → inspect exact requested project kiểm nguồn/account/header → read_view/read_list kiểm discipline nếu yêu cầu, readiness/data counts/artifact thật. No rows/heading/ok=true không là loaded/empty/full inventory.
- Người nhận được QAQC cho truy cập module và UI phù hợp. Khác/thiếu control/template/permission giữ pending; code generic không chứng minh mọi UI.

Để gọi **một nghiệp vụ** dùng được, thêm nguồn/định danh/permission/preconditions đúng nghiệp vụ và **terminal read-back**:
- All-pages: từng batch, keys/dedupe/conflict, terminal pager và total reconciliation; virtualized/hidden gaps không tự bao phủ.
- Create/edit/upload: approval + ownership + fields/ID/status/attachment readback sau successful uncached reload; remote attachment bytes chưa verified.
- Delete: observed exact return list + reload/all-pages absence; empty shell không là xóa thành công.
- Native: exact pid/window, reviewed capture SHA/active surface, fresh matching pixels/elements, one-use handoff; driver effect không là business persistence.
- Export/download/print: selected new path, một trigger có ledger, file mới ổn định/hết partial/đúng format/hash; click/toast/print prompt không là hoàn tất.
- Restore: exact owner/listener recovered, rồi kiểm lại browser/account/project/data; listener không là login proof.

**Không có bộ điều kiện cấu hình nào đủ bảo đảm “mọi chức năng trên mọi Hermes/QAQC UI”.** Phải nghiệm thu trên máy/role/nguồn được chọn. Các checks chỉ đủ cho phạm vi và thời điểm được kiểm.

## Tuỳ chọn không bắt buộc cho đọc cơ bản
- Computer Use: host-supported dispatcher/session/approval + cua-driver hoạt động trên interactive desktop. Chỉ dùng trong executor; không fallback sau refusal. `hermes computer-use doctor` kiểm health, không chứng minh click tới control.
- Vision: model/route do recipient chọn hỗ trợ ảnh; nội dung chọn có thể được xử lý bởi provider đó. Không hứa zero egress.
- OCR: MinerU local endpoint explicit, OpenAPI/format thực tế được kiểm; mặc định trống, không OCR fallback. Không ship service/binary/model của tác giả. Kết quả unreviewed/non-normative.
- Restore: mặc định false, own bindings/grant riêng. Không clone profile.

## Giới hạn phải biết trước
SharePoint source/revision/download chưa hoàn thiện/nghiệm thu; XLSX reader chỉ local file đã chọn, không là authenticated SharePoint connection. PDF text layers có scan/OCR gaps; full_document_read=false. XLSX không tính formula. DOCX/CSV/ZIP content reader chưa có. Native/print/template-specific live flows và caller/model/chat/baseline benchmark còn pending; không kết luận nhanh hơn từ fixtures.

Dữ liệu riêng nằm trong plugin data, không install tree. Không đưa state/receipts/screenshots/credentials/live documents vào repo, không tự publish company rules/Brain. Troubleshoot theo gate thất bại, không reinstall để chữa runtime/login/config sai.

Nguồn: https://hermes-agent.nousresearch.com/docs/developer-guide/plugins ; https://hermes-agent.nousresearch.com/docs/reference/package-management ; https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference ; https://github.com/ChromeDevTools/chrome-devtools-mcp ; https://developer.chrome.com/blog/remote-debugging-port .

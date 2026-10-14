# Prerequisites & thiếu thư viện — QAQC Fast 0.2.0-rc.3

Đọc trước cài/cấu hình. Khảo sát máy/backend/profile thật; **chỉ bổ sung phần thiếu sau consent**, không reinstall tất cả. Đây là hướng dẫn, không installer tự chạy. Plugin không chia sẻ browser/account/quyền của tác giả. Mặc định context_policy=auto, không nhập tên account/project.

## 1. Bảng phần mềm/thư viện thực sự cần

| Thành phần | Dùng cho | Kiểm | Khi thiếu |
|---|---|---|---|
| Hermes Agent + native PluginContext SDK | Tool, skills, state và native MCP | hermes --version, hermes doctor, plugin Doctor/version/actions | Đúng installer/update owner Hermes; không sửa core/registry |
| Python runtime do Hermes quản lý | Plugin Python | prepare.python_runtime.executable/version; import thật trong đúng interpreter | Bundled app có Python; source installer/PM bootstrap. Không cài Python hệ thống để thay managed runtime |
| Git | Native Repository install/update | git --version, hoặc PM installed-tool lookup | Sau consent: hermes pm install git --tools-only nếu bản nhận có lệnh này |
| Node.js + npm | Google Chrome MCP | node --version, npm --version, executable thực tế | Sau consent: hermes pm install node npm --tools-only; kiểm lại managed paths/version, không đổi pins bằng pm update |
| chrome-devtools-mcp 1.10.1 | Kết nối Chrome qua native STDIO | package.json version + engine, entrypoint --version/--help | Scoped npm install hoặc reuse đúng bản, không npm global mặc định |
| Google Chrome của người nhận | Own QAQC login/session | executable/version + endpoint loopback được cấp phép | Nguồn Google chính thức, browser attachment consent; không copy profile hoặc tự đóng Chrome |
| openpyxl==3.1.5 | Đọc XLSX | import openpyxl + distribution version | Native plugin dependency admission/PM sync, không pip chèn venv |
| pypdf>=6,<7 | Đọc PDF text layers | import pypdf + version | Native plugin dependency admission/PM sync |
| Pillow>=11,<13 | Verify/đọc ảnh | import PIL.Image + Pillow distribution version | Native plugin dependency admission/PM sync |
| cua-driver | Native dialog/canvas khi thực sự cần | hermes computer-use doctor theo CLI bản nhận | Optional: hermes pm install cua-driver sau consent; không bắt buộc đọc DOM cơ bản |
| MinerU | OCR scan/ảnh khi chọn OCR | Endpoint explicit trên máy/backend nhận, OpenAPI/task/file readback | Optional, consent riêng; không tự cài Docker/model hoặc dùng endpoint tác giả |

Node engine của MCP **1.10.1**: `^20.19.0 || ^22.12.0 || >=23`. Không rút gọn thành mọi Node >=20.19 (Node 21 không thuộc range). Ưu tiên managed Node phù hợp từ Hermes PM; nếu dùng OS-owned Node, nguồn https://nodejs.org/en/download và kiểm đúng OS/architecture/SHASUMS. Không nâng một runtime đang làm việc chỉ vì có latest mới.

Python hiện hành của first-party Hermes là 3.14 theo docs; range hỗ trợ updater cũ không là cam kết SDK/runtime đầy đủ trên mọi Python. Kiểm receiving build thực tế. `python`, `python3`, `pip` trên PATH có thể thuộc ba môi trường khác nhau. **Không dùng bare pip/pip3/uv pip để sửa Hermes.**

## 2. Khảo sát read-only trước

- Xác định native desktop/source/container/remote backend và active profile; tools chạy tại backend, không mặc định tại máy có cửa sổ chat.
- Đọc official docs và `hermes plugins install --help`, `hermes plugins enable --help`, `hermes pm install --help`, `hermes mcp add --help` của receiving build.
- `hermes doctor`, `hermes pm doctor`, `hermes pm status`; chỉ chia sẻ kết quả non-secret. `hermes pm env`/installed-tool lookup có thể chỉ ra tools đã có nhưng chưa vào PATH. Không cài trùng chỉ vì command not found.
- Nếu plugin đã nạp: capabilities → prepare. prepare không gọi MCP; dependency_imports thực sự import openpyxl/pypdf/PIL.Image, trả version hoặc error_type. find_spec=true **không đủ** khi native subdependency bị hỏng.
- prepare.ok chỉ nói local config gate, không khẳng định mọi imports, MCP/login/ACL đã đạt. Đọc từng dependency_imports entry. Missing document library không chứng minh browser không hỗ trợ URL.
- Nếu chưa nạp: native Doctor trên absolute installed directory và kiểm import bằng **selected interpreter** do launcher/PM của đúng installation chọn. Không ghép site-packages từ Python khác.

## 3. Bổ sung Python dependencies bằng owner đúng

1. Review plugin.yaml: ba requirements ở bảng trên. Native install disabled vẫn có bước consent deps; không mặc định --no-deps khi muốn ready.
2. Sau consent enable: `hermes plugins enable qaqc-fast --no-allow-tool-override`. Native PM kết hợp core + extras + enabled plugins thành union, kiểm rồi mới chọn generation. Plugin installation/enablement không cấp quyền MCP/browser.
3. Nếu đã enabled nhưng requirements thiếu/currency sai: giữ bản đang làm việc, xem PM receipt. Theo public PM API của bản nhận, `pm.sync_venv(explicit=True)` sync union đang enabled; chạy bằng installation-owned environment, không từ Python hệ thống. Đây là dependency sync, không phải protected business tool dispatch. Đọc docs/API receiving build trước gọi.
4. Nếu generation bị hỏng sau install: sau consent `hermes pm repair` replay graph/lock đã lưu, không tự thêm requirements mới. Không dùng repair để suy rằng một plugin chưa enabled đã được admit.
5. Admission/refusal/permissions/no wheels/compiler errors: ghi error class + dependency, giữ selection cũ; không pip fallback, không tắt plugin khác để ép thành công.
6. Khi generation đổi, mở phiên/runtime mới phù hợp rồi chạy prepare/import lại. Không chèn imports vào tiến trình đang chạy.

## 4. Node/npm và Google MCP — cài scoped khi thiếu

Sau consent và kiểm CLI hỗ trợ, PM named install chỉ tools, không bare install kéo thêm mọi extras:

`hermes pm install node npm --tools-only`

Read back exact Node/npm paths/versions. Nếu backend/container package owner không cho thay runtime, báo capability pending và dùng owner workflow được hỗ trợ; không giả đã cài trên host khác.

Chọn `<LOCAL_MCP_DIR>` mới, thuộc người nhận, không ghi đè package đang chạy. Nếu chưa có MCP 1.10.1, sau dependency/download consent:

`npm install --prefix "<LOCAL_MCP_DIR>" --save-exact chrome-devtools-mcp@1.10.1`

`<LOCAL_MCP_DIR>` là placeholder phải resolve trước thực hiện, không copy nguyên. Npm có thể tải dependencies/chạy lifecycle scripts; khai báo với người nhận. Không npm ci clone developer repo/build toàn TypeScript toolchain để chỉ dùng published MCP. Không global install hay xóa npm cache đang dùng.

Kiểm `<LOCAL_MCP_DIR>/node_modules/chrome-devtools-mcp/package.json` đúng version/engine và binary entry `build/src/bin/chrome-devtools-mcp.js`. Dùng absolute Node + entrypoint theo máy nhận; Windows npm.cmd có thể cần invocation phù hợp shell. Thử --version/--help chỉ kiểm package executable, không login QAQC.

Tạo/reuse native server key chrome_qaqc qua Hermes UI/CLI nhận được support, theo connector.example.json. Mẫu là DATA; không áp cả config lên máy. Consent riêng cho config/mcp_allowlist/enable/browser grants. Bảo toàn DMS/connector khác, không copy author profile/port, không trust upgrade sau refusal. `hermes mcp test chrome_qaqc` chỉ handshake/schema, không chứng minh browser attachment hoặc account/ACL.

## 5. Template: tách đúng loại, không cài nhầm

- **Template Nhật ký/Hồ sơ trên QAQC** do server/dự án/bộ môn quản lý. Thông báo “Chưa có cấu hình Template Nhật ký cho Dự án và Lĩnh vực này.” là business configuration blocker; không chữa bằng npm, pip, Node, Jinja2 hay docxtpl. Báo administrator đúng quyền; không tự chỉnh template global hoặc tạo lại hồ sơ.
- **Python/JS template engine của Hermes** thuộc dependency graph của Hermes. Nếu Hermes báo missing module thật, trace import/requirement và sửa qua owner PM; không thêm thư viện phỏng đoán.
- **Sinh Word/Excel/PDF theo mẫu local** không là chức năng template generator của plugin này. Không tự cài python-docx/docxtpl/Jinja2/reportlab/pandas/Playwright để hứa có feature chưa được implement. Muốn bổ sung: cần nhiệm vụ, template/source chọn và code/tests/declared dependencies riêng.
- DOCX/CSV/ZIP reader chưa có; cài thư viện không tự bổ sung action hoặc ACL. Không tải/nạp toàn thư viện templates DMS để setup QAQC.

## 6. Nghiệm thu tối thiểu sau bổ sung

- Installed files/version, enablement, native Doctor/validator đúng target.
- Actual selected-runtime imports + versions; Node/npm/MCP binary/package version; native handshake/schema.
- Chat mới thấy RC3 skills/actions, prepare.context_policy=auto và manual_context_required=false.
- Own Chrome/login/account/QAQC permissions; pages → inspect/read_view hoặc open_page theo URL đã chọn, không nhập tên. URL đúng + context + readiness/artifact là các kết quả riêng.
- Record writes/transition vẫn cần operator approval, TEST ownership scope và backend quyền hiện có. Không tăng/quét quyền QAQC, không service account/tokens tác giả.

**Native Windows Git install gate:** RC1/RC2 fresh installs đã gặp WinError 5 ở staged publication/rename, nguyên nhân chưa xác định. Dependency guidance không sửa được gate này. Giữ pending; không force/manual-copy/core patch để tuyên bố install PASS. Source/Doctor/SDK/tests không là physical independent-machine acceptance. Không có prompt nào bảo đảm bỏ qua login/ACL/OS policy.

## Nguồn chính thức đã đối chiếu
- https://hermes-agent.nousresearch.com/docs/getting-started/installation
- https://hermes-agent.nousresearch.com/docs/reference/package-management
- https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference
- https://raw.githubusercontent.com/ChromeDevTools/chrome-devtools-mcp/chrome-devtools-mcp-v1.10.1/package.json
- https://github.com/ChromeDevTools/chrome-devtools-mcp
- https://nodejs.org/en/download
- https://www.google.com/chrome/

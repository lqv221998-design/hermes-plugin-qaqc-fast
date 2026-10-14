---
name: tasks
description: Use when asked to open QAQC links/tabs or read diaries.
version: 0.2.0-rc.2
license: MIT
platforms: [windows]
---
# QAQC Fast — từ yêu cầu đến thao tác

Plugin này giúp Hermes mở và quan sát QAQC, đọc nhật ký/hồ sơ/ảnh/rủi ro, tra cứu và xử lý **hồ sơ thử được grant** có read-back. Không thay kỹ sư/ký duyệt, không nâng ACL và không điều khiển website khác. Nạp operations trước browser work; setup khi thiếu prerequisite. Không cần thư viện skills/memories riêng của tác giả.

## Bắt đầu mỗi máy/phiên mới
1. Gọi `qaqc_fast_session` với `{"action":"capabilities"}`. Bản này phải trả `0.2.0-rc.2` và có prepare/open_page/open_page_status. Không có thì **runtime chưa đúng**, không đoán giới hạn từ README mới; kiểm cài/enable/profile rồi mở phiên mới.
2. Nạp `qaqc-fast:setup`, `qaqc-fast:operations`, skill này. Không tìm thấy skill → discovery/activation pending; đọc START-HERE-HERMES.md trực tiếp để chẩn đoán, không raw browser fallback.
3. `{"action":"prepare"}` không gọi browser, không cài/configure gì, không đọc account/cookies. Thiếu expected_user_display_name → xin người nhận xác nhận tên hiển thị của mình và consent cấu hình. Không tự adopt account đang mở. Import specs không là dependency import/handshake/site acceptance.
4. Hỏi tên dự án chính xác nếu thiếu; hỏi phạm vi ghi nếu yêu cầu còn mơ hồ. URL parameters không phải tên dự án. Không yêu cầu password/OTP/token trong chat.

## Chọn đúng action
| Người dùng nói | Luồng | Không được suy |
|---|---|---|
| “Plugin làm gì/cài chưa?” | capabilities → prepare | Không gọi pages để chẩn đoán cả capability scope |
| “Mở link QAQC này” | open_page mode reuse trên page_id đã quan sát, hoặc mode new khi người dùng chọn tab mới | pages không mở Chrome; không sửa URL/IDs |
| “Mở tab QAQC mới” | open_page mode new; cần allow_open_page/allow_new_tab và native new_page include | Không đổi connector/profile hoặc tự grant |
| “Xem nhật ký/ảnh/hồ sơ” | mở đích → read_view, hoặc recipe legacy open_module/read_list | Ba recipe không là toàn bộ RC scope; current-page không là inventory |
| “Tìm/lọc ngày” | query với label/fields thực sự quan sát | Không đoán control ngày hoặc records bị ẩn |
| “Xem hồ sơ này” | open_record đúng record_id/detail_label/tabs | Không suy record_id từ dòng đầu |
| “Sửa nhật ký” | đúng row → Chỉnh sửa → kiểm template/control → write_record chỉ nếu plugin-owned TEST scope | Không sửa hồ sơ production có sẵn hoặc template global |
| “Gửi/duyệt/từ chối/đóng” | transition_record và grant/approval riêng | Đọc trang trình duyệt/cấu hình không là gửi/duyệt |
| “Xuất/tải/in” | begin_transfer → verify_transfer | Click/toast không là file hoàn tất; uncertainty không replay |
| “Chrome đóng” | setup/diagnose → controlled restore khi grant đúng owner | Không repoint/kill browser khác |

Đọc [ví dụ gọi tool](references/examples.md) và [Nhật ký thi công](references/construction-diary.md) trước tác vụ tương ứng. Các giá trị Fixture trong ví dụ là dữ liệu synthetic, **phải thay bằng thông tin người dùng chọn/quan sát**, không chạy literal fixture trên live site.

## Lỗi → kết luận đúng
- pending_user_binding + mcp_calls=0: chỉ chứng minh thiếu binding; **chưa kiểm browser/trang/ACL**. Không kết luận “trang không hỗ trợ” hay dự báo destination_not_verified.
- pages rỗng: không có tab thuộc nhóm được liệt kê; bootstrap/home có trạng thái riêng. Không là mất quyền/không có hồ sơ.
- pending_login: người nhận tự login trên đúng Chrome. Không đổi account/controller.
- project_mismatch/user_mismatch/permission_denied: dừng; không tự chấp nhận project/account khác.
- destination_not_verified: URL hoặc heading **thực tế sau thao tác** chưa khớp, không là lỗi suy trước khi mở.
- host_mcp_blocked_or_failed: setup gate chưa phân loại. Giữ attempted operation, không blind retry.
- open_page_pending_no_replay: đọc open_page_status với cùng operation_id, sau khi người dùng xử lý login/permission phù hợp; status chỉ quan sát, không mở lại. Không mint ID mới để replay. Chưa rõ tab nào → giữ pending.

## Báo cáo kết quả
Nêu version/action, source, project/account verification (không secrets), heading nếu được kiểm, readiness và coverage trang hiện tại. Phân biệt navigation đã verified với đọc data/ghi persistent/file verified. pending không completion. Đưa đúng next step nhỏ nhất, không yêu cầu người dùng chạy lại toàn bộ setup.

## Acceptance
First-use fixtures/Doctor/actual host registration chứng minh contract, không chứng minh mọi model sẽ luôn chọn đúng hoặc QAQC login/ACL/live templates trên mọi máy. Mỗi recipient vẫn nghiệm thu riêng. Native install Windows host gate chưa tự hết vì đổi docs/code; không force/core patch để che lỗi.

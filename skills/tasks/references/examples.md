# Ví dụ gọi qaqc_fast_session

Các JSON dưới đây là **request mẫu hợp schema**, không phải kết quả site được dựng. Fixture Project/Fixture IDs là synthetic: thay bằng project/URL/page_id/labels người dùng chọn hoặc quan sát trên máy nhận. Không copy dữ liệu/binding/profile tác giả. Chỉ dùng native executor, không terminal dispatch/raw Chrome để vượt hook.

## 1. Kiểm bản và chuẩn bị
```json
{"action":"capabilities"}
```
```json
{"action":"prepare"}
```
Prepare kiểm local config và actual dependency imports, mcp_calls=0; không handshake/browser/login proof. Runtime phải 0.2.0-rc.3. Default auto không cần tên. Đọc từng dependency_imports entry; thiếu thư viện theo PREREQUISITES.md, không pip fallback.

## 2. Tab hiện có
```json
{"action":"pages"}
```
pages có `pages` cho business routes và `bootstrap_pages` cho root; không tự login/open browser. Chọn đúng page_id được trả. Inspect:
```json
{"action":"inspect","page_id":9}
```

## 3. Mở link người dùng chọn trong tab mới
Sau consent: allow_open_page=true, allow_new_tab=true, native include new_page và own Chrome kết nối. Auto mode không hỏi tên dự án/account; project tự quan sát từ header. expected_project chỉ thêm khi user chỉ định explicit target.
```json
{"action":"open_page","url":"https://qaqc.newtecons.vn/#/nhat-ky-thi-cong/1/fixture/fixturegs","mode":"new","operation_id":"open-diary-fixture"}
```
Không truyền page_id ở mode new; plugin xác định duy nhất tab mới từ before/after inventory, mở background, không steal focus. Nếu heading đã được quan sát và cần đối chiếu, thêm `destination_heading` đúng nguyên văn; nếu chưa biết thì không đoán. page_opened_context_verified = đúng URL/user/project, **chưa data readiness/đọc toàn danh sách**.

## 4. Tái sử dụng tab QAQC được chọn
```json
{"action":"open_page","url":"https://qaqc.newtecons.vn/#/nhat-ky-thi-cong/1/fixture/fixturegs","mode":"reuse","page_id":9,"operation_id":"reuse-diary-fixture"}
```
Kiểm account/project/source trước navigate; không ghi đè tab website khác. Tab nguồn phải là business route của đúng project, không bootstrap/login root. Different project → stop, không tự adopt hoặc đổi mode để lách; xác nhận việc chuyển ngữ cảnh qua workflow được cấp quyền.

## 5. Chỉ mở trang gốc để bootstrap
```json
{"action":"open_page","url":"https://qaqc.newtecons.vn/","mode":"new","operation_id":"open-root-fixture"}
```
Không cần binding tên; vẫn cần browser grants và own Chrome. Không tự login. Bootstrap chỉ xác minh tab/root URL, không business/account/project. Redirect chưa kiểm giữ pending; sau login dùng inspect/read_view hoặc đối soát same attempt, không mở lặp.

## 6. Login/transport pending: chỉ đối soát attempt đã có
```json
{"action":"open_page_status","operation_id":"open-diary-fixture"}
```
Chỉ đọc same session/attempt, không create/navigate/cancel/reset/replay. User/project/discipline/URL/heading đã quan sát được giữ. Khác session/scope hoặc không biết owned tab → pending, không tự nhận ledger cũ/nhập credentials.

## 7. Đọc trang vừa mở
```json
{"action":"read_view","page_id":9,"expected_discipline":"XÂY DỰNG"}
```
Chỉ truyền expected_discipline khi người dùng yêu cầu và có thể kiểm selected-state. Kết quả readiness=false chưa chứng minh rỗng/loaded. Đọc artifact được trả khi cần toàn rows/text/links; không chỉ dựa vào count. Coverage current_page_only.

## 8. Ba recipe không giới hạn toàn executor
```json
{"action":"read_list","module":"work_acceptance","page_id":9}
```
Module legacy chỉ work_acceptance/photos/quality_risks. Nhật ký/trình duyệt có route families và read_view/navigate riêng; không gán nhầm module legacy.

## 9. Tra cứu và chi tiết — labels phải quan sát
```json
{"action":"query","page_id":9,"fields":{"Từ khóa":"Fixture keyword"},"submit_label":"Tìm kiếm"}
```
```json
{"action":"open_record","page_id":9,"record_id":"Fixture Record","detail_label":"Xem chi tiết","tabs":["Lịch sử"]}
```
Không chạy labels mẫu nếu UI thực không có. Nếu requested thao tác không có schema hoặc UI, báo gap; không chuyển raw browser.

## 10. Ghi là scope khác
write_record/upload_attachment/delete_record chỉ hồ sơ QAQC-PLUGIN-TEST mới do plugin sở hữu, đúng TEST đã grant. Không thể dùng open_page để cấp quyền sửa hồ sơ production có sẵn. Gửi/duyệt/từ chối/đóng cần workflow_transitions và approval riêng. Luôn đọc lại sau successful reload; uncertain giữ journal, không tạo op ID khác.

## Mẫu trả lời
“Runtime …; URL …; user/project … verified/unverified; heading …; coverage current_page_only; readiness …; đã/chưa có terminal read-back. Pending ở gate …; next step ….” Không nói mọi module đã hỗ trợ, mọi máy đã cài, hoặc tốc độ tăng từ fixtures.

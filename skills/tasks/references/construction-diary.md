# Nhật ký thi công — recipe portable, không là giấy phép ghi

## Yêu cầu “mở link nhật ký này”
1. capabilities → prepare → local grants/MCP/browser người nhận; không binding nhập tay. Thiếu dependencies theo PREREQUISITES.md.
2. Nhận nguyên URL QAQC đã chọn, project tự quan sát từ header. Chỉ dùng expected_project nếu user chỉ định target riêng. Không suy IDs hoặc dùng dữ liệu tác giả.
3. Nếu người dùng chọn tab mới, open_page mode new; nếu reuse thì chọn đúng page_id từ pages và kiểm project nguồn. Source/home/login có states riêng; pages không launch.
4. Exact URL sau mở, account/header/project phải khớp; expected_discipline khi yêu cầu phải selected-state. Heading chỉ xác minh nếu có expected heading thực được quan sát, không dựng heading để ép pass.
5. read_view kiểm readiness và artifact. Chưa có data_ready_verified giữ partial. URL đúng không tự chứng minh có nhật ký hoặc toàn danh sách.

## Yêu cầu “vào nhật ký” khi không có URL
Recipe ngữ nghĩa đã quan sát lịch sử: **QAQC → Tình hình thi công → Nhật ký thi công**. Dùng menu_path/destination_heading thật ở account hiện tại; tham chiếu lịch sử không chứng minh UI/ACL trên mọi recipient. Menu labels/heading thiếu hoặc khác → pending/discovery có phạm vi, không guessed link/UID/API.

## Yêu cầu “xem/sửa nhật ký ngày …”
- Đối chiếu project đã quan sát, discipline, date và row identity trước mở. Hỏi ngày/đích mới nếu chưa rõ ý định, không bắt gõ lại project hiện tại, không chọn row đầu.
- Trình tự đã quan sát lịch sử: tạo header → về list → chọn đúng row → **Chỉnh sửa** → form. “Xem chi tiết” hoặc form tự mở không thay bước Chỉnh sửa.
- **Tạo nhật ký có thể lưu header ngay trước nhập nội dung.** Form trống/gián đoạn không là chưa tạo. Đối soát row/date trước quyết định tiếp, không tạo lặp.
- Nếu sau đúng Chỉnh sửa vẫn hiện “Chưa có cấu hình Template Nhật ký cho Dự án và Lĩnh vực này.” và không có fields: đây là blocker template **quan sát ở scope đó**, không tự suy cho project khác. Không bấm Lưu/Tổng hợp lại số liệu hay sửa template global để chữa; cần administrator được phép.
- Code hiện chỉ ghi hồ sơ thử mới do plugin sở hữu trong TEST được grant. Không cấp quyền sửa diary thực có sẵn chỉ vì recipient có QAQC ACL. Cần triển khai/consent scope production riêng trước hỗ trợ; không nới guard trong setup.
- Dữ liệu synthetic phải ghi rõ thử nghiệm; không tự tạo sự kiện thi công, nghiệm thu, chữ ký hoặc quyết định kỹ thuật. Saved/persistent proof cần successful reload và read-back đúng identity/fields; click/toast không là kết quả.

## Phân biệt cấu hình/trình duyệt và workflow
Trang cấu hình hồ sơ/trình duyệt có thể được quan sát qua route family/read_view khi đủ prerequisites/ACL; không chỉ ba recipe legacy. Đọc trang ≠ sửa cấu hình ≠ gửi/duyệt. workflow_transitions=[] chỉ đóng transition quyền ghi, không chứng minh trang không đọc được.

## Nguồn và coverage
Recipe diary dựa trên quan sát lịch sử, không kèm IDs/records/credentials; RC3 auto open/read fixtures chỉ là contract. Live destination/template/role người nhận kiểm riêng. Không bắt cài skills của tác giả; template QAQC thiếu không chữa bằng npm/pip.

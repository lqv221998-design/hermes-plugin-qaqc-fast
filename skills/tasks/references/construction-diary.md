# Nhật ký thi công — recipe portable, không là giấy phép ghi

## Yêu cầu “mở link nhật ký này”
1. capabilities → prepare → binding/grants/MCP/browser local của recipient.
2. Nhận nguyên URL QAQC được chọn và **tên dự án do người dùng xác nhận**. Không coi route parameters là project/user ID. Không thay IDs bằng lịch sử tác giả.
3. Nếu người dùng chọn tab mới, open_page mode new; nếu reuse thì chọn đúng page_id từ pages và kiểm project nguồn. Source/home/login có states riêng; pages không launch.
4. Exact URL sau mở, account/header/project phải khớp; expected_discipline khi yêu cầu phải selected-state. Heading chỉ xác minh nếu có expected heading thực được quan sát, không dựng heading để ép pass.
5. read_view kiểm readiness và artifact. Chưa có data_ready_verified giữ partial. URL đúng không tự chứng minh có nhật ký hoặc toàn danh sách.

## Yêu cầu “vào nhật ký” khi không có URL
Recipe ngữ nghĩa đã quan sát lịch sử: **QAQC → Tình hình thi công → Nhật ký thi công**. Dùng menu_path/destination_heading thật ở account hiện tại; tham chiếu lịch sử không chứng minh UI/ACL trên mọi recipient. Menu labels/heading thiếu hoặc khác → pending/discovery có phạm vi, không guessed link/UID/API.

## Yêu cầu “xem/sửa nhật ký ngày …”
- Đối chiếu exact project, discipline, date và row identity trước mở. Nếu chưa biết tên project/ngày thì hỏi, không dùng row đầu.
- Trình tự đã quan sát lịch sử: tạo header → về list → chọn đúng row → **Chỉnh sửa** → form. “Xem chi tiết” hoặc form tự mở không thay bước Chỉnh sửa.
- **Tạo nhật ký có thể lưu header ngay trước nhập nội dung.** Form trống/gián đoạn không là chưa tạo. Đối soát row/date trước quyết định tiếp, không tạo lặp.
- Nếu sau đúng Chỉnh sửa vẫn hiện “Chưa có cấu hình Template Nhật ký cho Dự án và Lĩnh vực này.” và không có fields: đây là blocker template **quan sát ở scope đó**, không tự suy cho project khác. Không bấm Lưu/Tổng hợp lại số liệu hay sửa template global để chữa; cần administrator được phép.
- Code hiện chỉ ghi hồ sơ thử mới do plugin sở hữu trong TEST được grant. Không cấp quyền sửa diary thực có sẵn chỉ vì recipient có QAQC ACL. Cần triển khai/consent scope production riêng trước hỗ trợ; không nới guard trong setup.
- Dữ liệu synthetic phải ghi rõ thử nghiệm; không tự tạo sự kiện thi công, nghiệm thu, chữ ký hoặc quyết định kỹ thuật. Saved/persistent proof cần successful reload và read-back đúng identity/fields; click/toast không là kết quả.

## Phân biệt cấu hình/trình duyệt và workflow
Trang cấu hình hồ sơ/trình duyệt có thể được quan sát qua route family/read_view khi đủ prerequisites/ACL; không chỉ ba recipe legacy. Đọc trang ≠ sửa cấu hình ≠ gửi/duyệt. workflow_transitions=[] chỉ đóng transition quyền ghi, không chứng minh trang không đọc được.

## Nguồn và coverage
Recipe diary dựa trên quan sát UI đã lưu ở skill tác giả; không kèm live project IDs/records/credentials. Chỉ nguyên tắc/labels/giới hạn được chuyển. Native RC2 open/read fixtures chứng minh contract; live destination/template/role của recipient phải nghiệm thu riêng. Không yêu cầu cài skill qaqc-site-map/qaqc-business-map của tác giả.

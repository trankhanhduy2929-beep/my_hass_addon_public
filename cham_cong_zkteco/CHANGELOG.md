# Changelog

## 2.0.5

- Thêm chế độ **giờ tạm / đặt giờ tùy chọn** ngay trên trang **Tổng quan**, dùng cùng cơ chế an toàn với preset: đặt giờ theo ý muốn, giữ 3–300 giây, nhận vân tay rồi tự trả về GMT+7 hoặc trả ngay bằng nút khôi phục.
- Banner đếm ngược giờ tạm hiển thị toàn cục trên điện thoại và desktop, kể cả khi đang ở tab khác; trạng thái ghi rõ nguồn từ Tổng quan hay preset.
- Thay polling lượt chấm cố định bằng long-poll có đánh thức ngay khi Live Capture ghi bản ghi mới; request tự hủy khi tab ẩn và tự nối lại khi tab hiện.
- Giảm tải máy ZKTeco bằng cache metadata 15 phút, cache giờ có nội suy ngắn, chống kết nối trùng và bỏ lệnh `disable_device()`/`enable_device()` không cần thiết khi đặt giờ.
- Ranh giới lệnh được siết rõ: lớp thiết bị chỉ gọi `conn.set_time(value)` với một đối số `datetime`; username, cookie, header, session và tên nút chỉ lưu cục bộ trong audit/trạng thái.
- SQLite bật WAL checkpoint/busy timeout/synchronous phù hợp trên từng connection, giới hạn journal dư và tránh giữ connection trong lúc long-poll.
- Sửa đồng bộ nhân viên khi UID thay đổi, vô hiệu hóa user không còn trên máy, chống chạy hai full sync đồng thời và không còn đọc/lưu PIN hoặc password nhân viên; dữ liệu password cũ được xóa trắng khi migrate.
- Sửa bộ lọc theo ngày để dùng thời gian hiệu lực sau điều chỉnh, đánh dấu lượt chấm lẻ thay vì hiển thị như giờ ra, bảo vệ CSV khỏi formula injection và bổ sung trang login/setup standalone còn thiếu.
- Tối ưu modal đặt giờ cho màn hình nhỏ, touch target, safe area và reduced motion; đồng hồ vẫn chạy cục bộ từng giây nhưng chỉ đọc lại phần cứng theo chu kỳ nhẹ.

## 2.0.4

- Thêm chế độ **giờ tạm an toàn** cho từng preset, cấu hình hiệu lực từ 3 đến 300 giây và mặc định 10 giây.
- Sau khi hết thời gian, Add-on tự đặt máy về giờ hiện tại của `Asia/Ho_Chi_Minh` (GMT+7).
- Có tùy chọn nhận lượt chấm qua Live Capture rồi rút ngắn thời gian khôi phục, đồng thời vẫn giữ timer tối đa làm lớp dự phòng.
- Hiển thị banner đếm ngược trực tiếp, trạng thái đã nhận lượt chấm, lỗi phục hồi/retry và nút **Trả về GMT+7 ngay**.
- Lưu phiên giờ tạm trong SQLite; khi Add-on khởi động lại, phiên còn dang dở được khôi phục hoặc trả giờ ngay nếu đã quá hạn.
- Khi Add-on dừng bình thường, hệ thống cố gắng trả thiết bị về GMT+7 trước khi thoát; nếu thiết bị mất kết nối, worker tự thử lại mỗi 5 giây khi Add-on hoạt động.
- Giữ tương thích với preset cũ: dữ liệu từ 2.0.3 được migrate tự động và mặc định ở chế độ **Đặt và giữ nguyên**.

## 2.0.3

- Sửa luồng tạo preset để card xuất hiện ngay từ response POST, không phụ thuộc request GET có thể bị cache.
- Thêm `Cache-Control: no-store` cho trang động/API và `fetch(..., cache: "no-store")` để tránh frontend/backend lệch phiên bản trong Home Assistant Ingress.
- Thiết kế lại hoàn toàn tab **Đặt giờ** với hero, đồng hồ thiết bị, card preset lớn và trạng thái thao tác hiển thị trực tiếp.
- Chuyển form tạo preset sang modal tối ưu điện thoại, có xem trước nút và các lựa chọn nhanh Bây giờ/Hôm nay/Ngày mai/+7 ngày.
- Thêm sửa tên, ngày và giờ của preset đã lưu bằng API `PUT`.
- Cải thiện thông báo lỗi: lỗi tạo/sửa hiển thị ngay trong modal thay vì chỉ hiện toast ngắn.
- Giữ thao tác **Đặt giờ ngay** một chạm theo yêu cầu; xóa preset vẫn có bước xác nhận.

## 2.0.2

- Thêm menu **Giờ thủ công** riêng trên thanh điều hướng.
- Cho phép tạo không giới hạn nút preset gồm tên, ngày và giờ tùy chọn.
- Lưu preset bền vững trong SQLite `/data/cham_cong.db` để giữ nguyên sau khi khởi động lại Add-on.
- Bấm nút preset để đặt ngay đúng ngày giờ đã lưu lên máy ZKTeco.
- Cho phép xóa từng nút preset và ghi audit cho thao tác tạo, áp dụng và xóa.
- Tối ưu bố cục preset dạng lưới cho desktop và một cột nút lớn trên điện thoại.

## 2.0.1

- Sửa lỗi 422 với trình duyệt còn cache bản cũ gửi `limit=5000`; backend tự giới hạn xuống 200 thay vì từ chối request.
- Thêm công cụ dò IP máy chấm công trong mục Thiết bị.
- Hỗ trợ quét IPv4 CIDR tối đa /22, kiểm tra cổng 4370 và xác minh serial/model ZKTeco trước khi hiển thị.
- Cho phép sao chép IP tìm được để cập nhật lại cấu hình `zk_ip` của Add-on.
- Giữ nguyên ranh giới bảo mật: danh tính người dùng web không được chuyển vào scanner hoặc command ZKTeco.

## 2.0.0

- Thêm menu xuất báo cáo toàn nhân viên theo ngày, tháng hoặc năm.
- Báo cáo có giờ vào/ra, tổng lượt, lượt lẻ, giờ công từng ngày, số ngày có chấm và tổng giờ từng tháng.
- Giờ công được cộng theo từng cặp lượt liên tiếp; lượt chưa đủ cặp không được cộng sai vào tổng.
- Tối ưu điện thoại: phân trang 100 dòng, bộ lọc bám đầu trang, nút cảm ứng lớn, modal xuất báo cáo riêng và ngừng polling khi tab bị ẩn.
- Bật nén GZip cho phản hồi lớn để giảm dữ liệu truyền qua Home Assistant Ingress.
- Củng cố ranh giới lệnh thiết bị: danh tính/phiên web chỉ dùng trong ứng dụng và audit, không bao giờ được truyền vào command ZKTeco.

## 1.9.0

- Loại bỏ hoàn toàn chức năng chấm bằng PIN/chấm thủ công.
- Chuyển mục Nhân viên thành chỉ xem; gỡ API thêm, sửa và xóa nhân viên.
- Thêm tiến trình nền `live_capture()` tự nhận lượt chấm mới và tự cập nhật giao diện, không cần bấm tải lại.
- Tổng quan lấy giờ thực từ `get_time()` của máy, đồng bộ lại mỗi 5 giây và hiển thị đồng hồ chạy từng giây.
- Loại bỏ kiểm tra âm thanh.
- Thêm xem metadata mẫu vân tay bằng `get_templates()`; không đưa dữ liệu sinh trắc học thô lên trình duyệt.

## 1.8.0

- Loại bỏ toàn bộ chức năng khôi phục từ CSV.
- Loại bỏ cách chấm thủ công chỉ ghi dữ liệu cục bộ trong Add-on.
- Thêm phiên chấm PIN trực tiếp: Add-on lưu PIN vào hồ sơ nhân viên trên máy, chờ tối đa 60 giây và chỉ báo thành công khi máy ZKTeco gốc phát sinh lượt chấm.
- Tự lưu lượt chấm thật nhận từ thiết bị vào bảng công và không ghi mã PIN vào nhật ký kiểm toán.

## 1.7.0

- Thêm quy trình xem trước và khôi phục bảng công từ CSV vào cơ sở dữ liệu Add-on.
- Tự bỏ qua mốc giờ đã có, đánh dấu nguồn CSV và giữ tổng số lượt do CSV báo cáo.
- Không tự tạo giờ cho các lượt ở giữa khi CSV chỉ có giờ đầu/cuối; không đổi giờ hoặc ghi log giả lên máy ZKTeco.
- Thêm nút chấm thủ công theo thời gian TP.HCM hiện tại, lưu trong Add-on và ghi nhật ký đối soát.
- Làm rõ cách dùng mã PIN hoặc thẻ từ trên máy để chấm không cần vân tay nhưng vẫn có log gốc trên thiết bị.

## 1.6.0

- Chuyển điều khiển thời gian máy sang trang Tổng quan.
- Thiết kế bộ chọn ngày và giờ riêng, tối ưu thao tác cảm ứng trên điện thoại.
- Thêm nút điều chỉnh nhanh ±1 phút, ±5 phút và xem trước thời gian.

## 1.5.1

- Loại bỏ hoàn toàn chức năng xóa log trên thiết bị khỏi giao diện, API và lớp kết nối ZKTeco.
- Giữ lại ba công cụ thiết bị an toàn: chỉnh giờ, kiểm tra âm thanh và khởi động lại.

## 1.5.0

- Thêm bộ lọc theo tháng, khoảng ngày, hôm nay và toàn bộ dữ liệu.
- Thêm chế độ xem lượt chấm thô, mỗi lần chấm là một dòng riêng.
- Hiển thị phạm vi ngày và tổng dữ liệu đã đồng bộ.
- Thêm điều hướng tháng trước/tháng sau và sửa lỗi giới hạn ngày xem.

## 1.4.1

- Loại bỏ nút, biểu mẫu và API bổ sung lượt chấm thủ công.
- Giữ nguyên dữ liệu lịch sử đã có để tránh mất bảng công.

## 1.4.0

- Mục Chấm công tải đầy đủ tháng được chọn và mọi lượt chấm trong từng ngày.
- Thêm bảng công tháng riêng trong mục Nhân viên.
- Cho phép chỉnh trực tiếp từng lượt chấm từ bảng công nhân viên.
- Truy vấn nhân viên theo mã chính xác, không lẫn mã gần giống.

## 1.3.3

- Luôn hiển thị một dòng chi tiết chứa mọi lượt chấm bên dưới mỗi ngày công.
- Thêm cache-buster cho CSS/JavaScript khi cập nhật Add-on.

## 1.3.2

- Hiển thị đầy đủ mọi lượt chấm trong ngày, không chỉ lượt đầu và cuối.
- Cho phép bấm chỉnh sửa trực tiếp từng lượt chấm.

## 1.3.1

- Chuyển toàn bộ điều khiển thời gian máy sang mục Thiết bị.
- Mục Chấm công chỉ giữ dữ liệu nhân viên, bộ lọc, chỉnh sửa và bổ sung lượt chấm.

## 1.3.0

- Đồng bộ nhanh giờ GMT+7 theo múi giờ `Asia/Ho_Chi_Minh`.
- Bỏ màn hình tạo tài khoản và đăng nhập trong Home Assistant Ingress.

## 1.2.0

- Giao diện Home Assistant Ingress.
- Chỉnh giờ máy trực tiếp từ mục Chấm công.
- Bổ sung lượt vào/ra bị thiếu cho nhân viên.
- Bảng công tách cột giờ vào và giờ ra.

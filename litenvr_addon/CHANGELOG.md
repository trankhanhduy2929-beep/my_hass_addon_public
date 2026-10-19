# Changelog

## 1.4.3

- Xem lại bản ghi Drive: phát hiện kết nối bị treo sớm (20 giây) và tự tải tiếp, hiện
  tổng dung lượng ngay khi bắt đầu tải, báo "đang kết nối lại…" nếu chưa có dữ liệu.
- Sửa trạng thái bị gán nhầm khi quay lại xem trực tiếp ngay sau khi mở bản ghi.

## 1.4.2

- Xem lại bản ghi trên Google Drive không còn đứng ở "Đang tải… x%": tự tải tiếp khi
  kết nối đứt, phát hiện file tải thiếu và không coi là hoàn chỉnh.
- Thanh trạng thái hiện đúng tiến độ và cập nhật lại khi phát (kể cả camera H.265
  phải chuyển mã), kèm cảnh báo khi đang kết nối lại.

## 1.4.1

- Giao diện mượt hơn: modal/menu mở và đóng có hiệu ứng, thẻ có phản hồi hover,
  đổi theme chuyển màu êm; tôn trọng tuỳ chọn giảm chuyển động của hệ thống.

## 1.4.0

- Bỏ dò chuyển động nội bộ bằng CPU (ffmpeg scene-detect): chuyển động giờ nhận
  từ cảm biến Home Assistant, ONVIF/PTZ hoặc bộ nhận diện AI bên ngoài qua webhook.

## 1.3.0

- Cảm biến chuyển động Home Assistant: tải danh sách cảm biến kèm trạng thái và chọn
  điều kiện kích hoạt, chỉ ghi hình khi cảm biến chuyển sang trạng thái kích hoạt
  (hết ghi liên tục khi cảm biến giữ nguyên).

## 1.2.0

- Đánh dấu sự kiện, lọc theo nhãn và phân trang khi tìm lại bản ghi.
- Hạn mức dung lượng mỗi camera; tự tạm dừng ghi khi ổ trống thấp và ghi lại khi đủ chỗ.
- Xem danh sách phiên đăng nhập và đăng xuất các phiên khác.

## 1.1.0

- Thêm Ingress: hiển thị LiteNVR trực tiếp trong sidebar Home Assistant (bật "Show in sidebar" trên trang add-on).
- Ứng dụng dùng URL tương đối nên chạy đúng cả trong Ingress lẫn truy cập trực tiếp qua cổng 8099.

## 1.0.1

- Kích hoạt build lại để xuất bản ảnh add-on qua release pipeline.

## 1.0.0

- Bản phát hành đầu tiên: đóng gói LiteNVR thành add-on Home Assistant.
- Ánh xạ tuỳ chọn (tài khoản, múi giờ, iframe, go2rtc, FFmpeg, log) sang LiteNVR.
- Trỏ `/storage` vào `media`/`share`/`data` để bản ghi bền vững.
- Mở giao diện web qua cổng host và watchdog `/health`.

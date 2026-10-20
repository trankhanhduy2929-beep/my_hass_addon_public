# Changelog

## 1.4.7

- Thêm lịch tháng đánh dấu ngày có bản ghi (ổ cứng và Drive), bấm để nhảy nhanh.
- Thêm nút sự kiện trước/sau (⏮/⏭) và phím mũi tên ←/→ để nhảy giữa các sự kiện.
- Cảnh báo Telegram/webhook (dùng được webhook Home Assistant) khi camera đang ghi hình
  mất kết nối quá 60 giây, báo lại khi kết nối phục hồi; thẻ camera hiện nhãn đỏ.
- Nút "Kiểm tra" URL camera trong lúc thêm/sửa: báo codec, độ phân giải, fps và khả năng
  phát trực tiếp trước khi lưu.

## 1.4.6

- Thêm nút lùi/tới ngày (giữ Shift để nhảy 7 ngày) và nút về hôm nay ngay trên thanh
  công cụ; thanh thời gian hiện ngày đang xem khi xem lại lịch sử.
- Camera vừa thêm được chọn và phát ngay, tự chờ luồng HLS sẵn sàng thay vì báo lỗi;
  hiện rõ lỗi nếu lưu camera thất bại.

## 1.4.5

- Menu Cài đặt tự ẩn nhóm trống theo quyền người dùng; sửa bố cục menu trên điện thoại
  (không còn khoảng trống lớn, không tràn ngang).

## 1.4.4

- Gọn lại thanh công cụ: nhóm menu Cài đặt theo Camera / Lưu trữ / Kết nối / Hệ thống,
  gộp công cụ giao diện vào một menu, thu gọn nhóm công cụ phát lại và ẩn bảng xuất clip
  sau nút "Xuất clip".

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

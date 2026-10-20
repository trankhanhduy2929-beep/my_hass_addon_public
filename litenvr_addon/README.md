# LiteNVR (add-on)

NVR gọn nhẹ chạy trong Home Assistant: **xem trực tiếp, ghi hình và xem lại**
camera RTSP/ONVIF, lưu bản ghi trên ổ cứng (media/share), Google Drive hoặc NAS.
Điều khiển và cấu hình hoàn toàn bằng giao diện web LiteNVR — Home Assistant chỉ
là lớp hiển thị và tự động hoá.

## Add-on làm gì

- Xem trực tiếp nhiều camera RTSP/ONVIF (chọn luồng chính/phụ, hạ độ phân giải để nhẹ CPU).
- Ghi hình **liên tục** hoặc **theo chuyển động** (kích hoạt bởi cảm biến/nguồn sự kiện).
- Kích hoạt ghi hình từ **cảm biến Home Assistant** gán riêng cho từng camera (mọi thay đổi trạng thái).
- Nhãn sự kiện từ bộ nhận diện AI ngoài (Frigate, DeepStack, CodeProject.AI, Node-RED…).
- Xem lại theo dòng thời gian, tải clip, ảnh chụp nhanh, tua/tốc độ phát.
- ONVIF: dò/quét dải IP, tự thêm camera đa hãng, lấy RTSP, điều khiển PTZ và preset.
- Lưu trữ linh hoạt: ổ cứng, Google Drive, hoặc NAS (SMB/NFS/FTP) và chính sách giữ bản ghi.
- Thông báo chuyển động qua Telegram và liên kết sâu mở thẳng bản ghi.

## Cách dùng

1. Thêm kho add-on `https://github.com/trankhanhduy2929-beep/my_hass_addon_public` vào Home Assistant.
2. Cài **LiteNVR**, chỉnh tuỳ chọn (tài khoản, múi giờ, nơi lưu trữ…), rồi **Start**.
3. Bật **Show in sidebar** để xem trực tiếp trong Home Assistant, hoặc mở **OPEN WEB UI** / cổng `8099` mặc định để vào giao diện LiteNVR và thêm camera.

Chi tiết tuỳ chọn và lưu ý xem [DOCS.md](DOCS.md). Lịch sử thay đổi xem [CHANGELOG.md](CHANGELOG.md).

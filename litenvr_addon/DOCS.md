# LiteNVR — tài liệu add-on

Add-on này gói sẵn LiteNVR và chạy máy chủ web trong Home Assistant. Bản thân
LiteNVR là một NVR độc lập; add-on chỉ lo việc khởi động, ánh xạ tuỳ chọn Home
Assistant sang biến môi trường và trỏ nơi lưu trữ vào thư mục bền vững.

## Cổng và truy cập

- Add-on dùng **Ingress**: LiteNVR hiện ngay trong giao diện Home Assistant. Trên
  trang add-on, bật **Show in sidebar** để ghim LiteNVR vào thanh bên và xem trực
  tiếp trong Home Assistant. Nút **OPEN WEB UI** cũng mở qua Ingress.
- Giao diện web LiteNVR vẫn lắng nghe cổng **8080** trong container và mở ra ngoài
  ở cổng host **8099** nếu muốn truy cập trực tiếp (dùng cùng đăng nhập bên dưới).
- Có thể nhúng bằng thẻ dashboard khi bật tuỳ chọn **iframe**.
- Tài khoản mặc định là `admin` / `admin`. Hãy đổi trong tuỳ chọn add-on trước
  khi mở ra mạng.

## Tuỳ chọn

| Tuỳ chọn | Mặc định | Ý nghĩa |
| --- | --- | --- |
| `auth_enabled` | `true` | Bắt đăng nhập trước khi dùng giao diện. |
| `username` | `admin` | Tài khoản đăng nhập web. |
| `password` | (trống) | Mật khẩu web. Để trống giữ mặc định `admin`. |
| `iframe` | `true` | Cho nhúng giao diện vào iframe / thẻ dashboard. |
| `timezone` | (trống) | Múi giờ IANA, ví dụ `Asia/Ho_Chi_Minh`. |
| `log_level` | `info` | Mức log máy chủ web (`debug`/`info`/`warning`/`error`). |
| `go2rtc` | `auto` | Chế độ go2rtc: `auto`, `on`, `off`. |
| `ffmpeg_threads` | `2` | Số luồng cấp cho mỗi tiến trình FFmpeg. |
| `live_max_height` | `720` | Hạ chiều cao khung xem trực tiếp (pixel). `0` giữ nguyên. |
| `storage_location` | `media` | Nơi lưu cấu hình và bản ghi: `data`, `media`, `share`. |

## Nơi lưu trữ

LiteNVR lưu cấu hình, cơ sở dữ liệu và bản ghi vào `/storage`, được add-on trỏ
tới `<storage_location>/litenvr`:

- `media` → `/media/litenvr` (mặc định, hiện trong Media của Home Assistant, **không** vào bản sao lưu add-on).
- `share` → `/share/litenvr`.
- `data` → `/data/litenvr` (bền vững nhưng **có** nằm trong bản sao lưu add-on — tránh dùng cho ổ ghi hình lớn).

Add-on cần quyền ghi vào `media` và `share` (đã khai báo trong cấu hình).

## Kết nối camera

- Thêm camera bằng **RTSP thủ công** (nhập URL luồng chính/phụ) hoặc **ONVIF**
  (nhập IP, cổng; LiteNVR dò và lấy luồng). Camera phải nằm trong cùng mạng mà
  Home Assistant truy cập được.
- Gắn **cảm biến chuyển động Home Assistant** cho từng camera: mọi thay đổi trạng
  thái của cảm biến đều kích hoạt ghi hình + ảnh chụp (không cần ONVIF).

## Google Drive và NAS

- Google Drive: dán OAuth client/token trong giao diện LiteNVR (cần thông tin
  OAuth của bạn; add-on không kèm sẵn).
- NAS: cấu hình backup SMB/NFS/FTP trong giao diện LiteNVR.

## Kiểm tra sức khoẻ

Add-on có watchdog gọi `http://[HOST]:[PORT:8080]/health`; Home Assistant tự
khởi động lại add-on nếu nó ngừng phản hồi.

## Ghi chú triển khai

Ảnh add-on được xuất bản tự động thành `ghcr.io/trankhanhduy2929-beep/litenvr_addon`.
Sau lần xuất bản đầu tiên, đặt các gói GHCR sau thành **Public** trong GitHub
Package settings để Home Assistant tải được:

- `litenvr_addon`
- `litenvr_addon-amd64`
- `litenvr_addon-aarch64`

# LiteNVR — tài liệu add-on

Add-on này gói sẵn LiteNVR và chạy máy chủ web trong Home Assistant. Bản thân
LiteNVR là một NVR độc lập; add-on chỉ lo việc khởi động, ánh xạ tuỳ chọn Home
Assistant sang biến môi trường và trỏ nơi lưu trữ vào thư mục bền vững.

## Cổng và truy cập

- Add-on dùng **Ingress**: LiteNVR hiện ngay trong giao diện Home Assistant. Trên
  trang add-on, bật **Show in sidebar** để ghim LiteNVR vào thanh bên và xem trực
  tiếp trong Home Assistant. Nút **OPEN WEB UI** cũng mở qua Ingress.
- Giao diện web LiteNVR lắng nghe cổng **3333** trong container và mở ra ngoài ở
  cổng host **3333** nếu muốn truy cập trực tiếp (dùng cùng đăng nhập bên dưới).
- Có thể nhúng bằng thẻ dashboard khi bật tuỳ chọn **iframe**.
- Tài khoản mặc định là `admin`; **mật khẩu bắt buộc tối thiểu 12 ký tự** và không
  được là mật khẩu đã xuất hiện trong dữ liệu rò rỉ. Home Assistant sẽ từ chối giá
  trị yếu/rỗng. Dùng mật khẩu riêng, dài và duy nhất cho add-on.

## Độ trễ xem trực tiếp

LiteNVR dùng HLS segment **1 giây**, playlist **4 segment** và trình duyệt bắt đầu
gần live edge. Khi camera phải chuyển mã H.265/HEVC sang H.264, FFmpeg tự ép
keyframe đúng nhịp segment để không phải chờ GOP dài. Độ trễ thực tế thường khoảng
**1–4 giây**; camera có GOP dài hoặc mạng Wi-Fi yếu có thể cao hơn. Nếu cần ổn định
hơn, dùng luồng phụ H.264 cho live và hạ `live_max_height`.

## Tuỳ chọn

| Tuỳ chọn | Mặc định | Ý nghĩa |
| --- | --- | --- |
| `auth_enabled` | `true` | Bắt đăng nhập trước khi dùng giao diện. |
| `username` | `admin` | Tài khoản đăng nhập web. |
| `password` | (bắt buộc) | Mật khẩu web, tối thiểu 12 ký tự; không dùng mật khẩu đã rò rỉ. |
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

- **Quản lý Camera** có hai tab: **Tự động dò ONVIF** và **Nhập URL thủ công**.
  Camera phải nằm trong cùng mạng mà Home Assistant truy cập được.
- **Nhập URL thủ công** có preset cho Imou/Dahua (`/cam/realmonitor?channel=1&subtype=0`),
  EZVIZ/Hikvision (`/h264/ch01/main/av_stream`) và Hanet
  (`rtsp://ip:554/user:<user>;pwd:<pass>`).
- **Tự dò và thêm ONVIF**: mở **Quản lý Camera** → **Dò camera ONVIF**. Nếu add-on
  chạy trong Docker bridge và không nhận multicast, nhập dải IP LAN (ví dụ
  `192.168.1.0/24`) rồi bấm **Quét dải IP**. Chọn các camera tìm thấy, nhập tài khoản
  ONVIF một lần và bấm **Thêm camera đã chọn**; LiteNVR tự lấy luồng chính/phụ, tên,
  hãng và bỏ qua camera đã có trong cấu hình.
- Nếu camera không xuất hiện khi quét, nhập trực tiếp IP/cổng ONVIF ở ô **Hoặc nhập IP
  ONVIF**, bấm **Lấy luồng RTSP**, kiểm tra URL rồi lưu camera.
- Gắn **cảm biến chuyển động Home Assistant** cho từng camera: mọi thay đổi trạng
  thái của cảm biến đều kích hoạt ghi hình + ảnh chụp (không cần ONVIF).

## Google Drive và NAS

- Google Drive: dán OAuth client/token trong giao diện LiteNVR (cần thông tin
  OAuth của bạn; add-on không kèm sẵn).
- NAS: cấu hình backup SMB/NFS/FTP trong giao diện LiteNVR.

## Kiểm tra sức khoẻ

Add-on có watchdog gọi `http://[HOST]:[PORT:3333]/health`; Home Assistant tự
khởi động lại add-on nếu nó ngừng phản hồi.

## Ghi chú triển khai

Ảnh add-on được xuất bản tự động thành `ghcr.io/trankhanhduy2929-beep/litenvr_addon`.
Sau lần xuất bản đầu tiên, đặt các gói GHCR sau thành **Public** trong GitHub
Package settings để Home Assistant tải được:

- `litenvr_addon`
- `litenvr_addon-amd64`
- `litenvr_addon-aarch64`

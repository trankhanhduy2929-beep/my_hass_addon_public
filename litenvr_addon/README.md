# LiteNVR (add-on)

NVR gọn nhẹ chạy trong Home Assistant: **xem trực tiếp, ghi hình và xem lại**
camera RTSP/ONVIF, lưu bản ghi trên ổ cứng (media/share), Google Drive hoặc NAS.
Điều khiển và cấu hình hoàn toàn bằng giao diện web LiteNVR — Home Assistant chỉ
là lớp hiển thị và tự động hoá.

## Tính năng

- Xem trực tiếp nhiều camera RTSP/ONVIF với **HLS độ trễ thấp** (segment 1 giây,
  bắt đầu gần live edge), chọn luồng chính/phụ và hạ độ phân giải để nhẹ CPU.
- Ghi hình **liên tục** hoặc **theo chuyển động**.
- Kích hoạt ghi hình từ **cảm biến Home Assistant** gán riêng cho từng camera.
- Nhãn sự kiện từ bộ nhận diện AI ngoài (Frigate, DeepStack, CodeProject.AI,
  Node-RED…).
- Xem lại theo dòng thời gian, tải clip, xem ảnh sự kiện, tua/tốc độ phát.
- ONVIF: dò/quét dải IP, tự thêm camera đa hãng, lấy RTSP, điều khiển PTZ và preset.
- Lưu trữ linh hoạt: ổ cứng, Google Drive hoặc NAS (SMB/NFS/FTP).
- Thông báo chuyển động qua Telegram và liên kết sâu mở thẳng bản ghi.

## Yêu cầu

- Home Assistant OS hoặc Home Assistant Supervised.
- Kiến trúc `amd64` (x86_64) hoặc `aarch64` (ARM64).
- Home Assistant truy cập được camera qua mạng LAN.
- Dung lượng trống đủ cho số ngày ghi hình mong muốn.
- Mật khẩu web **tối thiểu 12 ký tự**, không dùng mật khẩu đã rò rỉ.

## Cài đặt từng bước

### 1. Thêm kho add-on

1. Mở **Settings → Add-ons → Add-on Store**.
2. Bấm **⋮** ở góc phải, chọn **Repositories**.
3. Dán URL sau rồi bấm **Add**:

   ```text
   https://github.com/trankhanhduy2929-beep/my_hass_addon_public
   ```

4. Đóng hộp thoại. Kho **LiteNVR** sẽ xuất hiện trong Add-on Store.

### 2. Cài add-on

1. Tìm **LiteNVR**, bấm vào add-on.
2. Bấm **Install** và chờ quá trình tải image hoàn tất.
3. Sau khi cài, mở tab **Configuration**.

### 3. Cấu hình lần đầu

Điền các tuỳ chọn sau rồi bấm **Save**:

| Tuỳ chọn | Gợi ý |
| --- | --- |
| `username` | `admin` (có thể đổi). |
| `password` | **Bắt buộc**, tối thiểu 12 ký tự, dùng mật khẩu riêng và duy nhất. |
| `timezone` | `Asia/Ho_Chi_Minh` hoặc múi giờ của bạn. |
| `storage_location` | `media` (mặc định), `share` hoặc `data`. |
| `live_max_height` | `720` để nhẹ CPU; `0` giữ nguyên độ phân giải. |
| `ffmpeg_threads` | `2` là mặc định; tăng khi CPU còn trống. |
| `go2rtc` | `auto` (khuyến nghị). |
| `iframe` | Bật nếu muốn nhúng giao diện vào dashboard. |
| `log_level` | `info`; đổi `debug` khi cần chẩn đoán. |

Lưu ý:

- Không dùng chung mật khẩu với tài khoản Home Assistant.
- Đổi `storage_location` chỉ khi add-on đang dừng. Dữ liệu cũ không tự di chuyển
  sang thư mục mới.
- Nếu Home Assistant báo mật khẩu yếu, nhập mật khẩu dài và duy nhất hơn.

### 4. Khởi động và mở giao diện

1. Mở tab **Info**, bấm **Start**.
2. Theo dõi tab **Log** đến khi thấy LiteNVR khởi động thành công.
3. Bật **Show in sidebar** để mở LiteNVR từ thanh bên Home Assistant.
4. Hoặc bấm **OPEN WEB UI**. Có thể truy cập trực tiếp qua cổng `3333`:
   `http://IP_HOME_ASSISTANT:3333`.
5. Đăng nhập bằng `username` và `password` đã đặt ở bước 3.

### 5. Thêm camera

1. Trong LiteNVR, mở **+ Quản lý Camera**.
2. Chọn một trong hai cách:

   **Tự động dò ONVIF**

   - Bấm **Dò camera ONVIF**.
   - Nếu không thấy camera, nhập dải IP LAN (ví dụ `192.168.1.0/24`) rồi bấm
     **Quét dải IP**.
   - Chọn camera, nhập tài khoản ONVIF và bấm **Thêm camera đã chọn**.

   **Nhập URL thủ công**

   - Chọn tab **Nhập URL thủ công**.
   - Chọn hãng/preset nếu có, hoặc nhập URL RTSP đầy đủ.
   - Kiểm tra luồng chính và luồng phụ, sau đó bấm **Lưu Camera**.

3. Mở **⚙️ Tùy chọn nâng cao** khi cần chỉnh:
   - Giao thức và codec video.
   - Chế độ ghi hình và lịch ghi.
   - Số ngày lưu riêng.
   - Cảm biến chuyển động Home Assistant.
4. Bấm **Lưu Camera**. Camera mới xuất hiện trong danh sách và lưới xem trực tiếp.

Mẹo:

- Camera phải cùng mạng hoặc có route từ Home Assistant tới camera.
- Nếu ONVIF không tìm thấy, dùng URL RTSP thủ công.
- Với camera H.265/HEVC, LiteNVR tự chuyển mã H.264 cho trình duyệt.
- Nên dùng luồng phụ H.264 cho live để giảm CPU.

## Độ trễ xem trực tiếp

LiteNVR dùng HLS segment **1 giây**, playlist **4 segment** và bắt đầu gần live
edge. Khi phải chuyển mã H.265/HEVC sang H.264, FFmpeg tự ép keyframe đúng nhịp
segment. Độ trễ thực tế thường khoảng **1–4 giây**.

Nếu live chậm hơn:

- Kiểm tra GOP/keyframe của camera; nên đặt keyframe 1–2 giây.
- Dùng luồng phụ H.264 cho live.
- Hạ `live_max_height` xuống `480` hoặc `720`.
- Tăng `ffmpeg_threads` nếu CPU còn trống.
- Với reverse proxy, tắt proxy buffering cho đường dẫn `/hls/`.

## Nơi lưu trữ

LiteNVR lưu cấu hình, cơ sở dữ liệu và bản ghi trong `/storage`, được add-on trỏ tới:

| `storage_location` | Thư mục thực tế | Ghi chú |
| --- | --- | --- |
| `media` | `/media/litenvr` | Mặc định, xem được trong Media của Home Assistant. |
| `share` | `/share/litenvr` | Dùng khi đã có cấu trúc thư mục trên NAS/share. |
| `data` | `/data/litenvr` | Nằm trong bản sao lưu add-on; không dùng cho kho ghi lớn. |

Bản ghi trong `media`/`share` **không** tự nằm trong bản sao lưu add-on. Hãy sao
lưu thư mục tương ứng hoặc dùng Google Drive/NAS trong giao diện LiteNVR.

## Sao lưu và cập nhật

### Sao lưu trước khi cập nhật

1. Vào **Settings → System → Backups** và tạo bản sao lưu Home Assistant.
2. Nếu dùng `media` hoặc `share`, sao chép thêm thư mục `/media/litenvr` hoặc
   `/share/litenvr`.
3. Nếu dùng Google Drive/NAS, kiểm tra trạng thái đồng bộ trong LiteNVR.

### Cập nhật add-on

1. Mở **Settings → Add-ons → LiteNVR**.
2. Sang tab **Info**, bấm **Update** khi có phiên bản mới.
3. Chờ add-on khởi động lại, sau đó kiểm tra tab **Log** và mở lại giao diện.
4. Nếu giao diện còn bản cũ, nhấn `Ctrl+F5` để xoá cache trình duyệt.

## Xử lý sự cố

### Add-on không khởi động

- Mở tab **Log** để xem lỗi.
- Kiểm tra `password` đã đủ 12 ký tự chưa.
- Kiểm tra `storage_location` có quyền ghi.
- Nếu vừa đổi thư mục lưu trữ, dừng add-on rồi kiểm tra lại cấu hình.
- Khởi động lại add-on sau khi sửa.

### Không mở được giao diện

- Thử **OPEN WEB UI** hoặc **Show in sidebar** trước.
- Kiểm tra cổng `3333` có bị firewall chặn không.
- Nếu nhúng iframe, bật tuỳ chọn `iframe`.
- Xoá cookie cũ của địa chỉ LiteNVR nếu đăng nhập xong vẫn quay lại trang login.

### Không thấy camera ONVIF

- Đảm bảo camera và Home Assistant cùng mạng LAN.
- Thử quét dải IP thay vì multicast.
- Kiểm tra tài khoản ONVIF và quyền xem luồng.
- Dùng **Nhập URL thủ công** với URL RTSP nếu ONVIF vẫn không tìm thấy.

### Không phát được live

- Kiểm tra URL RTSP bằng VLC hoặc ffplay từ máy khác.
- Thử luồng phụ H.264.
- Hạ `live_max_height` và kiểm tra CPU.
- Xem Log của LiteNVR để biết camera có từ chối kết nối không.

### Ảnh sự kiện không hiển thị

- LiteNVR chỉ hiển thị ảnh sau khi file JPEG ghi xong; ảnh lỗi/ghi dở không còn
  được đưa vào sự kiện.
- Kiểm tra Log nếu camera không trả được frame.
- Với go2rtc, thử đặt `go2rtc: on` rồi khởi động lại add-on.
- Ảnh cũ đã mất trước bản 1.8.1 không thể khôi phục tự động.

### Ổ đĩa đầy

- Giảm số ngày lưu trong LiteNVR.
- Chuyển `storage_location` sang ổ lớn hơn.
- Dọn bản ghi cũ hoặc bật sao lưu rồi xoá bớt.
- Không đặt kho ghi vào `data` nếu dung lượng lớn.

## Bảo mật

- Dùng mật khẩu mạnh, riêng cho LiteNVR.
- Không mở cổng `3333` trực tiếp ra Internet nếu không có HTTPS/reverse proxy.
- Giữ Home Assistant và add-on ở phiên bản mới.
- Kiểm tra **Nhật ký đăng nhập** và **Trạng thái bảo mật** trong LiteNVR.
- Tài khoản con chỉ nên được cấp camera và quyền cần thiết.

## Thông tin kỹ thuật

- Web UI: cổng `3333` trong container, Ingress qua Home Assistant.
- Watchdog: `http://[HOST]:[PORT:3333]/health`.
- Image: `ghcr.io/trankhanhduy2929-beep/litenvr_addon`.
- Kiến trúc: `amd64`, `aarch64`.

Xem thêm [DOCS.md](DOCS.md) để biết toàn bộ tuỳ chọn và [CHANGELOG.md](CHANGELOG.md)
để theo dõi thay đổi.

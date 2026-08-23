# Hướng dẫn HANET Connect Gateway 0.9.4

## 1. Yêu cầu

- Home Assistant OS hoặc Home Assistant Supervised có hỗ trợ add-on local.
- Kiến trúc `amd64`, `aarch64` hoặc `armv7`.
- Tài khoản HANET có quyền xem các địa điểm/camera cần quản lý.
- Home Assistant có kết nối Internet tới dịch vụ HANET Cloud.

## 2. Cài add-on local

1. Chép thư mục `addon_hanet_connect` vào `/addons/hanet_connect`.
2. Mở **Settings > Apps > App store**.
3. Mở menu góc phải và chọn **Check for updates**.
4. Chọn **HANET Connect Gateway** và nhấn **Install**.
5. Mở tab **Configuration** và nhập thông tin HANET.
6. Khởi động add-on, bật **Start on boot**, **Watchdog** và **Show in sidebar**.

## 3. Cấu hình

- `username`, `password`: tài khoản HANET Connect của riêng add-on.
- `api_base_url`: mặc định là HANET Mobile API V4.
- `api_access_key`: khóa cho API cục bộ. Nếu bật cổng `9091`, nên dùng chuỗi ngẫu
  nhiên tối thiểu 24 ký tự.
- `webhook_secret`: khóa riêng cho `POST /api/webhook`.
- `ui_auth_enabled`: mặc định `true`, dùng làm trạng thái khóa khi tạo dữ liệu lần
  đầu. Sau đó bật/tắt trực tiếp trong **Cài đặt > Bảo mật giao diện**.
- `poll_interval`: chu kỳ đồng bộ đầy đủ, từ 15 đến 3600 giây.
- `event_stream`: duy trì SSE; add-on tự fallback sang polling khi route không có.
- `verify_tls`: xác minh chứng chỉ HTTPS, nên luôn bật.
- `log_level`: `debug`, `info`, `warning` hoặc `error`.

Port `9091` mặc định không được ánh xạ ra host. Giao diện sidebar sử dụng Ingress
và không cần mở port.

## 4. Mở giao diện và quản lý khóa mật khẩu

Lần đầu bấm **HANET Connect** trong sidebar, nhập mật khẩu mặc định được cung cấp
riêng để mở dashboard. Sau khi đăng nhập nên đổi sang mật khẩu riêng.

1. Mở tab **Cài đặt > Bảo mật giao diện** để đổi mật khẩu.
2. Mật khẩu mới phải có ít nhất 4 ký tự và tối đa 128 ký tự.
3. Bấm **Tắt yêu cầu đăng nhập** nếu muốn những lần sau mở thẳng dashboard.
4. Khi khóa đang tắt, bấm **Bật yêu cầu đăng nhập** để bật lại; mật khẩu đã đổi
   vẫn được giữ.

Sau khi đổi mật khẩu, tất cả session cũ bị thu hồi và trình duyệt hiện tại nhận
session mới. Nút **Khóa ngay** hoặc biểu tượng đăng xuất trên thanh đầu trang sẽ
đóng session hiện tại.

Hash và trạng thái bật/tắt được lưu trong `/data/ui_auth.json`; mật khẩu rõ không
được lưu. Nếu mất mật khẩu, dừng add-on, xóa file này trong vùng dữ liệu add-on
rồi khởi động lại để khôi phục khóa mặc định được cung cấp riêng. Sau đó cần đổi
mật khẩu ngay.

## 5. Sử dụng các màn hình

### Camera

- Thẻ tổng quan cho biết số camera online/offline, RTSP và lần đồng bộ gần nhất.
- Nhấn camera để mở điều khiển PTZ, zoom, còi báo động và setting.
- Công tắc RTSP chỉ thay đổi setting firmware qua HANET Cloud.

### Sự kiện

- Chọn ngày, camera, loại sự kiện hoặc nguồn dữ liệu.
- Tìm theo tên người hoặc camera.
- Ảnh sự kiện được proxy có giới hạn từ domain HANET hợp lệ.

### Ghi hình

- Chọn ngày và camera để tải danh sách clip cloud.
- Add-on đổi đường dẫn clip sang URL ký tạm rồi proxy video MP4.

### Danh tính

- Tách riêng Face nhân viên (`type=0`) và Face khách (`type=1`) thành hai tab.
- Hỗ trợ tạo, sửa, xóa và tải nhiều ảnh Face ID định dạng JPEG, PNG, WebP, GIF,
  BMP, TIFF, HEIC, HEIF hoặc AVIF.
- Có màn hình nhân viên, phòng ban, biển số và chấm công.

### Cài đặt

- Xem trạng thái HANET Cloud, số địa điểm/camera và cổng add-on.
- Đổi mật khẩu hoặc khóa giao diện.
- Bật/tắt RTSP và mở setting từng camera.
- Mở **API nâng cao** để gọi endpoint theo catalog.

## 6. API cục bộ

Ngoài `/health` và webhook, request qua cổng mạng phải gửi:

```text
X-HANET-Gateway-Key: <api_access_key>
```

Các endpoint chính:

- `GET /health`: healthcheck công khai, không chứa credential.
- `GET /api/state`: snapshot chuẩn hóa.
- `GET /api/catalog`: endpoint, setting và command đã phát hiện.
- `GET /api/events?day=YYYY-MM-DD&limit=250`: lịch sử sự kiện.
- `GET /api/people`, `/api/departments`, `/api/plates`: dữ liệu danh tính.
- `PUT /api/people/{id}/department`: gán hoặc bỏ phòng ban của Face ID.
- `GET /api/recordings?day=YYYY-MM-DD`: clip cloud trong ngày.
- `POST /api/refresh`: đồng bộ ngay.
- `POST /api/call`: gọi endpoint theo tên catalog.
- `PUT /api/devices/{id}/settings/{key}`: cập nhật setting.
- `POST /api/devices/{id}/commands/{command}`: gửi command camera.
- `GET /api/devices/{id}/image`: ảnh camera/sự kiện gần nhất.
- `GET /api/ws`: WebSocket trạng thái và sự kiện.

API dùng `X-HANET-Gateway-Key` không yêu cầu mật khẩu khóa giao diện. Điều này giữ
API máy-máy độc lập với session của người dùng.

## 7. Webhook

Webhook chỉ nhận secret qua header để tránh secret xuất hiện trong URL và access
log:

```text
POST /api/webhook
X-HANET-Webhook-Secret: <webhook_secret>
Content-Type: application/json
```

Không dùng query string `?secret=...`.

## 8. Custom integration

Custom integration đăng nhập HANET Cloud bằng config entry riêng và tự chạy TUTK
P2P trong Home Assistant Core. Nó không cần cổng `9091`, API key, session hoặc mật
khẩu giao diện của add-on.

Chạy đồng thời hai phần sẽ tạo hai phiên HANET Cloud và hai chu kỳ đồng bộ độc lập.

## 9. Xử lý sự cố

- **Không mở được giao diện**: kiểm tra add-on đang chạy và mở từ sidebar Ingress.
- **Sai mật khẩu nhiều lần**: chờ hết thời gian khóa tạm rồi thử lại.
- **Đã đổi tài khoản HANET nhưng dữ liệu chưa đổi**: dừng add-on, xóa
  `/data/session.json`, sau đó khởi động lại để tạo phiên cloud mới.
- **Không có camera**: đăng nhập lại ứng dụng HANET chính thức và kiểm tra quyền
  chia sẻ/địa điểm.
- **SSE lỗi 404**: đây là trường hợp đã hỗ trợ; add-on chuyển sang cloud polling.
- **RTSP bật nhưng không xem được**: firmware có thể chỉ bật dịch vụ trong LAN của
  camera; chức năng này không thay thế TUTK P2P.

## 10. Giới hạn

- HANET Mobile API là API nội bộ và có thể thay đổi không báo trước.
- Âm thanh hai chiều chưa được đưa vào Home Assistant.
- PTZ, stream và setting cần xác nhận trên từng model/firmware.
- Chỉ sử dụng với tài khoản và thiết bị mà người dùng có quyền truy cập.

# Hướng dẫn HANET Connect Gateway 0.10.0

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
- `ui_auth_enabled`: tùy chọn tương thích cũ; bản `0.9.7` luôn mở trực tiếp qua
  Home Assistant Ingress và không yêu cầu mật khẩu dashboard riêng.
- `poll_interval`: chu kỳ đồng bộ đầy đủ, từ 15 đến 3600 giây.
- `event_stream`: duy trì SSE; add-on tự fallback sang polling khi route không có.
- `verify_tls`: xác minh chứng chỉ HTTPS, nên luôn bật.
- `log_level`: `debug`, `info`, `warning` hoặc `error`.
- `license_portal_url`: website đăng ký, mua và quản lý key; mặc định là
  `https://hanet-license-admin-vercel.vercel.app`.
- `license_required`: mặc định `false`, vì vậy cập nhật lên `0.10.0` không khóa
  hoặc thay đổi các chức năng đang chạy. Chỉ bật sau khi portal production ổn định.
- `license_offline_grace_hours`: số giờ tối đa tin kết quả verify đã ký khi portal
  tạm mất kết nối; mặc định 72 giờ và không bao giờ vượt ngày hết hạn của key.

Port `9091` mặc định không được ánh xạ ra host. Giao diện sidebar sử dụng Ingress
và không cần mở port.

## 4. Mở giao diện

Bấm **HANET Connect** trong sidebar để mở dashboard trực tiếp. Giao diện dùng lớp
xác thực Home Assistant Ingress, không còn màn hình nhập mật khẩu dashboard riêng.
Nếu ánh xạ cổng `9091`, mọi API ngoài Ingress vẫn phải gửi
`X-HANET-Gateway-Key`.

## 5. Kích hoạt License Key

1. Mở **Cài đặt > License addon** trong giao diện HANET Connect.
2. Bấm **Mở website lấy license**. Link chỉ mang installation ID, public key và
   phiên bản addon; không mang tài khoản HANET hoặc secret nào.
3. Đăng ký/đăng nhập bằng email, có thể lưu thêm số điện thoại.
4. Nhận trial miễn phí 1 ngày hoặc mua gói 1 tháng/vĩnh viễn qua PayOS.
5. Copy key từ dashboard, dán vào addon và bấm **Kích hoạt / kiểm tra**.

Nếu cần liên kết thủ công trên portal, nhập cả **Installation ID** và **Installation
public key** hiển thị trong thẻ License; chỉ biết ID không đủ để chiếm installation.

Nếu thử thay bằng một key sai trong khi key cũ vẫn còn hợp lệ, addon tự khôi phục
key cũ và không làm mất quyền đang dùng. Nút **Xóa key trên máy** chỉ xóa key đã
lưu; installation identity vẫn được giữ để không nhận trial lặp lại.

Addon lưu private Ed25519 identity và License Key đã mã hóa AES-GCM trong
`/data/license.json`. Addon chỉ có public signing key của portal; PayOS secret,
Supabase service role, khóa mã hóa database và quyền admin không nằm trong image.

Khi `license_required=false`, trạng thái license chỉ hiển thị để rollout/test và
mọi API HANET hiện có tiếp tục chạy như trước. Khi bật `true`, các route nghiệp vụ
bị chặn nếu không có license hợp lệ; route giao diện, trạng thái và kích hoạt vẫn
truy cập được để người dùng nhập key.

## 6. Sử dụng các màn hình

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
- Với nhân viên, có thể đổi hoặc bỏ phòng ban ngay từ menu trên từng thẻ; add-on
  đọc lại membership cloud trước khi báo thành công.
- Xóa FaceID thử các schema `person_id`, `personID`, FaceID và UUID, đồng thời
  xử lý trường hợp HANET trả HTTP 200 nhưng `returnCode` vẫn báo lỗi.

### Cài đặt

- Xem trạng thái HANET Cloud, số địa điểm/camera và cổng add-on.
- Đổi mật khẩu hoặc khóa giao diện.
- Bật/tắt RTSP và mở setting từng camera.
- Mở **API nâng cao** để gọi endpoint theo catalog.

## 7. API cục bộ

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
- Catalog nâng cao có `device_set_alert` (`POST /business/device/set-alert`) với
  payload `device_id` và `settings`; gateway giữ kiểu ID theo APK và không tự
  chuyển chuỗi số thành JSON number.
- `PUT /api/devices/{id}/settings/{key}`: cập nhật setting.
- `POST /api/devices/{id}/commands/{command}`: gửi command camera.
- `GET /api/devices/{id}/image`: ảnh camera/sự kiện gần nhất.
- `GET /api/ws`: WebSocket trạng thái và sự kiện.
- `GET /api/license/status`: trạng thái license và link portal.
- `POST /api/license/activate`: lưu và verify một License Key.
- `POST /api/license/verify`: ép đối soát lại key đang lưu.
- `DELETE /api/license`: xóa key cục bộ, không xóa installation identity.

API dùng `X-HANET-Gateway-Key` không yêu cầu mật khẩu khóa giao diện. Điều này giữ
API máy-máy độc lập với session của người dùng.

## 8. Webhook

Webhook chỉ nhận secret qua header để tránh secret xuất hiện trong URL và access
log:

```text
POST /api/webhook
X-HANET-Webhook-Secret: <webhook_secret>
Content-Type: application/json
```

Không dùng query string `?secret=...`.

## 9. Custom integration

Custom integration đăng nhập HANET Cloud bằng config entry riêng và tự chạy TUTK
P2P trong Home Assistant Core. Nó không cần cổng `9091`, API key, session hoặc mật
khẩu giao diện của add-on.

Chạy đồng thời hai phần sẽ tạo hai phiên HANET Cloud và hai chu kỳ đồng bộ độc lập.

## 10. Xử lý sự cố

- **Không mở được giao diện**: kiểm tra add-on đang chạy và mở từ sidebar Ingress.
- **Sai mật khẩu nhiều lần**: chờ hết thời gian khóa tạm rồi thử lại.
- **Đã đổi tài khoản HANET nhưng dữ liệu chưa đổi**: dừng add-on, xóa
  `/data/session.json`, sau đó khởi động lại để tạo phiên cloud mới.
- **Không có camera**: đăng nhập lại ứng dụng HANET chính thức và kiểm tra quyền
  chia sẻ/địa điểm.
- **SSE lỗi 404**: đây là trường hợp đã hỗ trợ; add-on chuyển sang cloud polling.
- **Xóa FaceID báo 404**: bản `0.10.0` gửi `person_id` đúng Android 4.1.21 trước,
  sau đó mới thử alias/method/form tương thích trên
  cùng HANET host và chỉ báo thành công sau khi FaceID biến mất khỏi cloud.
- **Thêm Face chọn phòng báo `This field is required`**: bản `0.10.0` gửi multipart
  đúng APK, sau đó mới tách bước tạo Face và gán membership nếu tenant từ chối
  field phòng ban.
- **Đổi phòng báo expected string/int64**: bản `0.10.0` thử JSON snake_case
  số/chuỗi rồi
  fallback form-urlencoded; thao tác bỏ phòng dùng `personID` đúng schema.
- **Đổi phòng vẫn báo lỗi dù profile đã lưu**: bản `0.10.0` ưu tiên
  `person/update` khi có đủ tên/profile, xác minh cả phòng mới lẫn phòng cũ rồi
  chỉ dùng membership fallback nếu cần.
- **Tạo Face thành công nhưng giao diện báo lỗi**: một số tenant trả response
  thành công không có ID; gateway giữ kết quả create nếu request APK đã nhận
  `department_id`, tránh báo thất bại giả.
- **RTSP bật nhưng không xem được**: firmware có thể chỉ bật dịch vụ trong LAN của
  camera; chức năng này không thay thế TUTK P2P.
- **Không nhận được trial**: phải mở portal từ link trong addon để gửi cả public
  installation key; mỗi account/installation chỉ được nhận một lần.
- **Portal tạm lỗi nhưng key trước đó hợp lệ**: addon dùng cache đã ký trong giới
  hạn `license_offline_grace_hours`, nhưng dừng ngay khi key thực sự hết hạn.
- **Key mới sai làm mất key cũ**: bản `0.10.0` tự khôi phục key cũ còn hợp lệ; tải
  lại trạng thái License để kiểm tra key masked đang được giữ.

## 11. Giới hạn

- HANET Mobile API là API nội bộ và có thể thay đổi không báo trước.
- Âm thanh hai chiều chưa được đưa vào Home Assistant.
- PTZ, stream và setting cần xác nhận trên từng model/firmware.
- Chỉ sử dụng với tài khoản và thiết bị mà người dùng có quyền truy cập.

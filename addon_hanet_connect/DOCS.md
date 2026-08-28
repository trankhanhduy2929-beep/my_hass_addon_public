# Hướng dẫn HANET Connect Gateway 0.10.5

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
- `poll_interval`: chu kỳ đồng bộ đầy đủ, từ 15 đến 3600 giây.
- `event_stream`: duy trì SSE; add-on tự fallback sang polling khi route không có.
- `verify_tls`: xác minh chứng chỉ HTTPS, nên luôn bật.
- `log_level`: `debug`, `info`, `warning` hoặc `error`.
- Website license, enforcement và cache offline được cấu hình cố định trong bản
  phát hành; người dùng không cần nhập các giá trị này trong Options.

Port `9091` mặc định không được ánh xạ ra host. Giao diện sidebar sử dụng Ingress
và không cần mở port.

## 4. Mở giao diện

Bấm **HANET Connect** trong sidebar để mở add-on. Nếu chưa có license, add-on chỉ
hiện màn hình activation và tự mở đúng trang `/activate` của installation hiện tại;
dashboard và API nghiệp vụ chưa được mở. Nếu ánh xạ cổng `9091`, mọi API ngoài Ingress vẫn phải gửi
`X-HANET-Gateway-Key`.

## 5. Kích hoạt License Key

1. Mở **HANET Connect**; lần đầu add-on tự mở License Center đúng installation.
2. Đăng ký/đăng nhập bằng email, có thể lưu thêm số điện thoại; installation được
   liên kết tự động từ link, không cần gõ thủ công.
3. Nhận trial miễn phí 1 ngày hoặc mua gói 1 tháng/vĩnh viễn qua PayOS.
4. Copy key từ portal, quay lại add-on, dán vào ô activation và bấm **Kích hoạt ngay**.
5. Khi key hợp lệ, dashboard tự mở; nếu sau này key hết hạn/khóa, add-on tự khóa
   lại và đưa người dùng về đúng trang gia hạn/kích hoạt.

Nếu cần liên kết thủ công trên portal, nhập cả **Installation ID** và **Installation
public key** hiển thị trong thẻ License; chỉ biết ID không đủ để chiếm installation.

Nếu thử thay bằng một key sai trong khi key cũ vẫn còn hợp lệ, addon tự khôi phục
key cũ và không làm mất quyền đang dùng. Nút **Xóa key trên máy** chỉ xóa key đã
lưu; installation identity vẫn được giữ để không nhận trial lặp lại.

Addon lưu private Ed25519 identity và License Key đã mã hóa AES-GCM trong
`/data/license.json`. Addon chỉ có public signing key của portal; PayOS secret,
Supabase service role, khóa mã hóa database và quyền admin không nằm trong image.

License luôn bắt buộc trong bản phát hành. Chỉ các route health, static UI và
license activation/verification được mở khi chưa có key; các route dữ liệu, camera,
FaceID, phòng ban, clip, webhook nghiệp vụ và WebSocket đều bị chặn cho tới khi
server xác minh key hợp lệ. Cache offline đã ký tối đa 72 giờ vẫn được dùng trong
thời gian đó, nhưng không vượt quá ngày hết hạn của license.

## 6. Sử dụng các màn hình

### Camera

- Thẻ tổng quan cho biết số camera online/offline, RTSP và lần đồng bộ gần nhất.
- Nhấn camera để mở điều khiển PTZ, zoom, còi báo động và setting.
- Trong tab **Cài đặt** của camera, phần **Thông tin RTSP cho đầu ghi** cho phép bật
  dịch vụ, đổi username/password và tải lại thông tin từ HANET Cloud.
- Nhập username và password rồi bấm **Lưu cấu hình RTSP**. Nếu chỉ đổi username,
  có thể để trống password khi add-on vẫn đọc được mật khẩu hiện tại; nếu cloud
  chỉ trả mật khẩu dạng che, cần nhập lại password để tạo URL.
- Sau khi camera xác nhận, bấm **Copy URL** và dán vào đầu ghi/NVR. Định dạng là
  `rtsp://<IP-camera>:554/user:<username>;pwd:<password>`; ký tự đặc biệt trong
  credential được percent-encode.
- RTSP là kết nối LAN riêng của camera: đầu ghi phải truy cập được IP camera qua
  cùng LAN/VLAN và cổng TCP `554`. Tính năng này không thay thế luồng P2P/TUTK.
- URL chứa thông tin đăng nhập; chỉ lưu trong đầu ghi tin cậy và không chia sẻ ra
  Internet.

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
- Bật/tắt RTSP, mở cấu hình username/password và copy URL từng camera.
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
- `GET /api/devices/{id}/rtsp`: đọc trạng thái, IP, username và URL RTSP qua API
  đã xác thực; response luôn có `Cache-Control: no-store`.
- `PUT /api/devices/{id}/rtsp`: bật/tắt hoặc lưu `username`, `password`; payload
  cũ chỉ có `{ "enabled": true }` vẫn được giữ tương thích.
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

- **Không mở được dashboard**: kiểm tra add-on đang chạy, Internet và mở từ sidebar
  Ingress; khi chưa active, đây là hành vi bảo vệ bình thường.
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
- **RTSP bật nhưng không xem được**: kiểm tra IP hiển thị trong URL, camera và đầu
  ghi có cùng LAN/VLAN, không bị chặn cổng `554`, và username/password trên đầu ghi
  khớp cấu hình vừa lưu. RTSP không đi qua HANET Cloud và không thay thế TUTK P2P.
- **Không có URL để copy**: cloud chưa trả IP LAN hoặc đang che password mà add-on
  chưa có bản rõ; tải lại cấu hình, nhập lại password rồi lưu để camera xác nhận.
- **Không nhận được trial**: phải mở portal từ link trong addon để gửi cả public
  installation key; mỗi account/installation chỉ được nhận một lần.
- **Portal tạm lỗi nhưng key trước đó hợp lệ**: add-on dùng cache đã ký tối đa 72 giờ,
  nhưng dừng ngay khi key thực sự hết hạn.
- **Key mới sai làm mất key cũ**: bản `0.10.0` tự khôi phục key cũ còn hợp lệ; tải
  lại trạng thái License để kiểm tra key masked đang được giữ.

## 11. Giới hạn

- HANET Mobile API là API nội bộ và có thể thay đổi không báo trước.
- Âm thanh hai chiều chưa được đưa vào Home Assistant.
- PTZ, stream và setting cần xác nhận trên từng model/firmware.
- Chỉ sử dụng với tài khoản và thiết bị mà người dùng có quyền truy cập.

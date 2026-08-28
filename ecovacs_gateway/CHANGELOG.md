# Changelog

## 2.1.3 - 2026-08-28

- Đổi màn hình license thành luồng liên kết tự động cho Ecovacs APK Mod trên Home
  Assistant; người dùng không cần chép Installation ID hoặc public key.
- Giữ lại nhập key và thông tin kỹ thuật để xử lý trường hợp nâng cao, không đổi
  protocol Ecovacs, MQTT hoặc cơ chế license hiện có.

## 2.1.2 - 2026-08-28

- Loại bỏ mật khẩu quản trị local; ingress tự mở session và dùng license làm
  cổng quyền duy nhất.
- Trước activation chỉ hiển thị panel license; key hợp lệ mở toàn bộ gateway,
  dashboard, MQTT và command.
- Xóa hai option license khỏi config, tích hợp cố định portal APK Mod và giữ
  nguyên protocol Ecovacs/MQTT.

## 2.1.1 - 2026-08-27

- Tách portal license, D1 gateway và cặp khóa ký riêng cho bản Ecovacs APK Mod.
- Giữ nguyên protocol Ecovacs, MQTT Discovery và toàn bộ chức năng gateway của
  bản 2.1.0.

## 2.1.0 - 2026-08-04

- Thêm sensor/binary_sensor telemetry lồng nhau, action button, room select/button.
- Thêm action trạm X1, gồm nút Giặt giẻ và realtime station state.
- Thêm kéo chọn vùng trên bản đồ ingress và lệnh `customArea` có validate server.
- Giới hạn 64 entity động, 32 phòng và lọc key credential trước MQTT publish.
- Giữ map digest, delta topic, QoS 0 và publish semaphore để không tăng tải HA.

## 2.0.1 - 2026-07-31

- Khởi động MQTT Home Assistant trước cloud login để broker kết nối tức thì.
- Retained discovery/state/map dùng QoS 0 với tối đa bốn publish đồng thời.
- Map event được ưu tiên và không chờ sensor/discovery không đổi.
- Connect timeout còn 5 giây; reconnect backoff còn 1–15 giây.
- Giữ discovery cũ trong lúc danh sách robot vẫn đang tải.

## 2.0.0 - 2026-07-31

- Thay custom integration bằng MQTT Discovery trực tiếp trong add-on.
- Thêm UI broker MQTT, encrypted credential, LWT, retained state và reconnect nền.
- Chỉ publish entity có payload đổi; event burst được coalesce và queue có giới hạn.
- Bản đồ chỉ publish khi SVG digest đổi; sensor event không render lại map.
- Subscribe command topic theo DID, route vacuum/control về `gateway.command` và
  giới hạn command đồng thời để không làm nghẽn gateway/Home Assistant.
- Loại bỏ toàn bộ source/test/release của custom component và nâng version `2.0.0`.

## 1.2.0

- Phát SSE API v3 kèm field đổi, gom map bằng `MapChangedEvent` debounce 1 giây
  và tránh vòng lặp revision khi client chỉ đọc SVG/ETag.
- Không poll REST cho robot MQTT khỏe; không refresh map khi docked/idle và chỉ
  chạy map fallback lúc cleaning/returning.
- Lưu app UID/access token trong secret AES-GCM để reconnect nhanh; token cũ tự
  fallback password rồi cập nhật lại cache mã hóa.
- Gỡ gRPC/protobuf không dùng và bắt buộc binary wheel/no-bytecode khi build để
  add-on cài nhẹ, nhanh và ổn định hơn trên amd64/aarch64.

## 1.1.0

- Thêm stream SSE cho dashboard và Home Assistant bridge, map revision/ETag và
  refresh sensor/map theo chu kỳ cấu hình trong ingress.
- Stream bridge dùng delta theo robot và không phát khi refresh trả dữ liệu cũ;
  heartbeat giữ kết nối nhưng không đánh thức entity Home Assistant.
- Thêm quét nóng đa thiết bị, dashboard hiện đại có map/quick controls và trạng
  thái MQTT realtime cho từng robot.
- Giảm độ dài tối thiểu mật khẩu quản trị xuống 4 ký tự theo yêu cầu người dùng.

## 1.0.7

- Đồng bộ release với bridge `1.0.7`; gateway protocol không thay đổi so với
  `1.0.6`.
- Bridge nhận đúng ErrorEvent code `0` và `100` là trạng thái không lỗi, tránh
  vacuum entity hiển thị `error` giả dù command vẫn hoạt động.

## 1.0.6

- Thêm transport MQTT P2P cho command trong mode `d248_full`, dùng request topic,
  header `0.0.22`, `bdTaskID` và response request ID theo APK.
- Không fallback command sang REST khi MQTT control chưa sẵn sàng; gateway ghi
  `command_error` rõ ràng để bridge trả lỗi đúng.
- Sinh metadata control typed từ capability graph: bật/tắt là `switch`, enum là
  `select`, số có giới hạn là `number`, hành động tức thời là `button`.
- Sửa đường dẫn state cho event dataclass và kiểm tra chặt boolean, option, số
  nguyên cùng min/max trước khi tạo protocol command.
- Tách worker publish khỏi worker subscription để lỗi reconnect không làm mất
  request hoặc treo command đang chờ.

## 1.0.5

- Profile family X1 suy luận dùng `clean_V2`, `CleanAreaV2` và
  `GetCleanInfoV2`, sửa các nút start/pause/stop và dọn theo phòng không hoạt
  động trên X1 Turbo/X1 Omni nội địa.
- Phản hồi lệnh rỗng từ `deebot-client` được xem là thất bại, ghi
  `command_error` và trả HTTP 502 thay vì báo thành công giả.
- Serializer dataclass duyệt từng field, không deepcopy enum Rust/PyO3; vị trí
  robot và góc xoay bản đồ không còn tạo task exception.
- Callback event giữ gateway hoạt động nếu gặp giá trị chưa tuần tự hóa được và
  lưu chẩn đoán theo event thay vì tạo lỗi task nền không được thu hồi.

## 1.0.4

- Ưu tiên broker NGIOT trong `service.jmq` của từng robot thay vì host MQTT
  discovery chung; nhiều broker được quản lý độc lập và tự retry định kỳ.
- Profile family X1 suy luận dùng `getMapSet_V2`, tránh chuỗi
  `getMapSubSet` legacy không tương thích với firmware nội địa.
- Không polling `GetCleanLogs` cho profile X1 suy luận khi cloud mod không có
  endpoint log tương ứng.
- REST fallback chỉ poll trạng thái cốt lõi mỗi 30 giây; map refresh mỗi 2 phút
  để giảm command storm và log lặp.
- Panel hiển thị broker đã chọn cho từng robot; map đang khởi tạo trả trạng thái
  chưa có dữ liệu thay vì làm lỗi API.

## 1.0.3

- Nhận profile X1 theo metadata sản phẩm thay vì yêu cầu class phải có sẵn trong
  `deebot-client`.
- Không khởi tạo robot profile ở trạng thái unavailable; hiển thị profile class
  suy luận trong panel.
- Cho phép đổi mật khẩu quản trị lại bất kỳ lúc nào.
- Không ghi mật khẩu khởi tạo dưới dạng plaintext trong source hoặc tài liệu.

## 1.0.2

- Bỏ toàn bộ `install_id`, activation key và license gate.
- Đổi mật khẩu quản trị xong có thể cấu hình cloud và dùng API ngay.
- Xóa module licensing, public key và endpoint `/ui/activate`.

## 1.0.1

- Sửa redirect đăng nhập để session cookie được ghi sau khi xác thực thành công.
- Đồng bộ version với bridge domain mới `ecovacs_cn_mod`.

## 1.0.0

- Gateway cloud/MQTT/map/control tập trung trên port `7890`.
- Admin password bắt buộc đổi, CSRF, rate limit, AES-GCM và bearer token.
- Panel ingress chỉ dành cho quản trị viên Home Assistant.
- License Ed25519 offline, gắn `install_id`, sử dụng vĩnh viễn.
- Capability/event động và raw-device fallback.
- MQTT degraded mode không làm mất toàn bộ robot.

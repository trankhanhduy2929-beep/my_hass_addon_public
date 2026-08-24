# Ecovacs đa vùng Backend

Add-on đăng nhập đồng thời nhiều tài khoản Ecovacs China/quốc tế, nhận realtime
từ Ecovacs cloud/MQTT và đưa entity vào Home Assistant trực tiếp bằng MQTT
Discovery. Không cần custom component.

## Cài đặt

1. Cài/rebuild **Ecovacs China Backend**, sau đó khởi động add-on.
2. Mở giao diện **Ingress** của add-on.
3. Quét QR/mở portal, nhận license và dán key vào add-on. Không cần PIN hoặc
   mật khẩu quản trị ban đầu.
4. Trong thẻ **Kết nối MQTT**, điền địa chỉ, cổng, tài khoản và mật khẩu broker.
5. Bật **Dùng TLS** nếu broker yêu cầu TLS, thường là cổng `8883`.
6. Bấm **Lưu và kết nối MQTT**; bridge sẽ kết nối lại ngay.
7. Để trống địa chỉ nếu muốn dùng MQTT service của Supervisor.
8. Thêm một hoặc nhiều tài khoản China bằng ID, điện thoại + mật khẩu hoặc SMS.
9. Tài khoản quốc tế dùng tab **Quốc tế**, mã quốc gia ISO 2 ký tự và ID/email
   cùng mật khẩu Ecovacs.
10. Với tài khoản Việt Nam, dùng `VN`. Nếu Ecovacs yêu cầu xác minh thiết bị mới,
   nhập mã được gửi tới email trong form xuất hiện ngay tại tab **Quốc tế**.

Gmail được dùng như email Ecovacs, không phải Google OAuth. Nếu tài khoản chỉ
đăng nhập bằng nút Google trong ứng dụng, hãy đặt/reset mật khẩu Ecovacs trước.

Nếu đã dùng bản custom integration cũ, hãy xóa config entry
**Ecovacs China Backend Client**, xóa `custom_components/ecovacs_cn` và restart
Home Assistant để không còn entity trùng.

## MQTT và realtime

- Add-on ưu tiên broker thủ công trong thẻ Ingress; khi địa chỉ trống, add-on
  dùng Supervisor service `mqtt:want`.
- Discovery config, state và availability được retain.
- Mỗi sensor/control có topic và cache riêng; payload không đổi không publish.
- Các sensor trạng thái robot, trạm, lực hút, mức nước, chế độ lau, firmware,
  khu vực đang dọn và thiết bị metadata-only được publish bằng tiếng Việt;
  vacuum entity, select và command vẫn dùng mã chuẩn để không ảnh hưởng điều
  khiển.
- Vacuum entity giữ state hợp lệ cuối cùng khi cloud phát `error`; sau restart
  dùng `idle` cho tới khi nhận state mới. Sensor **Lỗi** vẫn báo mã lỗi thật.
- Map SVG dùng topic riêng, mặc định tối đa một lần mỗi 5 giây và tối đa 2 MB.
- Fallback map mỗi 5 giây chỉ hỏi vị trí/đường đi; map tĩnh tiếp tục nhận qua
  event và full refresh, tránh tải lại dữ liệu nền không cần thiết.
- Position/trace chỉ được hỏi khi robot đang dọn hoặc đang về trạm. Khi robot
  chuyển sang idle/docked/paused, add-on giữ tối đa 3 giây cho bản đồ cuối rồi
  chặn event động lặp; event map tĩnh vẫn cập nhật bình thường.
- Broker lỗi chỉ làm MQTT bridge reconnect theo backoff; API Ingress, watchdog
  và cloud controller tiếp tục chạy.
- Đăng nhập Ecovacs trả ngay sau khi credential được xác thực; kết nối MQTT
  realtime và tải robot chạy nền. Nhiều tài khoản kết nối song song.
- Add-on không tạo handshake MQTT kiểm tra trùng. Subscription timeout được
  giữ lại và tự gửi lại ở kết nối kế tiếp thay vì bắt người dùng đăng nhập lại.
- Command được xử lý tuần tự, tối đa 4 KiB, bỏ qua retained command và luôn qua
  allow-list/type validation trước khi gửi tới Ecovacs.

## Options

| Option | Mặc định | Ý nghĩa |
| --- | ---: | --- |
| `log_level` | `info` | Mức log của add-on |
| `map_refresh_interval` | `5` | Fallback hỏi vị trí và đường đi từ Ecovacs |
| `state_refresh_interval` | `120` | Fallback yêu cầu full state |
| `mqtt_enabled` | `true` | Bật MQTT Discovery |
| `mqtt_map_enabled` | `true` | Publish SVG qua MQTT Image |
| `mqtt_map_min_interval` | `5` | Giới hạn tần suất map |
| `mqtt_map_max_bytes` | `2000000` | Bỏ qua map vượt kích thước này |

## API nội bộ

Cổng `4545` vẫn phục vụ Ingress UI và API quản trị, nhưng không cần ánh xạ ra
host và Home Assistant không cần mã token để nhận entity. Ingress tự nhận phiên
ngắn hạn; cài mới không có bước đăng nhập bằng PIN/mật khẩu.

API quản trị có thể thêm tài khoản qua `POST /api/v1/account/login`, xóa riêng
qua `DELETE /api/v1/accounts/{account_id}` và reconnect riêng qua
`POST /api/v1/accounts/{account_id}/reconnect`. API không trả mật khẩu hoặc
cloud token đã lưu.

## Xử lý lỗi

- **MQTT unavailable:** cài/khởi động broker rồi restart add-on.
- **MQTT disconnected:** kiểm tra broker log; bridge tự retry tối đa mỗi 300
  giây và không làm add-on/Core dừng.
- **Không có entity:** kiểm tra MQTT integration, MQTT Discovery và trạng thái
  MQTT trong Ingress.
- **Không có robot:** kiểm tra đúng tab China/quốc tế, mã quốc gia của tài khoản
  quốc tế và dùng nút reconnect riêng tài khoản.
- **Gmail không đăng nhập:** dùng tab **Quốc tế**, country `VN` và mật khẩu
  Ecovacs. Nếu tài khoản chỉ có Google OAuth, đặt/reset mật khẩu trong Ecovacs
  Home trước. Khi form mã email xuất hiện, nhập mã hoặc bấm **Gửi lại mã**.
- **Robot quốc tế chỉ có metadata:** class đó chưa được `deebot-client` nhận
  diện. Add-on không áp fallback China để tránh gửi lệnh sai thiết bị.
- **Nâng cấp hỏi lại license:** dùng bản `1.3.3`; key có backup mã hóa và recovery
  riêng. Nếu dữ liệu đã bị xóa trước khi cài bản này, nhập lại key hiện tại một
  lần; các lần update sau tự nhận.
- **Ecovacs MQTT `Operation timed out`:** dùng bản `1.3.3`; API đăng nhập không
  chờ MQTT, tài khoản chuyển sang **Đang kết nối**, client retry nền mỗi 5 giây
  và subscription chưa hoàn tất được giữ lại qua reconnect.
- **X1/X1 PRO/T10 OMNI timeout:** dùng bản `1.3.3`; mọi profile X1/T10 OMNI,
  kể cả class lạ nhận diện bằng tên sản phẩm, đều dùng map-set không sinh chuỗi
  `getMapSubSet`. Profile suy luận và class bảo thủ cũng không gọi `getWorkMode`;
  chỉ X1 class `8onkgl`/`1vxt52` đã xác minh giữ capability này.
- **Dọn một khu vực:** dùng MQTT button **Dọn [tên khu vực]** trong Home
  Assistant. Ingress không còn hiển thị bản đồ/nút chọn phòng vì firmware có
  thể chỉ trả room ID mà không có ranh giới hoặc tâm phòng đáng tin cậy.
- **Đặt tên khu vực:** trong thẻ robot ở Ingress, nhập tên cạnh từng room ID và
  bấm **Lưu tên**. Add-on lưu tên mã hóa theo robot/map, cập nhật MQTT Discovery
  nhưng giữ nguyên unique ID của button.
- **Khu vực đang dọn:** sensor này dùng `areaSts=1` của `CleanInfo_V2` để chỉ
  đúng phòng hiện tại; thuộc tính sensor vẫn có room ID và danh sách đã chọn.
- **Tên phòng:** X1/T10 đọc `getMapSet_V2` giống app China mà không gọi
  `getMapSubSet`. Nếu firmware không trả tên thì có thể đặt thủ công trong
  Ingress; mặc định MQTT button dùng **Khu vực N**.
- **Giặt giẻ không chạy:** bản `1.3.3` gửi `clean_V2` loại `washing` đúng giao
  thức DT10/X1 thay cho station action cũ.
- **Không reset được vật tư camelCase:** bản `1.3.3` sửa MQTT action cho chổi
  cạnh, giẻ lau tròn và bộ chăm sóc trạm.
- **Chỉ thấy Khu vực N, không có đa giác:** firmware chỉ trả ID trong
  `getMapSet`. Nút khu vực vẫn dọn đúng phòng; add-on không gọi `getMapSubSet`
  để tránh tái phát timeout trên X1/T10 nội địa.
- **Map không cập nhật:** kiểm tra `mqtt_map_enabled`, interval và giới hạn byte.
- **Map vẫn đổi khi robot đã ở trạm:** dùng bản `1.3.3`; bản này dừng polling
  position/trace và bỏ map event động sau cửa sổ cập nhật cuối 3 giây.
- **Log `getNetInfo`/`getBorderSpin` timeout:** bản `1.3.3` không còn gọi hai
  nhóm này mỗi 120 giây. Setting mặc định làm mới mỗi 600 giây, còn network,
  OTA và tuổi thọ mỗi 1200 giây; lỗi cloud tạm thời không làm vacuum entity lỗi.
- **MQTT gửi quá nhiều:** bản `1.3.3` gom event 350 ms, chỉ publish robot thay
  đổi, cache Discovery theo cấu trúc và chỉ render SVG map khi MQTT/API cần.
- **Log mạng lặp liên tục:** bản `1.3.3` chỉ giữ một warning cùng nội dung mỗi
  5 phút cho lỗi MQTT/command mạng lặp; reconnect vẫn chạy nền bình thường.
- **Một robot lỗi làm polling dừng:** bản `1.3.3` cô lập lỗi refresh/map theo
  từng robot và watchdog tự khởi động lại Ecovacs MQTT task bị dừng.
- **`8bja83 not recognized`:** bản `1.3.3` đăng ký X1 OMNI nội địa trực tiếp
  trước lúc `deebot-client` phân loại và xóa negative cache cũ. Nếu log vẫn có
  logger `custom_components.ecovacs_cn`, Home Assistant còn chạy integration
  cũ; hãy xóa integration/thư mục custom component và restart Home Assistant.

Credential của mọi tài khoản Ecovacs được mã hóa trong `/data`; tài khoản China
cũ được migration tự động và giữ device ID. License key được mã hóa trong
`/data/license`, có backup và recovery riêng trong `/data/license_recovery`; MQTT
credential được mã hóa riêng trong `/data/mqtt`. Không mở cổng `4545` trực tiếp
ra Internet.

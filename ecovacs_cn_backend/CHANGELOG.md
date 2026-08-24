# Changelog

## 1.3.3 - 2026-08-24

- Sửa lỗi nâng cấp add-on làm mất nhận diện license: Installation ID được lưu
  bền trong `security.json` và file dự phòng riêng, không còn chỉ tồn tại trong
  RAM như một số bản `1.3.0–1.3.1`.
- License store dùng ghi atomically, backup AES-GCM và recovery độc lập trong
  `/data/license_recovery`; file hỏng hoặc thư mục `/data/license` bị tạo lại
  được phục hồi trước khi UI yêu cầu nhập key.
- Nếu bản cũ từng publish MQTT Discovery, add-on thử các Installation ID cũ với
  chữ ký portal, chỉ nhận ID nào xác minh được rồi đồng bộ lại MQTT.
- Thêm regression test cho restart, corrupt file, mất thư mục license và
  migration Installation ID sau nâng cấp.

## 1.3.2 - 2026-08-24

- Xóa hoàn toàn PIN/mật khẩu quản trị cũ, token cố định `ecv1_` và các endpoint
  tạo, liệt kê hoặc thu hồi token cho custom integration.
- API quản trị chỉ chấp nhận phiên Ingress ký ngắn hạn `ecvui_`; license key chỉ
  dùng để kích hoạt dịch vụ và không còn hoạt động như bearer token.
- Xóa WebSocket `/api/v1/events`; Home Assistant nhận entity và điều khiển robot
  duy nhất qua MQTT Discovery, không cần custom integration.
- Khi nâng cấp, tự dọn password hash/token hash cũ trong `security.json` nhưng
  giữ nguyên Installation ID để license hiện tại không bị đổi máy.

## 1.3.1 - 2026-08-24

- Đổi bảng giá portal thành trial 1 ngày miễn phí, 7 ngày 50.000đ và vĩnh viễn
  200.000đ; giữ tương thích các đơn/key gói tháng cũ trong database.
- Xóa hoàn toàn option `license_portal_url`; domain Vercel production được đóng
  sẵn trong add-on nên người dùng không phải nhập địa chỉ portal.
- Giữ mặc định tắt endpoint mật khẩu quản trị cũ; kích hoạt và vận hành chỉ dựa
  trên license key hợp lệ gắn với Installation ID.

## 1.3.0 - 2026-08-23

- Thêm portal Vercel/Supabase cho đăng nhập Google hoặc email, liên kết
  Installation ID, trial 1 ngày, gói 1 tháng/6 tháng/vĩnh viễn và lịch sử key.
- Tích hợp PayOS/VietQR: tạo mã đơn riêng, xác minh webhook, đối soát payment
  link và tự cấp key idempotent ngay sau khi thanh toán.
- Thêm trang admin xem người dùng, installation, đơn hàng và license; hỗ trợ cấp
  key thủ công, copy key, thu hồi và kích hoạt lại.
- Bỏ yêu cầu mã khởi tạo, PIN và mật khẩu đăng nhập ban đầu. Ingress tự cấp phiên
  ngắn hạn; người dùng chỉ cần license key hợp lệ để mở backend/MQTT.
- Ràng buộc key theo Installation ID, lưu key mã hóa AES-256-GCM và dừng dịch vụ
  khi license hết hạn hoặc bị thu hồi; hỗ trợ grace ngoại tuyến tối đa 72 giờ.
- Ký mọi phản hồi verify bằng Ed25519 kèm nonce, hash key và domain portal;
  add-on từ chối máy chủ giả hoặc dữ liệu license bị sửa.
- Tiếp tục không đóng gói AIVI/video và giữ nguyên hỗ trợ China/quốc tế của bản
  `1.2.21`.

## 1.2.21 - 2026-08-20

- Giữ một add-on đa vùng duy nhất; tài khoản China và quốc tế tiếp tục dùng
  authenticator, controller, MQTT task và reconnect riêng để chạy song song.
- Nâng `deebot-client` lên `18.5.1`, bổ sung luồng xác minh thiết bị mới cho tài
  khoản quốc tế khi Ecovacs trả mã `1013`.
- Tự gửi mã xác minh tới email, hiện form nhập/gửi lại mã trong Ingress và giữ
  phiên xác thực tạm thời chỉ trong RAM cho tới khi hoàn tất hoặc add-on dừng.
- Trả hướng dẫn rõ khi Gmail thuộc tài khoản chỉ dùng Google OAuth: cần đặt hoặc
  reset mật khẩu Ecovacs trong ứng dụng trước khi đăng nhập add-on.
- Nâng `aiohttp` và `cryptography` theo yêu cầu runtime của client mới, bổ sung
  regression test cho login quốc tế, mã sai, resend và cleanup session.
- Đóng gói `icon.png` và `logo.png` Ecovacs vào add-on repository để Home
  Assistant hiển thị nhận diện đúng sau các lần cập nhật.

## 1.2.20 - 2026-08-11

- Đăng ký trước hardware alias `8bja83` của DEEBOT X1 OMNI nội địa vào registry
  dùng chung của `deebot-client` trước khi `ApiClient.get_devices()` phân loại.
- Xóa negative lookup cache cho `8bja83`, nên class vẫn được nhận diện ngay cả
  khi một lần dò trước đó từng kết luận module không tồn tại.
- Áp dụng cùng cơ chế phòng vệ cho `hxm494` T10 OMNI; giữ nguyên profile X1/T10
  bảo thủ, không bật lại `getWorkMode` hoặc `getMapSubSet` chưa được hỗ trợ.
- Thêm regression test gọi `ApiClient` với payload X1 OMNI thực tế và xác nhận
  thiết bị đi vào danh sách MQTT, không vào `not_supported` hay phát warning.

## 1.2.19 - 2026-08-07

- Thêm watchdog 30 giây để khởi động lại Ecovacs MQTT task nếu task dừng ngoài
  vòng reconnect chuẩn; một lỗi refresh/map riêng lẻ không còn làm chết poller
  của toàn tài khoản.
- Reset backoff MQTT Home Assistant về 2 giây ngay sau khi đã từng kết nối thành
  công, tránh phải chờ tới 300 giây nếu broker rớt lại sau một đợt lỗi dài.
- Giới hạn warning mạng/command trùng nội dung còn một lần mỗi 5 phút, giảm
  traceback, log I/O và tải lưu trữ nhưng vẫn giữ cảnh báo định kỳ để chẩn đoán.
- MQTT map chỉ cache digest BLAKE2s thay vì giữ thêm một bản SVG lớn; tự dọn
  cache state/map/topic của robot đã xóa và chỉ ghi manifest Discovery khi tập
  topic thực sự thay đổi.
- WebSocket chỉ snapshot robot có thay đổi. Ingress chống request chồng, poll
  15 giây thay vì 5 giây và ngừng poll khi tab bị ẩn; MQTT entity vẫn realtime.
- Tiếp tục không đóng gói AIVI/video và giữ nguyên toàn bộ bản rollback cũ.

## 1.2.18 - 2026-08-07

- Tách request đăng nhập khỏi quá trình tải controller/MQTT: sau khi credential
  được xác thực và lưu mã hóa, API trả ngay; kết nối realtime tiếp tục chạy nền.
- Bỏ MQTT `verify_config` tạo một handshake tạm trước kết nối chính, giảm một
  vòng TLS/auth không cần thiết khi broker Ecovacs phản hồi chậm.
- Cho phép nhiều tài khoản kết nối đồng thời bằng lock riêng từng account thay
  vì khóa toàn backend khiến account sau phải chờ account trước.
- Thêm MQTT client bảo toàn subscription khi `subscribe`/`unsubscribe` timeout;
  thay đổi mới hơn được ưu tiên để không phục hồi subscription đã bị xóa.
- Nút reconnect trả ngay và hiển thị **Đang kết nối**; warning broker tạm thời
  không còn làm request đăng nhập báo thất bại dù credential đã đúng.
- Tiếp tục không đóng gói AIVI/video và giữ nguyên toàn bộ bản rollback cũ.

## 1.2.17 - 2026-08-07

- Không quảng bá Work Mode cho X1/X1 PRO/T10 OMNI được suy luận theo tên sản
  phẩm hoặc class chưa xác minh, loại bỏ lệnh `getWorkMode` không được firmware
  phản hồi và warning timeout lặp.
- Giữ Work Mode cho hai class X1 `8onkgl` và `1vxt52` đã có profile xác minh;
  không làm mất select này trên thiết bị thực sự hỗ trợ.
- Bổ sung regression test cho X1 PRO/T10 class lạ và luồng `force=True`, đồng
  thời giữ nguyên sửa lỗi map subset, đa tài khoản và đăng nhập quốc tế.
- Tiếp tục không đóng gói AIVI/video và giữ nguyên toàn bộ bản rollback cũ.

## 1.2.16 - 2026-08-07

- Cho phép lưu và kết nối đồng thời nhiều tài khoản Ecovacs; mỗi tài khoản có
  controller, Ecovacs MQTT, trạng thái và vòng reconnect riêng.
- Thêm đăng nhập tài khoản quốc tế bằng Ecovacs ID/email, mật khẩu và mã quốc
  gia ISO 2 ký tự; REST/MQTT endpoint được chọn theo đúng quốc gia tài khoản.
- Tự migration tài khoản China đơn của bản cũ sang kho nhiều tài khoản, giữ
  nguyên device ID, room name và entity hiện có.
- Thêm danh sách tài khoản trong Ingress cùng thao tác reconnect/xóa từng tài
  khoản hoặc toàn bộ; API trạng thái không trả password/token.
- Gộp robot từ mọi tài khoản vào MQTT Discovery, giữ snapshot offline khi một
  tài khoản lỗi nhưng các tài khoản khác vẫn hoạt động.
- Chỉ dùng profile suy luận/lệnh riêng China cho tài khoản China; thiết bị quốc
  tế class chưa biết được giữ metadata-only để tránh gửi lệnh sai.
- Tiếp tục không đóng gói AIVI/video và giữ nguyên các bản rollback trước đó.

## 1.2.15 - 2026-08-07

- Buộc toàn bộ profile X1, X1 PRO và T10 OMNI dùng `GetMapSetWithoutSubsets`
  thay vì chỉ áp dụng cho class China live/T10 Curie.
- Nhận diện thêm tên sản phẩm `DEEBOT X1 PRO OMNI` và các biến thể chứa
  `X1` + `OMNI`, kể cả khi Ecovacs trả class chưa biết.
- Ngăn handler `getMapSet` tự sinh nhiều lệnh `getMapSubSet` không được firmware
  hỗ trợ, loại bỏ chuỗi warning timeout lặp trên X1 PRO OMNI.

## 1.2.14 - 2026-08-07

- Gom các backend event trong cửa sổ MQTT mặc định 350 ms và hợp nhất device,
  map, status trước khi publish.
- Chỉ snapshot/publish robot có `device_id` thay đổi; full/status reconnect vẫn
  đồng bộ toàn bộ và dọn Discovery topic của thiết bị đã mất.
- Cache MQTT Discovery theo schema entity, không dựng lại config khi chỉ state,
  pin, thuộc tính hoặc giá trị control thay đổi.
- Tách refresh thành state lõi 120 giây, setting 600 giây và diagnostic 1200
  giây; `getBorderSpin` và `getNetInfo` không còn chạy chung mỗi 120 giây.
- Map động mặc định 5 giây khi cleaning/returning, chỉ giữ bản cuối khi dừng và
  render SVG lười khi MQTT/API yêu cầu thay vì trên mọi `MapChangedEvent`.

## 1.2.13 - 2026-08-07

- Dừng yêu cầu `PositionsEvent` và `MapTraceEvent` khi robot không còn ở trạng
  thái `cleaning` hoặc `returning`, tránh bản đồ MQTT tiếp tục cập nhật liên tục
  khi robot đã dừng, tạm dừng hoặc về trạm.
- Khi chuyển từ trạng thái đang di chuyển sang trạng thái tĩnh, add-on yêu cầu
  một lượt position/trace cuối và giữ cửa sổ 3 giây để ghi đúng vị trí cùng
  đường đi cuối trước khi đóng luồng map động.
- Phân biệt event map động với map tĩnh: `MajorMapEvent`, `MinorMapEvent`,
  `MapInfoEvent`, `MapSetEvent`, `MapSubsetEvent` và cached map info vẫn được
  phép cập nhật SVG khi robot docked.
- Thêm regression test xác nhận rung vị trí ở trạm không tăng map revision,
  trong khi thay đổi mảnh nền tĩnh vẫn tạo revision mới.
- Không đóng gói AIVI/video; giữ nguyên trình đặt tên khu vực dạng danh sách.

## 1.2.12 - 2026-08-06

- Khôi phục mục **Đặt tên khu vực** trong từng thẻ robot dưới dạng danh sách
  `room ID + ô nhập tên`; không khôi phục bản đồ SVG, đa giác, tâm phòng hoặc
  nút dọn trực tiếp trong Ingress.
- Tên tự đặt tiếp tục được lưu mã hóa theo robot/map, cập nhật sensor **Khu vực
  đang dọn** và nhãn MQTT Discovery button nhưng giữ nguyên unique ID theo room
  ID, tránh Home Assistant tạo entity mới.
- Khi người dùng đang nhập tên, chu kỳ refresh Ingress không dựng lại thẻ robot
  nên nội dung và focus không bị mất; sau khi lưu thành công giao diện tự tải
  tên mới từ backend.
- Tiếp tục không đóng gói AIVI/video và giữ nhịp map tối ưu của bản `1.2.11`.

## 1.2.11 - 2026-08-06

- Bỏ toàn bộ giao diện bản đồ chọn phòng, nút dọn phòng và form đặt tên trong
  Ingress vì firmware X1/T10 có thể không trả ranh giới hoặc tâm phòng đủ tin
  cậy. Backend vẫn giữ room ID/tên nội bộ và MQTT Discovery button **Dọn [tên
  khu vực]**.
- Thêm sensor MQTT **Khu vực đang dọn**. Parser `CleanInfo_V2` ghép danh sách
  room ID trong `content.value` với `areaSts`; trạng thái `1` xác định phòng
  hiện tại, đồng thời publish thuộc tính ID và danh sách phòng đã chọn.
- Tự xóa sensor khu vực khi robot dừng, về trạm hoặc chuyển sang chế độ dọn
  không theo phòng; tên sensor tự đồng bộ khi metadata/tên phòng thay đổi.
- Tối ưu độ trễ bản đồ: fallback giảm từ 30 xuống 10 giây và chỉ hỏi vị trí với
  đường đi động, không tải lại mảnh nền tĩnh; MQTT map throttle giảm từ 5 xuống
  2 giây và Ingress refresh trạng thái mỗi 5 giây.
- Không đóng gói AIVI/video; giữ nguyên luồng vacuum ổn định không phát state
  `error` và các sửa lỗi vật tư/giặt giẻ của bản trước.

## 1.2.10 - 2026-08-06

- Sửa các MQTT button đặt lại **chổi cạnh**, **giẻ lau tròn** và **bộ chăm
  sóc trạm**: bridge ánh xạ topic chữ thường về đúng action camelCase
  `sideBrush`, `roundMop`, `unitCare` trước khi gửi lệnh `resetLifeSpan`.
- Sửa nút **Giặt giẻ** trên X1/T10 OMNI theo đúng app China: gửi `clean_V2`
  với `content.type=\"washing\"` thay vì `stationAction type=4` không hoạt động.
- Đọc tên phòng và tâm phòng qua `getMapSet_V2`, API mà app gốc dùng; không bật
  lại chuỗi `getMapSubSet` từng phòng từng gây timeout trên X1/T10 nội địa.
- Bản đồ Ingress hiển thị vùng đa giác khi firmware cung cấp; nếu chỉ có tâm
  phòng thì hiển thị điểm phòng có ID/tên ngay trên bản đồ. Tên tự đặt vẫn được
  ưu tiên và đồng bộ vào MQTT Discovery button ổn định theo room ID.
- Việt hóa tên sensor và nút reset vật tư. Không đóng gói AIVI/video.

## 1.2.9 - 2026-08-06

- Cho phép đặt tên thủ công cho từng room ID ngay trong mục **Dọn theo khu vực**;
  tên được lưu theo robot và map trong kho credential mã hóa hiện có.
- Tên đã đặt được giữ lại khi Ecovacs gửi lại `MapSetEvent`, `MapSubsetEvent`
  hoặc `RoomsEvent`, đồng thời cập nhật nhãn trên bản đồ và danh sách khu vực.
- MQTT Discovery tạo một button **Dọn [tên khu vực]** cho từng room ID; unique ID
  luôn dựa trên room ID nên đổi tên không làm Home Assistant tạo entity mới.
- Lệnh MQTT chỉ chấp nhận payload `PRESS` và room ID đang tồn tại trên bản đồ
  hoạt động. Bản phát hành tiếp tục không đóng gói AIVI/video.

## 1.2.8 - 2026-08-06

- Thêm mục **Dọn theo khu vực** trong Ingress: hiển thị bản đồ nhỏ và lớp đa
  giác phòng có thể chạm trực tiếp; luôn có danh sách nút phòng làm phương án
  dự phòng khi firmware không trả hình đa giác.
- Thu thập ID/tên/tọa độ phòng từ `MapSetEvent`, `MapSubsetEvent` và
  `RoomsEvent`; snapshot API có map ID, rotation, danh sách phòng và trạng thái
  hỗ trợ lệnh dọn phòng.
- Chạm một phòng gửi `CleanMode.SPOT_AREA` với đúng một room ID, kiểm tra ID phải
  thuộc bản đồ đang hoạt động trước khi phát lệnh tới robot.
- X1/T10 tiếp tục không tạo follow-up `getMapSubSet`; nếu `getMapSet` đã nhúng
  tên/đa giác phòng thì add-on dùng trực tiếp, tránh khôi phục chuỗi timeout cũ.
- Bản phát hành này không chứa AIVI/video; cập nhật metadata lên `1.2.8`.

## 1.2.7 - 2026-08-04

- Vacuum entity MQTT không còn publish state `error`, tránh automation bị kích
  hoạt sai bởi timeout hoặc mã lỗi thoáng qua từ Ecovacs cloud.
- Khi đang chạy, bridge giữ trạng thái hợp lệ gần nhất như `cleaning`, `docked`
  hoặc `returning`; nếu add-on vừa restart trong lúc state là lỗi thì dùng `idle`.
- Sensor **Lỗi** và sensor **Trạng thái** vẫn giữ dữ liệu lỗi để chẩn đoán; chỉ
  state chuẩn của vacuum entity được ổn định cho automation.

## 1.2.6 - 2026-08-04

- Đăng ký native class `8bja83` của DEEBOT X1 OMNI vào hardware của
  `deebot-client`, loại bỏ cảnh báo class chưa nhận diện khi tải danh sách máy.
- Giữ state V2, lệnh dọn, trạm, map metadata, ảnh nền, vị trí và trace đang hoạt
  động; chỉ chặn follow-up `getMapSubSet` mà firmware thực tế không phản hồi.
- Dùng chung bộ xử lý map-set không subset đã kiểm thử cho `8bja83` và T10
  `hxm494`, không ảnh hưởng X1/T10 class khác.

## 1.2.5 - 2026-08-04

- Đăng ký native class `hxm494` của DEEBOT T10 OMNI vào thư mục hardware của
  `deebot-client`, loại bỏ cảnh báo class chưa nhận diện và fallback vòng sau.
- Không quảng bá work-mode cho `hxm494` vì robot thật không phản hồi
  `getWorkMode`; các model X1/T10 khác giữ nguyên capability hiện tại.
- Giữ map metadata, ảnh nền, vị trí và trace nhưng chặn follow-up
  `getMapSubSet` riêng cho `hxm494`, tránh nhiều timeout nối tiếp mỗi lần refresh.
- Giữ nguyên báo lỗi robot thật từ `getError`; bản sửa không che mã lỗi thiết bị.

## 1.2.4 - 2026-08-01

- Việt hóa giá trị sensor trạng thái robot, trạng thái trạm, lực hút, mức nước,
  chế độ lau, firmware và thiết bị metadata-only khi publish qua MQTT Discovery.
- Giữ nguyên payload kỹ thuật của vacuum entity, select và command để các lệnh,
  automation điều khiển và chuẩn trạng thái Home Assistant không bị ảnh hưởng.
- Giá trị chưa biết từ firmware/model mới vẫn được publish nguyên bản thay vì
  đoán bản dịch; mức nước dạng số tùy chỉnh của X9 PRO không bị đổi sang enum.

## 1.2.3 - 2026-07-31

- Hỗ trợ rõ ràng DEEBOT X9 PRO OMNI với class quốc tế `ilt3k8` và hai class
  nội địa `lwmdoj`, `0jv4ti` đã có profile đầy đủ trong `deebot-client` 18.4.
- Với class X9 nội địa mới chưa có trực tiếp trong thư viện, add-on nhận diện từ
  model/tên sản phẩm bất biến và dùng profile X9 `ilt3k8` đã xác minh.
- Bật toàn bộ capability X9 hiện có gồm bản đồ/phòng/vị trí, dọn khu vực, bốn
  mức lực hút, ba work mode, mức nước tùy chỉnh, tần suất giặt giẻ, auto-empty,
  firmware, khóa trẻ em, hiệu suất và tuổi thọ vật tư.
- Ưu tiên model chính xác trước logic ID dùng chung để không nhận nhầm DEEBOT X8
  MAX PRO OMNI thành X9 PRO OMNI.
- Chỉ quảng bá nút hút rác của trạm theo profile đã xác minh; chưa tự thêm lệnh
  giặt/sấy/vệ sinh trạm không có trong profile X9 upstream.

## 1.2.2 - 2026-07-30

- Hiển thị rõ Home Assistant Core không phải MQTT broker và hướng dẫn dùng
  Mosquitto Broker hoặc địa chỉ broker ngoài ngay trong form cấu hình add-on.
- Khi lưu MQTT, add-on chờ kết quả kết nối đầu tiên và hiển thị trực tiếp lỗi
  broker thay vì chỉ báo trạng thái `connecting` hoặc giấu lỗi trong tooltip.
- Cho phép lưu lại cùng cấu hình để ép kết nối lại ngay khi bridge đang offline
  hoặc disconnected; reconnect backoff vẫn cô lập lỗi để không làm sập add-on.
- Dùng event bất đồng bộ cho trạng thái kết nối, không polling vòng lặp trong
  request lưu cấu hình.

## 1.2.1 - 2026-07-30

- Thêm cấu hình MQTT thủ công gồm host, port, username, password và TLS; broker
  thủ công được ưu tiên, Supervisor `mqtt:want` chỉ còn là fallback.
- Loại bỏ phần tạo/quản lý API token khỏi giao diện. Home Assistant chỉ cần
  MQTT Discovery; phiên bearer ẩn vẫn bảo vệ trang quản trị trong tab hiện tại.
- Thay kênh custom integration/WebSocket bằng MQTT Discovery trực tiếp từ
  add-on; Home Assistant không còn cần cài custom component hoặc API token.
- Chỉ publish từng state/control khi payload thay đổi, dùng retained discovery
  và availability riêng cho bridge/robot.
- Cô lập lỗi broker bằng reconnect backoff, command queue tuần tự, bỏ retained
  command và giới hạn payload 4 KiB.
- Thêm MQTT Image cho SVG map với interval/kích thước cấu hình được để tránh
  tạo tải cao cho broker và Home Assistant Core.
- Release builder chỉ còn tạo archive add-on repository.

## 1.2.0

- Thêm WebSocket trạng thái nội bộ từ add-on sang custom; MQTT event chỉ phát
  snapshot của robot thay đổi, còn lúc nghỉ chỉ giữ heartbeat và poll fallback.
- Bản đồ cập nhật theo `MapChangedEvent` đã debounce khoảng một giây; socket chỉ
  gửi revision nhỏ, custom tải SVG một lần cho mỗi revision và cache ảnh local.
- Mỗi entity lọc descriptor riêng trước khi ghi state, tránh map realtime làm
  toàn bộ sensor, switch, select và number ghi lại liên tục trong Home Assistant.
- Tăng fallback mặc định lên 30 giây cho map, 120 giây cho full state và 60 giây
  cho poll local; dữ liệu giống hệt không phát coordinator update.
- Tái sử dụng authenticator đã đăng nhập mật khẩu/SMS cho cloud controller,
  loại bỏ một vòng portal authentication lặp trước khi lấy robot và nối MQTT.
- API action trả snapshot mới ngay trong response để giao diện phản hồi nhanh,
  sau đó WebSocket tiếp tục đồng bộ event chính thức từ Ecovacs.

## 1.1.0

- Thêm catalog 218 profile toàn cầu và resolver chuẩn hóa vùng `cn`/`ww` trong
  `UILogicId`, giúp class nội địa dùng profile `deebot-client` tương đương khi
  có cùng định danh sản phẩm.
- Thêm fallback bảo thủ theo họ thiết bị cho DEEBOT và GOAT chưa có profile
  chính xác; GOAT được xuất thành entity `lawn_mower` chuẩn Home Assistant.
- WINBOT, AIRBOT, thiết bị legacy và protocol chưa hỗ trợ vẫn hiện metadata
  chẩn đoán thay vì làm lỗi đăng nhập toàn bộ tài khoản; không quảng bá lệnh hay
  bản đồ chưa được xác minh.
- Bỏ yêu cầu kết nối MQTT khi tài khoản chỉ có thiết bị metadata-only, đồng thời
  giữ nguyên luồng đăng nhập điện thoại và profile T10 OMNI `hxm494` đã hoạt động.

## 1.0.12

- Xác nhận và nhận diện trực tiếp class `hxm494` của DEEBOT T10 OMNI nội địa,
  vẫn dùng profile DT10/X1 OMNI bảo thủ đã tương thích với robot này.
- Tự chuyển số điện thoại Trung Quốc nhập trong tab Ecovacs ID sang luồng đăng
  nhập điện thoại, tránh báo sai lỗi credential với tài khoản chỉ có mobile.
- Tăng phiên bản add-on để Home Assistant buộc rebuild image thay vì tiếp tục
  chạy cache cũ chưa có fallback T10 OMNI.

## 1.0.11

- Thêm thực thể `vacuum` chuẩn Home Assistant cho từng robot, hỗ trợ bắt đầu,
  tạm dừng, dừng, về trạm, tìm robot và đặt lực hút theo capability thực tế.
- Tách setting khỏi dãy button thành `select`, `switch` và `number`: lực hút,
  mức nước, work mode, auto-empty, bản đồ đang dùng, khóa trẻ em, multi-map,
  firmware tự động, số lượt dọn, tần suất giặt giẻ và các setting được robot
  quảng bá.
- Thêm `binary_sensor` đúng kiểu cho trạng thái kết nối, giẻ lau và setting
  boolean; giữ button cho thao tác tức thời như hút rác, giặt/sấy giẻ, vệ sinh
  đế trạm, reset vật tư và làm mới dữ liệu.
- Sửa entity bản đồ luôn được tạo cho robot có capability map và khởi tạo đúng
  `ImageEntity` của Home Assistant; map tự chuyển khả dụng khi SVG cache sẵn
  sàng và cập nhật theo timestamp/revision mới.
- Mở rộng API action nhận giá trị đã kiểm tra kiểu/range, không cho custom gửi
  tùy ý command cloud ngoài allow-list capability của thiết bị.

## 1.0.10

- Bổ sung nhận diện DEEBOT T10 OMNI theo `company` và `deviceName` mà Ecovacs
  công bố, bao gồm các biến thể OMNI/OMNIWHITE/CURIEOMNI Trung Quốc và quốc tế.
- Áp dụng profile DT10/X1 OMNI bảo thủ cho T10 OMNI: giữ lệnh dọn legacy tương
  thích, đồng thời bổ sung capability trạm OMNI, hút rác, giặt/sấy giẻ, nhiều
  bản đồ và ba mức nước khi thiết bị quảng bá hỗ trợ.
- Token mới có tiền tố `ecv1_`; giao diện tự xác minh token vừa tạo trước khi
  hiển thị và có phương án sao chép dự phòng cho trình duyệt hạn chế clipboard.
- Ghi rõ giá trị 16 ký tự trong danh sách chỉ là ID quản lý để thu hồi token,
  không phải API token; custom integration báo lỗi riêng khi người dùng nhập
  nhầm ID hoặc hash token.

## 1.0.9

- Sửa custom integration không kết nối lại được khi hostname nội bộ của add-on
  thay đổi sau khi cài lại, đổi repository hoặc nâng cấp Supervisor.
- Luôn thử URL đã lưu trước, sau đó tự lấy toàn bộ hostname khả dụng từ
  Supervisor, lưu lại URL hoạt động và tự retry khi add-on khởi động chậm.
- Chuẩn hóa khoảng trắng khi sao chép API token và nâng config-entry migration
  lên phiên bản 4 để sửa cả các entry `1.0.8` đã lưu URL không còn hợp lệ.

## 1.0.8

- Sửa URL local mặc định từ hostname không tồn tại sang
  `http://local-ecovacs-cn-backend:4545` theo slug Supervisor thực tế.
- Custom integration tự tìm add-on qua Supervisor API, đọc hostname chính xác
  cho cả local add-on và add-on cài từ repository.
- Tự migration config entry cũ và tự chuẩn hóa URL legacy, không cần nhập lại
  Ecovacs credential; API token vẫn là dữ liệu xác thực duy nhất của custom.

## 1.0.7

- Cho phép mật khẩu quản trị add-on từ 4 ký tự để khách có thể dùng PIN 4 số;
  vẫn giữ scrypt, giới hạn thử sai và thu hồi token khi đổi mật khẩu.
- Làm mới toàn bộ giao diện add-on theo dạng dashboard responsive, không thêm
  framework hoặc dependency frontend nên không tăng tải tiến trình Python.
- Thêm trạng thái cloud/robot/token, làm mới thủ công, sao chép và thu hồi token,
  tab đăng nhập rõ ràng cùng thông báo lỗi tiếng Việt dễ hiểu hơn.

## 1.0.6

- Cài `addon_app` và protocol trực tiếp vào Python `site-packages`, cùng vị trí
  với `aiohttp` và `deebot-client`, thay vì import package từ `/app`.
- Bỏ hoàn toàn `PYTHONPATH`, `sys.path.insert` và quyền AppArmor `/app`; launcher
  dùng import Python tiêu chuẩn từ package đã cài trong image.
- Cho phép đọc và memory-map riêng vùng Python `site-packages` để các module
  native của `aiohttp`, `cryptography` và dependency có thể nạp dưới AppArmor.
- Docker build tiếp tục import-test package ở đúng đường dẫn runtime trước khi
  tạo image.

## 1.0.5

- Sửa AppArmor cấp quyền đọc chính thư mục `/app/` và các package con, tránh
  Python thấy file trực tiếp nhưng không thể resolve package `addon_app`.
- Thêm import self-test trong Docker build để image không thể build thành công
  nếu thiếu `addon_app` hoặc protocol source.
- Bỏ mã khởi tạo khỏi README, DOCS và giao diện; add-on chỉ lưu digest kiểm tra
  thay vì chuỗi plaintext trong runtime source được đóng gói.

## 1.0.4

- Tách năm module giao thức vào `protocol_components` của add-on để Docker build
  local không còn phụ thuộc thư mục `custom_components` bên ngoài.
- Thêm giá trị mặc định `BUILD_ARCH=amd64`, loại cảnh báo base image rỗng khi
  kiểm tra Dockerfile ngoài Supervisor.
- Giảm tải mặc định: map và custom local polling mỗi 10 giây, refresh trạng thái
  đầy đủ mỗi 30 giây; cho phép chỉnh interval trong options.

## 1.0.3

- Đặt `PYTHONPATH=/app` trực tiếp trong Docker image và launcher để không phụ
  thuộc working directory do s6 chọn.
- Launcher kiểm tra `/app/addon_app/server.py`, in rõ phiên bản `1.0.3` và báo
  lỗi yêu cầu rebuild nếu image cũ/thiếu file vẫn đang được dùng.
- Khởi chạy backend bằng import tuyệt đối sau khi chèn `/app` vào `sys.path`,
  tránh hoàn toàn lỗi tìm module từ `python -m`.

## 1.0.2

- Sửa s6 chạy legacy service từ `/` làm Python không tìm thấy package
  `addon_app` dù Dockerfile đã đặt `WORKDIR /app`.
- Cố định `PYTHONPATH=/app` và chuyển working directory sang `/app` ngay trong
  `run.sh` trước khi chạy backend.

## 1.0.1

- Sửa AppArmor chặn `/init`, khiến base image s6-overlay dừng với lỗi
  `can't open '/init': Permission denied`.
- Cho phép các đường dẫn runtime tối thiểu của s6 (`/package`, `/command`,
  `/etc/s6-overlay`, `/run`) nhưng tiếp tục chặn truy cập `/home` và `/root`.
- Ghim image Python 3.14 trực tiếp trong `Dockerfile` bằng `BUILD_ARCH`, không
  còn phụ thuộc việc Supervisor đọc `build.yaml`.

## 1.0.0

- Tách toàn bộ đăng nhập Ecovacs China, cloud REST, MQTT, map, sensor state và
  command sang Home Assistant add-on chạy cổng nội bộ `4545`.
- Thêm giao diện Ingress để khởi tạo bằng mã một lần, bắt buộc
  đổi sang mật khẩu quản trị mới, đăng nhập Ecovacs ID/điện thoại/SMS và tạo API
  token riêng cho từng máy khách.
- Mã hóa Ecovacs credential trong `/data` bằng AES-GCM; dùng scrypt cho mật khẩu
  add-on, token ngẫu nhiên có thể thu hồi, rate-limit, audit log, CSP và AppArmor.
- Refactor custom integration thành local-polling client không có Ecovacs
  credential/dependency cloud; chỉ tạo sensor, ảnh bản đồ SVG và button do
  add-on quảng bá.
- Không thêm master password hoặc backdoor. Đổi mật khẩu sẽ thu hồi token cũ;
  không cam kết DRM ngăn sao chép bởi người có toàn quyền hệ thống.

## 0.7.0

- Thêm profile xác minh cho DEEBOT T9 POWER nội địa class `dj8zpr`, dựa trên
  profile T9 gần nhất của `deebot-client` nhưng chỉ kích hoạt khi `company` và
  `class` bất biến khớp chính xác.
- Khớp cấu hình sản phẩm `dt9_CN`: ba mức nước, một/hai lượt dọn, vật tư bộ tạo
  hương, trạng thái/tự động cập nhật OTA và các capability bản đồ/lịch đã có.
- Thêm switch không làm phiền, hai time entity bắt đầu/kết thúc bằng
  `getBlock`/`setBlock`, cùng select kiểu lau tiêu chuẩn/lau sâu qua
  `setWaterInfo.sweepType`.
- Mở panel entity, bản đồ và lịch dọn cho T9 POWER; ẩn YIKO/AIVI và chặn cả
  backend WebSocket khi model không có feature tương ứng.
- Nâng tên integration, cache key panel, kiểm thử và gói phát hành lên `0.7.0`.

## 0.6.1

- Thêm phương thức đăng nhập bằng Ecovacs ID và mật khẩu qua endpoint
  `user/login` của ứng dụng Ecovacs Home 3.14.0.
- Mật khẩu Ecovacs ID được mã hóa RSA bằng public key động; ID và thông tin xác
  thực được che khỏi diagnostics/log.
- Thêm cấu hình ban đầu, reauthentication, bản dịch Việt/Anh và kiểm thử giao
  thức cho đăng nhập Ecovacs ID.
- Tách bước chọn phương thức khỏi biểu mẫu số điện thoại để giao diện không yêu
  cầu mã vùng khi người dùng chọn Ecovacs ID.
- Nâng cache key panel và gói phát hành lên `0.6.1`.

## 0.6.0

- Sửa tường ảo không tải khi robot trả danh sách `subsets` rỗng hợp lệ; không
  còn chờ sự kiện không bao giờ được thư viện phát.
- Tải đa giác tọa độ và tên phòng từ map-set X1, hỗ trợ cả định dạng tọa độ
  ngăn cách bằng dấu chấm phẩy.
- Nâng trình sửa lịch thành bản đồ chọn phòng trực tiếp: hiện tên trên từng
  vùng, chạm để chọn/bỏ chọn, đồng bộ với danh sách phòng và vẫn có fallback khi
  firmware không trả đa giác.
- Khớp AIVI với app 3.14.0: bật audio/video mặc định, ưu tiên H.264, gửi offer
  ngay để trickle ICE, lọc candidate loopback/TCP, báo `connected`/`closed` qua
  endpoint ICE event và sửa payload đóng phiên.
- Nâng cache key panel lên 0.6.0 và mở rộng kiểm thử offline.

## 0.5.0

- Thêm trang **Thực thể** trong panel: gom toàn bộ sensor, binary sensor, switch,
  select, number, button, vacuum, image và event; hiển thị tên/trạng thái tiếng
  Việt, thuộc tính và control phù hợp. Entity đang tắt trong registry vẫn được
  liệt kê.
- Thay trình sửa lịch JSON bằng biểu mẫu chọn giờ, lịch một lần/từng ngày và
  toàn bộ nhà/từng phòng. Các trường riêng của firmware vẫn được bảo toàn trong
  mục JSON nâng cao; backend kiểm tra giờ và giới hạn kích thước trước khi gửi.
- Sửa trình vẽ bản đồ không mở bằng cách chuyển SVG hiện có qua WebSocket quản
  trị đã xác thực rồi tạo ảnh Blob trong trình duyệt. Không còn phụ thuộc việc
  JavaScript có đọc được URL ảnh entity của Home Assistant hay không.
- Hoàn thiện AIVI signaling: sửa parser MQTT thiếu `NAME`, nhận các envelope JSON
  lồng nhau, alias session/answer/candidate, định tuyến event thiếu session cho
  đúng robot và chuẩn hoá STUN/TURN cho trình duyệt.
- Thêm chẩn đoán bốn bước AIVI, gom ICE candidate vào offer, cho phép bật âm
  thanh nhưng mặc định chỉ nhận video để tương thích X1 nội địa tốt hơn.
- Nâng cache key panel lên 0.5.0 và mở rộng kiểm thử offline lên 52 bài.

## 0.4.0

- Thêm đổi tên phòng từ danh sách phòng trên bản đồ bằng payload
  `setMapSet_V2`/`act: rename` đã truy từ module `multimap_v3` của app 3.14.0.
- Thêm chia phòng trực tiếp trên ảnh bản đồ: chọn phòng, kéo đường cắt hai điểm
  và gửi `setMapSet_V2`/`act: divide` với đúng hệ toạ độ robot.
- Sửa payload gộp phòng: `subsets` nay là danh sách object `mssid` giống app,
  thay cho mảng số.
- Bổ sung kiểm tra mã phòng, tên tối đa 16 ký tự, đường chia hữu hạn/khác điểm
  và đọc metadata phòng hiện tại trước mọi lệnh đổi tên/chia.
- Giữ nguyên `grpcio`/`protobuf` tương thích Home Assistant 2026.7 và đổi cache
  key panel lên 0.4.0.

## 0.3.1

- Sửa lỗi Home Assistant không nạp được integration với thông báo
  `RequirementsNotFound: grpcio==1.82.1`.
- Đồng bộ `grpcio==1.78.0` và `protobuf==6.32.0` với package constraints chính
  thức của Home Assistant 2026.7/Python 3.14.
- Đổi cache key của JavaScript panel để trình duyệt tải đúng bản đã sửa.

## 0.3.0

- Thêm panel quản trị **Ecovacs nâng cao** trong thanh bên Home Assistant với
  giao diện tiếng Việt và WebSocket API chỉ dành cho quản trị viên.
- Thêm đọc, bật/tắt và chỉnh sửa nguyên object lịch dọn `getSched_V2` /
  `setSched_V2`.
- Thêm hiển thị, vẽ và xoá tường ảo/vùng cấm lau trên ảnh bản đồ SVG; chuẩn hoá
  góc xoay và hệ toạ độ của X1 Omni trước khi gửi lệnh.
- Thêm gộp phòng theo mã với hộp xác nhận bắt buộc. Đổi tên/chia phòng vẫn bị
  khoá cho tới khi xác minh được payload firmware nội địa.
- Thêm YIKO dạng chữ và phản hồi NLP/TTS qua gRPC Trung Quốc; token Ecovacs chỉ
  nằm trong backend và không được trả về trình duyệt.
- Thêm phiên AIVI WebRTC thử nghiệm, báo hiệu qua API/MQTT Ecovacs, chỉ mở sau
  thao tác rõ ràng của quản trị viên và không ghi hình.
- Thêm kiểm tra payload nguy hiểm, giới hạn đầu vào, xác nhận thao tác và kiểm
  thử offline cho lịch, bản đồ, protobuf YIKO và JavaScript panel.

## 0.2.0

- Thêm profile chính xác cho class `8bja83` của DEEBOT X1 OMNI nội địa
  (model DEX11/T10 Omni) dựa trên capability đọc trực tiếp từ thiết bị thật.
- Chuyển trạng thái và lệnh dọn sang giao thức `clean_V2`; nhận đúng trạng thái
  robot đang ở trạm trong lúc sấy/hút rác.
- Thêm chế độ tiết kiệm năng lượng, xoay sát mép, chỉ lau, lưu nhiều bản đồ,
  trạng thái firmware và công tắc tự động cập nhật firmware.
- Bật mặc định các setting hữu ích đã được thiết bị xác nhận như âm lượng, số
  lượt dọn, TrueDetect, tiếp tục dọn và cảnh báo lỗi.
- Loại bỏ work mode, trợ lý giọng nói và tần suất tự giặt giẻ khỏi profile này
  vì firmware nội địa trả về không hỗ trợ hoặc bị giới hạn.
- Hoàn thiện bản dịch tiếng Việt cho toàn bộ entity, trạng thái và thuộc tính.

## 0.1.1

- Bổ sung cập nhật bù cho bản đồ X1 nội địa khi robot đang dọn hoặc về trạm.
- Làm mới vị trí mỗi 5 giây và chỉ lấy phần đường đi mới mỗi 10 giây để giảm tải
  cho Ecovacs cloud.
- Làm mới bản đồ lần cuối khi robot dừng để giữ đúng vị trí và đường đi cuối.

## 0.1.0

- Thêm đăng nhập tài khoản Trung Quốc bằng số điện thoại + SMS quick login.
- Thêm chế độ mật khẩu và reauthentication.
- Lưu client device ID cố định, hỗ trợ lỗi xác minh thiết bị `1013`.
- Tái sử dụng entity/map/vacuum hiện tại của Home Assistant.
- Bổ sung profile X1 Omni: 4 work mode, child lock, auto-empty và 4 nút trạm.
- Thêm diagnostics đã khử dữ liệu nhạy cảm và bản dịch Việt/Anh.

# Ecovacs đa vùng Backend cho Home Assistant

Ecovacs Backend `1.3.5` là add-on điều khiển robot từ nhiều tài khoản Ecovacs
China và quốc tế cùng lúc, sau đó đưa entity vào Home Assistant trực tiếp bằng
MQTT Discovery. Không cần cài custom component hoặc nhập cloud credential vào
Home Assistant Core.

Đây không phải phần mềm chính thức của Ecovacs.

## Cài đặt nhanh từ kho Add-on

1. Mở **Cài đặt → Add-ons → Add-on Store** trong Home Assistant.
2. Bấm menu **⋮** ở góc phải, chọn **Repositories**.
3. Dán địa chỉ kho add-on sau vào ô repository:

   `https://github.com/trankhanhduy2929-beep/my_hass_addon_public`

4. Bấm **Add** rồi đóng cửa sổ quản lý repository.
5. Tìm **Ecovacs China Backend** trong Add-on Store, mở add-on và bấm
   **Install**.
6. Sau khi cài xong, bấm **Start**. Có thể bật **Show in sidebar** rồi chọn
   **Open Web UI** để mở giao diện add-on.
7. Làm theo mục **Kích hoạt lần đầu** bên dưới để nhập license key, cấu hình
   MQTT và đăng nhập tài khoản Ecovacs.

> Nếu không thấy add-on sau khi thêm repository, hãy bấm **Reload** trong
> Add-on Store rồi tìm lại `Ecovacs China Backend`.

## Kiến trúc

```text
Ecovacs China/international cloud + MQTT
            │
            ▼
Ecovacs Backend add-on :4545
  ├─ kích hoạt bằng license key gắn Installation ID
  ├─ đăng nhập và lưu credential mã hóa
  ├─ nhận trạng thái robot từ Ecovacs MQTT
  ├─ đánh dấu map mới, chỉ dựng SVG khi cần
  ├─ kiểm tra và thực thi lệnh
  └─ batch/cache MQTT, chỉ publish robot và giá trị đổi
            │ MQTT Discovery + retained state
            ▼
Home Assistant MQTT integration
  ├─ vacuum / lawn_mower
  ├─ sensor / setting
  ├─ image bản đồ
  └─ button/action
```

## Tính năng

### License và truy cập Ingress

- Cài mới không còn yêu cầu mã khởi tạo, PIN hoặc mật khẩu quản trị.
- Add-on hiển thị nút lớn và QR tới portal; `Installation ID` cùng phiên bản được
  gửi và liên kết tự động, người dùng không phải nhập mã thủ công.
- Hỗ trợ trial 1 ngày miễn phí, gói 7 ngày 50.000đ và vĩnh viễn 200.000đ; key
  chỉ dùng cho installation đã liên kết.
- Domain portal được đóng sẵn trong add-on, không có ô nhập địa chỉ portal.
- Phản hồi verify từ portal được ký Ed25519. Đổi URL sang máy chủ giả không thể
  tự tạo phản hồi license hợp lệ.
- License key được lưu AES-256-GCM trong `/data/license`, có backup nguyên tử và
  bản recovery độc lập trong `/data/license_recovery`; backend và MQTT chỉ chạy
  khi key đang hợp lệ. Mất kết nối portal tạm thời có grace tối đa 72 giờ.
- Khi nâng cấp, add-on giữ Installation ID, tự phục hồi key từ recovery và có
  thể nhận lại ID từng dùng bởi bản `1.3.0–1.3.1` từ MQTT Discovery mà không yêu
  cầu người dùng nhập lại key.
- Ingress tự nhận phiên ngắn hạn. Home Assistant nhận entity trực tiếp qua MQTT
  Discovery và không gọi API quản trị của add-on.

### Đăng nhập Ecovacs trong add-on

- Chạy đồng thời nhiều tài khoản; mỗi tài khoản có cloud controller, Ecovacs
  MQTT và vòng reconnect riêng.
- Tài khoản China: Ecovacs ID + mật khẩu, số điện thoại + mật khẩu hoặc SMS.
- Tài khoản quốc tế: Ecovacs ID/email + mật khẩu và mã quốc gia ISO 2 ký tự như
  `VN`, `US`, `DE`; tài khoản China vẫn dùng tab China riêng.
- Khi Ecovacs yêu cầu xác minh thiết bị mới, add-on tự gửi mã tới email và hiện
  form nhập mã ngay trong Ingress; không cần đăng nhập lại từ đầu.
- Địa chỉ Gmail được hỗ trợ như email Ecovacs. Add-on không dùng Google OAuth;
  tài khoản chỉ tạo bằng **Đăng nhập bằng Google** phải đặt/reset mật khẩu
  Ecovacs trong ứng dụng trước.
- Số điện thoại Trung Quốc nhập nhầm ở tab Ecovacs ID được tự chuyển sang
  luồng điện thoại, không làm thay đổi cách xử lý ID thông thường.
- Tự migration tài khoản China của bản cũ, giữ nguyên device ID và dữ liệu đã
  lưu để entity không bị đổi sau khi nâng cấp.
- Lưu credential mã hóa để tự kết nối lại sau khi khởi động add-on.
- Kết nối lại hoặc xóa từng tài khoản; vẫn có nút thao tác tất cả tài khoản.
- Sau khi credential được cloud xác thực, API trả ngay với trạng thái **Đang
  kết nối**; MQTT realtime và tải robot tiếp tục chạy nền, tránh form chờ tới
  timeout rồi người dùng đăng nhập lặp lại.
- Các tài khoản kết nối cloud song song thay vì chờ tuần tự. Add-on bỏ lần MQTT
  handshake kiểm tra trùng trước khi mở kết nối realtime chính.
- Subscription gặp `Operation timed out` được giữ trong hàng đợi và tự thử lại
  sau reconnect, không còn mất đăng ký robot giữa chừng.

### Sensor trạng thái

Tùy capability robot thực tế cung cấp, add-on có thể tạo qua MQTT Discovery:

- trạng thái online/offline, pin và trạng thái làm việc;
- mã lỗi và mô tả lỗi;
- diện tích, thời gian và tổng số lượt dọn;
- cường độ Wi-Fi và địa chỉ IP;
- lực hút, mức nước, tình trạng gắn giẻ và chế độ lau;
- trạng thái trạm sạc/trạm Omni;
- khu vực/phòng robot đang dọn, kèm ID phòng và danh sách phòng đã chọn;
- phiên bản, trạng thái và tự động cập nhật firmware;
- phần trăm và thời gian còn lại của chổi, lọc, chổi cạnh và vật tư khác;
- trạng thái không làm phiền trên profile T9 POWER tương thích.

### Bản đồ

- Hiển thị bản đồ robot dưới dạng ảnh SVG.
- Entity bản đồ luôn được tạo khi robot quảng bá capability map, kể cả lúc SVG
  đầu tiên chưa tải xong.
- Cache bản đồ trong add-on; Home Assistant chỉ nhận SVG đã dựng xong.
- Theo dõi revision và tên bản đồ.
- Ingress không còn tải bản đồ chọn phòng vì nhiều firmware X1/T10 chỉ trả ID,
  không trả ranh giới hoặc tâm phòng đủ tin cậy.
- Ingress vẫn có mục **Đặt tên khu vực** dạng danh sách `room ID + tên`; tên
  được lưu mã hóa theo robot/map và không bị mất khi add-on khởi động lại.
- Mỗi khu vực được đưa lên Home Assistant thành MQTT button **Dọn [tên khu
  vực]**; đổi tên chỉ cập nhật nhãn, unique ID của entity vẫn giữ nguyên.
- X1/X1 PRO/T10 không bị gọi lại `getMapSubSet`: add-on lấy ID phòng và đa giác
  nhúng sẵn từ `getMapSet`; firmware chỉ trả ID vẫn có nút **Khu vực N** để dọn
  riêng.
- Với X1/T10 dùng bản đồ mới, add-on đọc thêm `getMapSet_V2` giống app China để
  lấy tên phòng và dữ liệu khu vực mà không gọi lệnh subset dễ timeout.
- Sensor **Khu vực đang dọn** ghép `CleanInfo_V2.content.value` với `areaSts`;
  giá trị trạng thái `1` xác định đúng phòng robot đang xử lý. Firmware không
  có `areaSts` sẽ fallback về danh sách phòng đã chọn.
- Khi robot di chuyển, event map từ Ecovacs chỉ đánh dấu revision mới. SVG được
  dựng lười khi MQTT hoặc API thật sự cần và chỉ phát bản mới nhất theo giới hạn
  `mqtt_map_min_interval`.
- Add-on chỉ theo dõi vị trí/đường đi khi robot đang `cleaning` hoặc `returning`.
  Khi robot dừng, tạm dừng hoặc đã về trạm, add-on lấy một bản đồ cuối trong 3
  giây rồi bỏ các event vị trí rung nhẹ, tránh MQTT image cập nhật liên tục.
- Event bản đồ tĩnh như mảnh nền, map info và khu vực vẫn được xử lý ở trạng
  thái docked nên đổi bản đồ/phòng không bị bỏ sót.
- Fallback 5 giây chỉ yêu cầu vị trí và đường đi động khi robot đang hoạt động,
  không tải lại các mảnh nền tĩnh; MQTT map mặc định phát tối đa mỗi 5 giây.

### Realtime và tải Home Assistant

- Mỗi sensor/control có topic riêng và cache payload riêng. Giá trị giống hệt
  lần trước không được publish lại.
- Event thay đổi được gom trong cửa sổ 350 ms; bridge chỉ đọc/publish robot có
  ID nằm trong batch thay vì quét lại toàn bộ robot.
- MQTT Discovery được cache theo cấu trúc entity. Thay đổi pin, trạng thái hoặc
  sensor value không dựng lại payload Discovery.
- Vacuum entity không publish state `error`: bridge giữ trạng thái hợp lệ cuối
  cùng, hoặc dùng `idle` nếu vừa restart. Sensor **Lỗi** và **Trạng thái** vẫn
  giữ dữ liệu lỗi để chẩn đoán mà không làm rối automation dùng vacuum entity.
- Discovery, state và availability được retain để Home Assistant phục hồi nhanh
  sau khi Core hoặc broker khởi động lại.
- Map dùng topic riêng nên robot di chuyển không ép toàn bộ sensor/control cập
  nhật; kích thước và tần suất map đều có giới hạn.
- Lỗi broker, DNS hoặc credential MQTT chỉ làm bridge reconnect theo backoff;
  không được ném ngược vào web server, watchdog hoặc Home Assistant Core.
- Backoff MQTT Home Assistant tự về 2 giây sau một phiên kết nối thành công;
  warning mạng/command trùng nội dung chỉ ghi lại mỗi 5 phút để giảm log I/O.
- Watchdog kiểm tra Ecovacs MQTT mỗi 30 giây; lỗi refresh/map của một robot được
  cô lập để không dừng polling và realtime của các robot còn lại.
- Cache map MQTT chỉ giữ digest ngắn thay vì thêm một bản SVG lớn; cache robot
  đã xóa và manifest Discovery không đổi được dọn/không ghi lại xuống đĩa.
- Command MQTT được xử lý tuần tự, giới hạn 4 KiB, bỏ qua retained command và
  tiếp tục đi qua allow-list/type validation của backend.
- Sau login mật khẩu/SMS, add-on chuyển thẳng authenticator đã xác thực sang
  controller thay vì đăng nhập portal lần thứ hai.

### Nút điều khiển

Tùy capability thiết bị, add-on có thể cung cấp:

- bắt đầu, tạm dừng và dừng dọn;
- về trạm và tìm robot;
- hút rác, giặt giẻ, sấy giẻ và vệ sinh đế trạm;
- đặt lại tuổi thọ vật tư;
- chọn lực hút, mức nước và số lượt dọn;
- bật/tắt tự động cập nhật firmware;
- bật/tắt không làm phiền;
- chọn lau tiêu chuẩn/lau sâu trên T9 POWER;
- yêu cầu làm mới trạng thái ngay lập tức.

Các nút chỉ được tạo khi add-on xác nhận robot hỗ trợ capability tương ứng.

### Thực thể vacuum và thiết lập

- Mỗi robot hút bụi có một thực thể `vacuum` chuẩn để bắt đầu, tạm dừng, dừng,
  về trạm, tìm robot và đặt lực hút.
- Các lựa chọn như lực hút, mức nước, work mode, auto-empty và bản đồ đang dùng
  xuất hiện dưới dạng `select`.
- Các thiết lập bật/tắt như khóa trẻ em, nhiều bản đồ, tự động cập nhật firmware
  và các capability tương thích xuất hiện dưới dạng `switch`.
- Số lượt dọn, âm lượng, tần suất tự giặt giẻ hoặc mức nước tùy chỉnh xuất hiện
  dưới dạng `number` khi profile thiết bị có hỗ trợ.
- Trạng thái boolean được đưa vào `binary_sensor`; sensor số/chữ, ảnh bản đồ và
  button trạm/vật tư tiếp tục được tạo đầy đủ từ DTO của add-on.
- Thiết bị GOAT có profile tương thích được tạo thành thực thể `lawn_mower`
  chuẩn với bắt đầu cắt, tạm dừng và về trạm theo capability thực tế.

### Hỗ trợ thiết bị nội địa

- DEEBOT X9 PRO OMNI hỗ trợ trực tiếp class quốc tế `ilt3k8` và hai class nội
  địa `lwmdoj`, `0jv4ti`; class X9 mới có model/tên sản phẩm khớp sẽ dùng profile
  `ilt3k8` đã xác minh.
- X9 PRO có bản đồ/phòng/vị trí, dọn khu vực, bốn mức lực hút, ba work mode, mức
  nước tùy chỉnh `0–50`, tần suất tự giặt giẻ `0–60`, auto-empty, khóa trẻ em,
  firmware, chế độ hiệu suất và các cảm biến tuổi thọ vật tư.
- Nút trạm X9 hiện chỉ gồm hút rác theo capability upstream. Add-on không tự
  quảng bá giặt giẻ, sấy giẻ hoặc vệ sinh đế khi lệnh chưa được xác minh.
- Class `8bja83` của X1 OMNI nội địa được đăng ký vào hardware registry trước
  khi `ApiClient` phân loại thiết bị, kể cả khi cache trước đó từng đánh dấu
  class là không tồn tại. Profile giữ state V2, lệnh dọn và bản đồ nhưng không sinh
  `getMapSubSet` vì firmware không phản hồi lệnh chi tiết subset này. ID phòng
  từ `getMapSet` vẫn dùng được cho chức năng dọn riêng khu vực.
- DEEBOT T10 OMNI được nhận diện tự động từ định danh sản phẩm bất biến của
  Ecovacs, gồm các biến thể OMNI, OMNIWHITE và CURIEOMNI đã xác nhận trong APK.
- Class `hxm494` của T10 OMNI nội địa được đăng ký trực tiếp trong
  `deebot-client`, không còn cảnh báo class chưa được nhận diện.
- T10 OMNI dùng profile DT10/X1 OMNI bảo thủ: giữ lệnh dọn legacy để tránh ép
  thiết bị sang giao thức live V2, không gọi `getWorkMode` và không tiếp tục gọi
  `getMapSubSet` sau map metadata vì firmware `hxm494` không phản hồi hai lệnh
  này; capability trạm OMNI và bản đồ nền vẫn được giữ.
- X1/X1 PRO/T10 OMNI được nhận diện bằng tên sản phẩm hoặc class chưa xác minh
  cũng không quảng bá Work Mode. Chỉ hai class X1 `8onkgl` và `1vxt52` đã xác
  minh còn gọi `getWorkMode`, tránh warning timeout lặp trên firmware bảo thủ.
- T10 Turbo/Newton và model OMNI không cùng dòng không bị nhận nhầm thành T10
  OMNI.
- Với class nội địa chưa có trực tiếp trong `deebot-client`, add-on chuẩn hóa
  vùng `cn`/`ww` trong `UILogicId` và tìm profile quốc tế tương đương từ catalog
  218 profile đã đóng gói.
- DEEBOT và GOAT chưa có cặp khớp chính xác dùng profile nền cùng thế hệ một
  cách bảo thủ để ưu tiên trạng thái realtime và các lệnh cơ bản.
- WINBOT, AIRBOT và thiết bị legacy chưa có protocol tương ứng vẫn xuất hiện
  dưới dạng sensor metadata; add-on không quảng bá lệnh hoặc bản đồ chưa được
  xác minh, và một thiết bị kiểu này không còn làm lỗi đăng nhập cả tài khoản.

### Hỗ trợ tài khoản quốc tế

- Add-on dùng luồng xác thực, REST endpoint và Ecovacs MQTT chuẩn của
  `deebot-client` `18.5.1` theo đúng quốc gia đã nhập.
- Việt Nam dùng mã quốc gia `VN`. Nếu cloud trả yêu cầu xác minh thiết bị mới,
  add-on gửi mã email, giữ phiên xác thực trong RAM và cho phép nhập/gửi lại mã
  trong tab **Quốc tế**.
- Gmail dùng được khi đó là email đăng nhập Ecovacs có mật khẩu Ecovacs. Nút
  **Đăng nhập bằng Google** của ứng dụng Ecovacs là một luồng OAuth riêng và
  không được add-on mô phỏng.
- China và quốc tế dùng chung một add-on nhưng mỗi tài khoản có authenticator,
  controller, MQTT task và reconnect riêng; không cần chạy add-on thứ hai.
- Robot quốc tế có class được thư viện nhận diện sẽ có trạng thái và lệnh theo
  capability thực tế giống luồng chuẩn của Ecovacs.
- Class quốc tế chưa được nhận diện chỉ xuất hiện dạng metadata để tránh áp
  profile/lệnh China sai thiết bị; log class đó có thể dùng để bổ sung sau.
- Nếu cùng một robot xuất hiện trong nhiều tài khoản, snapshot của tài khoản
  được thêm trước sẽ được dùng để tránh tạo entity MQTT trùng DID.

## Yêu cầu

- Home Assistant OS hoặc Supervised có hỗ trợ local add-on/app.
- Một MQTT broker có thể truy cập từ container add-on; có thể dùng broker bên
  ngoài hoặc MQTT service do Supervisor cung cấp.
- Kiến trúc `amd64` hoặc `aarch64`.
- Robot đã được thêm vào đúng vùng tài khoản Ecovacs China hoặc quốc tế.
- Home Assistant có kết nối Internet tới Ecovacs cloud của các vùng đã dùng.
- Python của add-on là `3.14`; Home Assistant Core không cần cài thư viện cloud
  Ecovacs hoặc custom component.

## Cài thủ công từ ZIP

1. Giải nén `ecovacs_cn_addon-repository-v1.3.5.zip`.
2. Chép nguyên thư mục `ecovacs_cn_backend` vào `/addons/`.
3. Mở Add-on Store và chọn **Reload/Check for updates**.
4. Chọn **Ecovacs China Backend** và nhấn **Install/Rebuild**.
5. Kiểm tra trang thông tin phải hiển thị phiên bản `1.3.5`.
6. Khởi động add-on và bật **Show in sidebar** nếu muốn.

Không chép riêng `addon_app` hoặc `protocol_components`. Docker build cần toàn bộ
thư mục `ecovacs_cn_backend`.

## Kích hoạt lần đầu

1. Mở giao diện **Ecovacs Backend** từ thanh bên Home Assistant.
2. Quét QR hoặc bấm nút lớn **Mở trang nhận license**.
3. Đăng nhập portal bằng Google hoặc email. Portal tự liên kết `Installation ID`
   từ add-on; không copy hoặc nhập ID thủ công.
4. Nhận trial/mua gói, copy key và dán vào form **Kích hoạt license**.
5. Sau khi key hợp lệ, cấu hình MQTT và tài khoản Ecovacs trong dashboard.

Không có bước đặt PIN hoặc mật khẩu đăng nhập ban đầu. License key là điều kiện
mở cloud backend và MQTT service.

## Đăng nhập tài khoản Ecovacs

1. Sau khi license hợp lệ, mở dashboard Ingress.
2. Với tài khoản China, chọn **Ecovacs ID**, **Điện thoại** hoặc **SMS**.
3. Với tài khoản quốc tế, chọn **Quốc tế**, nhập mã quốc gia ISO 2 ký tự nơi
   tài khoản đăng ký, Ecovacs ID/email và mật khẩu.
4. Có thể lặp lại để thêm nhiều tài khoản; danh sách bên dưới hiển thị trạng
   thái, vùng và số robot của từng tài khoản.
5. Đợi tài khoản chuyển sang `connected`. Nếu cloud/MQTT lỗi tạm thời, dùng nút
   reconnect của riêng tài khoản đó hoặc **Kết nối lại tất cả**.

Mật khẩu và mã SMS được xóa khỏi form sau khi gửi. Giao diện/API không có chức
năng đọc lại credential Ecovacs đã lưu.

## Kết nối Home Assistant bằng MQTT

1. Mở giao diện **Ingress** của add-on.
2. Trong thẻ **Kết nối MQTT**, điền địa chỉ, cổng, tài khoản và mật khẩu broker.
3. Bật **Dùng TLS** nếu broker yêu cầu TLS, thường là cổng `8883`.
4. Bấm **Lưu và kết nối MQTT**; bridge sẽ kết nối lại ngay.
5. Nếu để trống địa chỉ, add-on thử MQTT service `mqtt:want` của Supervisor.
6. Sau khi đăng nhập Ecovacs, device/entity tự xuất hiện qua MQTT Discovery.
7. Sau khi bản đồ trả room ID, dùng mục **Đặt tên khu vực** trong từng robot để
   đặt tên dễ nhớ. MQTT button sẽ cập nhật thành **Dọn [tên khu vực]**.

Home Assistant nhận entity trực tiếp qua MQTT Discovery, không cần kết nối API
quản trị của add-on. Nếu trước đây đã cài `custom_components/ecovacs_cn`, hãy
xóa integration cũ, xóa thư mục đó rồi restart Home Assistant để tránh entity
trùng.

## Cấu hình hiệu năng

Add-on mặc định ưu tiên tải nhẹ:

- một tiến trình Python;
- một MQTT bridge nền tách lỗi khỏi web server và cloud controller;
- mỗi topic chỉ publish khi payload thực sự thay đổi;
- availability kép cho trạng thái bridge và từng robot;
- reconnect broker theo exponential backoff tối đa 300 giây và reset về 2 giây
  sau khi từng kết nối thành công;
- map chỉ publish bản mới nhất theo interval và giới hạn byte;
- map động fallback 5 giây, state lõi 120 giây, setting 600 giây và chẩn đoán
  1200 giây;
- bản đồ và trạng thái được cache, không tạo tiến trình phụ;
- Ingress poll 15 giây, dừng khi tab ẩn và không tạo request refresh chồng nhau;
- warning mạng lặp được giới hạn theo cửa sổ 5 phút để tránh traceback liên tục;
- không dùng `host_network`, không privileged và không mở cổng host mặc định.

Options:

| Option | Mặc định | Phạm vi | Công dụng |
| --- | ---: | ---: | --- |
| `log_level` | `info` | debug–error | Mức log của backend |
| `map_refresh_interval` | `5` giây | 3–60 | Fallback hỏi vị trí và đường đi khi robot hoạt động |
| `state_refresh_interval` | `120` giây | 15–300 | Fallback trạng thái hoạt động cốt lõi |
| `settings_refresh_interval` | `600` giây | 300–1800 | Làm mới setting ít thay đổi như `border_spin` |
| `diagnostic_refresh_interval` | `1200` giây | 900–3600 | Làm mới IP/Wi-Fi, OTA, tuổi thọ và tổng thống kê |
| `mqtt_enabled` | `true` | true/false | Bật MQTT Discovery bridge |
| `mqtt_map_enabled` | `true` | true/false | Publish ảnh SVG qua MQTT Image |
| `mqtt_map_min_interval` | `5` giây | 1–60 | Khoảng cách tối thiểu giữa hai map publish |
| `mqtt_map_max_bytes` | `2000000` | 64000–10000000 | Bỏ qua map quá lớn để bảo vệ broker/Core |
| `mqtt_batch_window_ms` | `350` ms | 100–2000 | Gom event gần nhau thành một lần publish |

Máy yếu nên dùng map `10–20` giây, setting `900` giây và chẩn đoán `1800` giây.
Không bật debug lâu dài vì log nhiều hơn và có thể tăng I/O.

## Bảo mật và dữ liệu

- Không có mật khẩu/PIN quản trị bắt buộc; Ingress dùng phiên ký ngắn hạn tự cấp.
- License key được lưu mã hóa; phản hồi portal phải có chữ ký Ed25519 hợp lệ.
- Credential Ecovacs được mã hóa AES-256-GCM trong `/data/secrets.enc`.
- MQTT broker credential nhập trong Ingress được mã hóa riêng trong `/data/mqtt`.
- Khóa mã hóa chỉ nằm trong `/data` của installation.
- Form quản trị dùng `sessionStorage`, không dùng `localStorage`.
- API giới hạn body 64 KiB và rate-limit các lần xác thực thất bại.
- Audit log không ghi mật khẩu, SMS code hoặc token đầy đủ.
- AppArmor giới hạn filesystem; `/home` và `/root` bị chặn.
- Cổng `4545/tcp` không ánh xạ ra host theo mặc định.

Không thể chống sao chép tuyệt đối nếu một người có toàn quyền filesystem,
Docker image hoặc backup `/data`. Không mở trực tiếp cổng `4545` ra Internet.

## Sao lưu và cập nhật

- Dữ liệu add-on nằm trong `/data` và được Home Assistant backup cùng add-on.
- Bản `1.3.5` lưu thêm Installation ID dự phòng và một bản license recovery mã
  hóa ngoài thư mục license chính để tự nhận lại key sau restart/nâng cấp.
- Khi cập nhật local add-on, thay toàn bộ thư mục `ecovacs_cn_backend`, chọn
  **Reload** rồi **Rebuild**.
- Không chọn xóa dữ liệu nếu muốn giữ tài khoản, license key và cấu hình MQTT.
- Kiểm tra phiên bản trên trang add-on và dòng launcher trong log sau cập nhật.

## Xử lý lỗi

### Nâng cấp xong bị hỏi license key lại

- Cập nhật lên `1.3.5`; bản này giữ đồng thời `security.json`, Installation ID
  dự phòng, encrypted backup và `/data/license_recovery`.
- Nếu key của bản cũ vẫn còn trong `/data`, add-on tự nhận lại và không cần nhập.
- Nếu `/data/license` đã bị xóa trước khi cài `1.3.5` và chưa từng có recovery,
  dữ liệu key không thể tái tạo từ hash; nhập lại key hiện tại một lần. Các lần
  nâng cấp sau sẽ tự nhận.
- Không bấm **Uninstall** kèm xóa dữ liệu và không xóa thư mục `/data` của add-on.

### Docker báo thiếu protocol file

Phải dùng bản `1.3.5` và chép nguyên thư mục add-on. Trong thư mục phải có:

```text
ecovacs_cn_backend/
├── addon_app/
├── protocol_components/ecovacs_cn/
├── Dockerfile
├── config.yaml
├── icon.png
├── logo.png
└── run.sh
```

### Log không có launcher đúng phiên bản

Home Assistant vẫn đang dùng image cache cũ. Dừng add-on, Reload Add-on Store,
kiểm tra version rồi chọn **Rebuild**.

### `ModuleNotFoundError: addon_app`

Kiểm tra đang dùng `1.3.5`. Bản này cài package trực tiếp vào Python
`site-packages`; Docker build sẽ tự import-test package và không còn phụ thuộc
`PYTHONPATH` hoặc quyền đọc `/app`.

### Add-on kết nối nhưng không có robot

- Kiểm tra robot xuất hiện trong Ecovacs Home đúng vùng tài khoản.
- Tài khoản China dùng ba tab China; tài khoản quốc tế phải dùng tab **Quốc
  tế** và mã quốc gia ISO đúng nơi tài khoản đăng ký.
- Tài khoản Việt Nam dùng `VN`. Nếu Ecovacs gửi mã xác minh thiết bị mới, nhập
  mã trong form xuất hiện ngay trong tab **Quốc tế**.
- Nếu Gmail chỉ đăng nhập được qua nút Google trong ứng dụng, hãy đặt/reset mật
  khẩu Ecovacs trước rồi dùng Gmail + mật khẩu đó; add-on không dùng Google OAuth.
- Chọn reconnect của tài khoản lỗi và xem log cloud/MQTT.
- Robot quốc tế class chưa được `deebot-client` nhận diện chỉ có metadata, chưa
  có vacuum entity/lệnh cho tới khi profile tương ứng được hỗ trợ.
- Không chia sẻ log debug trước khi tự kiểm tra dữ liệu nhạy cảm.

### Ecovacs MQTT báo `Operation timed out`

- Bản `1.3.5` không chờ MQTT hoàn tất trong request đăng nhập và không tạo
  handshake kiểm tra trùng, nên giao diện sẽ trả nhanh sau khi xác thực account.
- MQTT client vẫn retry mỗi 5 giây theo thư viện Ecovacs. Subscription chưa gửi
  xong được giữ lại qua lần reconnect kế tiếp, không cần nhập lại tài khoản.
- Warning có thể xuất hiện khi đường truyền tới broker Ecovacs quốc tế/China bị
  chập chờn, nhưng không còn biến thành `Ecovacs account login failed` chỉ vì
  MQTT realtime đang kết nối chậm.

### MQTT không tạo entity

- Kiểm tra broker và MQTT integration của Home Assistant đang hoạt động.
- Kiểm tra ô **MQTT Home Assistant** trong giao diện add-on.
- Xem log có `MQTT service is unavailable` hoặc lỗi xác thực broker hay không.
- Restart add-on sau khi broker được cài để Supervisor cấp service credential.
- Không cấu hình retained command thủ công; add-on chủ động bỏ qua loại message
  này để tránh lặp lại lệnh cũ sau reconnect.

## Gói phát hành

- Mọi bản build mới được lưu trong thư mục `ket_qua` ở root workspace.
- `ecovacs_cn_addon-repository-v1.3.5.zip`: add-on repository/local build.
- `SHA256SUMS-v1.3.5.txt`: checksum của archive add-on.

Xem thêm hướng dẫn vận hành ngắn trong `DOCS.md` và lịch sử thay đổi trong
`CHANGELOG.md`.

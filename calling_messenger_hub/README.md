# Calling Messenger Hub

Trung tâm gọi, nhắn tin và báo động đa kênh cho Home Assistant. Quản lý Telegram, Discord, Signal, LINE Official Account, Zalo cá nhân và SIM 4G trong cùng một giao diện, dùng chung biểu mẫu gửi tin nhắn, ảnh, voice TTS và dịch vụ cho automation.

## Tính năng

- Gửi tin nhắn, SMS, ảnh và voice TTS qua nhiều dịch vụ.
- Gọi thoại Telegram, SIM 4G và Zalo một chiều; phát TTS khi người nhận nghe máy.
- Gọi lặp hoặc gửi voice TTS lặp làm chuông báo động.
- Trung tâm báo động với chính sách nhiều bước: gọi lần lượt nhiều người, leo thang khi không nghe máy, chống trùng, xác nhận, xử lý, hủy và lưu lịch sử.
- Quản lý nhiều tài khoản, xem trạng thái kênh, cuộc gọi và nhật ký trên một bảng điều khiển.
- Đồng bộ trạng thái và sự kiện theo thời gian thực qua SSE; Home Assistant nhận cuộc gọi, chuông, báo động, SMS/OTP gần như ngay lập tức và tự kết nối lại khi mất luồng.
- Với SIM 4G: hộp thư SMS có tìm kiếm, soạn mới/trả lời trực tiếp; xem nhà mạng, mức sóng, số dư, hạn dùng qua USSD (tự thử lại và fallback SMS số dư) và đọc OTP.
- Với EC20/EC25 hai cổng AT: tách **cổng điều khiển** (AT, USSD, SMS) và **cổng sự kiện** (RING, +CLIP, +CMTI, DTMF) để cuộc gọi không bị chặn khi đang tra USSD; tự fallback về một cổng nếu cổng sự kiện lỗi.
- Tự động hóa SIM: CLIP, lệnh SMS, chuyển OTP, DTMF, cảnh báo mất điện/Internet, nuôi SIM, failover 4G và cảnh báo ngưỡng sức khỏe SIM qua Telegram/Home Assistant.
- Sao lưu và khôi phục tài khoản, phiên đăng nhập, token, lịch sử cảnh báo và cấu hình automation bằng tệp mã hóa AES-256-GCM.
- Điều khiển từ Home Assistant qua custom integration hoặc REST API.

## Kênh hỗ trợ

| Kênh | Tin nhắn | Ảnh | Voice TTS | Gọi | Chuông |
| --- | --- | --- | --- | --- | --- |
| Telegram | Có | Có | Có | Có | Có |
| Discord | Có | Có | Có | Không | Voice lặp |
| Signal | Có | Có | Có | Không | Voice lặp |
| LINE Official Account | Có | URL HTTPS | Không | Không | Không |
| Zalo cá nhân | Có | Có | Có | Một chiều | Không |
| SIM 4G | SMS | Không | Trong cuộc gọi | Có | Có |

## Yêu cầu

- Home Assistant có add-on store, chạy `amd64` hoặc `aarch64`.
- License key còn hạn cho các thao tác gửi, gọi và báo động.
- Telegram: `api_id` và `api_hash` tạo tại <https://my.telegram.org/apps>.
- Discord: token phiên của tài khoản người dùng, không phải bot token. Chỉ nên dùng tài khoản phụ.
- Signal: một signal-cli REST API đã liên kết thiết bị.
- LINE: Messaging API channel access token.
- Zalo: ứng dụng Zalo trên điện thoại để quét QR.
- SIM 4G: module SIMCom A7670C-LANS hoặc Quectel EC20/EC2x, kết nối USB/UART hoặc TCP serial bridge; tắt PIN và dùng SIM đã đăng ký mạng.

## Cài add-on

### Từ repository add-on

1. Settings > Add-ons > Add-on Store.
2. Menu 3 chấm > Repositories.
3. Thêm `https://github.com/trankhanhduy2929-beep/my_hass_addon_private`.
4. Cài **Calling Messenger Hub**, sau đó bấm **Start**.

### Copy thủ công

Copy thư mục `calling_messenger_hub/` vào thư mục add-ons của Home Assistant, bấm **Check for updates**, rồi cài và start add-on.

### Sau khi cài

1. Mở **Open Web UI**. Không cần cấu hình trong tab **Configuration** của add-on.
2. Vào **Cài đặt → License**, nhập license key. Không cần nhập license server/site URL; add-on tự dùng mặc định.
3. Vào **Cài đặt → API token cho custom integration**, sao chép token nếu dùng Home Assistant integration.
4. Trong **Cài đặt → Mặc định add-on**, chỉnh giọng/tốc độ TTS, thời gian chờ và số lần gọi nếu cần.
5. Mở **Tài khoản & kênh** để thêm tài khoản.

## Hướng dẫn sử dụng

### Thêm tài khoản

- **Telegram:** nhập `api_id`, `api_hash`, số điện thoại, OTP và mật khẩu 2FA nếu có.
- **Discord:** dán token phiên và chọn người nhận mặc định nếu cần.
- **Signal:** nhập số E.164 và URL signal-cli REST API.
- **LINE:** nhập channel access token và channel secret nếu dùng webhook.
- **Zalo:** bấm **Thêm Zalo**, quét QR và xác nhận trên điện thoại.
- **SIM 4G:** chọn cổng serial/TCP, dòng module hoặc để tự nhận diện.
  - EC20/EC25 thường dùng `/dev/ttyUSB2`; A7670 dùng `/dev/ttyUSB2` hoặc `/dev/ttyACM0`.
  - SIMCom `1e0e:9011` (A7670): interface `if04` là cổng AT (`ttyUSB2`), interface `if05` là cổng Modem (`ttyUSB3`). Đặt **Cổng điều khiển** là `ttyUSB2` (hoặc `/dev/serial/by-id/...-if04-port0`) và **để trống Cổng sự kiện**; không dùng `ttyUSB3` làm cổng AT.
  - Với EC20/EC25, đặt **Cổng điều khiển** và **Cổng sự kiện** khác nhau nếu firmware tạo hai cổng AT, ví dụ `ttyUSB2` và `ttyUSB3`. Bấm **Quét cổng USB** để xem cổng đang map và gợi ý vai trò. Để trống nếu chỉ có một cổng.
  - Cổng sự kiện đọc URC liên tục; SMS vẫn được đối chiếu định kỳ 30 giây và ngay khi có `+CMTI`. Nếu firmware không route URC riêng, add-on tự quay lại chế độ poll một cổng.
  - Không dùng `/dev/bus/usb/...` cho pyserial. Add-on có thể tự đổi đường dẫn này sang cổng tty, nhưng nên nhập trực tiếp cổng tty.
  - Add-on đã bật `uart: true` và `kernel_modules: true`; tự nạp driver `option`/`usbserial` để EC20/EC25 tạo `/dev/ttyUSB*`. Không cần bật `usb: true` chỉ để gửi AT command.
  - Nếu vẫn báo “chưa tạo cổng tty”, kiểm tra `lsusb` và `ls -l /dev/ttyUSB* /dev/ttyACM*`. Modem ở chế độ chỉ QMI/ECM sẽ không có cổng AT; cần đổi USB composition sang chế độ có serial.

Giao diện có hướng dẫn ngắn cho từng loại tài khoản.

### Theo dõi kết nối SIM

- Trang **SIM & số dư** tự đọc lại trạng thái mô-đun khoảng 2,5 giây một lần, hiển thị thời điểm đồng bộ và độ trễ phản hồi.
- Add-on giữ nhịp kết nối bằng lệnh `AT` mỗi 5 giây và làm mới sóng/nhà mạng mỗi 15 giây khi SIM đang rảnh.
- Khi mất kết nối, add-on đóng cổng cũ, chuyển sang **Đang kết nối lại** và tự thử lại sau 2, 4, 8, 16 rồi tối đa 30 giây; không cần bấm kết nối lại thủ công.
- Trong cuộc gọi, add-on tạm dừng nhịp kiểm tra để không làm gián đoạn thoại.
- Khi tra cứu USSD, add-on tạm tắt IMS nếu module A76XX đang bật (bắt buộc để CUSD không trả `ERROR`) rồi bật lại sau khi tra; gửi lệnh không kèm DCS trước, tự thử lại kèm DCS nếu module trả `ERROR`, chờ phản hồi đến muộn, tự thử lại một lần nếu rỗng, tự kết nối lại nếu cổng serial/TCP mất kết nối giữa chừng và dùng SMS số dư nhận trong 30 phút gần nhất nếu nhà mạng trả kết quả qua SMS. Trạng thái `4` nghĩa là mạng hiện tại không hỗ trợ USSD cho thuê bao; kiểm tra cùng mã trên điện thoại hoặc thử khi SIM bắt được 2G/3G.

### Vận hành và giám sát

- **MQTT Discovery:** mở **Cài đặt → MQTT & Home Assistant**, bật cầu nối, nhập host/port/tài khoản và lưu. Add-on tự công bố cảm biến cho tài khoản online, cuộc gọi đang hoạt động, cảnh báo chưa xác nhận, sức khỏe SIM, bản cập nhật và cường độ sóng từng SIM. Topic mặc định `calling_messenger_hub/#`, discovery prefix `homeassistant`.
- **Prometheus:** scrape `http://<add-on>:3030/metrics`. Endpoint trả `cmh_*` cho uptime, tài khoản, cuộc gọi, cảnh báo, SIM, MQTT và bản cập nhật. `/metrics` không yêu cầu token; chỉ mở cổng 3030 trong LAN tin cậy hoặc đặt sau reverse proxy có xác thực.
- **Sức khỏe SIM:** trang **SIM & số dư** hiển thị badge tổng hợp; mặc định cảnh báo khi SIM offline, dữ liệu cũ quá 15 phút, sóng dưới 25% hoặc hạn dùng còn ≤ 7 ngày. Có thể bật cảnh báo sóng yếu, số dư thấp, sắp hết hạn và mất kết nối với ngưỡng riêng trong **Tự động hóa SIM → Cảnh báo sức khỏe SIM**; gửi qua Telegram và/hoặc action Home Assistant.
- **Kiểm tra cập nhật:** nút trong **Cài đặt** gọi GitHub Releases và báo phiên bản mới; add-on không tự cài đặt.
- **Sự kiện realtime:** integration mở `GET /api/events/stream` để nhận sự kiện qua SSE. Add-on gửi heartbeat mỗi 15 giây; integration tự kết nối lại với backoff 1–30 giây và vẫn dùng polling làm phương án dự phòng.

### Gửi tin nhắn, ảnh và voice

1. Mở tab gửi tin.
2. Chọn tài khoản gửi.
3. Nhập người nhận.
4. Chọn gửi văn bản, ảnh hoặc voice TTS.
5. Bấm gửi.

Với ảnh, có thể dùng URL, tải file lên hoặc chọn file trong `/data/media`. LINE chỉ nhận URL HTTPS công khai.

### SMS trên SIM

1. Mở **SIM 4G**, chọn mô-đun và bấm **Tải hộp thư**.
2. Tìm SMS theo số gửi hoặc nội dung, bấm **Trả lời** để điền số nhận, hoặc nhập số mới và nội dung rồi bấm **Gửi SMS**.
3. SMS gửi đi dùng chính mô-đun SIM đang chọn; tối đa 1.000 ký tự và có thể chia nhiều phần theo chuẩn GSM.

### Tự động hóa SIM

Add-on dùng `SUPERVISOR_TOKEN` với quyền `homeassistant_api` để gọi Home Assistant Core; bấm **Kiểm tra HA** để xác thực token và quyền.

Mở **SIM 4G → Tự động hóa SIM** để cấu hình:

- **CLIP:** gọi action Home Assistant khi có cuộc gọi từ số tin cậy; có thể tự từ chối để tránh cước.
- **Lệnh SMS:** số tin cậy gửi lệnh, add-on gọi action HA và trả lời SMS.
- **OTP:** chuyển mã OTP qua Telegram hoặc đọc trên media player.
- **DTMF:** gán phím 1/2/9 trong cuộc gọi cảnh báo; phím 9 có thể kết thúc cuộc gọi.
- **Mất điện/Internet:** gọi cảnh báo TTS khi entity nguồn tắt hoặc URL Internet lỗi.
- **Nuôi SIM:** gửi SMS hoặc nháy máy định kỳ hằng tháng và tra cứu số dư.
- **Failover 4G:** gọi action HA khi Internet chính lỗi. Việc đổi route/WAN do script hoặc `shell_command` trên host Home Assistant thực hiện.
- **Cảnh báo sức khỏe SIM:** đặt ngưỡng sóng, số dư, ngày hết hạn, thời gian mất kết nối và chống lặp; gửi Telegram, action HA hoặc cả hai. MQTT vẫn công bố `binary_sensor.sim_health` và cảm biến sóng từng SIM.

### Sao lưu và khôi phục

Mở **Cài đặt → Sao lưu & khôi phục**, nhập mật khẩu tối thiểu 8 ký tự rồi tải tệp `.cmhb`. Tệp chứa tài khoản, phiên đăng nhập, token, cấu hình automation, lịch sử cảnh báo và License state; dữ liệu được mã hóa AES-256-GCM bằng khóa PBKDF2-SHA256. Cache TTS và media không được đưa vào bản backup.

Để khôi phục, chọn tệp, nhập đúng mật khẩu và xác nhận. Add-on ghi đè các tệp trùng tên; khởi động lại add-on sau khi hoàn tất. Không có mật khẩu thì không thể giải mã bản backup.

### Gọi và chuông báo động

- **Gọi TTS:** chọn tài khoản, người nhận và lời thoại. Người nhận phải bấm nghe máy thì TTS mới phát.
- **Chuông:** chọn số lần lặp, khoảng nghỉ và thời gian đổ chuông.
- **Kết thúc:** dùng nút kết thúc cuộc gọi hoặc service `hangup`.

Telegram gọi thoại thật. SIM gọi cảnh báo và phát TTS một chiều; add-on không truyền mic/loa. Discord và Signal gửi voice TTS lặp. Zalo đổ chuông và phát TTS một chiều, không nghe mic.

### Trung tâm báo động

1. Mở tab **Báo động**.
2. Bấm **Tạo chính sách**.
3. Đặt tên, mức ưu tiên, lời thoại mặc định và số vòng lặp.
4. Thêm các bước theo thứ tự: chọn dịch vụ, hành động, tài khoản, người nhận và thời gian chờ.
5. Lưu chính sách.

Khi chạy, các bước được thực hiện lần lượt. Bước gọi thất bại hoặc không nghe máy sẽ chuyển sang bước kế tiếp. Có người nghe máy thì báo động được xác nhận và dừng leo thang, trừ khi bật **Vẫn chạy tiếp sau khi nghe máy**.

Có thể kích hoạt, xác nhận, đánh dấu đã xử lý hoặc hủy ngay trong giao diện, hoặc dùng service của integration.

### Lịch sử

Tab báo động hiển thị báo động đang chạy và lịch sử gần đây, gồm các bước đã gọi, trạng thái và người xác nhận.

## Tích hợp Home Assistant

1. HACS > Integrations > Custom repositories.
2. Thêm `https://github.com/trankhanhduy2929-beep/calling_messenger_hub`, category **Integration**.
3. Cài **Calling Messenger Hub** và restart Home Assistant.
4. Settings > Devices & services > Add integration > **Calling Messenger Hub**.
5. Nhập URL add-on và API token.

URL thường dùng:

```text
http://local-calling-messenger-hub:3030
```

Ví dụ automation:

```yaml
action: calling_messenger_hub.trigger_alert
data:
  policy_id: "a1b2c3d4e5"
  source: "automation cua_chinh"
  dedupe_key: "cua-chinh"
```

Integration tạo các sensor:

- `sensor.calling_messenger_hub_accounts_online`
- `sensor.calling_messenger_hub_active_calls`
- `sensor.calling_messenger_hub_alerts_active`
- `sensor.calling_messenger_hub_alerts_unacknowledged`

Các entity bổ sung:

- `binary_sensor`: kết nối API, license, MQTT, sự cố SIM, bản cập nhật.
- `button`: làm mới trạng thái, kiểm tra cập nhật.
- `switch.calling_messenger_hub_mqtt_bridge`: bật/tắt cầu nối MQTT.
- `event.calling_messenger_hub_activity`: cuộc gọi, chuông, báo động, tin nhắn, SMS/OTP, tài khoản, automation và các sự kiện khác. Sự kiện SMS/OTP không chứa nội dung tin nhắn hoặc mã OTP.
- Mỗi tài khoản có `binary_sensor` online riêng; mỗi tài khoản SIM có thêm cảm biến sóng, nhà mạng, số dư và hạn dùng. Entity được thêm hoặc gỡ tự động khi danh sách tài khoản thay đổi.

Gửi thông báo qua notify:

```yaml
action: notify.calling_messenger_hub
data:
  title: "Home Assistant"
  message: "Cửa chính đang mở."
  target:
    - "@username"
  data:
    account: "+84901234567"
```

Danh sách service và ví dụ chi tiết nằm trong README của integration.

## Lưu ý

- Chưa hỗ trợ gọi đồng thời nhiều người. Chính sách báo động gọi lần lượt từng người.
- Telegram chỉ gọi 1:1, không gọi nhóm.
- Discord, Signal, LINE và Zalo không truyền thoại hai chiều.
- SIM gọi TTS, gửi/đọc SMS, gửi USSD và nhận DTMF trong cuộc gọi cảnh báo; không gửi ảnh hoặc TTS như tin nhắn.
- SIM chỉ điều khiển cuộc gọi qua lệnh AT và phát TTS một chiều. Add-on không hỗ trợ truyền mic/loa hai chiều qua thiết bị Home Assistant.
- Edge TTS cần Internet.
- Tự động gọi/nhắn tin có thể vi phạm điều khoản nền tảng và gây cước phí SIM. Chỉ dùng tài khoản bạn sở hữu hoặc tài khoản phụ, và chỉ gửi đến người đã đồng ý.

## Bảo mật

- API token có toàn quyền với add-on; không chia sẻ hoặc đưa vào file công khai.
- Token, phiên đăng nhập và danh sách tài khoản được lưu trong `/data` với quyền hạn chế.
- Không công khai log, ảnh chụp bảng điều khiển hoặc bản backup Home Assistant. Bản backup `.cmhb` chứa token và phiên đăng nhập; dù đã mã hóa, vẫn phải lưu ở nơi an toàn và dùng mật khẩu mạnh.
- Nếu không cần truy cập trực tiếp, không publish port `3030`.

## License

License key có dạng `CMH-XXXX-XXXX-XXXX-XXXX`. Nhập tại **Cài đặt → License**. Key gắn với một instance add-on; khi cần chuyển sang instance khác, reset liên kết trên trang quản trị license. Add-on cho phép dùng tạm tối đa 72 giờ khi mất mạng.

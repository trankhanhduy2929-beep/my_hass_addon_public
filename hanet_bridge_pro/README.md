# Hanet Bridge Pro

Add-on Home Assistant nhận dữ liệu từ Hanet AI Camera qua MQTT, lưu lịch sử, hiển thị ảnh và tự tạo thiết bị/camera/sensor trong Home Assistant.

Bản `3.3.0` chỉ dùng dữ liệu do camera Hanet gửi. Add-on không tải model, không chạy nhận diện khuôn mặt local và không cần `numpy`, `scipy`, OpenCV hay InsightFace.

## Yêu cầu

- Home Assistant có Add-on Store.
- MQTT broker, ví dụ Mosquitto.
- Camera Hanet đã cấu hình gửi dữ liệu lên cùng MQTT broker.
- License Key của Hanet License. Có thể dùng thử 1 ngày, mua gói 1 tháng hoặc vĩnh viễn tại <https://hanet-license.vercel.app>.

## Cài đặt

1. Mở Home Assistant qua Samba Share, File Editor hoặc Studio Code Server.
2. Tạo thư mục `addons/hanet_bridge_pro`.
3. Copy các file sau vào thư mục đó:
   - `bridge.py`
   - `license_manager.py`
   - `Dockerfile`
   - `config.yaml`
   - `icon.png`
   - thư mục `static/` (Bootstrap, Font Awesome và Inter dùng offline)
4. Vào **Settings > Add-ons > Add-on Store**.
5. Mở menu ba chấm, chọn **Check for updates**.
6. Trong **Local Add-ons**, mở **Hanet Camera Bridge Pro** và chọn **Install**.
7. Bật **Start on boot** và **Watchdog**, sau đó bấm **Start**.
8. Bấm **Open Web UI** để mở giao diện add-on.

Lần build đầu chỉ cài Flask, paho-mqtt và cryptography nên nhanh hơn các bản có AI local. Web UI chỉ truy cập qua ingress của Home Assistant; add-on không publish port `2900` trực tiếp ra host.

## Cấu hình

Cấu hình được lưu trong add-on, không cần sửa `config.yaml` sau khi cài.

1. Mở Web UI.
2. Vào **License**, nhập License Key và bấm **Kích hoạt**. Nếu chưa có key, bấm **Mua License Key**.
3. Vào **Cài đặt**, nhập:
   - MQTT Host
   - MQTT Port, mặc định `1883`
   - MQTT Username và Password nếu broker yêu cầu
   - Bật **MQTT over TLS** nếu broker dùng cổng `8883`; có thể trỏ CA certificate tới tệp trong `/share`
   - Hanet Topic, mặc định `/topic/detected/#`
   - Số ngày lưu lịch sử, `0` là lưu vĩnh viễn
   - Tên hiển thị cho từng camera
4. Bấm **Lưu cấu hình**. Add-on tự kết nối lại MQTT, không cần khởi động lại.
5. Dùng **Sao lưu / phục hồi** trong trang Cài đặt để tải hoặc phục hồi cấu hình JSON. Tệp backup chứa mật khẩu MQTT, hãy cất giữ cẩn thận.

Có thể đổi website license trong phần Configuration của add-on qua tùy chọn `license_portal_url`.

## Dữ liệu và Home Assistant

Add-on tự gửi MQTT Discovery cho từng camera:

- `binary_sensor.hanet_<device>_motion`
- `camera.hanet_<device>_image`
- `sensor.hanet_<device>_name`
- `sensor.hanet_<device>_type`
- `sensor.hanet_<device>_time`

Topic trạng thái:

```text
hanet_bridge/DEVICE_ID/state
```

Payload:

```json
{
  "person_name": "Nguyễn Văn A",
  "person_id": "12345",
  "person_type": "Gia đình",
  "event_code": "0",
  "timestamp": "08:30:15 27/10/2026"
}
```

Giá trị `person_type`:

- `Gia đình`
- `Người quen`
- `Người lạ`

Add-on chỉ xử lý sự kiện FaceID (`0`, `1`, `2`, `FACE`, `CHECKIN`, `PERSON` hoặc sự kiện có `person_id`). Sự kiện cảnh báo/chuyển động/khác như `3`, `4`, `25`, `ALARM`, `HUMAN`, `OTHER` bị bỏ qua. Thời gian và `person_id` được lấy từ payload camera khi có; sự kiện trùng trong 30 giây bị loại.

Ảnh mới nhất được gửi tại:

```text
hanet_bridge/DEVICE_ID/image
```

Motion tự tắt sau 5 giây.

## Automation mẫu

Chào mừng người nhà:

```yaml
alias: "Hanet - Chào mừng về nhà"
triggers:
  - trigger: mqtt
    topic: "hanet_bridge/DEVICE_ID/state"
conditions:
  - condition: template
    value_template: "{{ trigger.payload_json.person_type in ['Gia đình', 'Người quen'] }}"
actions:
  - action: tts.google_translate_say
    data:
      entity_id: media_player.google_home
      message: "Chào mừng {{ trigger.payload_json.person_name }} đã về nhà."
mode: single
```

Cảnh báo người lạ kèm ảnh:

```yaml
alias: "Hanet - Cảnh báo người lạ"
triggers:
  - trigger: mqtt
    topic: "hanet_bridge/DEVICE_ID/state"
conditions:
  - condition: template
    value_template: "{{ trigger.payload_json.person_type == 'Người lạ' }}"
actions:
  - action: notify.mobile_app_iphone
    data:
      message: "Phát hiện người lạ tại cửa!"
      data:
        image: "/api/camera_proxy/camera.hanet_DEVICE_ID_image"
mode: single
```

Bật đèn khi có chuyển động:

```yaml
alias: "Hanet - Bật đèn khi có chuyển động"
triggers:
  - trigger: state
    entity_id: binary_sensor.hanet_DEVICE_ID_motion
    to: "on"
actions:
  - action: light.turn_on
    target:
      entity_id: light.hanh_lang
mode: single
```

Thay `DEVICE_ID` bằng ID camera thực tế trong entity hoặc topic.

## License

Mỗi key gắn với một thiết bị Home Assistant tại một thời điểm.

- Dùng thử: 1 ngày, miễn phí.
- Gói 1 tháng: 50.000đ.
- Gói vĩnh viễn: 200.000đ.

License được kiểm tra định kỳ qua internet. Khi mất kết nối tạm thời, add-on dùng cache tối đa 72 giờ. Khi đổi thiết bị, liên hệ quản trị viên Hanet License để reset thiết bị rồi kích hoạt lại.

> Hanet License là dịch vụ độc lập cấp phép cho add-on Hanet Bridge Pro, không phải sản phẩm, chi nhánh hoặc đại diện chính thức của Hanet. Tên "Hanet" và các nhãn hiệu liên quan thuộc quyền của chủ sở hữu tương ứng.

## Xử lý sự cố

### Không thấy camera hoặc sensor

- Kiểm tra MQTT Host, Port, Username, Password.
- Kiểm tra Hanet Topic đúng với cấu hình camera.
- Xem log add-on để tìm lỗi kết nối MQTT.
- Kiểm tra Home Assistant đã cấu hình MQTT integration.

### Có ảnh nhưng sai tên hoặc sai loại người

Dữ liệu tên/loại do camera Hanet gửi. Kiểm tra lại danh bạ và cấu hình nhận diện trên camera hoặc hệ thống Hanet.

### MQTT mất kết nối

Add-on tự kết nối lại. Nếu lỗi kéo dài, kiểm tra broker, mạng và thông tin đăng nhập trong **Cài đặt**.

### Watchdog và health check

Add-on có endpoint `/health` và đã cấu hình `watchdog` trong `config.yaml`. Home Assistant sẽ tự khởi động lại add-on nếu endpoint không phản hồi. Endpoint trả trạng thái MQTT và license nhưng không yêu cầu đăng nhập.

### License báo lỗi

- Kiểm tra add-on có truy cập được `https://hanet-license.vercel.app`.
- Kiểm tra key còn hạn và chưa gắn với thiết bị khác.
- Dùng **Installation ID** trong trang License khi cần quản trị viên hỗ trợ reset thiết bị.

## Phạm vi phiên bản 3.3.0

- Chỉ xử lý dữ liệu Hanet qua MQTT.
- Lọc sự kiện FaceID, dùng thời gian/face ID từ payload và chống trùng.
- Có `/health` và watchdog để Home Assistant tự khởi động lại khi cần.
- Đã bỏ Face Compare, model local, training, thêm người và test AI.
- Giữ Dashboard, Lịch sử, Cài đặt, License, MQTT Discovery và lưu ảnh/lịch sử.

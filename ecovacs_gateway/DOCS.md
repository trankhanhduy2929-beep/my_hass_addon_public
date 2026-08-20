# Cài đặt Ecovacs Private Gateway 2.1.0

## Yêu cầu

- Home Assistant có MQTT integration và một broker truy cập được từ add-on;
- tài khoản Ecovacs phù hợp với cloud Trung Quốc/chế độ đã chọn;
- không cần HACS hoặc custom component.

## Cài mới

1. Chép `ecovacs_gateway` vào thư mục local add-ons.
2. Refresh Add-on Store, cài và start add-on.
3. Mở Web UI, đăng nhập bằng mật khẩu khởi tạo và đổi sang mật khẩu riêng.
4. Nhập tài khoản Ecovacs. Credential được lưu mã hóa trong `/data`.
5. Nhập hostname/IP broker, port, username, password và TLS trong mục
   **Home Assistant MQTT trực tiếp**.
6. Giữ discovery prefix `homeassistant` nếu MQTT integration dùng mặc định.
7. Sau khi trạng thái HA MQTT là `connected`, robot và entity tự xuất hiện.

Với Mosquitto add-on chuẩn, hostname nội bộ thường là `core-mosquitto` và port
không TLS là `1883`. Không nhập `mqtt://` hoặc đường dẫn URL trong ô hostname.

## Nâng cấp từ bản có custom component

1. Không uninstall add-on để giữ `/data`.
2. Nâng add-on lên `2.1.0` và restart.
3. Xóa config entry `ecovacs_cn_mod` trong **Devices & services**.
4. Xóa `/config/custom_components/ecovacs_cn_mod`, restart Home Assistant.
5. Cấu hình MQTT broker trong Web UI add-on.

## Hoạt động realtime

- mỗi state topic là retained và chỉ publish khi payload đổi;
- dynamic event/control chỉ đánh thức entity phụ thuộc dữ liệu đó;
- map chỉ render/publish ở initial sync hoặc map event, và chỉ khi digest SVG đổi;
- robot MQTT Ecovacs khỏe không poll REST sensor;
- map fallback chỉ chạy khi cleaning/returning, không chạy khi docked/idle;
- bridge kết nối broker ngay khi add-on chạy, không chờ đăng nhập cloud;
- retained telemetry/map dùng QoS 0 và tối đa 4 publish đồng thời;
- reconnect broker bắt đầu sau 1 giây, backoff tối đa 15 giây;
- LWT tự đặt bridge offline nếu container hoặc mạng mất đột ngột.

## Entity và điều khiển mới

- button start/pause/resume/stop/về trạm/tìm robot theo capability;
- select dọn phòng và một button riêng cho từng phòng đã discovery;
- switch/select/number/button nâng cao từ capability graph;
- X1 đã xác nhận có Giặt giẻ, Sấy giẻ, Vệ sinh trạm và Hút rác theo profile;
- telemetry object được tách thành sensor/binary_sensor scalar, tối đa 64 entity
  động mỗi robot; field chứa token/password/secret không bao giờ publish;
- kéo chọn vùng ngay trên bản đồ ingress rồi chọn 1–4 lượt dọn.

Lệnh vùng được gateway đổi từ SVG theo góc xoay hiện tại sang `customArea`
`x1,y1,x2,y2`, kiểm tra số hữu hạn, kích thước tối thiểu và giới hạn tọa độ
trước khi gửi tới robot.

## Broker lỗi

Broker Home Assistant lỗi không làm dừng cloud gateway. Web UI hiển thị lỗi đã
khử credential và worker tự reconnect. Ecovacs telemetry/dashboard/API nội bộ
vẫn hoạt động. Khi broker trở lại, discovery và retained state hiện tại được
đồng bộ một lần, sau đó tiếp tục delta-only.

## Robot chưa có profile

Robot raw vẫn xuất hiện trong snapshot và MQTT device với trạng thái chẩn đoán.
Không phát lệnh typed nếu capability chưa được xác nhận. Khi dependency bổ sung
profile, nâng add-on và rescan là đủ.

## Bảo mật

- credential cloud/MQTT chỉ nằm trong secret box AES-GCM;
- API/status không trả password, username MQTT hoặc cloud token;
- TLS kiểm tra chứng chỉ bằng CA hệ thống;
- command payload giới hạn 8 KiB và timeout 45 giây;
- tối đa bốn command robot chạy đồng thời;
- incoming/outgoing MQTT queue đều có giới hạn.

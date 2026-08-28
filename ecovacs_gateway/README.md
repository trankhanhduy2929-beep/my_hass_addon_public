# Ecovacs Private Gateway – APK Mod 2.1.3

Add-on đa thiết bị cho Ecovacs, xuất trực tiếp Home Assistant MQTT Discovery.
Không cần cài custom component.

## Tính năng

- đăng nhập Ecovacs và lưu credential/app token bằng AES-GCM;
- tự discovery profile, event và control cho nhiều model;
- nhận telemetry Ecovacs MQTT realtime, REST chỉ làm fallback;
- publish riêng từng entity và bỏ mọi payload không đổi;
- publish bản đồ SVG chỉ khi digest thay đổi;
- MQTT LWT, retained discovery/state và reconnect exponential nền;
- kết nối broker ngay khi add-on chạy, không chờ Ecovacs cloud;
- QoS 0 retained và tối đa 4 publish đồng thời để giảm độ trễ có kiểm soát;
- sensor/binary_sensor lồng nhau, button thao tác, room select và room button;
- nút Giặt giẻ/Sấy giẻ/Vệ sinh trạm cho profile X1 đã xác nhận;
- kéo chọn vùng trực tiếp trên bản đồ ingress để gửi lệnh `customArea`;
- queue có giới hạn, event burst coalesce và command concurrency có giới hạn;
- Web UI nhập broker/port/username/password/TLS/prefix;
- dashboard ingress, API chẩn đoán và quick command vẫn chạy trên port `7890`.

## Cài đặt nhanh

1. Chép thư mục này vào local add-ons và cài add-on.
2. Start, mở Web UI và bấm **Liên kết thiết bị & kích hoạt**.
3. Đăng ký/đăng nhập portal; thiết bị được tự liên kết, không cần nhập ID/public
   key. Nhận trial hoặc mua license rồi dán key vào add-on.
4. Sau khi active, nhập tài khoản Ecovacs và broker MQTT Home Assistant.
5. Bật MQTT Discovery trong Home Assistant; entity tự xuất hiện.

Mục **License Ecovacs APK Mod** có link portal riêng `Ecovacs APK Mod`; URL đã
tích hợp trong add-on và tự mang theo installation identity hiện tại. Sau khi
đăng nhập/đăng ký, portal tự chọn đúng thiết bị Home Assistant. Khi chưa active,
add-on không mở dashboard hay gateway;
sau khi active key hợp lệ, toàn bộ chức năng được mở. Không xóa `/data`:
installation identity và license state được mã hóa ở
`/data/license_secret.key`, `/data/license_state.enc` và file backup tương ứng.

Addon chỉ chứa public signing key. PayOS secret, Cloudflare D1 gateway secret,
private signing key và admin secret nằm ở portal/Worker, không đưa vào add-on.
Hướng dẫn đầy đủ về Cloudflare D1, Worker, Vercel và PayOS nằm tại
`../../license_portal/README.md`; portal này không dùng chung với trang Ecovacs
app gốc.

Mật khẩu MQTT để trống khi sửa cấu hình sẽ giữ giá trị đã mã hóa. Để tắt bridge,
xóa hostname broker rồi lưu. Port `7890` không cần map ra LAN.

Xem hướng dẫn đầy đủ tại `DOCS.md` và kiến trúc tại
`../../docs/ADDON_ARCHITECTURE.md`.

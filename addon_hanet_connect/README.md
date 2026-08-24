# HANET Connect Gateway 0.9.6

Add-on quản lý hệ sinh thái HANET trực tiếp trong Home Assistant với giao diện
Ingress tiếng Việt, khóa truy cập có thể bật/tắt và API cục bộ có xác thực.

## Điểm mới trong 0.9.6

- Thêm License Center HANET tại `https://hanet-license-admin-vercel.vercel.app`.
- Tạo installation identity Ed25519 ổn định, xác minh response ký Ed25519 và
  lưu License Key cục bộ bằng AES-GCM; không chứa PayOS/database/admin secret.
- Có trial 1 ngày, link dashboard, nhập/kích hoạt key, cache offline 72 giờ và
  tùy chọn `license_required` (mặc định `false` để không ảnh hưởng bản đang chạy).
- Khi thử key thay thế không hợp lệ, addon giữ nguyên key cũ còn hiệu lực thay vì
  làm gián đoạn gateway.

## Điểm mới trong 0.9.5

- Xóa FaceID ổn định hơn với `personID`/FaceID/UUID fallback, đọc
  `returnCode` trong response HTTP 200 và xác minh lại danh sách cloud.
- Đổi hoặc bỏ phòng ban ngay trên thẻ nhân viên; hỗ trợ schema
  `departmentID` + `personIDs/personID` và trạng thái cloud cập nhật trễ.
- Audit API nâng cao xác nhận catalog hiện đã có nhóm phòng ban, subtype, nhóm
  biển số và báo cáo chấm công; chưa trộn Partner API khác host/auth vào mobile
  gateway để tránh mutation sai tài khoản.

## Điểm mới trong 0.9.4

- Sửa lỗi Face ID bị mất phòng ban sau khi thêm hoặc sửa.
- Đồng bộ phòng ban qua API membership chính thức và đọc ngược membership khi tải danh sách.
- Cho phép bỏ phòng ban khỏi nhân viên; thêm API cục bộ `PUT /api/people/{id}/department`.
- Giữ catalog 100 endpoint nâng cao; đánh dấu CRUD biển số và thống kê chấm công là các hạng mục tiếp theo.

## Điểm mới trong 0.9.3

- Lần đầu mở add-on phải nhập mật khẩu mặc định được cung cấp riêng.
- Sau khi mở khóa có thể đổi mật khẩu hoặc tắt/bật yêu cầu đăng nhập trong tab
  **Cài đặt**; trạng thái được giữ qua lần khởi động lại.
- Làm mới giao diện theo phong cách Liquid Glass sáng, trong và mượt hơn.
- Tách riêng tab **Face nhân viên** và **Face khách**.
- Sửa xóa FaceID và hỗ trợ nhiều định dạng ảnh khi thêm từng người hoặc thêm loạt.
- Sửa nút `×` và **Hủy** không đóng được các hộp thoại có trường bắt buộc.

## Tính năng

- Tự đăng nhập HANET Mobile API và HANET Connect Web để gộp camera sở hữu/chia sẻ.
- Tổng quan camera online, offline, RTSP và thời điểm đồng bộ gần nhất.
- Ảnh camera, ảnh sự kiện, lịch sử nhận diện và clip cloud theo ngày.
- Điều khiển PTZ, preset, zoom, còi báo động, cửa và các command được hỗ trợ.
- Quản lý Face ID thành viên/khách, thêm từng ảnh hoặc nhập nhiều ảnh.
- Quản lý nhân viên, phòng ban, biển số và dữ liệu chấm công.
- Bật/tắt RTSP, LED, IR, WDR, ghi hình, thông báo và setting theo model camera.
- Đồng bộ sự kiện qua SSE; tự chuyển sang cloud polling khi SSE không khả dụng.
- WebSocket nội bộ cập nhật dashboard mà không phải tải lại trang.
- API nâng cao cho toàn bộ catalog endpoint đã reverse engineering.
- API cục bộ bằng `X-HANET-Gateway-Key` và webhook bằng secret riêng.

## Cài đặt nhanh

1. Chép thư mục `addon_hanet_connect` vào `/addons/hanet_connect`.
2. Trong Home Assistant, mở **Settings > Apps > App store**.
3. Chọn **Check for updates**, sau đó cài **HANET Connect Gateway**.
4. Trong tab **Configuration**, nhập tài khoản và mật khẩu HANET.
5. Khởi động add-on và bật **Show in sidebar**.
6. Mở **HANET Connect** từ sidebar và nhập mật khẩu mặc định được cung cấp riêng.
7. Vào **Cài đặt > Bảo mật giao diện** để đổi mật khẩu hoặc tắt yêu cầu đăng nhập.

Không cần ánh xạ cổng `9091` khi chỉ dùng giao diện Ingress. Chỉ bật cổng này khi
một hệ thống trong mạng nội bộ cần gọi API hoặc webhook; không mở cổng trên router
ra Internet.

## Hai lớp đăng nhập độc lập

- **Tài khoản HANET** nằm trong cấu hình add-on và dùng để gọi HANET Cloud.
- **Mật khẩu giao diện** mặc định bật với mã ban đầu được cung cấp riêng, không
  thay đổi tài khoản HANET và có thể tắt sau khi đã mở khóa.
- Custom integration đăng nhập HANET bằng config entry riêng, không dùng session,
  mật khẩu giao diện hay API key của add-on.

## Sử dụng giao diện

- **Camera**: xem trạng thái, ảnh mới nhất, điều khiển và mở phần setting từng máy.
- **Sự kiện**: lọc theo ngày, camera, loại nhận diện, nguồn và từ khóa.
- **Ghi hình**: tìm clip cloud theo ngày/camera và xem trực tiếp trong dialog.
- **Danh tính**: quản lý Face ID, nhân viên, phòng ban, biển số và chấm công.
- **Cài đặt**: kiểm tra kết nối, đổi mật khẩu, bật/tắt yêu cầu đăng nhập, khóa giao
  diện, quản lý License Key, bật RTSP và dùng API nâng cao.

## License rollout

- Mặc định `license_required: false`, do đó cài/nâng cấp `0.9.6` không khóa các
  chức năng camera, FaceID, phòng ban, biển số hoặc chấm công hiện có.
- Người dùng chưa có key sẽ thấy link tới License Center để nhận trial/mua gói.
- Chỉ bật `license_required: true` sau khi database, PayOS webhook và verify
  production đã được kiểm tra đầy đủ.
- Xem hướng dẫn backend/Vercel tại `../hanet-license-portal/README.md`.

## Bảo mật

- Hash mật khẩu và trạng thái bật/tắt khóa được lưu tại `/data/ui_auth.json` với
  quyền owner-only; mật khẩu rõ không được lưu.
- Token HANET được lưu riêng tại `/data/session.json` và không gửi tới trình duyệt.
- Credential P2P chỉ tồn tại ngắn hạn trong bộ nhớ và được truyền tới worker qua
  `stdin`.
- Khi bật khóa, session giao diện chỉ nằm trong bộ nhớ add-on; khởi động lại
  add-on sẽ yêu cầu mở khóa lại.
- Nếu vẫn dùng mật khẩu mặc định, nên đổi ngay sau lần đăng nhập đầu tiên.

Xem `DOCS.md` để biết cấu hình chi tiết, API và xử lý sự cố.

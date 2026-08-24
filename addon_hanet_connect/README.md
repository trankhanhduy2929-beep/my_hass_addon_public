# HANET Connect Gateway 0.9.9

Add-on quản lý hệ sinh thái HANET trực tiếp trong Home Assistant với giao diện
Ingress tiếng Việt mở trực tiếp, còn API cục bộ ngoài Ingress vẫn có xác thực.

## Điểm mới trong 0.9.9

- Sửa lỗi thêm Face có chọn phòng ban báo `This field is required`.
- Sửa lỗi đổi phòng ban báo `Invalid type: expected string but got number`.
- Khi API JSON nội bộ không nhận đúng kiểu ID, addon tự dùng form-urlencoded
  giống HANET Developer API với `token`, `departmentID` và
  `personIDs/personID`, đồng thời vẫn xác minh lại membership trên cloud.
- Danh sách thành viên phòng ban qua form API được đọc đủ theo phân trang 50
  người/trang; custom component và các chức năng addon khác không thay đổi.

## Điểm mới trong 0.9.8

- Sửa xóa FaceID khi endpoint mobile trả `404 Not Found`, có fallback tới API
  `personID` chính thức bằng form-urlencoded và vẫn xác minh lại danh sách cloud.
- Thử đúng cả ID dạng chuỗi và số cho phòng ban, khắc phục lỗi
  `Invalid type: expected string but got number` mà không phá tenant cần `int64`.
- Sửa tạo phòng ban, đổi phòng ban và thêm Face nhân viên/khách có chọn phòng ban.

## Điểm mới trong 0.9.7

- Bỏ bước nhập mật khẩu dashboard riêng; nâng cấp xong mở thẳng từ Home Assistant
  Ingress, trong khi cổng ngoài vẫn yêu cầu `X-HANET-Gateway-Key`.
- Sửa payload `int64` khi cập nhật FaceID, tạo/sửa/xóa phòng ban và gán membership.
- Cho phép cả khách lẫn nhân viên tạo, chọn, đổi và bỏ phòng ban.
- Từ sự kiện có thể mở đúng clip theo `event_id` hoặc camera/thời gian gần nhất;
  video tự tua đến thời điểm sự kiện.

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
6. Mở **HANET Connect** từ sidebar; dashboard hiển thị trực tiếp qua Ingress.
7. Vào **Cài đặt** để quản lý License Key, camera và API nâng cao.

Không cần ánh xạ cổng `9091` khi chỉ dùng giao diện Ingress. Chỉ bật cổng này khi
một hệ thống trong mạng nội bộ cần gọi API hoặc webhook; không mở cổng trên router
ra Internet.

## Xác thực

- **Tài khoản HANET** nằm trong cấu hình add-on và dùng để gọi HANET Cloud.
- Giao diện sidebar dựa vào Home Assistant Ingress và không yêu cầu mật khẩu
  dashboard thứ hai.
- API gọi trực tiếp qua cổng `9091` vẫn cần `X-HANET-Gateway-Key`.
- Custom integration đăng nhập HANET bằng config entry riêng, không dùng session,
  mật khẩu giao diện hay API key của add-on.

## Sử dụng giao diện

- **Camera**: xem trạng thái, ảnh mới nhất, điều khiển và mở phần setting từng máy.
- **Sự kiện**: lọc theo ngày, camera, loại nhận diện, nguồn và từ khóa.
- **Ghi hình**: tìm clip cloud theo ngày/camera và xem trực tiếp trong dialog.
- **Danh tính**: quản lý Face ID, nhân viên, phòng ban, biển số và chấm công.
- **Cài đặt**: kiểm tra kết nối, quản lý License Key, bật RTSP và dùng API nâng cao.

## License rollout

- Mặc định `license_required: false`, do đó cài/nâng cấp `0.9.9` không khóa các
  chức năng camera, FaceID, phòng ban, biển số hoặc chấm công hiện có.
- Người dùng chưa có key sẽ thấy link tới License Center để nhận trial/mua gói.
- Chỉ bật `license_required: true` sau khi database, PayOS webhook và verify
  production đã được kiểm tra đầy đủ.
- Xem hướng dẫn backend/Vercel tại `../hanet-license-portal/README.md`.

## Bảo mật

- Home Assistant Ingress bảo vệ giao diện sidebar; add-on không yêu cầu thêm mật
  khẩu dashboard riêng từ bản `0.9.7`.
- Token HANET được lưu riêng tại `/data/session.json` và không gửi tới trình duyệt.
- Credential P2P chỉ tồn tại ngắn hạn trong bộ nhớ và được truyền tới worker qua
  `stdin`.
- Truy cập trực tiếp qua cổng ngoài vẫn bắt buộc API key; không mở cổng `9091`
  trên router ra Internet.

Xem `DOCS.md` để biết cấu hình chi tiết, API và xử lý sự cố.

# Chấm Công ZKTeco

Home Assistant Local App/Add-on để quản lý máy chấm công ZKTeco qua giao diện Ingress.

## Tính năng

- Đồng bộ nhân viên và lịch sử chấm công từ thiết bị.
- Bảng công tách cột giờ vào và giờ ra.
- Xem đầy đủ bảng công tháng và toàn bộ lượt chấm trong ngày.
- Lọc theo tháng, khoảng ngày, hôm nay hoặc xem toàn bộ dữ liệu lịch sử.
- Chế độ lượt chấm thô để xem từng bản ghi riêng biệt.
- Mở bảng công tháng riêng của từng nhân viên ở chế độ chỉ xem.
- Theo dõi lượt chấm trực tiếp bằng `live_capture()` và tự cập nhật bảng công.
- Danh sách nhân viên chỉ xem, không có thao tác thêm, sửa hoặc xóa.
- Xem metadata mẫu vân tay từ `get_templates()` mà không gửi dữ liệu mẫu thô tới trình duyệt.
- Quét mạng LAN để tìm lại IP máy ZKTeco khi địa chỉ thiết bị thay đổi.
- Chỉnh giờ máy ZKTeco trực tiếp.
- Đồng bộ nhanh giờ GMT+7 theo múi giờ TP.HCM.
- Điều khiển giờ máy ngay tại **Tổng quan** với bộ chọn ngày/giờ tối ưu cho điện thoại, gồm chế độ đặt giữ nguyên và giờ tạm tự khôi phục.
- Tab **Đặt giờ** dùng giao diện card, cho phép tạo/sửa nhiều preset ngày giờ và bấm để đặt ngay lên máy ZKTeco.
- Preset có chế độ giờ tạm 3–300 giây, tự về GMT+7, đếm ngược trực tiếp và có thể phục hồi sớm sau lượt chấm vân tay.
- Giờ tạm có thể giữ thêm 1–30 giây sau lượt chấm để máy kịp ghi log, đồng thời luôn có timer dự phòng nếu Live Capture mất kết nối.
- Quản lý nhân viên, xuất CSV và sao lưu dữ liệu.
- Đồng hồ Tổng quan lấy trực tiếp từ `get_time()` của thiết bị và tự cập nhật liên tục.
- Xuất báo cáo toàn nhân viên theo ngày/tháng/năm, có giờ công mỗi ngày và tổng giờ từng tháng.
- Giao diện, phân trang và long-poll realtime được tối ưu cho điện thoại/Home Assistant Ingress; tab ẩn không giữ request nền.
- Không lưu PIN/password nhân viên vào database; log nội bộ dùng múi giờ GMT+7 nhất quán.
- Danh tính người đăng nhập web chỉ lưu trong audit cục bộ; lệnh gửi tới máy chấm công chỉ chứa `datetime` hoặc tham số giao thức, không chứa username/cookie/session.
- Có security header, giới hạn đăng nhập sai và kiểm thử tự động cho ranh giới danh tính.
- Dữ liệu bền vững trong volume `/data` của Add-on.

## Cài đặt

Giải nén thư mục `cham_cong_zkteco` vào `/addons` trên Home Assistant OS. Sau đó vào **Settings → Apps → App store**, chọn **Check for updates** và cài **Chấm Công ZKTeco** trong mục Local apps. Giao diện mở thẳng bằng Home Assistant Ingress, không cần tạo thêm tài khoản.

Xem `DOCS.md` để biết cấu hình và giới hạn của thiết bị.

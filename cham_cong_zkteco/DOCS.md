# Chấm Công ZKTeco cho Home Assistant

Ứng dụng quản lý máy chấm công ZKTeco trực tiếp trong Home Assistant bằng Ingress.

## Cấu hình

- `zk_ip`: IP máy chấm công trong mạng LAN.
- `zk_port`: Cổng giao tiếp, mặc định `4370`.
- `zk_password`: Communication Password của thiết bị, mặc định `0`.
- `zk_timeout`: Thời gian chờ mỗi gói tin.
- `force_udp`: Buộc giao tiếp UDP nếu TCP không hoạt động.
- `omit_ping`: Bỏ bước ping khi mạng chặn ICMP.

Home Assistant và máy chấm công phải truy cập được nhau qua mạng LAN.

## Bảng công tháng

Trong mục **Chấm công**, chọn tháng để tải toàn bộ ngày công và mọi lượt chấm trong tháng đó. Trong mục **Nhân viên**, bấm biểu tượng đồng hồ cạnh nhân viên để mở bảng công tháng riêng ở chế độ chỉ xem. Việc điều chỉnh lượt chấm, nếu cần, được thực hiện trong mục **Chấm công**.

Nếu cần xem ngoài tháng hiện tại, chọn **Khoảng ngày** hoặc **Toàn bộ dữ liệu**. Chế độ **Tất cả lượt chấm thô** hiển thị mỗi lần chấm thành một dòng riêng và có phân trang, phù hợp để kiểm tra dữ liệu cũ mà không qua bước gom giờ vào/ra.

## Chỉnh giờ thiết bị

Ngay tại **Tổng quan**, bấm **Đồng bộ GMT+7 ngay** để đặt giờ TP.HCM hoặc bấm **⌛ Đặt giờ tạm / tùy chọn** để mở bộ chọn cảm ứng. Bộ chọn tách riêng ngày/giờ, hỗ trợ điều chỉnh nhanh ±1 phút và ±5 phút.

Trong modal Tổng quan, chọn một trong hai chế độ:

- **Giờ tạm an toàn**: đặt ngày giờ theo ý muốn trong 3–300 giây. Bật **Về giờ thật sớm sau khi chấm** nếu muốn khi máy nhận vân tay thì chờ thêm 1–30 giây rồi tự về GMT+7. Dù không nhận được sự kiện live, timer tối đa vẫn khôi phục giờ.
- **Đặt và giữ nguyên**: đặt giờ cố định, không tạo phiên tự khôi phục.

Sau khi đặt giờ tạm, banner đếm ngược xuất hiện ngay bên dưới thanh đầu trang trên mọi tab. Có thể bấm **Trả về GMT+7 ngay** nếu không muốn chờ hết thời gian.

## Preset ngày giờ thủ công

Mở menu **Đặt giờ** và chọn **Tạo preset mới**. Modal cho phép nhập tên, ngày và giờ, xem trước card trước khi lưu và chọn nhanh Bây giờ, Hôm nay, Ngày mai hoặc +7 ngày.

Mỗi preset có hai chế độ:

- **Giờ tạm an toàn**: đặt ngày giờ đã lưu trong 3–300 giây, mặc định 10 giây, sau đó tự đặt lại giờ hiện tại của TP.HCM (GMT+7).
- **Đặt và giữ nguyên**: hoạt động như preset cũ; thời gian được giữ cho tới khi có lệnh đặt giờ khác.

Với giờ tạm, có thể bật **Về giờ thật sớm sau khi chấm**. Khi Live Capture nhận lượt chấm mới, Add-on chờ thêm số giây đã chọn rồi trả máy về GMT+7. Timer hiệu lực tối đa vẫn luôn chạy dự phòng, nên nếu không nhận được sự kiện live thì máy vẫn được trả giờ khi hết timer.

Sau khi bấm **Bật giờ tạm**, giao diện hiển thị đếm ngược, ngày giờ đang áp dụng và nút **Trả về GMT+7 ngay**. Lượt chấm được máy ghi theo đồng hồ thiết bị tại thời điểm quét; vì vậy cần chấm vân tay trong lúc banner giờ tạm còn hiệu lực.

Preset và phiên giờ tạm được lưu trong database `/data/cham_cong.db`. Nếu Add-on khởi động lại khi phiên chưa kết thúc, hệ thống đọc trạng thái đã lưu và tiếp tục khôi phục GMT+7. Khi Add-on dừng bình thường, nó cũng cố gắng trả giờ trước khi thoát. Mất điện toàn bộ, thiết bị mất mạng kéo dài hoặc Add-on không chạy có thể ngăn lệnh khôi phục đến máy; trong trường hợp đó cần bật lại Add-on và dùng nút **Đồng bộ GMT+7 ngay** để kiểm tra.

Các thao tác tạo, sửa, áp dụng, nhận lượt chấm trong phiên tạm, khôi phục và xóa đều được ghi vào nhật ký kiểm toán. Preset từ bản 2.0.3 được giữ nguyên và mặc định ở chế độ **Đặt và giữ nguyên** để tránh thay đổi hành vi ngoài ý muốn. Phiên giờ tạm từ bản cũ được migrate an toàn trong `app_state`.

## Sử dụng

Sau khi khởi động, bấm **Open Web UI** hoặc mở mục **Chấm công** ở thanh bên. Home Assistant Ingress kiểm soát quyền truy cập nên không cần tạo thêm tài khoản cho ứng dụng.

Dữ liệu SQLite và khóa đăng nhập nằm trong volume `/data`, được đưa vào bản sao lưu Add-on khi Home Assistant sao lưu.

## Theo dõi chấm công trực tiếp

Khi Add-on khởi động, một kết nối riêng chạy `live_capture()` để nhận sự kiện do máy ZKTeco phát sinh. Mục **Chấm công** hiển thị trạng thái kết nối live và tự cập nhật khi có lượt mới, không cần bấm **Đồng bộ** hoặc tải lại trang. Nếu kết nối bị gián đoạn, Add-on tự thử kết nối lại.

Trình duyệt dùng một request long-poll tối đa 10 giây, không phải polling 2 giây. Backend không giữ connection SQLite trong lúc chờ; khi Live Capture ghi bản ghi mới, request được đánh thức ngay. Khi tab bị ẩn, request bị hủy để giảm tải điện thoại và được nối lại khi tab hiện.

Nút **Đồng bộ** vẫn dùng để tải lại toàn bộ người dùng và lịch sử từ thiết bị khi cần đối soát.

Mỗi lần full sync chỉ chạy một phiên tại một thời điểm. Người không còn trên máy được chuyển sang `active=0`; nếu mã nhân viên giữ nguyên nhưng UID đổi, Add-on cập nhật UID thay vì làm hỏng transaction. PIN/password của user trên máy không được đọc vào database; database cũ có cột này sẽ được xóa trắng khi khởi động.

## Xuất dữ liệu và tính giờ công

Trong mục **Chấm công**, chọn **Xuất dữ liệu** rồi chọn báo cáo theo ngày, tháng hoặc năm. File CSV dùng UTF-8 và bao gồm toàn bộ nhân viên, chi tiết mỗi ngày có chấm và các dòng tổng theo tháng.

Giờ công một ngày được tính bằng tổng thời gian của từng cặp lượt theo thứ tự: lượt 1–2, 3–4, 5–6… Lượt cuối chưa có cặp được ghi ở cột **Lượt chưa ghép** và không cộng vào giờ công. Báo cáo tháng/năm có thêm số ngày có chấm và tổng giờ tháng dạng `HH:MM` lẫn số giờ thập phân.

Khi xuất theo một ngày, nhân viên không có lượt chấm vẫn xuất hiện với 0 giờ để dễ kiểm tra vắng mặt. Khi xuất tháng hoặc năm, phần tổng tháng luôn có đủ danh sách nhân viên đang hoạt động.

## Ranh giới bảo mật lệnh ZKTeco

Tên đăng nhập, cookie, session, địa chỉ người dùng web và thông tin người bấm nút không được truyền vào bất kỳ command ZKTeco nào. Ví dụ, thao tác chỉnh giờ chỉ gọi `device.set_time(value)` và lớp thiết bị chỉ thực hiện `conn.set_time(value)`. Danh tính người thao tác, nếu có, chỉ được giữ cục bộ trong audit của Add-on sau khi lệnh hoàn tất.

Khi chạy chế độ Ingress của Home Assistant, request thiếu header danh tính Ingress bị từ chối; chỉ endpoint health dành cho watchdog được mở không cần danh tính. Đây là lớp bảo vệ chống gọi nhầm trực tiếp vào cổng nội bộ, không thay thế tường lửa hoặc xác thực của Home Assistant.

## Nhân viên và mẫu vân tay

Mục **Nhân viên** chỉ cho phép tìm kiếm, xem thông tin và xem bảng công tháng. Add-on không cung cấp API thêm, sửa tên hoặc xóa nhân viên.

Trong mục **Thiết bị**, chọn **Xem mẫu vân tay** để gọi `get_templates()`. Giao diện chỉ hiển thị nhân viên, UID, vị trí ngón, trạng thái và kích thước mẫu; chuỗi mẫu sinh trắc học không được gửi tới trình duyệt.

## Dò lại IP máy chấm công

Trong mục **Thiết bị**, chọn **Quét tìm thiết bị**. Để trống CIDR để quét mạng `/24` dựa trên IP ZKTeco đang cấu hình, hoặc nhập rõ dải như `192.168.1.0/24`. Phạm vi lớn nhất được phép là `/22` tương đương tối đa 1024 địa chỉ.

Add-on kiểm tra cổng 4370 song song, sau đó chỉ hiển thị thiết bị đọc được thông tin ZKTeco như serial, platform, firmware và MAC. Khi tìm được IP mới, sao chép IP, cập nhật `zk_ip` trong cấu hình Add-on rồi khởi động lại Add-on.

## Cài dưới dạng Local App/Add-on

1. Dùng Samba hoặc SSH để mở thư mục `/addons` trên Home Assistant OS.
2. Sao chép toàn bộ thư mục dự án này vào `/addons/cham_cong_zkteco`.
3. Vào **Settings → Apps → App store**.
4. Mở menu ba chấm và chọn **Check for updates**.
5. Chọn **Chấm Công ZKTeco** trong mục Local apps, cài đặt rồi khởi động.

Nếu build thất bại, kiểm tra máy Home Assistant có Internet để tải base image và Python packages trong lần cài đầu.

## Giới hạn thiết bị

Chức năng xóa log, chấm thủ công, sửa/xóa nhân viên và kiểm tra âm thanh đã bị loại bỏ. Add-on chỉ đọc/đồng bộ nhân viên, nhận sự kiện chấm thật, đọc giờ, xem metadata mẫu vân tay và giữ các công cụ thời gian/khởi động lại thiết bị.

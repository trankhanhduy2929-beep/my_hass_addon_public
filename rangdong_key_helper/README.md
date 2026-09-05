# Rạng Đông Key Helper

Add-on Home Assistant để đăng nhập tài khoản Rạng Đông và chuyển `local_key`
đến custom integration Rạng Đông Smart qua bridge nội bộ.

## Cài đặt

1. Trong Home Assistant vào **Cài đặt → Add-ons → Add-on Store**.
2. Chọn menu ba chấm → **Repositories**.
3. Thêm repository add-on của chủ dự án.
4. Mở **Rạng Đông Key Helper** → **Install** → **Start**.
5. Bật **Show in sidebar** để mở giao diện add-on.

Nếu repository đã có sẵn, chỉ cần cập nhật add-on lên bản mới nhất rồi restart.

## License

Mở giao diện add-on và nhập License Key đã nhận tại website license. Dùng cùng
một key cho một add-on và một custom integration trên cùng Home Assistant.

License gồm dùng thử 1 ngày, 1 tháng và vĩnh viễn. Dùng thử chỉ nhận một lần cho
mỗi tài khoản và installation. Nếu chưa có key, mở nút mua/nhận key trong add-on,
tạo tài khoản bằng email + mật khẩu, sau đó sao chép key từ dashboard website.

## Lấy key Rạng Đông

1. Nhập email/số điện thoại và mật khẩu **tài khoản Rạng Đông** trong add-on.
2. Bấm **Đăng nhập và lấy key**.
3. Chọn thiết bị cần thêm.
4. Vào **Cài đặt → Thiết bị & Dịch vụ → Thêm tích hợp → Rạng Đông Smart**.
5. Chọn **LAN nội bộ → Key Helper / bridge**, rồi chọn thiết bị.

Mật khẩu trong add-on là mật khẩu Rạng Đông, không phải mật khẩu website license.
Mật khẩu chỉ được dùng trong lần đăng nhập và không được lưu vào giao diện.

## Lưu ý

- Home Assistant phải truy cập được cùng mạng LAN với thiết bị Rạng Đông.
- Không chia sẻ License Key hoặc mật khẩu Rạng Đông.
- Không cần Android root, ADB, Frida, Tuya IoT Cloud project hay import APK.
- Nút xóa key tạm chỉ xóa dữ liệu tạm trong bridge, không xóa thiết bị đã cấu hình.
- Thiết bị đã cấu hình tiếp tục điều khiển bình thường nếu server license tạm thời
  không truy cập được; license kiểm soát việc thiết lập mới/lấy key mới.

## Xử lý lỗi

- **License không hợp lệ:** kiểm tra key, trạng thái license và đúng installation.
- **Đăng nhập thất bại:** kiểm tra thông tin tài khoản Rạng Đông và kết nối mạng.
- **Không thấy thiết bị:** kiểm tra VLAN/firewall, IP Home Assistant và thiết bị
  có cùng LAN; thử khởi động lại add-on.
- **Key đã gắn nơi khác:** không đổi email để vượt giới hạn; liên hệ admin reset
  sau khi xác minh quyền sở hữu.

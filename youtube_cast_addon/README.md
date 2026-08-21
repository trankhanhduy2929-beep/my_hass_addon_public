🎵 YouTube Music Cinematic Addon (v1.20.1)
YouTube Music Cinematic là một Add-on cao cấp dành cho Home Assistant, cho phép bạn tìm kiếm, phát nhạc trực tuyến từ YouTube và điều khiển các thiết bị Media Player trong nhà với giao diện hiện đại, mượt mà.

✨ Tính năng nổi bật
Premium Interface: Giao diện lấy cảm hứng từ YouTube Music với hiệu ứng kính mờ (Glassmorphism).

Proxy Stream: Vượt qua các rào cản địa lý và chặn IP từ YouTube để phát nhạc ổn định.
Infinite Scroll: Cuộn vô tận để khám phá hàng ngàn bài hát mới.

Multi-Device Casting: Phát nhạc trực tiếp trên trình duyệt điện thoại hoặc Cast sang các loa thông minh (Google Home, Sonos, v.v.) trong hệ thống HA.

Smart Playlist: Tạo và quản lý danh sách phát yêu thích không giới hạn.

Automation Timer: Hẹn giờ tự động phát hoặc tắt nhạc theo lịch trình hàng ngày.

Ingress Support: Truy cập trực tiếp và bảo mật từ thanh điều hướng của Home Assistant.

🚀 Hướng dẫn cài đặt (A-Z)
1. Thêm Repository
Mở giao diện Home Assistant của bạn.
Đi tới Settings (Cài đặt) -> Add-ons (Tiện ích bổ sung).
Nhấn vào nút Add-on Store (Cửa hàng tiện ích) ở góc dưới bên phải.
Nhấn vào dấu 3 chấm (góc trên bên phải) -> Chọn Repositories (Kho lưu trữ).
Dán đường link GitHub vào và nhấn Add (Thêm).

2. Cài đặt Add-on
Sau khi thêm Repo, tìm kiếm "YouTube Music Cinematic" trong cửa hàng.
Nhấn Install (Cài đặt). Quá trình này có thể mất vài phút để tải Docker image.
Bật tùy chọn Show in sidebar (Hiển thị ở thanh bên) để truy cập nhanh.
Nhấn Start (Bắt đầu).

📖 Hướng dẫn sử dụng

🔍 Tìm kiếm & Khám phá
Nhập từ khóa vào ô tìm kiếm và nhấn TÌM.
Hệ thống sẽ tự động gợi ý các bài hát hot nhất năm 2025 nếu bạn để trống.
Cuộn xuống dưới cùng để tải thêm kết quả (Infinite Scroll).

🔊 Chọn thiết bị phát (Speaker)
Ở góc trên bên phải, chọn thiết bị bạn muốn phát nhạc.

📱 ĐIỆN THOẠI: Phát nhạc trực tiếp trên trình duyệt bạn đang mở.

🔊 Media Players: Danh sách các loa thông minh hiện có trong Home Assistant của bạn.

📂 Quản lý Playlist
Tạo mới: Chuyển sang tab Playlist, nhập tên và nhấn nút +.
Thêm bài hát: Tại tab Khám phá, nhấn biểu tượng + nhỏ trên mỗi bài hát để chọn playlist muốn thêm vào.

Nghe Playlist: Nhấn vào tên playlist để xem danh sách bài hát và chọn bài muốn phát.
⏰ Hẹn giờ tự động (Timer)
Chuyển sang tab Hẹn giờ.
Chọn các thứ trong tuần, thời gian (Giờ:Phút).
Chọn hành động: PHÁT (kèm playlist) hoặc TẮT nhạc.
Bạn có thể đặt thời gian tự động tắt sau khi phát (ví dụ: phát nhạc 30 phút rồi tự tắt).

🛠 Yêu cầu hệ thống
Hệ điều hành: Home Assistant OS hoặc Supervised.
Kiến trúc: Hỗ trợ đa nền tảng (aarch64, amd64, armhf, armv7).
Phụ thuộc: Yêu cầu quyền truy cập vào API của Home Assistant (đã cấu hình sẵn trong config.yaml).

📄 Giấy phép & Đóng góp
Add-on này được phát triển dựa trên Flask, yt-dlp và Tailwind CSS. Mọi đóng góp về code hoặc báo lỗi vui lòng tạo Issue trên GitHub.
Chúc bạn có những giây phút thư giãn âm nhạc tuyệt vời!

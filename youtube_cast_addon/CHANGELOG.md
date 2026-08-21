# Changelog

## 2.3.0 - 2026-08-21

- Dừng audio trên điện thoại ngay khi chọn bài khác; với loa Home Assistant, lệnh dừng được gửi ngay và lệnh phát mới được xếp sau để không phát chồng.
- Chặn race khi bấm nhanh nhiều bài: chỉ yêu cầu mới nhất được quyền cập nhật trình phát hoặc gửi lệnh cast.
- Tăng cache frontend từ 6 lên 10 bài, làm nóng 3 kết quả tìm kiếm đầu và 2 bài tiếp theo trong ngữ cảnh đang phát.
- Bỏ chờ xóa hàng chờ trước khi chuyển bài và đánh dấu trực tiếp bài đang tải/đang phát trên mọi danh sách.
- Rút kiểm tra stream từ hai request Range xuống một request `bytes=0-`, vẫn đọc dữ liệu thật trước khi cấp token.
- Viết lại CSS mobile-first theo phong cách glass/premium, tối ưu thanh phát thu gọn và điều hướng đáy.
- Thêm dark/light mode theo hệ thống, ghi nhớ lựa chọn và cập nhật màu giao diện trình duyệt.

## 2.2.1 - 2026-08-21

- Sửa lỗi tìm kiếm có kết quả nhưng bấm Play không phát do URL format 140 chỉ đọc được đoạn đầu rồi trả HTTP 403.
- Nâng `yt-dlp` từ `2026.7.4` lên `2026.8.19` để loại các HTTPS format thiếu GVS PO token không an toàn.
- Kiểm tra `Range: bytes=0-` và byte ở giữa stream trước khi cache/trao token cho trình phát.
- Ưu tiên `visionos` audio nhẹ; tự fallback sang MP4 `android` hoặc `android_vr` nếu stream audio không phát liên tục được.
- Mở khóa audio ngay trong thao tác chạm để tránh chính sách autoplay của Home Assistant WebView/Safari chặn lần phát đầu.
- Giữ MIME cast `audio/mp4` tương thích với các media player Home Assistant hiện có.

## 2.2.0 - 2026-08-10

- Thêm adaptive extractor: ghi nhớ chiến lược thành công gần nhất và thử trước ở các bài tiếp theo.
- Tạm làm nguội 10 phút với extractor lỗi lặp lại, tránh phải chờ nhiều lần fallback khi chuyển bài.
- Gộp các yêu cầu resolve trùng URL đang chạy và dùng connection pool cho audio relay.
- Sửa prefetch sai bài khi phát từ playlist, hàng chờ hoặc lịch sử; làm nóng bài ngay từ thao tác chạm và prefetch đúng bài kế tiếp.
- Không chờ cập nhật lịch sử trước khi bắt đầu prefetch bài sau.
- Thêm API `/api/details`, nút `ⓘ` trên mọi bài và trình phát, cùng hộp chi tiết video tối ưu điện thoại.
- Bổ sung channel, lượt xem, ngày đăng, mô tả và chẩn đoán thời gian từng lần resolve.

## 2.1.0 - 2026-08-09

- Thêm cache resolve 60 phút và prefetch giới hạn để giảm thời gian chờ khi phát lại/bài kế tiếp.
- Thêm player thu gọn dạng thanh mini, ghi nhớ trạng thái trên điện thoại.
- Đổi danh sách tìm kiếm sang infinite scroll tự tải thêm khi gần cuối trang.
- Nâng giới hạn kết quả tìm kiếm liên tục lên 300 mục và trả cờ `has_more` cho frontend.

## 2.0.2 - 2026-08-09

- Khôi phục hành vi không cookie của addon gốc bằng cách ưu tiên riêng client `android_vr`.
- Thêm fallback no-cookie lần lượt qua `visionos` và client `android` với MP4 360p kiểu bản gốc.
- Chỉ sử dụng cookie sau khi toàn bộ chiến lược không cookie thất bại.
- Chuyển cache yt-dlp sang `/tmp` để dữ liệu extractor cũ không tồn tại qua các lần cập nhật addon.
- Nâng `yt-dlp-ejs` từ `0.3.1` lên `0.8.0` và hiển thị extractor/format vừa phát thành công.

## 2.0.1 - 2026-08-07

- Thêm nhập và xóa `cookies.txt` trực tiếp trong giao diện Ingress để xử lý lỗi xác minh bot của YouTube.
- Kiểm tra định dạng Netscape, trạng thái hết hạn và cookie đăng nhập trước khi lưu.
- Chỉ giữ cookie thuộc `youtube.com`, đặt quyền file `0600` và xóa cache stream sau khi thay cookie.
- Trả thông báo tiếng Việt dễ hiểu khi YouTube yêu cầu xác thực.
- Dùng danh sách player client mặc định của phiên bản yt-dlp hiện tại thay cho cấu hình client cứng.

## 2.0.0 - 2026-08-07

- Viết lại backend theo hướng audio-only và giảm mạnh số route/tính năng phụ.
- Thêm Deno và `yt-dlp-ejs` để hỗ trợ JavaScript challenge của YouTube.
- Thêm audio relay token có HTTP Range, tự refresh URL khi gặp 401/403/410.
- Cast loa qua cổng LAN của addon thay vì gửi URL Google Video trực tiếp.
- Viết lại toàn bộ giao diện mobile-first bằng HTML/CSS/JavaScript thuần.
- Giữ playlist, queue, history và timer từ dữ liệu 1.x; migrate lịch nâng cao cũ sang timer cơ bản.
- Giảm quyền addon, giới hạn API qua Ingress và chỉ mở route media token ra LAN.

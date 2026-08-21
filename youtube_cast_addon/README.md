# YouTube Music Lite 2.3.0

Addon phát nhạc YouTube dành cho Home Assistant, được viết lại theo hướng nhẹ và ưu tiên điện thoại.

## Điểm mới

- Giao diện mobile-first bằng HTML, CSS và JavaScript thuần; không còn Tailwind CDN hoặc Google Fonts.
- Chỉ tập trung vào audio: tìm kiếm, phát trên điện thoại, cast tới `media_player`, playlist, hàng chờ và hẹn giờ.
- Danh sách khám phá tự tải thêm khi cuộn gần cuối, không cần bấm chuyển trang.
- Trình phát có chế độ thu gọn thành thanh mini để dùng các chức năng khác trên điện thoại.
- Có dark/light mode tự nhận theo điện thoại và ghi nhớ lựa chọn cho lần mở sau.
- Có nút `ⓘ` tại mỗi bài và trên trình phát để xem kênh, thời lượng, lượt xem, lượt thích, ngày đăng và mô tả video.
- Khi chọn bài khác, frontend hủy lượt phát cũ, dừng audio điện thoại ngay lập tức và gửi lệnh dừng loa song song với quá trình resolve bài mới.
- Chỉ yêu cầu phát mới nhất được phép chạy, nên bấm/chuyển bài liên tục không còn phát nhầm bài cũ.
- Cache frontend tăng lên 10 bài; tự làm nóng 3 kết quả đầu và 2 bài kế tiếp của tìm kiếm, playlist, hàng chờ hoặc lịch sử.
- Backend ghi nhớ extractor vừa chạy tốt và thử extractor đó trước ở bài tiếp theo; client lỗi lặp lại được tạm làm nguội 10 phút.
- Trước khi trả token phát, backend kiểm tra `Range: bytes=0-` và đọc block đầu 4 KB; giữ kiểm tra stream thật nhưng bỏ request probe thứ hai để giảm thời gian chờ lần đầu.
- Kết nối relay dùng pool tái sử dụng để giảm thời gian mở audio khi bấm phát hoặc chuyển bài.
- Frontend mở khóa phần tử audio ngay trong lần chạm, tránh WebView/Safari chặn tự phát sau khi chờ resolve.
- Dùng Deno cùng `yt-dlp-ejs` để xử lý JavaScript challenge mới của YouTube.
- Addon ưu tiên audio nhẹ bằng `visionos`; nếu stream bị YouTube từ chối khi phát thật, addon tự fallback sang MP4 bằng client `android`, rồi `android_vr` và cuối cùng là cookie tùy chọn. Từ bài sau, chiến lược vừa thành công được thử trước.
- Audio được relay qua addon bằng token ngẫu nhiên; URL hết hạn hoặc trả về 403 sẽ được resolve lại tự động.
- Loa tải audio từ cùng máy Home Assistant, nhờ đó giữ đúng IP và HTTP headers mà YouTube yêu cầu.
- Giữ tương thích dữ liệu playlist, queue, lịch sử và timer của các bản 1.x.

## Cài đặt

1. Build/cài addon trên Home Assistant OS hoặc Supervised.
2. Bật **Show in sidebar** và khởi động addon.
3. Mở giao diện `Music Lite`, chọn **Điện thoại này** hoặc một loa Home Assistant rồi phát nhạc.

Addon hỗ trợ `amd64` và `aarch64`.

## Cast tới loa

Addon mở cổng `2232/tcp` để loa trong LAN lấy audio relay. Mặc định backend tự đọc `internal_url` của Home Assistant và tạo URL dạng:

```text
http://<home-assistant-host>:2232/api/media/<token>/audio.m4a
```

Nếu loa không truy cập được URL tự nhận diện, đặt option `media_base_url`, ví dụ:

```yaml
media_base_url: "http://192.168.1.20:2232"
```

Chỉ route audio có token và health check được truy cập trực tiếp qua cổng này; giao diện cùng các API quản trị vẫn bị giới hạn qua Home Assistant Ingress.

## Khắc phục lỗi YouTube

- Kiểm tra mục **Hẹn giờ → Trạng thái hệ thống**: Home Assistant, Deno và yt-dlp phải báo `OK`.
- Cookie không bắt buộc. Bản 2.3.0 dùng `yt-dlp 2026.8.19` và kiểm tra quyền đọc stream thật trước khi báo phát thành công.
- Dòng **Extractor** trong trạng thái hệ thống cho biết chiến lược, format, cache và số mili giây của lần resolve gần nhất; dòng **Ưu tiên lần sau** cho biết client sẽ được thử trước.
- Lựa chọn extractor được lưu tại `/data/extractor_preference.json`, nên vẫn giữ sau khi khởi động lại addon.
- Chỉ khi cả ba chiến lược đều bị YouTube chặn, có thể mở **Hẹn giờ → Cookie YouTube** và nhập file `cookies.txt`.
- File phải ở định dạng Mozilla/Netscape, được xuất từ một phiên trình duyệt đang đăng nhập YouTube. Nên dùng tài khoản phụ vì YouTube có thể giới hạn tài khoản dùng với công cụ tải media.
- Cách xuất ổn định: mở một cửa sổ ẩn danh chỉ có một tab, đăng nhập YouTube, trong chính tab đó mở `https://www.youtube.com/robots.txt`, xuất cookie `youtube.com`, rồi đóng hẳn cửa sổ ẩn danh và không mở lại phiên đó.
- Addon tự loại bỏ cookie của website khác, chỉ lưu cookie thuộc `youtube.com` tại `/data/cookies.txt` với quyền `0600`.
- Khi cookie hết hạn hoặc lỗi xuất hiện lại, xuất một file mới rồi nhập đè; không cần khởi động lại addon.
- Sau khi thay đổi `media_base_url`, khởi động lại addon.

## Công nghệ

- Flask + Gunicorn
- yt-dlp + yt-dlp-ejs
- Deno JavaScript runtime
- CSS/JavaScript thuần, không phụ thuộc frontend bên ngoài

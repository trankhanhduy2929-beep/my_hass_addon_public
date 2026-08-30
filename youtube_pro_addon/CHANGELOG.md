# Changelog

## 5.3.1 - 2026-08-30

- Cho phép tài khoản Home Assistant không phải quản trị mở panel YouTube Pro bằng cách tắt giới hạn `panel_admin`.
- Giữ nguyên Home Assistant Ingress và không thêm `auth_api` hoặc quyền Supervisor mới; các request vẫn phải đi qua phiên đăng nhập Home Assistant.
- Giữ nguyên playback, Cast/AirPlay/HomePod, video, Mix cá nhân, Media Browser, license và custom integration.

## 5.3.0 - 2026-08-29

- Thêm menu **Nhạc cá nhân** riêng cạnh Trang chủ và chuyển toàn bộ Mix cá nhân, Hồ sơ nghe cùng thao tác tạo/đổi tên/xóa hồ sơ sang trang này.
- Làm gọn Trang chủ để tập trung vào tìm kiếm, khám phá và phát nhạc thông thường.
- Chỉ tạo Mix khi người dùng mở tab Nhạc cá nhân; vẫn nạp nhẹ hồ sơ nghe để giữ nguyên phản hồi thích/không thích trong player.
- Giữ nguyên ID giao diện, API, dữ liệu hồ sơ local-first, playback, Cast/AirPlay/HomePod, video, queue, license và custom integration hiện có.
- Tối ưu thanh điều hướng mobile cho sáu menu, gồm nhãn rút gọn trên màn hình rất hẹp.

## 5.2.1 - 2026-08-28

- Sửa lỗi mở lại add-on bị kẹt ở màn hình kiểm tra key dù license vẫn còn hợp lệ.
- Nạp trạng thái license hợp lệ đã cache ngay khi render trang; kiểm tra server tiếp tục chạy nền và không chặn giao diện.
- Giữ lại offline grace có giới hạn; license không được duy trì vô thời hạn khi server không thể xác minh hoặc đã hết grace.
- Tự sao lưu và khôi phục activation token để không mất liên kết installation khi file token chính bị thiếu.
- Thêm khóa chống validation đồng thời, bảo đảm refresh thủ công vẫn có thể nhận trạng thái thu hồi từ server.
- Giữ nguyên playback, Cast/AirPlay/HomePod, video, queue, Media Browser, custom integration và các API hiện có.

## 5.2.0 - 2026-08-27

- Thêm **Mix cá nhân local-first** với hồ sơ nghe riêng, xếp hạng theo lịch sử/thích/không thích và cache có thể làm mới.
- Thêm phản hồi đề xuất trong player và dialog chi tiết: thích, không thích, ẩn bài, ẩn kênh và hoàn tác.
- Thêm service/API `play_personal_mix`, `listener_feedback`; Smart Radio nhận `profile_id`.
- Media Browser 3.2 thêm mục **Mix cá nhân**.
- Bỏ hoàn toàn luồng đăng nhập Google/Google OAuth khỏi giao diện; portal license chỉ dùng email/mật khẩu.
- Ẩn giao diện nhập YouTube cookie để người dùng không phải đăng nhập tài khoản Google; backend tương thích cũ vẫn được giữ an toàn.
- Giữ nguyên playback, Cast/AirPlay/HomePod, video, queue, license và API cũ.

## 5.1.0 - 2026-08-27

- Thêm **Queue Pro**: phát tiếp theo, thêm cuối hàng chờ, đổi thứ tự, xóa, xáo trộn và lưu hàng chờ thành playlist.
- Queue theo phiên phát giữ nguyên bài hiện tại, tự chuyển về hàng chờ chung khi phiên đã dừng và giới hạn an toàn 300 bài.
- Thêm **Smart Radio** cho audio/video: tạo đề xuất từ bài gốc, loại bài trùng với phiên/lịch sử, tự refill khi sắp hết và chống race khi phiên bị thay thế.
- Thêm service/API `youtube_pro.start_radio`, mở rộng `youtube_pro.enqueue` với `position` và `entity_id`.
- Media Browser lấy đúng queue của loa đích; giao diện mobile gọn hơn khi có nhiều thao tác trên một bài.
- Giữ nguyên license enforcement, Cast/AirPlay/HomePod, video, Media Browser và các API cũ.

## 5.0.1 - 2026-08-26

- Tối ưu phát nhạc trên trình duyệt: bỏ lượt probe mạng dư trước khi phát, để audio bắt đầu ngay khi relay nhận được dữ liệu đầu tiên.
- Relay audio nhả chunk nhỏ hơn và tắt buffering trung gian; không cần chờ tải hết bài hát.
- Tăng prefetch sáu kết quả đầu và tách cache browser/loa để thao tác bấm phát phản hồi nhanh mà Cast vẫn được xác minh đầy đủ.
- Mở rộng Integration API cho tìm kiếm, resolve, play và enqueue video bằng trường `media_kind` tùy chọn; audio vẫn là mặc định để không phá client cũ.
- Trả thêm danh mục `video_discovery` cho custom integration YouTube Pro 5.0.1 và tự hạ video xuống audio khi đích phát chỉ hỗ trợ âm thanh.
- Giữ nguyên đường phát Cast/AirPlay/HomePod và toàn bộ đường Video.

## 5.0.0 - 2026-08-25

- Tự phát hiện địa chỉ LAN qua Supervisor; bỏ nhu cầu nhập IP Home Assistant cho relay.
- Tự quét và phân loại `media_player` Cast, Apple TV, AirPlay và HomePod từ state/registry của Home Assistant.
- Thêm resolver video độc lập, cache video riêng và progressive MP4 relay có Range support.
- Thêm tab **YouTube Video** với tìm kiếm, chủ đề khám phá, thumbnail grid, watch view và related navigation.
- Cast TV nhận video; HomePod/AirPlay tự chuyển audio fallback để không gửi video không tương thích tới loa chỉ có âm thanh.
- Giữ nguyên license enforcement, nhạc, playlist, queue, timer, Media Browser 3.2 và Integration API.

## 4.2.0 - 2026-08-25

- Bỏ hoàn toàn nhu cầu cấu hình `license_server_url`; add-on dùng endpoint production tích hợp sẵn và chỉ cho phép override qua biến môi trường khi debug.
- Đổi link kết nối sang URL fragment, không gửi claim token trong HTTP request hoặc log Vercel.
- Luồng **Kích hoạt tự động** đăng ký installation trực tiếp Cloudflare Worker, portal liên kết tài khoản một lần và add-on tự nhận activation token bằng installation ID + secret.
- Rút polling sau khi người dùng quay lại add-on xuống khoảng 1,25 giây; giữ polling nền 30 giây và offline grace an toàn.
- Giữ nguyên enforcement, playback, Media Browser 3.2, queue, playlist, timer và Integration API hiện có.

## 4.1.0 - 2026-08-25

- Bắt buộc nhập License Key hợp lệ trước khi truy cập hoặc sử dụng toàn bộ tính năng YouTube Pro; option `license_enforcement` cũ chỉ còn để tương thích cấu hình nâng cấp và không thể tắt khóa.
- Giữ lại duy nhất các route cần cho health, giao diện kích hoạt, icon và API license; queue, playlist, Media Browser, Integration API, relay và playback đều trả `402 license_required` khi chưa active key.
- Khi license hết hạn, bị thu hồi hoặc bị khóa, add-on dừng playback/cast đang chạy và xóa cache resolve/stream; worker kiểm tra nền định kỳ để không giữ phiên phát trái phép.
- Làm lại màn hình kích hoạt toàn màn hình, không tải dữ liệu ứng dụng trước khi xác minh; polling license tự đóng audio/realtime khi trạng thái chuyển invalid.
- Đồng bộ Portal/Worker 1.3.0: quick connect gọi thẳng Cloudflare Worker bằng một RPC gộp, có fallback Vercel, trạng thái loading/error rõ ràng và chống bấm lặp.

## 4.0.0 - 2026-08-25

- Tách thành add-on độc lập **YouTube Pro**, không thay thế hoặc dùng chung slug với YouTube Music Lite.
- Đổi cổng add-on, relay và Integration API sang `2032`.
- Tách domain Home Assistant thành `youtube_pro`, localStorage trình duyệt, integration token và dữ liệu license riêng.
- Đổi prefix License Key sang `YTP` để không dùng nhầm key của bản Lite.
- Giữ nguyên playback engine, Media Browser 3.2 và giao diện YouTube Music đã ổn định từ bản Lite.
- Kết nối mặc định tới portal YouTube Pro trên Vercel; backend license dùng Cloudflare Worker + D1 riêng, không dùng chung tài nguyên Hanet/Maika.

## 3.3.0 - 2026-08-25

- Thêm License Manager opt-in, mặc định `license_enforcement: false` để không ảnh hưởng playback hiện tại khi nâng cấp.
- Sinh installation ID/secret và activation token riêng, lưu file quyền `0600`; License Key không được ghi vào state hoặc log.
- Thêm panel License trong tab Hẹn giờ: mở portal, liên kết installation, nhập key, refresh trạng thái và deactivate.
- Thêm validate nền, offline grace tối đa 72 giờ và chỉ chặn search/resolve/playback mới khi chủ hệ thống chủ động bật enforcement.
- Giới hạn trạng thái license trên Integration API để không lộ claim URL, activation token hoặc installation secret.
- Bổ sung portal Next.js + PayOS trong `projects/youtube_license_portal`, gồm auth, trial, thanh toán QR, webhook tự cấp key, dashboard và admin; backend production đã chuyển sang Cloudflare Worker + D1.
- Bộ hồi quy add-on tăng lên 26 test; production build portal, 3 test crypto, typecheck, lint, Media Browser và Chromium desktop/mobile đều qua.

## 3.2.0 - 2026-08-24

- Nâng Integration API lên v2 với library, playlist items, queue, history, YouTube search, resolve relay và playback control dành riêng cho Media Browser.
- Thêm Media Source native `media-source://youtube_music_lite`, cho phép duyệt playlist, hàng chờ, lịch sử, khám phá và tìm kiếm gần đây trên mọi media player hỗ trợ Home Assistant Media Browser.
- Thêm entity ảo **YouTube Music Lite Media Browser** hỗ trợ `BROWSE_MEDIA`, `SEARCH_MEDIA`, `PLAY_MEDIA`, next/previous, repeat và shuffle; kết quả tìm kiếm được phát qua playback engine tới loa mặc định đã chọn.
- Thêm tùy chọn chọn `media_player` mặc định ngay lúc cấu hình hoặc qua **Configure**, tương thích cả config entry nâng cấp từ 3.1.0.
- Lưu tối đa 12 từ khóa tìm kiếm gần đây tại `/data/search_history_v320.json` và đưa chúng vào Media Browser; dữ liệu này có trong backup nhưng không chứa token hay URL stream.
- Thiết kế lại toàn bộ Ingress UI theo phong cách YouTube Music: sidebar desktop, bottom navigation mobile, hero, quick search, album rail, artwork animation và glass mini-player responsive.
- Dùng icon YouTube người dùng cung cấp xuyên suốt favicon, header, hero và player; dark mode là mặc định, vẫn hỗ trợ light mode thủ công.
- Thêm phím `/` để focus tìm kiếm, quick search theo mood, số lượng queue/playlist/history thời gian thực và mini-player mobile thu gọn mặc định.
- Kiểm tra giao diện bằng Chromium tại 1440×1000 và 390×844, không tràn ngang hoặc lỗi console; bộ hồi quy add-on tăng lên 22 test.
- Xác minh Media Source và virtual player bằng Home Assistant `2026.2.3`, gồm browse, search, resolve, phát playlist, phát URL và playback control.

## 3.1.0 - 2026-08-24

- Thêm Integration API biệt lập tại `/api/integration/*`, xác thực bằng Bearer token sinh ngẫu nhiên và so sánh constant-time.
- Lưu token tại `/data/integration_api_token` với quyền `0600`; thêm giao diện xem, sao chép và rotate token chỉ qua Ingress.
- Giữ nguyên hàng rào mạng cũ: bearer integration không thể truy cập giao diện, cookie, backup hoặc API quản trị.
- Thêm endpoint health/status, phát URL, phát playlist, enqueue và set timer cho Home Assistant custom integration.
- Tạo custom integration `youtube_music_lite` với config flow, re-auth, coordinator polling, 5 sensor chẩn đoán và 4 service automation.
- Thêm brand icon 256/512px từ logo YouTube người dùng cung cấp.
- Bổ sung test chống lộ token và chống auto-next cũ nhảy phiên mới; tổng bộ hồi quy add-on tăng lên 18 test.
- Xác minh custom integration bằng Ruff và Home Assistant `2026.2.3` trong môi trường tạm; chưa kiểm thử trên Home Assistant/loa thật.

## 3.0.0 - 2026-08-24

- Thêm playback engine phía backend theo từng `media_player`, hỗ trợ auto-next, previous, repeat `off/all/one`, shuffle và prefetch bài kế tiếp.
- Lưu phiên phát, queue và chế độ phát tại `/data/playback_sessions_v300.json`; khôi phục an toàn sau khi add-on khởi động lại.
- Theo dõi `state_changed` qua Home Assistant WebSocket và tự dùng REST polling làm fallback khi WebSocket mất kết nối.
- Thêm SSE `/api/events` để giao diện đồng bộ bài, artwork, trạng thái và tiến độ khi backend tự chuyển bài.
- Mở rộng `/api/cast` để nhận toàn bộ ngữ cảnh phát; thêm API start/session/control dành cho playback engine.
- Nâng timer để phát toàn playlist, chỉ đánh dấu hoàn tất sau khi thực thi thành công và retry có throttle khi gặp lỗi.
- Sửa race Stop có thể kích hoạt auto-next và sửa tiến độ không nhận thao tác tua lùi.
- Thêm `websocket-client 1.9.0` và mở rộng bộ hồi quy lên 12 test.

## 2.5.0 - 2026-08-24

- Thêm adaptive cast profile theo từng `media_player`, ghi nhớ direct/relay, MIME thành công và cooldown transport lỗi lặp lại.
- Giảm thời gian chờ fallback direct xuống khoảng 3 giây và tự thử transport còn lại nếu loa không chuyển sang trạng thái phát.
- Thêm PO Token Provider tùy chọn với plugin `bgutil-ytdlp-pot-provider 1.3.2` và add-on provider Deno đi kèm.
- Thêm Media Session cho metadata, màn hình khóa, tai nghe và các lệnh play/pause/next/previous/seek trên trình duyệt hỗ trợ.
- Tìm kiếm theo block 40 kết quả, tái sử dụng các trang đã tải và giới hạn cache ở 32 truy vấn.
- Nâng Flask lên 3.1.3, Gunicorn lên 26.1.0 và Requests lên 2.34.2.

## 2.4.1 - 2026-08-24

- Thay icon add-on bằng logo YouTube do người dùng cung cấp và chuyển sang PNG vuông 128×128 đúng chuẩn Home Assistant.

## 2.4.0 - 2026-08-21

- Cast loa ưu tiên URL audio trực tiếp tương thích với bản gốc, gửi stream dạng `BUFFERED` và tự chuyển sang relay LAN nếu lệnh direct thất bại.
- Sửa relay audio để tự nhận IP LAN từ Supervisor, hỗ trợ `HEAD`, HTTP Range, CORS và `Content-Disposition: inline`, giúp loa nhận được kích thước stream và dữ liệu audio ổn định hơn.
- Thêm thanh thời gian, trạng thái phát và tua bằng `media_player.media_seek` cho loa Home Assistant hỗ trợ `SEEK`.
- Tăng kích thước artwork trong danh sách và player, đồng thời làm nút điều khiển cast dễ chạm hơn trên điện thoại.

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

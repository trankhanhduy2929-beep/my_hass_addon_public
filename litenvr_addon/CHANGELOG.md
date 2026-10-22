# Changelog

## 1.9.2

- Ghi hình **luôn giữ codec gốc** (`-c:v copy`); lựa chọn H.264 chỉ ép transcode
  cho luồng live. Giảm mạnh CPU/RAM với camera 4K/HEVC.
- Tự khởi động lại ffmpeg camera nếu RSS vượt `CAMERA_MAX_RSS_MB` (mặc định
  900 MB) sau 60 giây grace, chống rò rỉ RAM hoặc ffmpeg phình quá mức.
  Tắt bằng `CAMERA_MAX_RSS_MB=0`; đổi thời gian grace bằng `CAMERA_RSS_GRACE_SEC`.
- Ghim image LiteNVR `dc59509` cho bản phát hành này.

## 1.9.1

- WebRTC ưu tiên **luồng phụ** khi camera đã khai báo, giảm CPU và băng thông
  so với kéo luồng chính.
- Hỗ trợ H.265 trực tiếp qua WebRTC trên Chrome 136+/Safari 18+; trình duyệt
  không hỗ trợ mới quay về HLS chuyển mã.
- Ghi log nguồn WebRTC (`<cam>` hoặc `<cam>_sub`) và lỗi go2rtc để dễ chẩn đoán.
- Thanh trạng thái ghi rõ `WebRTC`, `HLS` hoặc `HLS - H.265 chuyển mã`.
- Ghim image LiteNVR `0586215` cho bản phát hành này.

## 1.9.0

- Tách ba chỉ báo **CPU, RAM, SSD** thành ba thẻ riêng; bấm thẻ nào mở chi tiết
  đúng tài nguyên đó thay vì mở chung một hộp thoại.
- CPU: tải 1/5/15 phút, số nhân, thời gian máy chủ hoạt động và CPU từng camera.
- RAM: container, app, tiến trình con, bộ đệm HLS/motion, page cache và shared memory.
- SSD: dung lượng, số ngày lưu, ngưỡng tự xoá, inode, quyền ghi và SMART.
- Giao diện chi tiết responsive: ba thẻ gọn trên điện thoại, chuyển tab bằng bàn
  phím, giữ focus/ARIA và biểu đồ lịch sử.
- Ghim image LiteNVR `f9e2461` cho bản phát hành này.

## 1.8.9

- Live **WebRTC nhẹ CPU** qua go2rtc nội bộ: camera H.264 được truyền thẳng,
  không chuyển mã; tự quay về HLS khi camera H.265 hoặc cổng WebRTC bị chặn.
- Mở cổng **8556/TCP + 8556/UDP** cho WebRTC; có thể đặt `WEBRTC_PUBLIC_HOST`
  khi truy cập qua tên miền/reverse proxy.
- Live không còn tạo nhánh HLS/ffmpeg khi không có người xem.

## 1.8.8

- Sửa âm thanh live EZVIZ/Hikvision: luồng HLS tự chuyển audio sang AAC và có nút
  bật/tắt tiếng cạnh nút Trực tiếp.
- Lưu bản ghi trực tiếp ra SMB/Samba/CIFS hoặc FTP/FTPS, không cần mount share;
  chọn "Xoá bản gốc" để chỉ giữ dữ liệu trên máy chủ ngoài.
- Thư mục lưu ngoài và Google Drive tự chia theo ngày `YYYY-MM-DD` cho dễ tìm.

## 1.8.7

- Trỏ add-on sang image LiteNVR tại repository mới `litenvr_docker_zimaos`.

## 1.8.6

- Giảm RAM phình sau nhiều giờ: chuyển cache thumbnail khỏi tmpfs, dọn HLS/buffer
  mồ côi mỗi phút, giải phóng page cache của segment đã ghi và giảm đệm motion.

## 1.8.5

- Giữ 10 giây trước sự kiện chuyển động: đệm được đẩy xuống bản ghi ngay khi
  phát hiện chuyển động, clip không còn mất đoạn đầu.

## 1.8.4

- Ghim image LiteNVR theo đúng bản phát hành để add-on nhận giao diện chip CPU/RAM/SSD gọn.
- Sửa camera đúng camera đang chọn; không tự nhảy sang camera khác hoặc lưu đè camera cũ.
- Khóa mã camera khi sửa, xóa sạch form khi thêm mới và giữ nguyên tab/camera đang xem.

## 1.8.3

- Gộp CPU, RAM và SSD thành chip gọn trên thanh trên; bấm để mở chi tiết tài nguyên.
- Cập nhật thông số mỗi giây và biểu đồ lịch sử CPU/RAM/SSD mỗi 2 giây.
- Backend dùng mẫu thống kê dùng chung, có khóa luồng để tránh đọc lệch số liệu.

## 1.8.2

- Khôi phục các hộp thoại **Lưu trữ**, **Google Drive** và **Nhật ký** bị thiếu
  trong menu Cài đặt.
- Bỏ mục **Test Motion** khỏi menu Cài đặt.
- Thêm hiệu ứng chuyển cảnh mượt khi chuyển trực tiếp/xem lại, lưới camera,
  đổi camera hoặc đổi ngày; tự tắt khi bật giảm chuyển động.

## 1.8.1

- Bỏ nút **i** và hộp thoại hướng dẫn trong ứng dụng; hướng dẫn cài đặt add-on
  được chuyển thành tài liệu từng bước trong `README.md`.
- Sửa lỗi ảnh sự kiện lúc có lúc không: snapshot được ghi ra file tạm rồi đổi tên
  nguyên tử, sự kiện chỉ trỏ tới ảnh đã tồn tại, ảnh chụp nền tự cập nhật vào sự kiện.
- Ưu tiên lấy frame tức thời từ go2rtc khi khả dụng; giữ ffmpeg làm phương án dự phòng.

## 1.8.0

- Giảm độ trễ xem trực tiếp: HLS dùng segment **1 giây**, playlist **4 segment**,
  trình duyệt bắt đầu gần live edge và FFmpeg ép keyframe đúng nhịp segment khi chuyển mã.
  Độ trễ thực tế thường còn khoảng **1–4 giây** thay vì 10–15 giây.
- Sửa độ tương phản giao diện tối/sáng: chữ phụ, nền kính, nút nhấn mạnh, ngày đang chọn,
  nhãn cảnh báo và màu nhấn tuỳ chỉnh đều đạt mức đọc tốt hơn.
- Gọn **Quản lý Camera**: giao thức, codec, lịch ghi, thời gian lưu và cảm biến
  Home Assistant được gom vào **⚙️ Tùy chọn nâng cao**, tự mở khi sửa camera đã có cấu hình.
- Thêm nút **i** cạnh Cài đặt với hướng dẫn cài đặt chi tiết: tab Home Assistant Add-on
  và tab Docker/Compose (cổng, biến môi trường, lưu trữ, sao lưu, HTTPS, xử lý sự cố).
- Cập nhật tài liệu độ trễ HLS, cổng add-on 3333 và quy trình cài đặt.

## 1.7.0

- Tách **Quản lý Camera** thành hai tab: **Tự động dò ONVIF** và **Nhập URL thủ công**;
  tab thủ công có preset Imou/Dahua, EZVIZ/Hikvision và Hanet, giữ nguyên thêm hàng loạt.
- Đổi cổng add-on sang **3333** cho Ingress, Web UI và ánh xạ host; cập nhật watchdog,
  healthcheck và tài liệu. **Lưu ý:** truy cập trực tiếp đổi từ `8099` sang `3333`.
- Bảo mật: mật khẩu add-on **bắt buộc tối thiểu 12 ký tự** và không dùng mật khẩu đã rò rỉ;
  bỏ mặc định rỗng/`admin`, sửa cảnh báo pwned password của Home Assistant. Người dùng đang
  dùng mật khẩu yếu cần đổi trước khi khởi động bản 1.7.0.

## 1.6.0

- Tự dò camera ONVIF và **tự thêm hàng loạt**: chọn nhiều camera, nhập tài khoản ONVIF
  một lần, LiteNVR tự lấy luồng chính/phụ, tên, hãng rồi thêm vào danh sách.
- Thêm **quét dải IP nội bộ** (`192.168.1.0/24` hoặc khoảng IP) cho trường hợp Docker
  bridge chặn multicast; quét các cổng ONVIF phổ biến và bỏ qua camera đã có.
- Hỗ trợ thêm nhanh camera Reolink, Uniview, Foscam, Amcrest, Imou/Dahua, Hikvision/EZVIZ,
  Tapo, Yoosee, Xiaomi và thiết bị ONVIF chung; giữ nguyên cách nhập RTSP thủ công.
- Sửa lỗi dò ONVIF không tìm thấy camera trong một số môi trường mạng; nhận diện đúng
  thiết bị yêu cầu Basic/Digest và không nhầm web server 401 thành camera ONVIF.

## 1.5.0

- Dòng thời gian có thể thu phóng 24 giờ / 6 giờ / 1 giờ, nút lùi/tới khung giờ; kéo,
  chạm hoặc lăn chuột tua chính xác theo khung đang xem và tự bám theo lúc phát lại.
- Tìm sự kiện trên điện thoại nhanh hơn: nút Hôm nay / 7 ngày / 30 ngày, chip bỏ từng
  bộ lọc, nhóm kết quả theo ngày, ảnh tải dần và tự tải thêm khi cuộn. Sửa lỗi đổi camera
  trong bộ lọc chưa áp dụng ngay.
- Bấm sự kiện để xem chi tiết: ảnh lớn, camera, ngày giờ, nhãn, mã sự kiện; xem lại trên
  dòng thời gian, tải ảnh JPG hoặc tải clip quanh sự kiện.
- Thanh bộ lọc trên máy tính gọn hơn, vẫn giữ đủ camera, nhãn, khoảng ngày và đánh dấu.

## 1.4.9

- Thu gọn bộ lọc tìm sự kiện trên điện thoại: ô tìm kiếm và nút "Bộ lọc" nằm một hàng,
  các bộ lọc camera/nhãn/ngày chỉ mở khi cần, hiện số bộ lọc đang bật; không còn chiếm
  nhiều dòng và gây rối màn hình nhỏ. Bố cục máy tính giữ nguyên.

## 1.4.8

- Thu gọn thanh CPU / RAM / ổ cứng trên điện thoại thành 3 thẻ nhỏ một hàng, ẩn biểu đồ
  phụ và giữ số liệu, thanh % dễ đọc; không còn chiếm nhiều chiều cao.
- Sửa chữ bị chìm trong chế độ sáng: nhãn, mô tả, trạng thái và màu cảnh báo dùng biến
  màu theo giao diện; nền thanh % và bóng thẻ cũng đổi theo sáng/tối.

## 1.4.7

- Thêm lịch tháng đánh dấu ngày có bản ghi (ổ cứng và Drive), bấm để nhảy nhanh.
- Thêm nút sự kiện trước/sau (⏮/⏭) và phím mũi tên ←/→ để nhảy giữa các sự kiện.
- Cảnh báo Telegram/webhook (dùng được webhook Home Assistant) khi camera đang ghi hình
  mất kết nối quá 60 giây, báo lại khi kết nối phục hồi; thẻ camera hiện nhãn đỏ.
- Nút "Kiểm tra" URL camera trong lúc thêm/sửa: báo codec, độ phân giải, fps và khả năng
  phát trực tiếp trước khi lưu.

## 1.4.6

- Thêm nút lùi/tới ngày (giữ Shift để nhảy 7 ngày) và nút về hôm nay ngay trên thanh
  công cụ; thanh thời gian hiện ngày đang xem khi xem lại lịch sử.
- Camera vừa thêm được chọn và phát ngay, tự chờ luồng HLS sẵn sàng thay vì báo lỗi;
  hiện rõ lỗi nếu lưu camera thất bại.

## 1.4.5

- Menu Cài đặt tự ẩn nhóm trống theo quyền người dùng; sửa bố cục menu trên điện thoại
  (không còn khoảng trống lớn, không tràn ngang).

## 1.4.4

- Gọn lại thanh công cụ: nhóm menu Cài đặt theo Camera / Lưu trữ / Kết nối / Hệ thống,
  gộp công cụ giao diện vào một menu, thu gọn nhóm công cụ phát lại và ẩn bảng xuất clip
  sau nút "Xuất clip".

## 1.4.3

- Xem lại bản ghi Drive: phát hiện kết nối bị treo sớm (20 giây) và tự tải tiếp, hiện
  tổng dung lượng ngay khi bắt đầu tải, báo "đang kết nối lại…" nếu chưa có dữ liệu.
- Sửa trạng thái bị gán nhầm khi quay lại xem trực tiếp ngay sau khi mở bản ghi.

## 1.4.2

- Xem lại bản ghi trên Google Drive không còn đứng ở "Đang tải… x%": tự tải tiếp khi
  kết nối đứt, phát hiện file tải thiếu và không coi là hoàn chỉnh.
- Thanh trạng thái hiện đúng tiến độ và cập nhật lại khi phát (kể cả camera H.265
  phải chuyển mã), kèm cảnh báo khi đang kết nối lại.

## 1.4.1

- Giao diện mượt hơn: modal/menu mở và đóng có hiệu ứng, thẻ có phản hồi hover,
  đổi theme chuyển màu êm; tôn trọng tuỳ chọn giảm chuyển động của hệ thống.

## 1.4.0

- Bỏ dò chuyển động nội bộ bằng CPU (ffmpeg scene-detect): chuyển động giờ nhận
  từ cảm biến Home Assistant, ONVIF/PTZ hoặc bộ nhận diện AI bên ngoài qua webhook.

## 1.3.0

- Cảm biến chuyển động Home Assistant: tải danh sách cảm biến kèm trạng thái và chọn
  điều kiện kích hoạt, chỉ ghi hình khi cảm biến chuyển sang trạng thái kích hoạt
  (hết ghi liên tục khi cảm biến giữ nguyên).

## 1.2.0

- Đánh dấu sự kiện, lọc theo nhãn và phân trang khi tìm lại bản ghi.
- Hạn mức dung lượng mỗi camera; tự tạm dừng ghi khi ổ trống thấp và ghi lại khi đủ chỗ.
- Xem danh sách phiên đăng nhập và đăng xuất các phiên khác.

## 1.1.0

- Thêm Ingress: hiển thị LiteNVR trực tiếp trong sidebar Home Assistant (bật "Show in sidebar" trên trang add-on).
- Ứng dụng dùng URL tương đối nên chạy đúng cả trong Ingress lẫn truy cập trực tiếp qua cổng 8099.

## 1.0.1

- Kích hoạt build lại để xuất bản ảnh add-on qua release pipeline.

## 1.0.0

- Bản phát hành đầu tiên: đóng gói LiteNVR thành add-on Home Assistant.
- Ánh xạ tuỳ chọn (tài khoản, múi giờ, iframe, go2rtc, FFmpeg, log) sang LiteNVR.
- Trỏ `/storage` vào `media`/`share`/`data` để bản ghi bền vững.
- Mở giao diện web qua cổng host và watchdog `/health`.

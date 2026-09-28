# Camera Drive Storage (add-on)

Ghi hình camera RTSP/ONVIF liên tục hoặc theo chuyển động, lưu vào Google
Drive, thư mục media Home Assistant, hoặc NAS đã gắn — điều khiển hoàn toàn
bằng giao diện web trong bảng điều khiển Home Assistant. Xem lại clip đã lưu
ngay trong trình duyệt.

## Add-on làm gì

- Ghi RTSP/ONVIF theo chế độ **liên tục** hoặc **theo chuyển động** (ONVIF
  event hoặc phân tích hình ảnh).
- Mỗi clip được chuyển đến một hoặc nhiều đích: **Google Drive**, **Local
  HA** (thư mục media), **NAS đã gắn**.
- Xem lại clip trên Drive / Local / NAS theo ngày và camera, phát trực tiếp
  trong trình duyệt hoặc tải xuống.
- Phát hiện thực thể tự động qua MQTT: cảm biến chuyển động, đang ghi, clip
  cuối, số clip đã tải lên.

## Cài đặt

1. Sao chép thư mục `camera_drive_storage` vào `/addons/` trên máy Home
   Assistant.
2. **Settings → Add-ons → Add-on Store → ⋮ → Check for updates** → cài
   "Camera Drive Storage".
3. Start add-on. Mở panel "Camera Storage" từ thanh bên (icon
   `mdi:cctv`).

## Bắt đầu nhanh — checklist

1. Mở tab **Camera** → thêm camera (xem mục URL bên dưới) → lưu.
2. Tab **Nơi lưu** → bật đích lưu muốn dùng: Drive / Local HA / NAS → lưu.
3. Nếu chọn **Google Drive**: tab **Gói Drive** → nhập key (hoặc dùng thử
   24 giờ) → tab **Nơi lưu** → bấm **Kết nối Google Drive** → cho phép
   truy cập.
4. Quay lại tab **Tổng quan**: camera chuyển `Đang ghi`, số clip đã lên đích
   tăng dần. Tab **Xem lại** để phát clip.

## URL camera và tài khoản

Add-on cần **đường RTSP** (hoặc **ONVIF service URL**) của camera. Lấy từ
tài liệu hãng, ứng dụng cấu hình camera, hoặc dùng mẫu sẵn có.

- Trong tab **Camera** chọn **Thêm camera theo hãng** — chọn hãng, nhập IP /
  user / pass / kênh, add-on tự dựng đúng dạng URL.
- Hoặc dán tay một URL quen thuộc, ví dụ:
  `rtsp://192.168.1.10:554/...`, `onvif://192.168.1.10:80/onvif/device_service`.
- Nếu form có ô **username/password riêng**, nhập vào đó — **không** chèn
  mật khẩu vào URL (và không để mật khẩu lộ trong ảnh chụp màn hình khi hỏi
  hỗ trợ).
- Mật khẩu có ký tự đặc biệt sẽ được mã hóa an toàn khi cần.
- Camera chỉ có ONVIF: add-on tự lấy link RTSP bên trong, không cần nhập
  tay.

## Kết nối Google Drive

Không cần tạo Google Cloud project, không cần client_id/secret, không dán
mã xác thực.

1. Tab **Nơi lưu** → bấm **Kết nối Google Drive**.
2. Trình duyệt mở trang cấp quyền của Google — đăng nhập tài khoản muốn
   dùng và **Cho phép**.
3. Google chuyển về **camera portal** (trang trung gian do add-on cung cấp),
   portal chuyển tiếp kết quả về add-on của bạn.
4. Quay lại tab **Nơi lưu**: tài khoản và hạn mức hiện ra, thư mục lưu mặc
   định `HomeAssistantCameras` sẽ được tạo khi clip đầu tiên tải lên.

Quyền `drive.file`: add-on chỉ nhìn thấy các file do chính nó tạo trong
Drive của bạn. Token OAuth chỉ nằm trong add-on trên máy Home Assistant —
không lưu ở portal, không gửi đi nơi khác.

Nút **Ngắt kết nối** xoá token và dừng tải lên Drive; clip vẫn ghi và vẫn
đi đến các đích Local/NAS.

## Nơi lưu clip — Drive, Local HA, NAS

Mỗi clip được chuyển đến mọi đích đã bật trong tab **Nơi lưu** (Drive,
Local HA & NAS).

- **Google Drive** — cần license hợp lệ và đã kết nối OAuth.
- **Local HA** — mặc định lưu trong `/media/camera_drive_storage`. Truy cập
  qua **Media → camera_drive_storage** hoặc Samba/Studio Code.
- **NAS đã gắn** — chọn đường dẫn con trong một share NFS/CIFS do Home
  Assistant tự mount: **Settings → System → Storage → Add network
  storage**, chọn kiểu **Media** (thấy dưới `/media/<tên>`) hoặc **Share**
  (dưới `/share/<tên>`), rồi nhập đường đó vào ô NAS của add-on, ví dụ
  `/media/nas_name/camera_drive_storage`. Add-on không tự mount NAS và
  không giữ credential NAS.

Clip nguồn chỉ bị xoá khỏi bộ đệm tạm sau khi **mọi** đích đã xác nhận nhận
được file. Nếu một đích hỏng (NAS mất kết nối, Drive hết quota, v.v.) clip
vẫn ở bộ đệm và thử lại — không mất dữ liệu.

**Lưu ý quan trọng:** Local HA và NAS là **kho lưu trữ** — add-on không tự
xoá. Bạn tự dọn khi muốn. Chỉ Drive có chính sách tự xoá (xem dưới).

## Dọn dẹp Google Drive

Ba cài đặt trong tab **Cài đặt** quyết định khi nào Drive được dọn:

- **Giữ bao nhiêu ngày** — xoá clip cũ hơn N ngày.
- **Giới hạn dung lượng** — xoá clip cũ nhất cho tới khi dưới mức đặt.
- **Xoá vĩnh viễn** — xoá thẳng, bỏ qua Thùng rác Drive.

> **Cảnh báo:** nếu không bật **Xoá vĩnh viễn**, file bị xoá chỉ vào
> **Thùng rác Google Drive** và **vẫn chiếm quota** cho tới khi bạn tự dọn
> thùng rác hoặc Drive tự xoá sau 30 ngày. Bật tuỳ chọn này nếu muốn add-on
> giải phóng dung lượng thật.

Add-on chỉ xoá các clip do chính nó tạo trong thư mục gốc, không đụng file
khác của bạn.

## License

- **Local HA và NAS miễn phí**, không cần license — add-on vẫn ghi và lưu
  đầy đủ.
- **Google Drive** là đích trả phí; cần License Key để bật upload.
- **Dùng thử 24 giờ** một lần duy nhất cho mỗi tài khoản + mỗi cài đặt,
  bắt đầu từ lúc kích hoạt.
- Gói trả phí: **50.000đ/tuần** hoặc **200.000đ vĩnh viễn**.

Kích hoạt:

1. Tab **Gói Drive** → bấm **Mua / quản lý license** → mở portal.
2. Đăng ký bằng email + mật khẩu.
3. Claim **Dùng thử 24 giờ** hoặc thanh toán PayOS QR cho gói tuần /
   vĩnh viễn.
4. Sau khi portal xác nhận, key `CC-…` hiện trong dashboard.
5. Dán key vào ô **License Key** trong add-on → **Kích hoạt**.

Một key gắn với **một** cài đặt Home Assistant; chuyển sang máy khác cần
admin reset. Khi license hết hạn hoặc bị thu hồi: ghi hình và lưu Local/NAS
vẫn chạy, clip chờ upload Drive giữ nguyên trong bộ đệm và sẽ tải lên khi
kích hoạt lại. Kích hoạt lại không cần restart Home Assistant.

## Troubleshooting

| Triệu chứng | Nút / nơi xử lý |
|---|---|
| Không kết nối được Google Drive, báo phiên hết hạn | Tab **Nơi lưu** → **Kết nối Google Drive** lại |
| Drive hiển thị tài khoản nhưng clip chưa lên | Tab **Tổng quan** → xem cột trạng thái tải lên; clip vẫn ở bộ đệm, chờ hoặc thử lại — đừng ngắt kết nối |
| Drive báo hạn mức / quá nhiều yêu cầu | Đợi — add-on tự giãn nhịp và thử lại; nếu kéo dài, kiểm tra quota Drive của tài khoản |
| Drive báo hết dung lượng | Dọn Drive hoặc bật **Giới hạn dung lượng** + **Xoá vĩnh viễn** trong **Cài đặt** |
| Google bắt đăng nhập lại / quyền đã bị thu hồi | Tab **Nơi lưu** → **Kết nối Google Drive** lại |
| Clip chờ license | Tab **Gói Drive** → nhập key hợp lệ hoặc dùng thử |
| NAS không ghi được / báo đường dẫn không hợp lệ | Kiểm tra share đã được HA mount trong **Settings → System → Storage**, đường dẫn NAS phải nằm trong share đó |
| Add-on tạm dừng ghi vì bộ đệm đầy | Giải phóng dung lượng đĩa hoặc chờ các đích nhận clip rồi ghi tiếp |
| Camera báo lỗi / không thấy clip mới | Tab **Camera** → **Test kết nối** xem lỗi cụ thể (sai URL, sai mật khẩu, camera offline) |
| Xem lại không ra clip | Tab **Xem lại** → chọn đúng nguồn (Drive / Local / NAS) và tháng có dữ liệu |
| Muốn xoá liên kết Google | Tab **Nơi lưu** → **Ngắt kết nối** |

## Bảo mật & riêng tư

- Clip camera chỉ đi từ Home Assistant **thẳng** đến Google Drive, Local
  HA, hoặc NAS — không qua trung gian.
- Portal kết nối Google chỉ **chuyển tiếp phiên OAuth** giữa Google và
  add-on của bạn; token OAuth và video không lưu trên portal.
- Portal license chỉ kiểm tra trạng thái key — không nhận nội dung video,
  không nhận credential camera.
- Thông tin thanh toán (PayOS) xử lý ngoài add-on, không đi vào add-on.

## Gỡ cài đặt

Trước khi gỡ add-on:

- Clip đã lên Drive / Local / NAS **giữ nguyên** — chỉ dữ liệu nội bộ của
  add-on (bộ đệm tạm, token OAuth, license key, cấu hình) bị xoá.
- Nếu muốn giữ định danh license cho lần cài lại, lưu key `CC-…` ra ngoài
  trước.
- Ngắt kết nối Google trong tab **Nơi lưu** trước khi gỡ nếu muốn thu hồi
  token OAuth ngay lập tức; hoặc vào tài khoản Google → Bảo mật → ứng
  dụng bên thứ ba để thu hồi tay.

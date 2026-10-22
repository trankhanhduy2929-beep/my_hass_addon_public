# LiteNVR — tài liệu add-on

Add-on này gói sẵn LiteNVR và chạy máy chủ web trong Home Assistant. Bản thân
LiteNVR là một NVR độc lập; add-on chỉ lo việc khởi động, ánh xạ tuỳ chọn Home
Assistant sang biến môi trường và trỏ nơi lưu trữ vào thư mục bền vững.

## Cài đặt A–Z

### 1. Chuẩn bị

- Home Assistant OS hoặc Home Assistant Supervised, kiến trúc `amd64`/`aarch64`.
- Home Assistant truy cập được camera qua LAN.
- Có dung lượng trống cho số ngày ghi hình mong muốn.
- Một mật khẩu mới, dài tối thiểu 12 ký tự, không dùng lại mật khẩu Home Assistant.

### 2. Thêm kho add-on

1. Mở **Settings → Add-ons → Add-on Store**.
2. Bấm **⋮** (góc phải) → **Repositories**.
3. Dán `https://github.com/trankhanhduy2929-beep/my_hass_addon_public` → **Add** → đóng hộp thoại.
4. Tìm **LiteNVR** trong Add-on Store.

### 3. Cài và cấu hình add-on

1. Mở **LiteNVR** → **Install**, chờ tải image xong.
2. Sang tab **Configuration**, điền tối thiểu:
   - `username`: tài khoản quản trị, ví dụ `admin`.
   - `password`: mật khẩu mạnh, tối thiểu 12 ký tự.
   - `timezone`: ví dụ `Asia/Ho_Chi_Minh`.
   - `storage_location`: `media` (mặc định), `share` hoặc `data`.
3. Bấm **Save**.

### 4. Khởi động và mở giao diện

1. Tab **Info** → **Start**.
2. Xem tab **Log** đến khi LiteNVR báo khởi động thành công.
3. Bật **Show in sidebar**, hoặc bấm **OPEN WEB UI**.
4. Truy cập trực tiếp (tuỳ chọn): `http://IP_HOME_ASSISTANT:3333`.
5. Đăng nhập bằng `username`/`password` ở bước 3.

### 5. Thêm camera

1. Trong LiteNVR, mở **+ Quản lý Camera**.
2. Dò ONVIF hoặc nhập URL RTSP thủ công; nhập tài khoản camera nếu cần.
3. Lưu camera, kiểm tra live và trạng thái ghi hình.
4. Camera H.265 nên khai báo thêm luồng phụ H.264 để live nhẹ CPU.

### 6. Chọn nơi lưu và kiểm tra ghi hình

- Vào **⚙️ → Tùy chọn nâng cao** để đặt chế độ ghi, lịch ghi và số ngày lưu.
- Bảng **CPU/RAM/SSD** giúp kiểm tra tải hệ thống và dung lượng trống.
- Khi ổ gần đầy, LiteNVR tự dọn bản ghi cũ theo chính sách lưu trữ; có thể bật
  Google Drive hoặc SMB để giữ bản sao.

### 7. Sao lưu Google Drive

Xem hướng dẫn đầy đủ ở mục [Google Drive từng bước](#google-drive-từng-bước) bên dưới.

### 8. Sao lưu và xem lại từ SMB/Samba

Xem mục [SMB/Samba từng bước](#smbsamba-từng-bước) bên dưới.

### 9. Xem lại bản ghi theo nguồn

Trong LiteNVR, ngay trên dòng thời gian có ô **Nguồn phát**:

| Lựa chọn | Dùng khi |
| --- | --- |
| `Tự động (ổ gốc + Drive)` | Mặc định; ưu tiên file trên ổ gốc, bổ sung đoạn chỉ còn trên Drive. |
| `Chỉ ổ gốc` | Chỉ xem bản ghi còn trên ổ cứng của add-on. |
| `Chỉ Google Drive` | Chỉ hiện các đoạn đã tải lên Drive; bấm xem sẽ tải về ổ cứng trước khi phát. |
| `Chỉ SMB/Samba` | Đọc trực tiếp file đã sao lưu lên share SMB; hỗ trợ tua bằng Range. |

Chọn nguồn trước khi tua/xem; LiteNVR tải lại dòng thời gian theo nguồn đó. Nếu
nguồn không có bản ghi, dòng thời gian trống thay vì tự phát từ nguồn khác.

### 10. Cập nhật add-on

1. Tạo bản sao lưu Home Assistant trước khi cập nhật.
2. **Settings → Add-ons → LiteNVR → Info → Update**.
3. Chờ add-on khởi động lại, kiểm tra **Log** rồi mở giao diện.
4. Nếu giao diện còn cache cũ, nhấn `Ctrl+F5`.

## Cổng và truy cập

- Add-on dùng **Ingress**: LiteNVR hiện ngay trong giao diện Home Assistant. Trên
  trang add-on, bật **Show in sidebar** để ghim LiteNVR vào thanh bên và xem trực
  tiếp trong Home Assistant. Nút **OPEN WEB UI** cũng mở qua Ingress.
- Giao diện web LiteNVR lắng nghe cổng **3333** trong container và mở ra ngoài ở
  cổng host **3333** nếu muốn truy cập trực tiếp (dùng cùng đăng nhập bên dưới).
- WebRTC dùng cổng **8556/TCP + 8556/UDP** (mở/forward cả hai khi truy cập ngoài
  LAN), ưu tiên luồng phụ nếu camera đã khai báo. Camera H.264/H.265 được truyền
  thẳng trên trình duyệt hỗ trợ; không mở được cổng hoặc trình duyệt không hỗ trợ
  H.265 thì live tự quay về HLS.
- Có thể nhúng bằng thẻ dashboard khi bật tuỳ chọn **iframe**.
- Tài khoản mặc định là `admin`; **mật khẩu bắt buộc tối thiểu 12 ký tự** và không
  được là mật khẩu đã xuất hiện trong dữ liệu rò rỉ. Home Assistant sẽ từ chối giá
  trị yếu/rỗng. Dùng mật khẩu riêng, dài và duy nhất cho add-on.

## Độ trễ xem trực tiếp

LiteNVR dùng HLS segment **1 giây**, playlist **4 segment** và trình duyệt bắt đầu
gần live edge. Khi camera phải chuyển mã H.265/HEVC sang H.264, FFmpeg tự ép
keyframe đúng nhịp segment để không phải chờ GOP dài. Độ trễ thực tế thường khoảng
**1–4 giây**; camera có GOP dài hoặc mạng Wi-Fi yếu có thể cao hơn. Nếu cần ổn định
hơn, dùng luồng phụ H.264 cho live và hạ `live_max_height`.

## Tuỳ chọn

| Tuỳ chọn | Mặc định | Ý nghĩa |
| --- | --- | --- |
| `auth_enabled` | `true` | Bắt đăng nhập trước khi dùng giao diện. |
| `username` | `admin` | Tài khoản đăng nhập web. |
| `password` | (bắt buộc) | Mật khẩu web, tối thiểu 12 ký tự; không dùng mật khẩu đã rò rỉ. |
| `iframe` | `true` | Cho nhúng giao diện vào iframe / thẻ dashboard. |
| `timezone` | (trống) | Múi giờ IANA, ví dụ `Asia/Ho_Chi_Minh`. |
| `log_level` | `info` | Mức log máy chủ web (`debug`/`info`/`warning`/`error`). |
| `go2rtc` | `auto` | Chế độ go2rtc: `auto`, `on`, `off`; `auto`/`on` bật WebRTC. |
| `ffmpeg_threads` | `2` | Số luồng cấp cho mỗi tiến trình FFmpeg. |
| `live_max_height` | `720` | Hạ chiều cao khung xem trực tiếp (pixel). `0` giữ nguyên. |
| `storage_location` | `media` | Nơi lưu cấu hình và bản ghi: `data`, `media`, `share`. |

## Nơi lưu trữ

LiteNVR lưu cấu hình, cơ sở dữ liệu và bản ghi vào `/storage`, được add-on trỏ
tới `<storage_location>/litenvr`:

- `media` → `/media/litenvr` (mặc định, hiện trong Media của Home Assistant, **không** vào bản sao lưu add-on).
- `share` → `/share/litenvr`.
- `data` → `/data/litenvr` (bền vững nhưng **có** nằm trong bản sao lưu add-on — tránh dùng cho ổ ghi hình lớn).

Add-on cần quyền ghi vào `media` và `share` (đã khai báo trong cấu hình).

## Kết nối camera

- **Quản lý Camera** có hai tab: **Tự động dò ONVIF** và **Nhập URL thủ công**.
  Camera phải nằm trong cùng mạng mà Home Assistant truy cập được.
- **Nhập URL thủ công** có preset cho Imou/Dahua (`/cam/realmonitor?channel=1&subtype=0`),
  EZVIZ/Hikvision (`/h264/ch01/main/av_stream`) và Hanet
  (`rtsp://ip:554/user:<user>;pwd:<pass>`).
- **Tự dò và thêm ONVIF**: mở **Quản lý Camera** → **Dò camera ONVIF**. Nếu add-on
  chạy trong Docker bridge và không nhận multicast, nhập dải IP LAN (ví dụ
  `192.168.1.0/24`) rồi bấm **Quét dải IP**. Chọn các camera tìm thấy, nhập tài khoản
  ONVIF một lần và bấm **Thêm camera đã chọn**; LiteNVR tự lấy luồng chính/phụ, tên,
  hãng và bỏ qua camera đã có trong cấu hình.
- Nếu camera không xuất hiện khi quét, nhập trực tiếp IP/cổng ONVIF ở ô **Hoặc nhập IP
  ONVIF**, bấm **Lấy luồng RTSP**, kiểm tra URL rồi lưu camera.
- Gắn **cảm biến chuyển động Home Assistant** cho từng camera: mọi thay đổi trạng
  thái của cảm biến đều kích hoạt ghi hình + ảnh chụp (không cần ONVIF).

## Google Drive từng bước

LiteNVR dùng OAuth **device flow** và chỉ xin quyền `drive.file` (chỉ thấy file do
chính LiteNVR tạo). Add-on không kèm OAuth client; bạn tự tạo trong Google Cloud.

### Phía Google Cloud

1. Mở <https://console.cloud.google.com>, đăng nhập đúng tài khoản Google sẽ chứa
   bản ghi Drive.
2. Tạo hoặc chọn một dự án (ví dụ `litenvr-nvr`).
3. Vào **APIs & Services → Library**, tìm **Google Drive API**, bấm **Enable**.
4. Cấu hình màn hình đồng ý:
   - **APIs & Services → OAuth consent screen** (Google mới có thể gọi là
     **Google Auth Platform**).
   - **Branding**: nhập tên ứng dụng (ví dụ `LiteNVR`), email hỗ trợ, email liên hệ.
   - **Audience**: chọn **External** cho tài khoản Google cá nhân; **Internal** nếu
     dùng Google Workspace cùng tổ chức.
   - Nếu đang ở **Testing**, thêm địa chỉ Google của bạn vào **Test users**.
   - **Data access**: thêm scope `https://www.googleapis.com/auth/drive.file` nếu
     giao diện yêu cầu.
   - Nên bấm **Publish app** để chuyển sang **In production**. Ở chế độ Testing,
     Google có thể hết hạn refresh token sau khoảng 7 ngày, khiến backup dừng và
     phải kết nối lại. Nếu Google yêu cầu xác minh, làm theo hướng dẫn trên màn hình.
5. Vào **APIs & Services → Credentials → Create credentials → OAuth client ID**.
   - **Application type**: chọn **TVs and Limited Input devices**.
   - Đặt tên, ví dụ `LiteNVR device`.
   - Bấm **Create**, sao chép **Client ID** và **Client secret**.
   - Không cần thêm Redirect URI cho loại client này.
6. Không chọn nhầm **Web application** hoặc **Desktop app**: LiteNVR gọi
   `/device/code` nên cần đúng loại **TVs and Limited Input devices**.

### Phía LiteNVR / Home Assistant

1. Mở giao diện LiteNVR bằng tài khoản quản trị.
2. Bấm **☁️ Google Drive** trên thanh công cụ.
3. Dán **Client ID** và **Client secret** vừa tạo.
4. Bấm **🔗 Kết nối bằng mã thiết bị**.
5. Mở địa chỉ Google hiện ra (thường là `https://www.google.com/device`), nhập mã
   thiết bị, chọn đúng tài khoản Google và bấm **Allow/Cho phép**.
6. Quay lại LiteNVR, chờ trạng thái **Đã kết nối Google Drive**. LiteNVR tự tạo
   thư mục gốc `LiteNVR` trên Drive.
7. Bấm **🔎 Kiểm tra kết nối** để xác nhận quyền và xem dung lượng còn trống.
8. Bật **Bật sao lưu bản ghi lên Google Drive**.
9. Chọn camera cần sao lưu, đặt:
   - **Giới hạn dung lượng NVR dùng (GB)**: `0` = chỉ dọn khi Drive gần đầy.
   - **Dọn file cũ nhất khi Drive còn trống dưới (MB)**: ngưỡng an toàn.
   - **Giới hạn tốc độ tải lên (Mbps)**: `0` = không giới hạn; đặt `1`–`10` Mbps
     nếu đường truyền yếu.
10. Bấm **💾 Lưu cài đặt**.
11. Bấm **🔼 Tải lên ngay** để đưa bản ghi cũ trong khoảng ngày lên Drive, hoặc chờ
    LiteNVR tự sao lưu các đoạn mới.
12. Kiểm tra danh sách file và trạng thái trong cùng cửa sổ. File trên Drive nằm ở
    `LiteNVR/YYYY-MM-DD/<tên camera>/<tên file>.mp4`.

### Xem lại từ Google Drive

- Trên dòng thời gian, chọn **Nguồn phát → Chỉ Google Drive**.
- Đoạn chỉ còn trên Drive có biểu tượng ☁️. Khi bấm, LiteNVR tải file về ổ cứng
  (có thanh tiến độ) rồi phát; các lần sau file đã có sẵn trên ổ cứng nên phát ngay.
- Không xoá/đổi tên/thay đổi quyền file trong thư mục `LiteNVR` trên Drive khi NVR
  đang quản lý, nếu không sẽ mất khả năng xem lại đoạn đó.
- Drive dùng chung hạn mức với Gmail/Photos. LiteNVR xoá **vĩnh viễn** file cũ nhất
  (không vào thùng rác) khi vượt `max_gb` hoặc khi Drive dưới ngưỡng trống; bản ghi
  trên ổ cứng không bị ảnh hưởng.

### Xử lý lỗi Google Drive

| Hiện tượng | Cách xử lý |
| --- | --- |
| `invalid_client` | Sai Client ID/secret hoặc client không phải **TVs and Limited Input devices**. Tạo lại đúng loại. |
| `invalid_scope` | Scope bị đổi khác `drive.file`; xoá biến `NVR_DRIVE_SCOPE` tuỳ chỉnh hoặc dùng đúng scope mặc định. |
| `access_denied` | Bạn bấm từ chối ở trang Google; kết nối lại và bấm Allow. |
| `expired_token` | Mã thiết bị hết hạn (khoảng 15 phút); bấm kết nối lại để lấy mã mới. |
| Không có `refresh_token` | Xoá quyền cũ tại <https://myaccount.google.com/permissions>, rồi kết nối lại. |
| Backup dừng sau ~7 ngày | Ứng dụng còn ở **Testing**; chuyển **In production** (hoặc dùng Internal) rồi kết nối lại. |
| `401 invalid_grant` | Refresh token bị thu hồi/đổi mật khẩu Google; ngắt kết nối rồi kết nối lại. |
| `403` quota/rate limit | Drive đầy hoặc tải quá nhanh; kiểm tra dung lượng, giảm tốc độ tải lên, chờ rồi thử lại. |
| Đã kết nối nhưng không thấy file | Kiểm tra camera có **Nơi lưu** là Drive/Cả hai, mục camera trong cấu hình Drive, và bấm **Tải lên ngay**. |

### Bảo mật Google Drive

- Client secret và refresh token được lưu trong `config.json` ở thư mục lưu trữ
  LiteNVR (`/media/litenvr`, `/share/litenvr` hoặc `/data/litenvr`). Chỉ cấp quyền
  đọc thư mục này cho người quản trị.
- **⛔ Ngắt kết nối** xoá refresh token khỏi LiteNVR nhưng không xoá file đã tải lên.
- Thu hồi quyền tại <https://myaccount.google.com/permissions> nếu nghi ngờ lộ token;
  sau đó tạo client/refresh token mới.
- Không dán Client secret hoặc refresh token vào chat, issue, log hay ảnh chụp màn hình.

### Cách nâng cao: dán refresh token

Nếu đã có refresh token từ cùng OAuth client, có thể dán vào ô **Refresh token** và
bấm **Kết nối bằng token**. Token phải được tạo bởi đúng **Client ID/secret** đang
nhập. Cách này không cần mã thiết bị nhưng dễ sai nếu token thuộc client khác.

## SMB/Samba từng bước

### Phía NAS/Samba

1. Tạo share, ví dụ `Camera`, và một tài khoản chỉ dùng cho LiteNVR.
2. Cấp quyền **đọc + ghi** cho tài khoản đó (ghi để sao lưu, đọc để xem lại).
3. Bật SMB2/SMB3 nếu có; LiteNVR dùng thư viện `smbprotocol`.
4. Đảm bảo Home Assistant truy cập được `IP_NAS:445`. Không mở SMB ra Internet.

### Phía LiteNVR

1. Mở **💾 Lưu trữ ngoài (SMB/FTP)**.
2. Bật **Lưu trữ ngoài tự động**.
3. Chọn **SMB / Samba / CIFS**.
4. Nhập máy chủ, cổng (mặc định `445`), tên share, tài khoản, mật khẩu; nhập
   domain/workgroup nếu NAS yêu cầu.
5. **Thư mục con** (tuỳ chọn), ví dụ `LiteNVR`.
6. Chọn chế độ:
   - **Sao chép**: giữ file trên ổ cứng và gửi bản sao lên SMB.
   - **Di chuyển**: xoá file trên ổ cứng sau khi sao lưu thành công.
7. Chọn camera cần sao lưu (bỏ trống = tất cả).
8. Bấm **Kiểm tra đích** để LiteNVR lưu cấu hình và ghi thử, sau đó bấm **Lưu**.
9. Đường dẫn trên NAS:
   `\\<host>\<share>\<thư mục con>\YYYY-MM-DD\<cam_id>\<file>.mp4`.
10. Chờ worker sao lưu các đoạn hoàn chỉnh (khoảng 60 giây/lần kiểm tra).

### Xem lại từ SMB/Samba

- Chọn **Nguồn phát → Chỉ SMB/Samba** trên dòng thời gian.
- LiteNVR liệt kê file trong thư mục ngày/camera và phát trực tiếp qua HTTP Range,
  nên có thể tua mà không tải cả file về ổ cứng.
- Chỉ file đã sao lưu bằng chế độ SMB mới xuất hiện. Nếu đang dùng **Thư mục đã mount**
  hoặc FTP, chọn nguồn SMB sẽ trống.
- Trình duyệt cần phát được codec gốc (thường H.264). LiteNVR không chuyển mã H.265
  khi phát trực tiếp từ SMB; hãy dùng luồng phụ H.264 hoặc xem từ ổ gốc/Drive.
- Nếu SMB chậm, tua có thể khựng; kiểm tra mạng LAN, SMB2/3 và tải của NAS.

## Kiểm tra sức khoẻ

Add-on có watchdog gọi `http://[HOST]:[PORT:3333]/health`; Home Assistant tự
khởi động lại add-on nếu nó ngừng phản hồi.

## Ghi chú triển khai

Ảnh add-on được xuất bản tự động thành `ghcr.io/trankhanhduy2929-beep/litenvr_addon`.
Sau lần xuất bản đầu tiên, đặt các gói GHCR sau thành **Public** trong GitHub
Package settings để Home Assistant tải được:

- `litenvr_addon`
- `litenvr_addon-amd64`
- `litenvr_addon-aarch64`

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
| `Chỉ SMB/Samba` | Đọc file đã sao lưu lên share SMB; H.264 an toàn phát trực tiếp bằng Range, H.265/H.264 lạ được cache tạm rồi chuyển mã. |

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
hơn, dùng luồng phụ H.264 cho live và hạ `live_max_height`. Live H.265/HEVC được cap tối đa 576p và dùng 1 thread để giảm RAM.

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
| `live_max_height` | `576` | Hạ chiều cao khung xem trực tiếp (pixel). Camera H.265/HEVC luôn bị cap tối đa 576p và dùng 1 thread để giảm RAM; `0` giữ nguyên mức cap mặc định. |
| `storage_location` | `media` | Nơi lưu cấu hình và bản ghi: `data`, `media`, `share`. |

## Nơi lưu trữ

LiteNVR lưu cấu hình, cơ sở dữ liệu và bản ghi vào `/storage`, được add-on trỏ
tới `<storage_location>/litenvr`:

- `media` → `/media/litenvr` (mặc định, hiện trong Media của Home Assistant, **không** vào bản sao lưu add-on).
- `share` → `/share/litenvr`.
- `data` → `/data/litenvr` (bền vững nhưng **có** nằm trong bản sao lưu add-on — tránh dùng cho ổ ghi hình lớn).

Add-on cần quyền ghi vào `media` và `share` (đã khai báo trong cấu hình).

### Chọn nơi lưu cho từng camera

Trong **Sửa camera → Nơi lưu bản ghi**, tick một hoặc nhiều ô:

- **Ổ gốc**: giữ bản ghi trên ổ NVR.
- **Google Drive**: tải lên Drive nếu đã bật. Bỏ **Ổ gốc** thì bản gốc được xoá sau khi tải xong.
- **SMB/Samba**: sao lưu sang share SMB ở **💾 Lưu trữ ngoài**. Bỏ **Ổ gốc** thì bản gốc được xoá sau khi chuyển xong.

Phải chọn ít nhất một nơi. Nếu chọn cả Drive + SMB mà không giữ ổ gốc, LiteNVR giữ
bản gốc tới khi cả hai đích nhận xong. Camera mới mặc định chỉ lưu **Ổ gốc**. Ô
**Google Drive**/**SMB/Samba** chỉ bật được khi dịch vụ tương ứng đã cấu hình và
đang bật; nếu chưa, camera chỉ lưu ổ gốc.

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

## MQTT Discovery cho camera

LiteNVR có thể tự công bố từng camera thành entity `camera.litenvr_<slug>` qua MQTT
Discovery. Entity chỉ hiển thị **ảnh snapshot**, cập nhật theo chu kỳ hoặc khi có
chuyển động — không truyền video live qua MQTT.

### Chuẩn bị broker

1. **Settings → Add-ons → Add-on Store**, cài và bật **Mosquitto broker**.
2. **Settings → Devices & Services**, bật tích hợp **MQTT** nếu chưa có; broker mặc
   định là `core-mosquitto:1883`.
3. Tạo user riêng cho LiteNVR: **Settings → People → Users → Add user**, không dùng
   tài khoản quản trị. Dùng user/mật khẩu này cho kết nối MQTT.

### Cấu hình trong LiteNVR

1. Mở **🛰️ Home Assistant** → mục **MQTT Discovery**, bật **MQTT Discovery**.
2. **MQTT host**: `core-mosquitto` khi LiteNVR là add-on; hoặc IP Home Assistant nếu
   broker đã mở cổng `1883` ra LAN.
3. Nhập **cổng** `1883`, **tài khoản/mật khẩu MQTT**; bật **TLS** nếu broker yêu cầu.
4. Giữ **Discovery prefix** `homeassistant`, **Base topic** `litenvr`; đặt **chu kỳ
   ảnh** 5–300 giây.
5. Bấm **Kiểm tra MQTT**, sau đó **Lưu**. Entity xuất hiện trong **Settings →
   Devices & Services → MQTT → LiteNVR** sau vài giây.

### Dùng trong dashboard

```yaml
type: picture-entity
entity: camera.litenvr_cam1
camera_view: auto
show_name: true
show_state: false
```

Tên entity lấy theo **ID camera** đã chuẩn hoá: chữ thường, dấu cách/ký tự đặc biệt
thay bằng `_`. Ảnh được publish retained lên `<base_topic>/camera/<slug>/image`,
trạng thái online/offline ở `<base_topic>/status` qua LWT; mất kết nối thì entity
chuyển unavailable.

**Lưu ý:**

- Đây là camera ảnh tĩnh, không có live. Dùng **Generic Camera** với luồng H.264
  (hoặc luồng phụ) nếu cần card live, hoặc mở LiteNVR để xem WebRTC/HLS.
- Tắt MQTT hoặc xoá camera sẽ xoá discovery và ảnh retained tương ứng.
- Nếu đổi `base_topic`/`discovery_prefix`, entity cũ được dọn; thiết bị cũ còn sót
  có thể xoá trong **MQTT → Devices**.
- Mật khẩu MQTT lưu trong `config.json` trên thiết bị và không trả về giao diện; nên
  dùng user MQTT riêng, quyền tối thiểu.

## Live trong Home Assistant (Generic Camera)

MQTT chỉ gửi ảnh snapshot. Để xem live trong Home Assistant, tạo **Generic Camera**
trỏ vào HLS của LiteNVR; entity MQTT vẫn giữ để làm badge/card ảnh.

1. Trong LiteNVR, mở **🛰️ Home Assistant** → **Live trong Home Assistant (Generic
   Camera)**. Nhập địa chỉ HA truy cập được, thường là `http://IP-HA:3333` (add-on đã
   map cổng `3333/tcp`), rồi copy URL live và URL ảnh của camera.
2. Trong HA, vào **Settings → Devices & Services → Add Integration → Generic Camera**:
   - **Stream Source**: dán URL live, dạng
     `http://IP-HA:3333/hls/<camera>/live.m3u8`.
   - **Still Image URL**: dán URL ảnh nếu muốn ảnh tĩnh riêng, dạng
     `http://IP-HA:3333/api/cameras/<camera>/snapshot.jpg`; có thể **để trống** để HA
     tự tạo ảnh từ stream. Endpoint trả 404 nếu camera chưa có snapshot nào.
   - **Username/Password**: điền tài khoản LiteNVR (không phải tài khoản HA). Không
     dán mật khẩu vào URL.
   - Nếu có **Authentication**, chọn **Basic**; **RTSP transport** để mặc định/TCP.
3. Lưu cấu hình, thêm entity Generic Camera vào dashboard bằng card **Picture Glance**
   hoặc **WebRTC Camera**.

**Lưu ý:**

- Dùng **luồng phụ H.264** cho live nếu camera có; H.265 có thể không phát trực tiếp
  trên Chrome và sẽ tốn CPU khi HA chuyển mã.
- Không dùng URL `/api/hassio_ingress/...` cho Generic Camera: URL này gắn phiên đăng
  nhập HA và không phù hợp với ffmpeg.
- Generic Camera dùng Basic Auth; tài khoản LiteNVR cần quyền **live** với camera đó.
- Nếu đổi cổng add-on, dùng đúng cổng đã map thay cho `3333`.

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
8. Bấm **↻ Kiểm tra** trong mục **Dung lượng share SMB** để xem còn trống, tổng
   dung lượng và tỷ lệ đã dùng. Nếu vừa đổi cấu hình, bấm **Lưu** trước.
9. Bấm **Kiểm tra đích** để LiteNVR lưu cấu hình và ghi thử, sau đó bấm **Lưu**.
10. Đường dẫn trên NAS:
    `\\<host>\<share>\<thư mục con>\YYYY-MM-DD\<cam_id>\<file>.mp4`.
11. Chờ worker sao lưu các đoạn hoàn chỉnh (khoảng 60 giây/lần kiểm tra).

### Tự động xóa bản ghi cũ trên SMB

Bật **Tự động xóa bản ghi cũ trên SMB** và đặt một hoặc nhiều giới hạn:

- **Giữ tối đa (ngày)**: xóa bản ghi LiteNVR cũ hơn số ngày này.
- **Tối đa (GB)**: chỉ giữ tối đa dung lượng bản ghi LiteNVR trên share.
- **Giữ trống tối thiểu (GB)**: xóa bản ghi cũ nhất khi share còn trống dưới mức này.

Nhập `0` để tắt từng giới hạn. LiteNVR chỉ xóa file do chính nó đã sao lưu và ghi
nhận trong `backup_done`; không xóa file khác trên share. Bản ghi đang khóa hoặc
vừa chuyển lên trong 2 phút được bỏ qua; mỗi lượt xóa tối đa 300 file. Worker tự
kiểm tra mỗi 10 phút, hoặc bấm **🧹 Dọn SMB ngay** để chạy theo cấu hình đang lưu.
Tính năng này chỉ áp dụng cho bản ghi LiteNVR sao lưu từ bản 1.9.6 trở đi; bản ghi
cũ hơn không có thông tin đích nên được giữ nguyên.

### Xem lại từ SMB/Samba

- Chọn **Nguồn phát → Chỉ SMB/Samba** trên dòng thời gian.
- LiteNVR liệt kê file trong thư mục ngày/camera. File H.264 an toàn được phát
  trực tiếp qua HTTP Range, nên có thể tua mà không tải cả file về ổ cứng.
- File H.265/HEVC hoặc H.264 10-bit/4:2:2/4:4:4 được tải vào cache tạm rồi chuyển
  mã H.264/AAC. Lần xem đầu chậm hơn do phải tải đoạn ghi; cache tự dọn theo TTL
  và giới hạn dung lượng.
- Chỉ file đã sao lưu bằng chế độ SMB mới xuất hiện. Nếu đang dùng **Thư mục đã mount**
  hoặc FTP, chọn nguồn SMB sẽ trống.
- Trình duyệt chỉ cần phát H.264; LiteNVR tự chuyển mã H.265/H.264 lạ khi xem lại
  từ SMB.
- Nếu SMB chậm, tua có thể khựng; kiểm tra mạng LAN, SMB2/3 và tải của NAS.

## Kiểm tra sức khoẻ

Add-on có watchdog gọi `http://[HOST]:[PORT:3333]/health`; Home Assistant tự
khởi động lại add-on nếu nó ngừng phản hồi.

## Bản quyền Pro

- Mở [trang bán license](https://litenvr-license.vercel.app), đăng ký bằng email
  hoặc số điện thoại. Có gói dùng thử 1 ngày, 7 ngày (50.000đ) và vĩnh viễn
  (200.000đ); thanh toán PayOS, key hiện tại mục **Tài khoản**.
- Trong LiteNVR vào **Cài đặt → Bản quyền**, dán key, bấm **Kích hoạt**, sau đó
  **Kiểm tra lại**. Chưa kích hoạt thì menu **Mô tả sự kiện AI** tự mở mục này.
- Add-on kiểm tra license mỗi 6 giờ; nếu mất mạng vẫn dùng tiếp tối đa 7 ngày kể
  từ lần kiểm tra thành công cuối. Mô tả AI và Telegram cần license còn hiệu lực.
- Đổi thiết bị: vào trang quản trị license để **Gỡ máy**, rồi kích hoạt lại trên
  máy mới.

## Ghi chú triển khai

Ảnh add-on được xuất bản tự động thành `ghcr.io/trankhanhduy2929-beep/litenvr_addon`.
Sau lần xuất bản đầu tiên, đặt các gói GHCR sau thành **Public** trong GitHub
Package settings để Home Assistant tải được:

- `litenvr_addon`
- `litenvr_addon-amd64`
- `litenvr_addon-aarch64`

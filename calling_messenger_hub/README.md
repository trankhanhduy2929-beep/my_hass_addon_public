# Calling Messenger Hub

Trung tâm gọi và tin nhắn đa dịch vụ cho Home Assistant. Bản `0.6.0` hỗ trợ Telegram, Discord và Signal trên cùng một bảng điều khiển, dùng chung biểu mẫu gửi tin nhắn, ảnh và voice TTS.

Chức năng hiện có:

- đăng nhập nhiều tài khoản Telegram bằng OTP/2FA;
- gửi tin nhắn văn bản;
- gửi ảnh từ URL, file tải lên hoặc `/data/media` kèm chú thích;
- tạo voice message từ văn bản bằng Edge TTS, có thể bật/tắt cache để gửi lại nhanh;
- gọi P2P 1:1 và phát TTS khi người nhận nghe máy;
- gọi lặp làm chuông báo động Telegram; Discord/Signal gửi voice TTS lặp;
- đăng nhập tài khoản Discord bằng token phiên, gửi tin nhắn/ảnh/voice TTS đến DM hoặc kênh;
- kết nối Signal qua signal-cli REST API, gửi tin nhắn/ảnh/voice TTS đến số, nhóm hoặc username;
- xem trạng thái kênh, cuộc gọi, log và điều khiển qua ingress UI;
- kích hoạt license key, kiểm tra hạn dùng và tự chặn thao tác khi hết hạn;
- gọi REST API từ automation Home Assistant.

> Chưa kiểm thử với tài khoản Telegram, tài khoản Discord hoặc Signal API thật, hoặc trên thiết bị Home Assistant thật. Cần build lại image `amd64`/`aarch64` cho bản `0.6.0`.

## Định hướng đa dịch vụ

`Calling Messenger Hub` là lớp trung tâm cho gọi và nhắn tin. Telegram, Discord và Signal dùng chung danh sách tài khoản, biểu mẫu gửi và REST API; cuộc gọi P2P hiện chỉ có trên Telegram.

Discord dùng token phiên của tài khoản người dùng, không dùng bot. Add-on đăng nhập trực tiếp qua Discord REST API, gửi DM/group DM hoặc kênh server mà tài khoản tham gia. Tin nhắn dài được chia theo giới hạn 2.000 ký tự.

> **Cảnh báo:** tự động hóa tài khoản Discord bằng token phiên là self-bot, trái Điều khoản Discord và có thể khiến tài khoản bị khóa. Chỉ dùng tài khoản phụ; token tương đương mật khẩu đăng nhập. Add-on không hỗ trợ gọi thoại Discord vì API người dùng không cung cấp cuộc gọi 1:1.

Signal dùng [signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api) làm cầu nối, không nhúng signal-cli vào add-on. Cần chạy Signal API riêng, liên kết thiết bị bằng QR rồi nhập số E.164 và URL API trong hộp thoại **Thêm Signal**. Signal API không có xác thực mặc định; chỉ mở trong LAN hoặc đặt sau reverse proxy có Bearer token. Add-on hỗ trợ nhắn tin, ảnh và voice TTS; không hỗ trợ gọi Signal.

## Thay đổi tên từ bản cũ

Bản `0.2.1` đổi tên add-on và integration:

| Thành phần | Bản cũ | Bản mới |
| --- | --- | --- |
| Tên add-on | Telegram VoIP Notifier | Calling Messenger Hub |
| Add-on slug | `telegram_voip` | `calling_messenger_hub` |
| Integration domain | `telegram_voip` | `calling_messenger_hub` |
| Service prefix | `telegram_voip.*` | `calling_messenger_hub.*` |
| Sensor entity ID | `sensor.telegram_voip_*` | `sensor.calling_messenger_hub_*` |

Dữ liệu trong `/data` (`accounts.json`, session, cache, `api_token`) giữ nguyên. Biến môi trường `TGVOIP_*` vẫn được đọc để tương thích với `/data/.env` cũ.

Khi nâng cấp, gỡ add-on và integration cũ, cài lại bản mới, rồi cập nhật automation sang service prefix mới.

Bản `0.2.3` thêm công tắc **Bật cache TTS để gửi lại nhanh** trong Cài đặt. Cache dùng chung nội dung + giọng + tốc độ; tắt cache thì mỗi lần gửi đều tạo audio mới. Edge TTS cũng tăng thời gian chờ và giãn cách thử lại khi Microsoft/Cloudflare trả lỗi tạm thời.

Bản `0.2.4` thêm license key: nhập trong **Cài đặt → License**, key gắn với một `instance_id` của add-on, kiểm tra định kỳ và dùng cache tối đa 72 giờ khi mất mạng. Các thao tác đăng nhập, gửi tin, gọi và chuông báo trả `403` nếu license chưa hợp lệ; trạng thái và cấu hình vẫn xem được để nhập key hoặc mua/gia hạn.

Bản `0.2.6` khóa toàn bộ bảng điều khiển bằng màn hình kích hoạt license khi key chưa có, hết hạn hoặc bị thu hồi. Chỉ `/health`, `/api/config`, `/api/status`, `/api/license`, `/api/license/check` và `/api/settings/license` còn mở để chẩn đoán và kích hoạt; danh sách tài khoản, nhật ký, giọng đọc và thay đổi cache TTS cũng yêu cầu license hợp lệ.

Bản `0.2.7` bỏ các trường máy chủ license nâng cao khỏi màn hình kích hoạt và **Cài đặt → License**; giao diện chỉ còn ô nhập key. Máy chủ license tùy chỉnh vẫn cấu hình được qua add-on options hoặc `TGVOIP_LICENSE_SERVER_URL`.

Bản `0.2.8` thêm version vào URL `app.js`/`styles.css` và trả `Cache-Control: no-store` để trình duyệt không dùng JS cũ sau khi cập nhật add-on.

Bản `0.3.0` thêm Discord: quản lý nhiều bot token, gửi tin nhắn/ảnh/voice TTS vào kênh hoặc DM, tự chia tin nhắn dài và hiển thị chung trong danh sách tài khoản. Cuộc gọi và chuông báo vẫn chỉ dành cho Telegram.

Bản `0.4.0` thêm Signal qua signal-cli REST API: quản lý nhiều số Signal, kiểm tra tài khoản định kỳ, gửi tin nhắn/ảnh/voice TTS đến số, nhóm hoặc username, tải danh bạ/nhóm và hỗ trợ Bearer token khi API đặt sau reverse proxy. Cuộc gọi và chuông báo vẫn chỉ dành cho Telegram.

Bản `0.5.0` chuyển Discord từ bot token sang token tài khoản người dùng: đăng nhập bằng REST API, gửi DM/group DM/kênh server, ảnh và voice TTS; bỏ phụ thuộc `discord.py`. Token tài khoản là self-bot, trái Điều khoản Discord và có nguy cơ khóa tài khoản. Discord vẫn không hỗ trợ gọi thoại.

Bản `0.6.0` thêm chuông TTS lặp cho tài khoản Discord và Signal qua `ring`: gửi text tùy chọn một lần rồi gửi voice TTS theo `attempts`/`interval`. UI cho chọn tài khoản Discord/Signal trong màn hình chuông; nút gọi thoại vẫn chỉ dành cho Telegram.

## Cấu trúc

```text
input/telegram_voip/
├── calling_messenger_hub/            # add-on
│   ├── app/
│   │   ├── main.py                   # FastAPI + auth + UI routes
│   │   ├── telegram_manager.py       # provider Telegram: Telethon + PyTgCalls
│   │   ├── discord_manager.py        # provider Discord: REST API tài khoản người dùng
│   │   ├── discord_store.py          # discord_accounts.json (quyền 600)
│   │   ├── signal_manager.py         # provider Signal: signal-cli REST API
│   │   ├── signal_store.py           # signal_accounts.json (quyền 600)
│   │   ├── tts.py                    # Edge TTS -> OGG/Opus
│   │   ├── license.py                # license service + offline cache
│   │   ├── store.py                  # accounts.json + session files
│   │   └── ui/                       # ingress dashboard
│   ├── config.yaml
│   ├── Dockerfile
│   └── rootfs/usr/bin/calling_messenger_hub
├── custom_components/calling_messenger_hub/ # integration HA
├── tests/
├── analysis/REPORT.md
└── dist/
```

## Yêu cầu

1. Tạo Telegram application tại <https://my.telegram.org/apps> để lấy `api_id` và `api_hash`. Hướng dẫn 4 bước có ngay trong hộp thoại **Thêm tài khoản Telegram** của add-on.
2. Tài khoản gửi phải đăng nhập được bằng mã OTP; tài khoản bật 2FA cần thêm mật khẩu.
3. Tài khoản nhận phải cho phép nhận cuộc gọi từ tài khoản gửi (danh bạ hoặc quyền privacy phù hợp).
4. Edge TTS cần Internet. Giọng mặc định là `vi-VN-HoaiMyNeural` (Tiếng Việt, nữ); đổi trong Configuration hoặc truyền `voice` khi gọi service. Add-on tự thử lại 5 lần; với tiếng Việt, nếu Edge TTS vẫn lỗi add-on báo lỗi thay vì dùng `espeak-ng` để tránh phát âm sai. Add-on image có cả `ffmpeg` và `espeak-ng` cho giọng ngôn ngữ khác.
5. Với Discord, lấy token phiên của tài khoản người dùng (không phải bot token). Chỉ dùng tài khoản phụ vì self-bot trái Điều khoản Discord và có thể bị khóa.
6. Với Signal, chạy signal-cli-rest-api, liên kết thiết bị qua `/v1/qrcodelink` bằng QR trong ứng dụng Signal, rồi nhập số E.164 và URL API vào add-on. Không mở Signal API trực tiếp ra Internet khi chưa có xác thực.
7. Chỉ dùng tài khoản phụ hoặc tài khoản bạn sở hữu. Gọi tự động có thể vi phạm Telegram Terms of Service và bị giới hạn tài khoản.
8. Add-on cần license key còn hạn cho các thao tác gửi/gọi. Key dùng thử, gói tháng hoặc vĩnh viễn được cấp từ trang license; xem mục **License** bên dưới.

## Cài add-on

### Cách 1: copy thư mục local

Copy thư mục `calling_messenger_hub/` vào thư mục add-ons của Home Assistant, sau đó:

1. Settings > Add-ons > Add-on Store > Check for updates.
2. Cài add-on **Calling Messenger Hub**.
3. Start add-on.
4. Mở ingress panel bằng nút **Open Web UI**. Bảng điều khiển tự kết nối, không cần nhập token.
5. Vào **Cài đặt → Thông tin Telegram**, nhập `api_id`, `api_hash`, bấm **Lưu thông tin**. Add-on tự ghi `/data/.env` với quyền `600`; không cần sửa Configuration, SSH hay chạy lệnh.
6. API token cho custom integration nằm ngay trong **Cài đặt → API token cho custom integration**. Bấm biểu tượng mắt để xem hoặc biểu tượng copy để sao chép.
7. Mở **Tài khoản & kênh → Thêm Discord**, dán token tài khoản và (tùy chọn) người nhận mặc định. Token Discord được lưu trong `/data/discord_accounts.json` với quyền `600`.

Các mặc định TTS và chuông (`tts_voice`, `tts_rate`, `ring_timeout`...) vẫn có thể đổi trong Configuration nếu muốn; không bắt buộc.

## License

License key có dạng `CMH-XXXX-XXXX-XXXX-XXXX`. Nhập tại **Cài đặt → License** (hoặc đặt `license_key` trong Configuration). Key được lưu trong `/data/.env` với quyền `600`, gắn với `instance_id` trong `/data/instance_id` ở lần kiểm tra đầu tiên. Muốn chuyển key sang add-on khác phải reset liên kết trên trang quản trị license.

Add-on kiểm tra license qua `license_server_url` mặc định là `https://calling-messenger-hub-license.vercel.app`. Giao diện chỉ nhập license key; nếu tự triển khai license server, đổi `license_server_url` trong Configuration hoặc biến môi trường `TGVOIP_LICENSE_SERVER_URL`. Trang mua/gia hạn dùng `license_site_url`.

Tài khoản quản trị đăng nhập tại `/admin/login`. Lần đầu, server tạo một user trong D1 với `is_admin=1`; sau đó tài khoản này dùng được cả trang license `/dashboard`, mua/gia hạn và đổi mật khẩu. Link **Quản trị** chỉ hiện trên dashboard khi user có `is_admin`. Sau lần đăng nhập đầu, mật khẩu admin lấy từ D1; đổi mật khẩu trong mục **Bảo mật tài khoản**. File `license_server/.admin-credentials` chỉ dùng để bootstrap, không phải nguồn mật khẩu sau khi đã đổi.

Khi license hợp lệ, add-on lưu trạng thái đã ký nhận và cho phép dùng tối đa 72 giờ nếu mất mạng. License hết hạn hoặc bị thu hồi sẽ bị chặn ngay khi kiểm tra được. Giao diện hiện màn hình kích hoạt thay vì bảng điều khiển; các endpoint `/health`, `/api/config`, `/api/status`, `/api/license`, `/api/license/check`, `/api/settings/license` vẫn mở để chẩn đoán và nhập key. Các endpoint vận hành còn lại trả `403` nếu license chưa hợp lệ.

Nếu chưa nhập token, add-on tự sinh token và ghi vào `/data/api_token`.

### /data/.env

Giao diện add-on tự tạo và cập nhật `/data/.env`, không cần thao tác thủ công. File nằm ngoài repo/image, không commit.

```dotenv
TGVOIP_API_ID=123456
TGVOIP_API_HASH=your_api_hash
TGVOIP_API_TOKEN=your_long_random_token
TGVOIP_TTS_VOICE=vi-VN-HoaiMyNeural
TGVOIP_TTS_CACHE=true
TGVOIP_LICENSE_KEY=CMH-XXXX-XXXX-XXXX-XXXX
TGVOIP_LICENSE_SERVER_URL=https://calling-messenger-hub-license.vercel.app
TGVOIP_LICENSE_SITE_URL=https://calling-messenger-hub-license.vercel.app
```

Tiền tố `TGVOIP_*` được giữ để tương thích với bản cũ. Chỉ dùng cách thủ công nếu muốn sửa ngoài giao diện; sau đó restart add-on. Quyền khuyến nghị: `chmod 600 /data/.env`.

Thứ tự ưu tiên: biến môi trường → `/data/.env` → `/data/options.json`. Có thể đổi đường dẫn bằng biến `TGVOIP_ENV_FILE`.

### Cách 2: dùng repository add-on

Mã nguồn add-on nằm tại <https://github.com/trankhanhduy2929-beep/my_hass_addon_private> trong thư mục `calling_messenger_hub/`. Custom integration nằm tại <https://github.com/trankhanhduy2929-beep/calling_messenger_hub>.

## Thêm integration

Custom integration `2.0.3` tự đổi URL mặc định cũ `3332` sang `3030` khi khởi động; URL tùy chỉnh cần sửa tay.

1. Copy `custom_components/calling_messenger_hub/` vào `/config/custom_components/calling_messenger_hub/`.
2. Restart Home Assistant.
3. Settings > Devices & Services > Add Integration > **Calling Messenger Hub**.
4. Nhập:
   - URL: `http://local-calling-messenger-hub:3030` nếu add-on cài local;
   - API token: sao chép từ **Cài đặt → API token cho custom integration**;
   - chu kỳ cập nhật.

Nếu add-on cài từ repository, hostname có thể khác `local-calling-messenger-hub`; dùng hostname hiển thị trong add-on hoặc IP/port nếu đã publish port.

Integration tạo 2 sensor:

- `sensor.calling_messenger_hub_accounts_online`: số tài khoản online; attributes có danh sách tài khoản.
- `sensor.calling_messenger_hub_active_calls`: số cuộc gọi đang hoạt động; attributes có calls/rings/stats.

## Services

### Gửi tin nhắn

```yaml
service: calling_messenger_hub.send_message
data:
  to: "@username"
  message: "Cửa đang mở."
  account: "+84901234567"
  silent: false
```

`to` nhận username/số điện thoại/user ID với Telegram, hoặc ID kênh/người dùng, `#ten-kenh`, `@username` với Discord. `account` nhận ID tài khoản, số điện thoại, tên tài khoản hoặc ID Discord (`dc_...`); bỏ trống để dùng tài khoản Telegram online đầu tiên.

### Gửi voice TTS

```yaml
service: calling_messenger_hub.send_tts
data:
  to: "@username"
  message: "Có người ở cửa chính."
  voice: "vi-VN-HoaiMyNeural"
```

Với Discord, TTS được gửi dưới dạng file audio đính kèm. `voice` bỏ trống sẽ dùng giọng mặc định trong Configuration. `vi-VN-HoaiMyNeural` là giọng tiếng Việt chuẩn mặc định; `vi-VN-NamMinhNeural` chỉ là giọng nam thay thế. Voice TTS được cache theo nội dung + giọng + tốc độ khi bật cache; bản audio fallback `espeak-ng` không được dùng lại làm cache Edge TTS. Tắt cache trong **Cài đặt** hoặc đặt `TGVOIP_TTS_CACHE=false`.

### Gửi ảnh

```yaml
service: calling_messenger_hub.send_photo
data:
  to: "@username"
  image: "https://example.com/camera.jpg"
  caption: "Ảnh camera cửa chính."
  silent: false
```

`image` nhận URL `http(s)` truy cập được từ Internet, data URL base64 hoặc đường dẫn file trong `/data/media` của add-on. Ảnh tải lên tối đa 8 MB. Discord gửi ảnh dưới dạng file đính kèm.

### Gọi và phát TTS

```yaml
action: calling_messenger_hub.call
data:
  account: "+84901234567"
  to: "@username"
  message: "Báo động. Có người ở cửa chính."
  ring_timeout: 45
  wait: true
  wait_seconds: 90
```

`account` nhận ID tài khoản Telegram, số điện thoại quốc tế hoặc tên tài khoản. Bỏ trống để dùng tài khoản Telegram online đầu tiên. Discord và Signal không hỗ trợ gọi thoại; dùng `ring` để gửi voice TTS lặp hoặc `send_message`/`send_tts`. `wait: true` giữ service cho đến khi cuộc gọi kết thúc hoặc hết `wait_seconds` (mặc định 60). Không nên dùng `wait: true` trong automation dài.

### Chuông báo động

```yaml
service: calling_messenger_hub.ring
data:
  to: "@username"
  message: "Báo động. Có người ở cửa chính."
  attempts: 3
  interval: 10
  ring_timeout: 30
  send_message: true
```

Với Telegram, mỗi lần là một cuộc gọi P2P; người nhận phải bấm nghe máy thì TTS mới phát, `ring_timeout` giới hạn thời gian chờ. Với Discord/Signal, add-on gửi tin nhắn văn bản một lần nếu `send_message: true`, sau đó gửi voice TTS `attempts` lần, nghỉ `interval` giây; không có cuộc gọi, không có phát hiện nghe máy và `ring_timeout` bị bỏ qua.

### Kết thúc cuộc gọi

```yaml
service: calling_messenger_hub.hangup
data:
  call_id: "call-id"
```

Bỏ `call_id` để kết thúc mọi cuộc gọi đang hoạt động. Có thể lọc theo `account`.

## API nội bộ

Mọi endpoint `/api/*` yêu cầu `Authorization: Bearer <token>` hoặc `X-API-Token`. `/health` công khai. Ngoài ra, các endpoint vận hành cần license hợp lệ; nhóm chẩn đoán/kích hoạt được liệt kê trong mục **License**.

```text
GET    /health
GET    /api/config
GET    /api/status
GET    /api/accounts
POST   /api/accounts/login
POST   /api/discord/accounts
POST   /api/signal/accounts
POST   /api/accounts/login/{login_id}/verify
DELETE /api/accounts/login/{login_id}
POST   /api/accounts/{account_id}/reconnect
DELETE /api/accounts/{account_id}
GET    /api/accounts/{account_id}/dialogs
POST   /api/messages
POST   /api/photos
POST   /api/tts
POST   /api/calls
GET    /api/calls
GET    /api/calls/{call_id}
POST   /api/calls/{call_id}/hangup
POST   /api/hangup
POST   /api/rings
GET    /api/rings
POST   /api/rings/{ring_id}/cancel
GET    /api/logs
```

## Bảo mật

- API token là bearer token toàn quyền với add-on; không đưa vào file public.
- `accounts.json`, `discord_accounts.json`, `signal_accounts.json`, token và session nằm trong `/data`; không copy ra ngoài.
- Session Telegram và token tài khoản Discord tương đương quyền đăng nhập tài khoản; token Signal API tương đương quyền gửi tin qua cầu nối. Bảo vệ bản backup Home Assistant.
- Không commit `data/`, `*.session`, `accounts.json`, `discord_accounts.json`, `signal_accounts.json`, `api_token`, `options.json`.
- Add-on publish port `3030`; nếu không cần truy cập trực tiếp, bỏ mapping port và chỉ dùng ingress/integration nội bộ.

## Kiểm thử

```bash
cd /opt/apk-lab/input/telegram_voip
python3 -m venv .venv
.venv/bin/pip install -r calling_messenger_hub/app/requirements.txt pytest pytest-asyncio httpx pyyaml ruff
.venv/bin/python -m pytest tests -q
.venv/bin/ruff check --select E4,E7,E9,F,I,UP,SIM calling_messenger_hub/app custom_components/calling_messenger_hub tests
node --check calling_messenger_hub/app/ui/app.js
```

Kết quả hiện tại: 69 test add-on pass, 15 test license server pass, `ruff`, Python compile, JavaScript syntax, TypeScript typecheck và Next build pass. License server đã deploy tại `https://calling-messenger-hub-license.vercel.app`; đã test đăng ký, trial, tạo key, validate, tạo/hủy link PayOS, admin dùng dashboard, link quản trị theo `is_admin`, đổi mật khẩu user/admin và đăng nhập lại bằng mật khẩu mới. Chưa test thanh toán chuyển tiền thật, đăng nhập/gọi Telegram thật, tài khoản Discord/Signal thật hoặc Home Assistant runtime thật.

## Giới hạn đã biết

- Discord dùng token tài khoản người dùng (self-bot), trái Điều khoản Discord và có thể bị khóa tài khoản; không hỗ trợ gọi thoại. Chỉ dùng tài khoản phụ.
- Signal cần signal-cli REST API riêng; add-on không đăng ký số Signal và không có cuộc gọi Signal.
- Signal API không có xác thực mặc định; phải giới hạn mạng hoặc đặt sau reverse proxy. Tính năng Bearer token chỉ hoạt động khi proxy kiểm tra token.
- Gửi ảnh/TTS Signal dùng tệp đính kèm; một số bản signal-cli có thể không hiển thị voice dưới dạng voice note.
- Discord `@username` chỉ tìm trong bạn bè hoặc DM đã có; nên dùng ID người dùng hoặc ID kênh. Token hết hạn sau khi đổi mật khẩu/đăng xuất mọi thiết bị.
- P2P call chỉ hoạt động với user Telegram, không gọi nhóm.
- Người nhận phải bấm nghe máy; không có cách phát TTS vào voicemail.
- Chất lượng/khả năng gọi phụ thuộc privacy setting và phiên bản Telegram của người nhận.
- Edge TTS phụ thuộc dịch vụ Microsoft; nội dung TTS được gửi qua Internet.
- `ntgcalls` cần manylinux 2.28; image dùng `python:3.12-slim-bookworm` và chỉ chạy trên `amd64`/`aarch64`.
- Chưa có xác minh thực tế với Home Assistant Supervisor build.
- License server và PayOS đã được deploy/cấu hình; D1 chạy qua Worker proxy `license_server/d1_proxy/`. Chưa có giao dịch chuyển tiền thật để xác nhận webhook cấp key tự động sau thanh toán.
- Không có cách bỏ qua license bằng biến môi trường; muốn dùng nội bộ lâu dài cần cấp license `lifetime` hoặc chạy license server riêng.
- Worker proxy D1 chỉ chấp nhận bearer token trong `CLOUDFLARE_API_TOKEN`; không public quyền query nếu thiếu token.

# Calling Messenger Hub

Trung tâm gọi và tin nhắn đa dịch vụ cho Home Assistant. Bản `0.14.0` hỗ trợ Telegram, Discord, Signal, LINE Official Account, Zalo cá nhân và mô-đun SIM 4G SIMCom A7670C-LANS hoặc Quectel EC20/EC2x trên cùng một bảng điều khiển, dùng chung biểu mẫu gửi tin nhắn và ảnh; SIM 4G xem được nhà mạng, mức sóng, số dư, hạn dùng qua USSD và đọc hộp thư SMS/OTP.

Chức năng hiện có:

- đăng nhập nhiều tài khoản Telegram bằng OTP/2FA;
- gửi tin nhắn văn bản;
- gửi ảnh từ URL, file tải lên hoặc `/data/media` kèm chú thích;
- tạo voice message từ văn bản bằng Edge TTS, có thể bật/tắt cache để gửi lại nhanh;
- gọi P2P 1:1 và phát TTS khi người nhận nghe máy;
- gọi lặp làm chuông báo động Telegram; Discord/Signal gửi voice TTS lặp;
- đăng nhập tài khoản Discord bằng token phiên, gửi tin nhắn/ảnh/voice TTS đến DM hoặc kênh;
- kết nối Signal qua signal-cli REST API, gửi tin nhắn/ảnh/voice TTS đến số, nhóm hoặc username;
- kết nối LINE Official Account qua Messaging API, gửi tin nhắn/ảnh URL HTTPS và nhận ID người nhận qua webhook có xác thực chữ ký;
- đăng nhập Zalo cá nhân bằng QR, xem hội thoại/tin nhắn, trả lời tin nhắn, tải thêm lịch sử nhóm, quản lý nhóm (tạo, đổi tên, thêm/xoá thành viên, rời nhóm) và gửi tín hiệu đổ chuông Zalo;
- kết nối SIMCom A7670C-LANS hoặc Quectel EC20/EC2x qua serial/UART hoặc TCP bridge, tự nhận diện dòng module, gọi thoại thật, phát TTS khi nghe máy và gọi lặp làm chuông báo động;
- xem nhà mạng, mức sóng, số dư, hạn dùng SIM bằng USSD, đọc SMS/OTP trong ingress UI;
- xem trạng thái kênh, cuộc gọi, log và điều khiển qua ingress UI;
- kích hoạt license key, kiểm tra hạn dùng và tự chặn thao tác khi hết hạn;
- gọi REST API từ automation Home Assistant.

> Chưa kiểm thử với tài khoản Telegram, tài khoản Discord, Signal API, LINE Official Account, Zalo cá nhân hoặc mô-đun A7670C-LANS/EC20 thật, hoặc trên thiết bị Home Assistant thật. Luồng đổ chuông Zalo (401 `requestcall` rồi 416 `request` kèm media) mới được kiểm thử bằng mock, chưa xác minh với tài khoản Zalo thật. Định dạng USSD/SMS khác nhau theo nhà mạng và thế hệ SIM; cần xác minh lại trên SIM thật. Cần build lại image `amd64`/`aarch64` cho bản `0.14.0`.

## Định hướng đa dịch vụ

`Calling Messenger Hub` là lớp trung tâm cho gọi và nhắn tin. Telegram, Discord, Signal, LINE, Zalo và SIM dùng chung danh sách tài khoản, biểu mẫu gửi và REST API; gọi thoại hỗ trợ Telegram P2P, SIM 4G A7670/EC20 và tín hiệu đổ chuông Zalo (không truyền âm thanh).

Discord dùng token phiên của tài khoản người dùng, không dùng bot. Add-on đăng nhập trực tiếp qua Discord REST API, gửi DM/group DM hoặc kênh server mà tài khoản tham gia. Tin nhắn dài được chia theo giới hạn 2.000 ký tự.

> **Cảnh báo:** tự động hóa tài khoản Discord bằng token phiên là self-bot, trái Điều khoản Discord và có thể khiến tài khoản bị khóa. Chỉ dùng tài khoản phụ; token tương đương mật khẩu đăng nhập. Add-on không hỗ trợ gọi thoại Discord vì API người dùng không cung cấp cuộc gọi 1:1.

Signal dùng [signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api) làm cầu nối, không nhúng signal-cli vào add-on. Cần chạy Signal API riêng, liên kết thiết bị bằng QR rồi nhập số E.164 và URL API trong hộp thoại **Thêm Signal**. Signal API không có xác thực mặc định; chỉ mở trong LAN hoặc đặt sau reverse proxy có Bearer token. Add-on hỗ trợ nhắn tin, ảnh và voice TTS; không hỗ trợ gọi Signal.

LINE dùng **Messaging API** của LINE Official Account, không dùng tài khoản LINE cá nhân. Tạo channel tại [LINE Developers Console](https://developers.line.biz/console/), phát hành **Channel access token (long-lived)** rồi nhập cùng tên gợi nhớ trong hộp thoại **Thêm LINE**. Add-on kiểm tra token qua `/v2/bot/info`, lưu token trong `/data/line_accounts.json` với quyền `600` và chỉ hiển thị trạng thái.

Để gửi tin, nhập user ID `U...`, group ID `C...` hoặc room ID `R...` (33 ký tự). Bật **Channel secret** nếu muốn dùng webhook nhận ID tự động: mở Messaging API settings, bật webhook với URL `https://PUBLIC_HOST/api/line/webhook/ACCOUNT_ID`, rồi nhắn thử cho Official Account. Nút **Webhook** trong thẻ tài khoản sao chép URL hiện tại; phải thay host bằng URL công khai. Add-on xác thực header `X-Line-Signature`, không yêu cầu Bearer token cho webhook.

LINE chỉ gửi ảnh bằng URL `https://` công khai, không nhận file `/data/media` hay data URI; không gửi được voice TTS cục bộ và không hỗ trợ gọi thoại/chuông. Tin nhắn dài được chia theo giới hạn 5.000 ký tự.

Zalo dùng tài khoản cá nhân qua giao thức nội bộ không chính thức, không phải Zalo OA API. Mở **Tài khoản & kênh → Thêm Zalo**, quét QR bằng ứng dụng Zalo trên điện thoại rồi xác nhận đăng nhập. Add-on lưu phiên trong `/data/zalo/` với quyền `600`, gửi/nhận văn bản và gửi tín hiệu đổ chuông qua `requestcall` (401), `request` (416, `subCommand:3`) và `cancel`/`endcall`. Zalo chỉ đổ chuông: không truyền thoại, không phát TTS và không gửi ảnh/voice cho tài khoản `zl_...` vì giao thức media cần client Zalo chính thức cùng RTP/SRTP/Opus. Tin nhắn dài được chia theo giới hạn 2.000 ký tự.

> **Cảnh báo:** đăng nhập Zalo bằng giao thức không chính thức có thể vi phạm điều khoản Zalo và khiến tài khoản bị hạn chế hoặc khóa. Chỉ dùng tài khoản bạn sở hữu hoặc tài khoản phụ; phiên đăng nhập tương đương quyền truy cập tài khoản. Giao thức có thể thay đổi mà không báo trước.

SIM dùng mô-đun 4G **SIMCom A7670C-LANS** hoặc **Quectel EC20/EC2x/EG2x** qua lệnh AT. Add-on hỗ trợ hai kiểu kết nối: serial/UART (`/dev/ttyUSB2`, `/dev/ttyACM0`, cần `uart: true` trong add-on) hoặc TCP serial bridge. Khi thêm SIM, chọn dòng module hoặc để **Tự động nhận diện**; add-on đọc `AT+CGMM`/`AT+CGMR` để chọn profile A7670 hoặc EC20. Quá trình kiểm tra gồm `AT+CPIN?`, `AT+CEREG?`/`AT+CREG?`, `AT+COPS?`, `AT+CSQ`, `AT+CGSN`, `AT+QCCID`/`AT+CCID`, `AT+CNUM`, rồi lưu cấu hình trong `/data/sim_accounts.json` với quyền `600`. SIM phải đã tắt mã PIN, đăng ký mạng và bật VoLTE nếu nhà mạng yêu cầu gọi thoại trên 4G.

Bảng **SIM 4G** hiển thị nhà mạng từ `AT+COPS?`, mức sóng từ `AT+CSQ`, số dư và hạn dùng sau khi gửi USSD (mặc định `*101#`, có thể nhập mã khác). Hộp thư SMS đọc bằng `AT+CMGL="ALL"` ở text mode, giải mã UCS2/hex và tách mã OTP để sao chép nhanh. Một số SIM Viettel trả kết quả USSD qua SMS từ `195` thay vì `+CUSD`; khi đó xem trong hộp thư SMS. Add-on không gửi SMS và không tự động gửi OTP ra ngoài.

Cuộc gọi SIM thực hiện `ATD< số >;`, chờ `AT+CLCC` báo cuộc gọi thoại đang active trong `ring_timeout` (bỏ qua các dòng CLCC là data call), rồi tải từng đoạn audio và phát khi nghe máy. Với A7670, add-on dùng `AT+CFTRANRX` vào EFS, phát bằng `AT+CCMXPLAY`, dừng bằng `AT+CCMXSTOP` và xóa bằng `AT+FSDEL`. Với EC20/EC2x, add-on dùng `AT+QFUPL` vào UFS bằng tên file không tiền tố, phát tới đầu xa bằng `AT+QPSND=1,"<file>",0,1,1`, dừng bằng `AT+QPSND=0,"<file>",0` và xóa bằng `AT+QFDEL`. Audio 8 kHz mono được chia nhỏ để vừa giới hạn bộ nhớ USB/UART: ưu tiên AMR 60 giây, sau đó MP3 30 giây, cuối cùng WAV 5 giây. SIM không gửi tin nhắn/ảnh/TTS qua API; `send_message` trong chuông SIM bị bỏ qua. USSD và SMS chỉ được đọc, không dùng để gửi tin.

EC20/EC2x phát TTS trực tiếp vào đường lên cuộc gọi nên host không cần card âm thanh; A7670C-LANS cần cấu hình loa/mic hoặc đường audio phần cứng phù hợp. Add-on chỉ điều khiển lệnh AT, không truyền audio USB. Cước gọi do nhà mạng của SIM tính. Không hỗ trợ cuộc gọi đến, voicemail hoặc gửi SMS; chỉ đọc SMS và gửi USSD. Số dư/hạn dùng chỉ là thông tin nhà mạng trả về, không thay thế hóa đơn. Chỉ gọi tới người đã đồng ý và tuân thủ quy định viễn thông địa phương.

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

Bản `0.7.0` thêm LINE Official Account qua Messaging API: thêm tài khoản bằng channel access token, gửi văn bản và ảnh URL HTTPS, chia tin dài, tự kiểm tra token định kỳ, nhận user/group/room ID qua webhook có xác thực `X-Line-Signature`, và hiển thị danh bạ đã nhận. LINE không hỗ trợ gọi thoại, chuông TTS hoặc voice TTS cục bộ.

Bản `0.8.0` thêm SIM A7670C-LANS qua serial/UART hoặc TCP bridge: thêm tài khoản SIM trong UI, kiểm tra SIM/sóng/nhà mạng, gọi thoại thật, tải audio TTS theo đoạn AMR/MP3/WAV, phát khi nghe máy, gọi lặp làm chuông và dừng/xóa file tạm đúng cách. SIM chỉ gọi thoại, không gửi tin nhắn/ảnh và không nhận cuộc gọi đến.

Bản `0.9.0` thêm profile Quectel EC20/EC2x/EG2x bên cạnh A7670C-LANS: tự nhận diện qua `AT+CGMM`/`AT+CGMR`, cho phép chọn dòng module thủ công, đọc ICCID bằng `AT+QCCID`, tải audio UFS bằng `AT+QFUPL`, phát tới đầu xa bằng `AT+QPSND`, xóa bằng `AT+QFDEL`, lọc data call khi đọc `AT+CLCC` và hỗ trợ đăng ký qua `AT+CEREG?`. Integration `2.0.6` đi kèm add-on `0.9.0`; không cần cấu hình lại entity.

Bản `0.10.0` thêm bảng **SIM 4G**: nhà mạng từ `AT+COPS?`, mức sóng %, dBm và số vạch từ `AT+CSQ`, gửi USSD để lấy số dư/hạn dùng, đọc hộp thư SMS text mode và tách OTP để sao chép. Bổ sung API `refresh`, `ussd`, `sms`; integration `2.0.6` không đổi.

Bản `0.11.0` thêm **Zalo cá nhân**: đăng nhập bằng QR, lưu phiên cục bộ, xem danh sách hội thoại và tin nhắn, gửi văn bản tới bạn bè/nhóm, tự làm mới và chia tin dài. Thêm thư viện mã hóa/QR và API `/api/zalo/*`; tài khoản Zalo chỉ hỗ trợ văn bản, không gọi thoại, ảnh, voice TTS hoặc chuông. Integration `2.0.6` không đổi.

Bản `0.11.1` sửa giải mã phản hồi `getLoginInfo` để lấy đúng `zpw_enk`/`zpw_sek` từ envelope mã hóa, khắc phục lỗi đăng nhập QR xong nhưng báo **Chưa có khóa phiên Zalo**. Phiên Zalo cũ có `zpw_sek` sẽ tự khôi phục khóa khi kết nối lại; nếu vẫn lỗi, xóa tài khoản Zalo và đăng nhập QR lại.

Bản `0.11.2` thu thập cookie `zpw_sek` được Zalo xoay vòng trong toàn bộ quá trình polling/confirm QR và giữ giá trị mới nhất, khắc phục lỗi **600: zpw_sek bị thiếu hoặc không đúng** sau khi đăng nhập QR thành công.

Bản `0.11.3` lưu nhiều cookie `zpw_sek` ứng viên trong phiên QR, thử lại hồ sơ với từng cookie khi gặp lỗi `102`/`600`, đồng thời hiển thị chẩn đoán không chứa bí mật (`cookie`, `key`, số ứng viên) khi đăng nhập thất bại.

Bản `0.12.0` mở rộng Zalo cá nhân: trả lời/trích dẫn tin nhắn, tải thêm lịch sử nhóm qua `getoldv2`, và quản lý nhóm (tạo nhóm, đổi tên, thêm/xoá thành viên, rời nhóm) ngay trong ingress UI. Thêm API nhóm `/api/zalo/accounts/{account_id}/groups/*` và trường `reply_to` cho tin nhắn; Integration `2.0.6` không đổi.

Bản `0.12.1` sửa lỗi hội thoại Zalo bị lẫn tin nhắn giữa các nhóm: lọc tin theo `thread_id` ở client, manager và UI; tự tra cứu tên nhóm khi mở hội thoại và chấp nhận `gridInfoMap` khóa `g<id>`; thêm ô tìm kiếm và bộ lọc Tất cả/Nhóm/Cá nhân trong cột hội thoại. Bản này vẫn chưa thêm gọi thoại Zalo; tính năng đổ chuông được bổ sung ở `0.13.0`.

Bản `0.12.2` sửa cách xác định hội thoại 1:1: dùng người nhận/người gửi còn lại thay vì UID của chính tài khoản, nên không còn gộp mọi chat cá nhân vào mục "Người dùng <uid>"; bổ sung tra cứu tên qua `getprofiles/v2` (kèm `getminiprofiles`) và lấy tên từ người gửi khi API hồ sơ không trả về.

Bản `0.13.0` thêm tín hiệu **đổ chuông Zalo** qua `requestcall`/`cancel`/`endcall`: gọi một lần hoặc từ trang Cuộc gọi với tài khoản `zl_...`, dùng call ID 9 chữ số, đọc `id`/`status` từ phản hồi, hủy khi hết `ring_timeout` và hỗ trợ kết thúc cuộc gọi. Zalo chỉ đổ chuông, không truyền thoại/TTS/ảnh vì thiếu lớp media RTP/SRTP/Opus. UI ghi rõ giới hạn này và không bắt nhập lời thoại khi gọi Zalo. Integration `2.0.7` cho phép bỏ trống `message` trong service `call` để dùng với Zalo.

Bản `0.14.0` sửa lỗi Zalo chỉ ghi nhận cuộc gọi nhỡ mà không đổ chuông: gửi đủ chuỗi 401 `requestcall` tạo call record rồi 416 `/api/voicecall/request` với `subCommand:3`, `extendData`, `session` và địa chỉ RTP/RTCP để nâng invite của người nhận. Thêm **tải danh bạ Zalo** trên trang Cuộc gọi, cho phép nhập tên trong danh bạ, số điện thoại (tự chuẩn hóa `0...` → `84...`) hoặc UID; tên được so khớp không phân biệt hoa thường/dấu tiếng Việt và báo lỗi nếu trùng tên. Thêm API `GET /api/zalo/accounts/{account_id}/contacts`; integration `2.0.7` không đổi vì service `call` đã nhận chuỗi `to`.

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
│   │   ├── line_manager.py           # provider LINE: Messaging API + webhook
│   │   ├── line_store.py             # line_accounts.json (quyền 600)
│   │   ├── zalo_client.py            # giao thức Zalo cá nhân: QR, mã hóa, chat
│   │   ├── zalo_manager.py           # provider Zalo: phiên, polling, gửi văn bản
│   │   ├── zalo_store.py             # zalo_accounts.json + zalo/ (quyền 600/700)
│   │   ├── sim_manager.py            # provider SIM: AT commands A7670/EC20 + call audio
│   │   ├── sim_store.py              # sim_accounts.json (quyền 600)
│   │   ├── tts.py                    # Edge TTS -> OGG/Opus, AMR/MP3/WAV cho SIM
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
7. Với LINE, tạo Messaging API channel, phát hành channel access token và nhập channel secret nếu dùng webhook. Webhook phải dùng URL công khai HTTPS trỏ tới `/api/line/webhook/{account_id}`.
8. Với Zalo, mở **Thêm Zalo**, quét QR bằng ứng dụng Zalo trên điện thoại và xác nhận trên thiết bị. Phiên Zalo được lưu cục bộ; đăng xuất khỏi add-on sẽ xóa phiên đã lưu.
9. Với SIM, cắm A7670C-LANS hoặc EC20/EC2x qua USB/UART hoặc nối TCP serial bridge, tắt mã PIN, lắp SIM đã đăng ký mạng và bật `uart: true` nếu dùng serial trong Home Assistant. Chọn đúng dòng module hoặc để tự nhận diện; bật VoLTE nếu cần. EC20/EC2x không cần card âm thanh trên host; A7670C-LANS cần cấu hình đường audio phần cứng phù hợp. Add-on không truyền audio qua USB.
10. Chỉ dùng tài khoản phụ hoặc tài khoản bạn sở hữu. Gọi tự động có thể vi phạm Telegram Terms of Service, quy định viễn thông và gây cước phí SIM.
11. Add-on cần license key còn hạn cho các thao tác gửi/gọi. Key dùng thử, gói tháng hoặc vĩnh viễn được cấp từ trang license; xem mục **License** bên dưới.

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

Custom integration `2.0.7` đi kèm add-on `0.14.0`; service `call` cho phép bỏ trống `message` khi dùng với Zalo. Từ `2.0.3`, integration tự đổi URL mặc định cũ `3332` sang `3030` khi khởi động; URL tùy chỉnh cần sửa tay.

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

`to` nhận username/số điện thoại/user ID với Telegram, ID kênh/người dùng hoặc `#ten-kenh`/`@username` với Discord, ID hội thoại Zalo khi gửi tin; riêng `call` với Zalo nhận UID, số điện thoại hoặc tên trong danh bạ. `account` nhận ID tài khoản, số điện thoại, tên tài khoản, ID Discord (`dc_...`) hoặc ID Zalo (`zl_...`); bỏ trống để dùng tài khoản Telegram online đầu tiên. Zalo chỉ nhận `message` văn bản; không dùng `send_photo` hoặc `send_tts` với tài khoản `zl_...`. Dùng service `call` với `account: zl_...` để gửi tín hiệu đổ chuông; Zalo không phát TTS.

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

`account` nhận ID tài khoản Telegram, số điện thoại quốc tế, tên tài khoản, ID SIM (`sm_...`) hoặc ID Zalo (`zl_...`). Bỏ trống để dùng tài khoản Telegram online đầu tiên; SIM/Zalo chỉ dùng khi chọn rõ ID. Với Zalo, `message` có thể bỏ trống: add-on chỉ gửi tín hiệu đổ chuông, không phát TTS. Discord và Signal không hỗ trợ gọi thoại; dùng `ring` để gửi voice TTS lặp hoặc `send_message`/`send_tts`. `wait: true` giữ service cho đến khi cuộc gọi kết thúc hoặc hết `wait_seconds` (mặc định 60). Không nên dùng `wait: true` trong automation dài.

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

Với Telegram, mỗi lần là một cuộc gọi P2P; người nhận phải bấm nghe máy thì TTS mới phát, `ring_timeout` giới hạn thời gian chờ. Với SIM, mỗi lần là một cuộc gọi điện thoại thật tới số trong `to`; TTS phát khi người nhận nghe máy, `ring_timeout` giới hạn thời gian chờ và `send_message` bị bỏ qua. Với Discord/Signal, add-on gửi tin nhắn văn bản một lần nếu `send_message: true`, sau đó gửi voice TTS `attempts` lần, nghỉ `interval` giây; không có cuộc gọi, không có phát hiện nghe máy và `ring_timeout` bị bỏ qua.

### Kết thúc cuộc gọi

```yaml
service: calling_messenger_hub.hangup
data:
  call_id: "call-id"
```

Bỏ `call_id` để kết thúc mọi cuộc gọi đang hoạt động. Có thể lọc theo `account`.

## API nội bộ

Mọi endpoint `/api/*` yêu cầu `Authorization: Bearer <token>` hoặc `X-API-Token`, trừ webhook LINE dùng `X-Line-Signature`. `/health` công khai. Ngoài ra, các endpoint vận hành cần license hợp lệ; nhóm chẩn đoán/kích hoạt được liệt kê trong mục **License**.

```text
GET    /health
GET    /api/config
GET    /api/status
GET    /api/accounts
POST   /api/accounts/login
POST   /api/discord/accounts
POST   /api/signal/accounts
POST   /api/line/accounts
POST   /api/line/webhook/{account_id}
POST   /api/zalo/login
GET    /api/zalo/login/{login_id}
DELETE /api/zalo/login/{login_id}
GET    /api/zalo/accounts/{account_id}/threads?limit=100&refresh=true
GET    /api/zalo/accounts/{account_id}/contacts?limit=1000
GET    /api/zalo/accounts/{account_id}/messages?thread_id=...&limit=100&is_group=true&before=GLOBAL_MSG_ID
POST   /api/zalo/accounts/{account_id}/refresh
GET    /api/zalo/accounts/{account_id}/groups/{group_id}
POST   /api/zalo/accounts/{account_id}/groups
PATCH  /api/zalo/accounts/{account_id}/groups/{group_id}
POST   /api/zalo/accounts/{account_id}/groups/{group_id}/members
DELETE /api/zalo/accounts/{account_id}/groups/{group_id}/members
POST   /api/zalo/accounts/{account_id}/groups/{group_id}/leave
POST   /api/zalo/messages
POST   /api/sim/accounts
POST   /api/sim/accounts/{account_id}/refresh
POST   /api/sim/accounts/{account_id}/ussd
GET    /api/sim/accounts/{account_id}/sms?limit=50
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

### Zalo

Bắt đầu đăng nhập QR bằng `POST /api/zalo/login` với `{"name":"Zalo nhà"}`. Kết quả `login.qr.image` là data URI; poll `GET /api/zalo/login/{login_id}` cho đến khi `state` là `online` hoặc `done`. Hủy phiên chờ bằng `DELETE /api/zalo/login/{login_id}`. Sau khi đăng nhập, dùng ID `zl_...` cho các endpoint hội thoại.

```bash
curl -X POST http://HOST:3030/api/zalo/login \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Zalo nhà"}'

curl "http://HOST:3030/api/zalo/accounts/zl_1234567890/threads?limit=100" \
  -H "Authorization: Bearer TOKEN"

curl -X POST http://HOST:3030/api/zalo/messages \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"account":"zl_1234567890","to":"group_123","message":"Cửa đang mở.","is_group":true}'
```

`threads` trả các hội thoại đã chuẩn hóa (`id`, `name`, `preview`, `time`, `is_group`, `avatar`, `updated_ts`). `contacts` trả danh bạ Zalo (`id`, `name`, `phone`, `avatar`). `messages` trả `thread` và danh sách `messages`; `POST /api/zalo/messages` trả số đoạn đã gửi trong `messages`. Zalo không hỗ trợ endpoint ảnh/TTS. Gọi Zalo dùng `POST /api/calls` với `account: zl_...` và `to` là UID, số điện thoại hoặc tên trong danh bạ; add-on gửi `requestcall` rồi `request` để đổ chuông, không phát TTS.

### SIM 4G

`refresh` đọc lại `AT+COPS?`/`AT+CSQ` và trả tài khoản SIM. `ussd` gửi mã USSD, lưu số dư/hạn dùng nếu nhận diện được và trả nguyên văn kết quả. `sms` trả tối đa `limit` tin (1-200), mới nhất trước.

```bash
curl -X POST http://HOST:3030/api/sim/accounts/ACCOUNT_ID/refresh \
  -H "Authorization: Bearer TOKEN"

curl -X POST http://HOST:3030/api/sim/accounts/ACCOUNT_ID/ussd \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"code":"*101#"}'

curl "http://HOST:3030/api/sim/accounts/ACCOUNT_ID/sms?limit=50" \
  -H "Authorization: Bearer TOKEN"
```

Kết quả `ussd` có dạng:

```json
{
  "result": {
    "code": "*101#",
    "status": 0,
    "status_label": "Thành công",
    "text": "TKC: 12.345đ\nHSD: 31/12/2026",
    "pending": false,
    "error": "",
    "fallback": false,
    "balance": "12.345đ",
    "expiry": "31/12/2026",
    "updated_at": "2026-11-01T00:00:00+00:00"
  },
  "account": {}
}
```

Nếu `pending` hoặc `fallback` là `true`, gọi endpoint `sms` để xem phản hồi đến sau hoặc OTP. Một số nhà mạng yêu cầu mã USSD khác `*101#`.

## Bảo mật

- API token là bearer token toàn quyền với add-on; không đưa vào file public.
- `accounts.json`, `discord_accounts.json`, `signal_accounts.json`, `line_accounts.json`, `zalo_accounts.json`, `sim_accounts.json`, token và session nằm trong `/data`; không copy ra ngoài. Phiên Zalo nằm trong `/data/zalo/` với quyền thư mục `700` và tệp `600`.
- Session Telegram và token tài khoản Discord tương đương quyền đăng nhập tài khoản; token Signal API tương đương quyền gửi tin qua cầu nối; channel access token LINE cho phép gửi tin dưới danh nghĩa Official Account; phiên Zalo tương đương quyền đăng nhập và nhắn tin bằng tài khoản cá nhân; quyền truy cập mô-đun SIM 4G cho phép gọi, phát audio, gửi USSD và đọc SMS bằng SIM. Hộp thư SMS có thể chứa OTP hoặc thông tin cá nhân; không chia sẻ log/ảnh chụp bảng điều khiển. Bảo vệ bản backup Home Assistant.
- Không commit `data/`, `*.session`, `accounts.json`, `discord_accounts.json`, `signal_accounts.json`, `line_accounts.json`, `zalo_accounts.json`, `zalo/`, `sim_accounts.json`, `api_token`, `options.json`.
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

Kết quả hiện tại: 120 test add-on pass (gồm 30 test Zalo), 15 test license server pass, `ruff`, Python compile và JavaScript syntax pass. Bản `0.14.0` thêm test mock cho chuỗi 401/416, dựng `extendData`/`session`, tra số điện thoại, tải danh bạ và resolve tên/số khi gọi; test cũ cho call ID 9 chữ số, dùng `id` từ phản hồi và từ chối khi Zalo trả `status` lỗi vẫn giữ. Chưa chạy lại smoke Playwright cho giao diện `0.14.0`. Smoke Playwright desktop/mobile/dark mode đã chạy lại ở bản `0.12.2` cho các luồng Zalo (tìm/lọc hội thoại, trả lời, tải lịch sử, quản lý/tạo nhóm), không có lỗi console và không tràn ngang; ảnh chụp lưu tại `/var/tmp/cmh-ui-shots`. License server đã deploy tại `https://calling-messenger-hub-license.vercel.app`; đã test đăng ký, trial, tạo key, validate, tạo/hủy link PayOS, admin dùng dashboard, link quản trị theo `is_admin`, đổi mật khẩu user/admin và đăng nhập lại bằng mật khẩu mới. Chưa test thanh toán chuyển tiền thật, đăng nhập/gọi Telegram thật, tài khoản Discord/Signal/LINE/Zalo thật, A7670C-LANS/EC20 thật hoặc Home Assistant runtime thật.

## Giới hạn đã biết

- Discord dùng token tài khoản người dùng (self-bot), trái Điều khoản Discord và có thể bị khóa tài khoản; không hỗ trợ gọi thoại. Chỉ dùng tài khoản phụ.
- Signal cần signal-cli REST API riêng; add-on không đăng ký số Signal và không có cuộc gọi Signal.
- Zalo dùng giao thức không chính thức, có thể bị Zalo thay đổi hoặc chặn; hỗ trợ văn bản, trả lời, lịch sử nhóm, quản lý nhóm, tải danh bạ và gửi tín hiệu đổ chuông qua 401/416, không có ảnh/TTS và không truyền âm thanh cuộc gọi. Lịch sử nhóm cũ chỉ tải được khi tin nhắn có `globalMsgId`; thêm/xoá thành viên, đổi tên và rời nhóm còn phụ thuộc quyền của tài khoản trong nhóm. Phiên QR và cookie là dữ liệu nhạy cảm, không đưa vào log hoặc backup công khai.
- Signal API không có xác thực mặc định; phải giới hạn mạng hoặc đặt sau reverse proxy. Tính năng Bearer token chỉ hoạt động khi proxy kiểm tra token.
- Gửi ảnh/TTS Signal dùng tệp đính kèm; một số bản signal-cli có thể không hiển thị voice dưới dạng voice note.
- Discord `@username` chỉ tìm trong bạn bè hoặc DM đã có; nên dùng ID người dùng hoặc ID kênh. Token hết hạn sau khi đổi mật khẩu/đăng xuất mọi thiết bị.
- P2P call chỉ hoạt động với user Telegram, không gọi nhóm. SIM chỉ gọi số điện thoại, không gọi Telegram/Discord/Signal/Zalo. Zalo chỉ gửi tín hiệu đổ chuông, không phát TTS và không đảm bảo cuộc gọi được kết nối.
- Người nhận phải bấm nghe máy; không có cách phát TTS vào voicemail.
- Chất lượng/khả năng gọi phụ thuộc privacy setting và phiên bản Telegram của người nhận.
- SIM A7670C-LANS và EC20/EC2x chưa được kiểm thử trên phần cứng thật. Cần xác minh đường audio, mức âm lượng, `AT+CFTRANRX`/`AT+QFUPL` ở 115200 baud, quyền ghi EFS/UFS và dung lượng bộ nhớ của từng firmware. Cần xác minh thêm `AT+COPS?`/`AT+CSQ`, `AT+CUSD`, cách nhà mạng trả USSD qua SMS, mã hóa UCS2 và thời gian phản hồi. Add-on chia audio 60/30/5 giây và có thể chuyển AMR → MP3 → WAV nếu `ffmpeg` thiếu encoder.
- SIM chỉ đọc SMS và gửi USSD; không hỗ trợ cuộc gọi đến, voicemail, gửi SMS/ảnh/TTS. Add-on không xóa SMS, không ghép tin multipart và không tự làm mới hộp thư ngoài lúc mở tab/bấm làm mới. USSD trả sau `OK` chỉ đọc được qua SMS. Cước phí và giới hạn gọi do nhà mạng quyết định.
- Edge TTS phụ thuộc dịch vụ Microsoft; nội dung TTS được gửi qua Internet.
- `ntgcalls` cần manylinux 2.28; image dùng `python:3.12-slim-bookworm` và chỉ chạy trên `amd64`/`aarch64`.
- Chưa có xác minh thực tế với Home Assistant Supervisor build.
- License server và PayOS đã được deploy/cấu hình; D1 chạy qua Worker proxy `license_server/d1_proxy/`. Chưa có giao dịch chuyển tiền thật để xác nhận webhook cấp key tự động sau thanh toán.
- Không có cách bỏ qua license bằng biến môi trường; muốn dùng nội bộ lâu dài cần cấp license `lifetime` hoặc chạy license server riêng.
- Worker proxy D1 chỉ chấp nhận bearer token trong `CLOUDFLARE_API_TOKEN`; không public quyền query nếu thiếu token.

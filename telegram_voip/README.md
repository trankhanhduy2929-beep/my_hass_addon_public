# Telegram VoIP Notifier

Add-on Home Assistant dùng nhiều tài khoản Telegram để gửi tin nhắn, voice TTS,
gọi P2P 1:1 và gọi lặp làm chuông báo động.

## Chức năng

- Đăng nhập nhiều số điện thoại Telegram bằng OTP và mật khẩu 2FA.
- Gửi tin nhắn văn bản.
- Tạo voice message bằng Edge TTS, fallback `espeak-ng`.
- Gọi P2P và phát TTS khi người nhận nghe máy.
- Gọi lặp với số lần và khoảng nghỉ cấu hình được.
- Ingress UI quản lý tài khoản, cuộc gọi, cấu hình và log.
- REST API có Bearer token cho custom integration/automation.

## Cài đặt

1. Thêm repository add-on vào Home Assistant.
2. Cài **Telegram VoIP Notifier**.
3. Start add-on rồi mở ingress panel. Bảng điều khiển tự kết nối, không cần nhập token.
4. Vào **Cài đặt → Thông tin Telegram**, nhập `api_id`, `api_hash`, bấm **Lưu thông tin**. Add-on tự ghi `/data/.env` quyền `600`; không cần SSH, chạy lệnh hay sửa Configuration.
5. API token cho custom integration nằm trong **Cài đặt → API token cho custom integration**; bấm biểu tượng mắt để xem hoặc copy.

Các mặc định TTS và chuông (`tts_voice`, `tts_rate`, `ring_timeout`...) vẫn có thể đổi trong Configuration nếu muốn; không bắt buộc.

Nếu chưa nhập token, add-on tự sinh token tại `/data/api_token`.

Giao diện tự tạo và cập nhật `/data/.env`; file nằm ngoài repo/image và không commit. Chỉ sửa thủ công nếu cần, sau đó restart add-on.

Thứ tự ưu tiên: biến môi trường → `/data/.env` → `/data/options.json`.

## Yêu cầu

- Tạo Telegram application tại <https://my.telegram.org> để lấy `api_id` và
  `api_hash`.
- Tài khoản gửi phải đăng nhập được bằng OTP; tài khoản bật 2FA cần thêm mật
  khẩu.
- Tài khoản nhận phải cho phép nhận cuộc gọi từ tài khoản gửi.
- Edge TTS cần Internet. Add-on image có `ffmpeg` và `espeak-ng`.
- Chỉ dùng tài khoản phụ hoặc tài khoản bạn sở hữu. Gọi tự động có thể vi phạm
  Telegram Terms of Service và bị giới hạn tài khoản.

## Custom integration

Cài integration tại
<https://github.com/trankhanhduy2929-beep/telegramvoip_homeassistant> để dùng
service `telegram_voip.*`, sensor và automation trong Home Assistant.

URL nội bộ cho integration: `http://local-telegram-voip:3332`.

## Giới hạn

Chưa kiểm thử với tài khoản Telegram thật hoặc Home Assistant runtime thật.
Cuộc gọi P2P cần người nhận bấm nghe máy; nếu không, add-on kết thúc cuộc gọi
theo `ring_timeout`.

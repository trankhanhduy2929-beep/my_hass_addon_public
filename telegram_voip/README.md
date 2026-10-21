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
3. Nhập cấu hình:

```yaml
api_id: 123456
api_hash: "your_api_hash"
api_token: "optional-long-random-token"
tts_voice: "vi-VN-HoaiMyNeural"
tts_rate: "+0%"
ring_timeout: 45
ring_attempts: 2
ring_interval: 15
max_call_seconds: 180
log_limit: 300
```

4. Start add-on rồi mở ingress panel. Bảng điều khiển tự kết nối, không cần nhập token; chỉ nhập token khi truy cập trực tiếp cổng `3332`.

Nếu để trống `api_token`, add-on tự sinh token tại `/data/api_token`.

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

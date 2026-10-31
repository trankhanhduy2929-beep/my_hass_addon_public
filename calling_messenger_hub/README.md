# Calling Messenger Hub

Trung tâm gọi và tin nhắn đa dịch vụ cho Home Assistant. Bản `0.2.1` dùng Telegram làm provider đầu tiên; các dịch vụ khác sẽ được bổ sung sau.

## Chức năng

- Đăng nhập nhiều tài khoản Telegram bằng OTP và mật khẩu 2FA.
- Gửi tin nhắn văn bản.
- Gửi ảnh từ URL, file tải lên hoặc `/data/media` kèm chú thích.
- Tạo voice message bằng Edge TTS; mặc định `vi-VN-HoaiMyNeural`, tự thử lại 5 lần. Với tiếng Việt, add-on báo lỗi thay vì dùng `espeak-ng` để tránh phát âm sai.
- Gọi P2P và phát TTS khi người nhận nghe máy.
- Gọi lặp với số lần và khoảng nghỉ cấu hình được.
- Ingress UI quản lý tài khoản, cuộc gọi, cấu hình và log.
- REST API có Bearer token cho custom integration/automation.

## Cài đặt

1. Thêm repository add-on vào Home Assistant.
2. Cài **Calling Messenger Hub**.
3. Start add-on rồi mở ingress panel. Bảng điều khiển tự kết nối, không cần nhập token.
4. Vào **Cài đặt → Thông tin Telegram**, nhập `api_id`, `api_hash`, bấm **Lưu thông tin**. Add-on tự ghi `/data/.env` quyền `600`; không cần SSH, chạy lệnh hay sửa Configuration.
5. API token cho custom integration nằm trong **Cài đặt → API token cho custom integration**; bấm biểu tượng mắt để xem hoặc copy.

Các mặc định TTS và chuông (`tts_voice`, `tts_rate`, `ring_timeout`...) vẫn có thể đổi trong Configuration nếu muốn; không bắt buộc. Giọng mặc định là `vi-VN-HoaiMyNeural` (Tiếng Việt chuẩn); `vi-VN-NamMinhNeural` chỉ là giọng nam thay thế. Nếu service truyền `voice`, giá trị đó được dùng thay cho mặc định.

Nếu chưa nhập token, add-on tự sinh token tại `/data/api_token`.

Giao diện tự tạo và cập nhật `/data/.env`; file nằm ngoài repo/image và không commit. Chỉ sửa thủ công nếu cần, sau đó restart add-on.

Thứ tự ưu tiên: biến môi trường → `/data/.env` → `/data/options.json`. Tiền tố `TGVOIP_*` được giữ để tương thích với bản cũ.

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
<https://github.com/trankhanhduy2929-beep/calling_messenger_hub> để dùng
service `calling_messenger_hub.*`, sensor và automation trong Home Assistant.

URL nội bộ cho integration: `http://local-calling-messenger-hub:3332`.

## Nâng cấp từ Telegram VoIP Notifier

- Add-on slug đổi từ `telegram_voip` sang `calling_messenger_hub`.
- Integration domain và service prefix đổi sang `calling_messenger_hub`.
- Dữ liệu `/data` (`accounts.json`, session, cache, `api_token`) giữ nguyên.
- Gỡ add-on và integration cũ, cài lại bản mới, rồi cập nhật automation.

## Giới hạn

Chưa kiểm thử với tài khoản Telegram thật hoặc Home Assistant runtime thật.
Cuộc gọi P2P cần người nhận bấm nghe máy; nếu không, add-on kết thúc cuộc gọi
theo `ring_timeout`.

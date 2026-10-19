# Changelog

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

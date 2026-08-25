# YouTube Pro 4.0.0

Add-on YouTube Pro cho Home Assistant, được tách riêng hoàn toàn khỏi YouTube Music Lite để có thể cài song song.

## Định danh riêng

- Add-on slug: `youtube_pro_addon`
- Cổng relay và Integration API: `2032/tcp`
- Custom integration: `youtube_pro`
- License Key: `YTP-XXXXX-XXXXX-XXXXX-XXXXX`
- Dữ liệu add-on, integration token, license installation và localStorage không dùng chung với bản Lite.

## Tính năng giữ nguyên

- Giao diện Ingress phong cách YouTube Music, tối ưu desktop và mobile.
- Tìm kiếm, playlist, hàng chờ, lịch sử, yêu thích, hẹn giờ và phát trên điện thoại.
- Phát tới `media_player` Home Assistant qua audio relay có Range support.
- Media Browser 3.2 native, tìm kiếm và điều khiển next/previous/repeat/shuffle.
- Integration API dùng Bearer token riêng; API quản trị vẫn chỉ mở qua Home Assistant Ingress.
- License tự động có activation token, kiểm tra định kỳ và offline grace; mặc định chưa cưỡng chế.

## Cài add-on

1. Chép thư mục `youtube_pro_addon` vào repository add-on local.
2. Reload add-on store rồi cài **YouTube Pro 4.0.0**.
3. Giữ port host `2032` nếu không có dịch vụ khác sử dụng cổng này.
4. Khởi động add-on và mở Web UI.

Nếu loa cần URL LAN cố định, cấu hình:

```yaml
media_base_url: "http://192.168.1.20:2032"
```

## Cài custom integration

1. Chép `projects/youtube_pro/custom_components/youtube_pro` vào `/config/custom_components/youtube_pro`.
2. Khởi động lại Home Assistant.
3. Trong add-on, mở **Hẹn giờ → Home Assistant integration** và sao chép token.
4. Thêm integration **YouTube Pro** với URL `http://homeassistant.local:2032` hoặc IP Home Assistant cùng cổng `2032`.

Các service:

- `youtube_pro.play`
- `youtube_pro.play_playlist`
- `youtube_pro.enqueue`
- `youtube_pro.set_timer`

## License

Portal production đã được cấu hình mặc định:

```yaml
license_server_url: "https://youtube-pro-license-portal.vercel.app"
license_enforcement: false
```

Chỉ bật `license_enforcement: true` sau khi installation đã kích hoạt thành công. Add-on không chứa PayOS secret, database secret, service token hoặc admin secret.

## Lưu ý

- Bản Lite tại `ket_qua/youtube_cast_addon` không bị sửa.
- Bản Pro và Lite có thể chạy đồng thời trên `2032` và `2232`.
- Chưa tuyên bố kiểm thử loa thật cho bản Pro cho tới khi cài trên thiết bị Home Assistant thực tế.

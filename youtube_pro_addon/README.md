# YouTube Pro 5.2.1

Add-on YouTube Pro cho Home Assistant, được tách riêng hoàn toàn khỏi YouTube Music Lite để có thể cài song song.

## Định danh riêng

- Add-on slug: `youtube_pro_addon`
- Cổng relay và Integration API: `2032/tcp`
- Custom integration: `youtube_pro`
- License Key: `YTP-XXXXX-XXXXX-XXXXX-XXXXX`
- Dữ liệu add-on, integration token, license installation và localStorage không dùng chung với bản Lite.

## Tính năng

- Giao diện Ingress phong cách YouTube Music và YouTube Video, tối ưu desktop và mobile.
- Tìm kiếm, playlist, hàng chờ, lịch sử, yêu thích, hẹn giờ và phát trên điện thoại.
- **Queue Pro** cho phép chọn **Phát tiếp theo** hoặc **Thêm cuối**, quản lý đúng phiên phát của loa đang chọn, đổi thứ tự, xóa từng bài, xóa các bài tiếp theo, phát ngẫu nhiên và lưu hàng chờ thành playlist.
- **Smart Radio** tạo đài phát từ bài hát hoặc video hiện tại, lọc bài trùng với phiên phát/lịch sử và tự bổ sung đề xuất khi danh sách sắp hết.
- **Mix cá nhân local-first** học từ lượt nghe, thích/không thích và bài/kênh bị ẩn; có nhiều hồ sơ nghe, làm mới đề xuất và phát trực tiếp tới loa.
- Phản hồi đề xuất ngay trong player: thích, không thích, ẩn bài, ẩn kênh và hoàn tác; dữ liệu chỉ lưu trên installation này.
- Tự lấy địa chỉ LAN của Home Assistant qua Supervisor; người dùng không phải nhập IP Hass.
- Tự phát tới Cast/Google Cast qua `media_player`, đồng thời nhận diện Apple TV/AirPlay/HomePod.
- Video dùng progressive MP4 relay có Range support; HomePod/AirPlay tự dùng audio fallback.
- Media Browser 3.2 native, thêm mục **Mix cá nhân**, tìm kiếm và điều khiển next/previous/repeat/shuffle.
- Integration API dùng Bearer token riêng; API quản trị vẫn chỉ mở qua Home Assistant Ingress.
- License tự động có activation token, kiểm tra định kỳ và offline grace; add-on khóa bắt buộc khi chưa có key hợp lệ.

## Cài add-on

1. Chép thư mục `youtube_pro_addon` vào repository add-on local.
2. Reload add-on store rồi cài **YouTube Pro 5.2.1**.
3. Giữ port host `2032` nếu không có dịch vụ khác sử dụng cổng này. Không cần điền `media_base_url` trong cấu hình thông thường.
4. Khởi động add-on và mở Web UI.

`media_base_url` chỉ là override tùy chọn cho mạng đặc biệt; mặc định add-on tự phát hiện địa chỉ LAN:

```yaml
media_base_url: "http://192.168.1.20:2032"
```

## Cài custom integration

1. Chép `projects/youtube_pro/custom_components/youtube_pro` vào `/config/custom_components/youtube_pro`.
2. Khởi động lại Home Assistant.
3. Trong add-on, mở **Hẹn giờ → Home Assistant integration** và sao chép token.
4. Thêm integration **YouTube Pro**, giữ URL là `auto` (khuyến nghị), dán token và chọn loa mặc định. Integration tự dò add-on qua Supervisor/DNS nội bộ; chỉ nhập URL thủ công khi mạng có cấu hình đặc biệt.

Các service:

- `youtube_pro.play`
- `youtube_pro.play_playlist`
- `youtube_pro.enqueue`
- `youtube_pro.start_radio`
- `youtube_pro.play_personal_mix`
- `youtube_pro.listener_feedback`
- `youtube_pro.set_timer`

Service `youtube_pro.enqueue` nhận `entity_id` tùy chọn và `position: next|end`. Service `youtube_pro.start_radio` tạo đài phát cho đúng `media_player`, hỗ trợ audio/video và chế độ thay thế hoặc nối cuối hàng chờ.

## License

Add-on 5.2.1 tự kết nối tới License API/Portal production đã tích hợp sẵn; không cần và không có option `license_server_url` trong Home Assistant. Bấm **Kích hoạt tự động**, đăng nhập bằng email trên trang mở ra, rồi quay lại add-on; add-on tự nhận quyền qua installation secret, không cần copy/dán key và không dùng tài khoản Google.

Khi mở lại add-on, license hợp lệ đã lưu được nạp ngay từ dữ liệu cục bộ trong thời gian offline grace; việc kiểm tra server chạy nền nên không còn làm kẹt màn hình kiểm tra key. Activation token có bản sao dự phòng riêng để tự khôi phục nếu file chính bị thiếu. Nếu server xác nhận key bị thu hồi hoặc hết offline grace, add-on vẫn khóa đúng theo chính sách license.

URL activation dùng fragment bảo mật (`#token=...`) nên claim token không đi vào request HTTP hoặc log máy chủ. Nhập License Key thủ công vẫn có trong mục thu gọn để dự phòng. `license_enforcement` chỉ còn để tương thích cấu hình cũ và không thể tắt khóa.

Add-on không chứa PayOS secret, database secret, service token hoặc admin secret.

## Lưu ý

- Bản Lite tại `ket_qua/youtube_cast_addon` không bị sửa.
- Bản Pro và Lite có thể chạy đồng thời trên `2032` và `2232`.
- HomePod cần được Home Assistant nhận diện qua Apple TV/AirPlay integration; add-on không lưu pairing credential và không quảng bá mDNS trực tiếp.
- Smart Radio và Mix cá nhân 5.2.1 không dùng Google OAuth và không đồng bộ tài khoản YouTube; playlist, hồ sơ và phản hồi lưu cục bộ trong add-on.
- Chưa tuyên bố kiểm thử phát thực tế trên loa Cast/HomePod nếu chưa có thiết bị tương ứng trong môi trường chạy.

# HA Camera Face ID

Home Assistant local add-on lấy trực tiếp các entity `camera.*` đã có trong Home Assistant, đọc ảnh qua Core API, tự crop khuôn mặt bằng InsightFace, phân biệt người quen và publish sự kiện qua MQTT. Người dùng không nhập URL RTSP và addon không cần ONVIF hoặc Frigate.

## Chức năng

- Tự lấy danh sách entity `camera.*` từ Home Assistant.
- Chọn camera bằng dropdown, không nhập username/password hoặc URL luồng.
- Đọc danh sách entity qua Supervisor API và lấy ảnh bằng access token riêng của camera.
- Phân tích từ `0.2` đến `10` FPS tùy cấu hình và tốc độ camera entity.
- Preset NUC6CAYH mặc định dùng `buffalo_sc`, detector `640`, `2` CPU thread và `1 FPS`.
- Motion-skip bỏ qua inference khi cảnh đứng yên nhưng vẫn quét định kỳ để nhận người đứng yên.
- InsightFace detect nhiều khuôn mặt, lưu crop và lịch sử SQLite.
- Một người có tối đa `100` ảnh mẫu; hỗ trợ thêm ảnh, xóa từng ảnh, đổi tên và retrain nền.
- Cache embedding trong RAM/đĩa để khởi động và retrain nhanh hơn, phù hợp máy có `16 GB RAM`.
- Quản lý/tải/kích hoạt `buffalo_sc`, `buffalo_s` và `buffalo_l` ngay trong Web UI.
- Ghi SQLite, encode ảnh và publish MQTT qua hàng đợi nền để không chặn camera worker.
- MQTT Discovery tự tạo camera, binary sensor và sensor.
- Dashboard polling nhẹ mỗi `3 giây`, tự thêm event mới và cập nhật trạng thái camera/AI/MQTT mà không reload trang.
- Lịch sử có tra cứu AJAX theo khoảng ngày, camera, tên người, người lạ/đã biết và match tối thiểu; có phân trang và tự làm mới trang đầu.
- Cleanup chạy nền theo lịch cấu hình, hiển thị lần chạy gần nhất/kế tiếp và số event/ảnh đã dọn.
- License tự động qua portal Vercel/PayOS, ràng buộc theo installation và có cache offline đã ký; không phải copy/paste key.
- Web UI chỉ mở qua Home Assistant Ingress, không publish port `6868` ra host và không dùng mật khẩu riêng của add-on.
- Khi license chưa hợp lệ, chỉ trang kích hoạt được hiển thị; camera, Face ID, lịch sử, cài đặt và API nội bộ đều bị khóa.

## Cài đặt

1. Copy thư mục `rtsp_face_bridge` vào `/addons` của Home Assistant.
2. Vào **Settings → Add-ons → Add-on Store**.
3. Chọn menu ba chấm và bấm **Check for updates**.
4. Cài đặt hoặc cập nhật **HA Camera Face ID**.
5. Restart addon để Home Assistant cấp `SUPERVISOR_TOKEN` theo quyền `homeassistant_api: true`.
6. Mở Web UI bằng nút **Open Web UI** trong Home Assistant. Add-on không yêu cầu mật khẩu cục bộ.
7. Nếu installation chưa có license, add-on chỉ hiện trang **Kích hoạt HA Camera Face ID**. Bấm **Mở portal kích hoạt / mua license**, đăng nhập/đăng ký và chọn trial 1 ngày hoặc gói mua.
8. Sau khi portal cấp quyền, add-on tự nhận license trong tối đa 30 giây và mở giao diện bên trong; không cần nhập URL, Installation ID hoặc key.

Lần chạy đầu InsightFace tải model `buffalo_sc` vào `/data/insightface`. Dữ liệu khuôn mặt, embedding cache, lịch sử và MQTT vẫn được giữ qua các lần cập nhật. Khi nâng cấp lên `2.4.0`, hash mật khẩu Web UI cũ được xóa khỏi `/data/config.json`; các dữ liệu camera/Face ID khác không bị thay đổi.

## Preset NUC6CAYH

Vào **Cài đặt → Preset hiệu năng → NUC6CAYH tiết kiệm**. Preset đặt:

- `buffalo_sc`, detector `640`, ONNX Runtime `2` CPU thread.
- Camera `1 FPS`, chiều rộng xử lý `960`.
- Motion threshold `3.5`, quét lại cảnh tĩnh sau `3 giây`.
- OpenCV `1` thread và Web UI `4` worker.

RAM `16 GB` đủ rộng cho model, cache embedding và lịch sử; CPU J3455 vẫn là giới hạn chính nên không nên dùng detector `1280` trừ khi thật sự cần mặt rất xa.

## Quản lý Face ID

1. Vào **Face ID**, nhập tên và tải cùng lúc nhiều ảnh.
2. Sau khi tạo người, có thể tiếp tục thêm nhiều ảnh góc mặt khác.
3. Dùng **Đổi tên** để cập nhật cả tên trong lịch sử cũ.
4. Dùng **Retrain toàn bộ** để bỏ cache cũ và tính lại embedding trong worker nền.
5. Có thể xóa từng ảnh kém chất lượng; mỗi người phải còn ít nhất một ảnh.

Nên dùng 5–20 ảnh rõ mặt cho mỗi người. Quá nhiều ảnh gần như giống nhau không cải thiện đáng kể bằng ảnh đa dạng góc nhìn và ánh sáng.

## Thêm camera

1. Tạo camera trong Home Assistant bằng integration phù hợp. Entity phải xuất hiện dưới dạng `camera.ten_camera`.
2. Vào trang **Camera** của addon.
3. Chọn entity trong danh sách lấy từ Home Assistant.
4. Có thể để trống tên để dùng `friendly_name` của entity.
5. Chọn FPS phân tích và chiều rộng xử lý, sau đó bấm **Thêm camera entity**.

Nút **Test ảnh camera** yêu cầu Home Assistant trả về một ảnh hợp lệ. Nếu entity ở trạng thái `unavailable`, addon sẽ tiếp tục thử lại nền.

Nút **Test Face ID** lấy ảnh hiện tại và chạy ngay InsightFace. Kết quả sẽ cho biết model chưa sẵn sàng, không thấy mặt, mặt bị lọc do score/kích thước, nhận ra tên hoặc đang là `Unknown`. Muốn phân biệt tên, cần thêm ảnh mẫu trong mục **Người**.

## License

- Khi chưa có license hợp lệ, camera worker nền dừng lấy ảnh và toàn bộ trang/API nội bộ trả về cổng kích hoạt hoặc lỗi `license_required`.
- Chỉ `/activate`, thao tác kiểm tra/nhập key tại trang kích hoạt, trạng thái license đã rút gọn, static asset và health check được truy cập trước khi active.
- Sau khi license hợp lệ, dashboard, camera, thư viện khuôn mặt, lịch sử, MQTT, model và nút **Test Face ID** hoạt động như trước.
- Mỗi add-on tự tạo một Ed25519 installation identity trong `/data/license_identity.json`; không chia sẻ hoặc sao chép file này.
- Add-on chỉ gửi License Key, installation ID/public key và chữ ký chứng minh quyền sở hữu installation tới portal.
- Add-on không chứa PayOS secret, D1 secret, private signing key hoặc admin secret.
- Phản hồi server được ký Ed25519 bằng public key cấu hình trong add-on; key không phải secret nhưng phải khớp private key trên portal. Khi mất mạng chỉ cache đã ký mới được dùng, mặc định tối đa `72` giờ và không vượt hạn license.

Nếu deploy portal bằng URL khác `https://camera-face-id-license.vercel.app`, đổi `license_portal_url` trong tab **Configuration** của add-on hoặc trong phần License của Web UI. Khi xoay private signing key trên Vercel, cập nhật public key tương ứng trong tab **Configuration** của add-on rồi kiểm tra lại license.

## Nâng cấp từ bản RTSP-only

Bản `2.0.x` xóa URL RTSP đã lưu, tắt các camera cũ và đánh dấu `migration_required` để không tiếp tục giữ mật khẩu camera trong `/data/config.json`. Vào **Sửa**, chọn entity Home Assistant tương ứng và bật lại nhận diện. Thư viện khuôn mặt và lịch sử không bị xóa.

Addon tự dùng `access_token` xoay vòng của từng camera entity để gọi trực tiếp Core API tại `http://homeassistant:8123/api`, sau đó tự fallback qua Supervisor proxy nếu cần. Biến môi trường `HOME_ASSISTANT_DIRECT_API_URL` cho phép đổi địa chỉ Core API trong hệ thống đặc biệt. Nếu Home Assistant vẫn từ chối ảnh, hãy mở chính entity đó trong dashboard để xác nhận integration camera có hiển thị ảnh hợp lệ.

Từ bản `2.0.2`, addon giữ quyền tối thiểu `homeassistant_api: true`; không yêu cầu quyền quản lý Supervisor. Bản `2.1.0` tự chuyển cấu hình cũ sang preset NUC6CAYH, giữ nguyên camera entity, người đã học và lịch sử.

Bản `2.2.0` bổ sung dashboard realtime, tra cứu lịch sử không reload và lịch cleanup cấu hình được.

Bản `2.3.2` giữ nguyên license tự động và các chức năng camera, đồng thời cho phép Docker build chịu lệch giờ repository tối đa 3 ngày mà không tắt kiểm tra chữ ký hoặc hạn dùng APT.

Bản `2.4.0` loại bỏ hoàn toàn login/mật khẩu Web UI cục bộ, xóa hash cũ khi migrate, chỉ cho truy cập qua Home Assistant Ingress và khóa mọi giao diện/API nội bộ cho đến khi license hợp lệ.

## Realtime và tra cứu

Dashboard dùng polling JSON incremental, chỉ lấy event có ID mới hơn lần cuối nên nhẹ hơn việc tải lại toàn bộ lịch sử. Khi có khuôn mặt mới, card ảnh crop được thêm với animation; trạng thái frame, inference, motion, queue MQTT và bộ đếm cũng được cập nhật trực tiếp.

Trang **Lịch sử** hỗ trợ:

- Khoảng ngày bắt đầu/kết thúc.
- Camera và tìm một phần tên người.
- Chỉ người đã biết tên hoặc chỉ `Unknown`.
- Match tối thiểu và số lượng kết quả mỗi trang.
- Lọc, phân trang, dạy lại/xóa event bằng fetch mà không tải lại trang.

## Dọn dẹp dữ liệu

Mặc định addon giữ event và ảnh crop trong `30` ngày, worker chạy mỗi `6` giờ. Lần đầu worker chạy ngay khi addon khởi động; các lần sau theo lịch đã chọn trong **Cài đặt → MQTT và dữ liệu addon**. Có thể chọn `1`, `3`, `6`, `12`, `24`, `48` giờ hoặc `7 ngày`; chọn `0` ngày để giữ vô thời hạn. Khi dọn, addon xóa bản ghi SQLite và ảnh crop tương ứng, sau đó hiển thị thống kê trong dashboard/cài đặt.

## MQTT

Cấu hình broker tại **Cài đặt**. Mặc định:

- Host: `core-mosquitto`
- Port: `1883`
- Base topic: `rtsp_face_bridge`
- Discovery prefix: `homeassistant`

Sự kiện được publish không retain tại `rtsp_face_bridge/events`. Các topic theo camera vẫn giữ prefix cũ để tương thích với automation hiện có:

```text
rtsp_face_bridge/<camera_id>/state
rtsp_face_bridge/<camera_id>/image
rtsp_face_bridge/<camera_id>/face
```

## Truy cập Web UI

Add-on không còn màn hình login hoặc mật khẩu riêng. Truy cập bằng Home Assistant Ingress; manifest không map port `6868` ra host và panel được giới hạn cho tài khoản quản trị Home Assistant. License gate vẫn được kiểm tra độc lập trên mọi route nội bộ.

## Dữ liệu persistent

```text
/data/config.json
/data/events.db
/data/events/
/data/faces/
/data/insightface/
/data/license_identity.json
```

## Lưu ý model

Addon dùng code InsightFace và model pretrained do InsightFace phân phối. Hãy tự kiểm tra giấy phép model trước khi sử dụng ngoài phạm vi cá nhân hoặc phân phối thương mại.

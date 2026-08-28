# Changelog

## 0.10.3 - 2026-08-28

- Sửa lỗi `device/set-user-config` gửi sai content type khiến camera trả HTTP 200
  nhưng không lưu username/password RTSP; request giờ khớp APK Android 4.1.21:
  `application/x-www-form-urlencoded`, `device_id` và `config` JSON string.
- Không còn chấp nhận password bị che như bằng chứng read-after-write; URL chỉ được
  cập nhật khi cloud trả lại đúng credential, tránh báo thành công giả.
- Nếu camera không xác nhận thay đổi, add-on xóa credential cache cũ và giao diện
  tự tải lại cấu hình cloud thực tế, không giữ username/password hoặc URL vừa nhập.
- Giữ nguyên RTSP enable, P2P, FaceID, phòng ban, clip, license, HANET login và
  custom component.

## 0.10.2 - 2026-08-28

- Add per-camera RTSP username/password editing using the exact Android 4.1.21
  `device/set-user-config` JSON-string payload and read-after-write verification.
- Show the complete legacy camera URL with percent-encoded credentials and a Copy
  button for NVR/DVR setup, plus explicit LAN/VLAN and TCP port 554 guidance.
- Add authenticated GET/PUT RTSP endpoints while preserving the legacy
  `{ "enabled": true }` toggle response and the existing HANET P2P live transport.
- Keep RTSP credentials outside public device state; redact camelCase, nested and
  JSON-encoded RTSP secrets/URLs from snapshots, WebSocket and generic APIs.
- Abort in-flight RTSP requests when the camera dialog closes so sensitive URLs do
  not repopulate the browser cache after the user leaves the screen.
- Leave FaceID, departments, recordings, licensing, HANET login and the custom
  component unchanged.

## 0.10.1 - 2026-08-28

- Bắt buộc License Key trước khi mở dashboard hoặc sử dụng API nghiệp vụ; bỏ các
  option người dùng có thể dùng để tắt enforcement hoặc đổi portal production.
- Thêm activation gate toàn màn hình với link `/activate` tự gắn installation ID,
  public key, `client_type=addon` và phiên bản add-on.
- Tự mở License Center khi installation chưa có key; hỗ trợ copy ID, dán key,
  kiểm tra lại và tự quay về gate khi license hết hạn, bị khóa hoặc bị thu hồi.
- Giữ nguyên xác minh chữ ký Ed25519, proof-of-possession, mã hóa key local,
  cache offline 72 giờ và khả năng dùng chung một key cho addon/custom component.
- Không thay đổi luồng camera, P2P, FaceID, phòng ban, clip, HANET login hoặc
  custom component.

## 0.10.0 - 2026-08-24

- Phân tích lại XAPK HANET Connect Android `4.1.21` build `770` và đối chiếu
  trực tiếp contract FaceID, phòng ban, video, sự kiện và chấm công.
- Ưu tiên payload snake_case đúng app: xóa `person_id` dạng chuỗi; tạo FaceID
  multipart đầy đủ; update dùng `department_id` int64; membership dùng
  `department_id` + `person_ids` CSV.
- Giữ fallback có giới hạn cho tenant trả `expected string/int64`, binder lỗi,
  thiếu field hoặc 404; form-urlencoded chỉ chạy sau payload 4.1.21 và mọi
  mutation vẫn được đọc lại cloud để xác nhận/rollback.
- Sửa fallback không chạy khi HANET trả HTTP 500 kèm `returnMessage`, ưu tiên
  `person.person_id` trong row membership lồng nhau và không báo lỗi giả sau khi
  create FaceID thành công nhưng response không có mã người.
- Đổi phòng có đủ profile sẽ thử `person/update` đúng APK trước, xác minh phòng
  mới và phòng cũ rồi mới dùng membership; thêm endpoint nâng cao
  `device_set_alert` và sửa route đăng ký thành `/auth/register` theo AOT.
- Sửa parser clip lồng nhau kế thừa `event_id`/`timestamp` group cha, bỏ `count`
  khỏi tổng phân trang và không mặc định ghi đè `type`/`sex` khi client cũ bỏ
  trống.
- Thêm gửi yêu cầu **Xuất báo cáo chấm công** theo `place_id`, `day_from`,
  `day_to`, `export_type`; catalog nâng lên 102 endpoint.
- Bổ sung regression test cho envelope lỗi HTTP, ID membership lồng nhau, profile
  update, create không trả ID và schema `device_set_alert`.
- Không thay đổi custom component, camera/P2P, Ingress, đăng nhập HANET hoặc
  License Center; `license_required` tiếp tục mặc định `false`.

## 0.9.9 - 2026-08-24

- Sửa thêm Face nhân viên/khách có chọn phòng ban trên tenant trả
  `This field is required` dù ID đã gửi dạng chuỗi.
- Sửa đổi phòng ban cho FaceID trên tenant trả
  `Invalid type: expected string but got number` ở API JSON nội bộ.
- Sau các fallback JSON cũ, gateway tự chuyển sang API form-urlencoded dùng
  `token`, `departmentID` và `personIDs/personID`, thử cả route V4 và route
  tương thích cùng host.
- Đọc membership qua form API có phân trang tối đa 50 người/trang rồi vẫn giữ
  read-after-write, nên không báo thành công giả và không thay đổi custom component.

## 0.9.8 - 2026-08-24

- Sửa xóa FaceID khi route mobile `/business/person/delete` trả 404: ưu tiên
  `personID`, thử cả chuỗi/số, sau đó fallback form-urlencoded tới endpoint
  `/person/removePersonByID` hoặc `/person/remove` trên cùng HANET host.
- Không còn ép mọi `departmentID`, `personID` và `placeID` chuỗi thành JSON number;
  từng mutation giờ thử cả kiểu số và chuỗi theo đúng lỗi schema cloud trả về.
- Sửa tạo phòng ban, đổi phòng ban và thêm Face nhân viên/khách có chọn phòng ban
  trên tenant báo `Invalid type: expected string but got number`.
- Giữ xác minh read-after-write để chỉ báo thành công khi FaceID hoặc membership
  thực sự thay đổi trên cloud.

## 0.9.7 - 2026-08-24

- Mở giao diện trực tiếp qua Home Assistant Ingress, không còn yêu cầu mật khẩu
  dashboard riêng; dữ liệu khóa cũ cũng được tự chuyển sang trạng thái tắt.
- Sửa lỗi `Invalid type: expected int64 but got string` khi cập nhật FaceID và
  membership phòng ban bằng payload numeric cùng fallback schema có kiểm chứng.
- Cho phép khách và nhân viên cùng tạo, chọn, đổi hoặc bỏ phòng ban; CRUD phòng
  ban dùng payload tối thiểu `placeID`/`id` trước khi thử biến thể mobile cũ.
- Nút **Xem clip cùng ngày** ưu tiên `event_id`, fallback theo camera/thời gian và
  tự tua video tới thời điểm xảy ra sự kiện.

## 0.9.6 - 2026-08-24

- Thêm License Center HANET tự động: trial 1 ngày, PayOS QR, webhook đối soát,
  cấp key tự động, dashboard khách hàng và admin lifecycle.
- Add-on tạo installation identity Ed25519 riêng, proof-of-possession mỗi lần
  verify, cache offline 72 giờ và lưu key local bằng AES-GCM.
- Mặc định `license_required: false` để rollout không làm gián đoạn gateway;
  có thể bật enforcement sau khi đã cấu hình portal.
- Giữ license cũ còn hiệu lực nếu người dùng thử nhập một key thay thế không hợp
  lệ; bổ sung option/translation và tài liệu rollout production.

## 0.9.5 - 2026-08-23

- Sửa xóa FaceID khi HANET trả HTTP 200 nhưng `returnCode` báo lỗi; gateway tiếp
  tục thử payload khác và chỉ xác nhận khi FaceID biến mất khỏi danh sách cloud.
- Ưu tiên `personID` hơn `id` chung, bổ sung `faceID`, UUID và các biến thể
  singular/plural để tương thích nhiều tenant mobile API.
- Sửa đổi phòng ban bằng schema chính thức `departmentID`, `personIDs` và
  `personID`; chấp nhận cloud cập nhật membership trễ trước khi thử fallback.
- Thêm menu chọn phòng ban trực tiếp trên từng thẻ nhân viên trong danh sách.
- Audit tài liệu Developer API chính thức: giữ catalog mobile hiện tại, chưa trộn
  endpoint Partner API khác host/auth; ưu tiên tiếp theo là lọc chấm công theo
  người/thời gian và thao tác phòng ban hàng loạt.

## 0.9.4 - 2026-08-23

- Sửa lỗi Face ID bị mất phòng ban sau khi thêm hoặc cập nhật.
- Đồng bộ membership qua `department/list-person`, `department/add-person` và
  `department/remove-person`, có fallback payload cho các phiên bản HANET khác nhau.
- Đọc ngược membership khi tải Face ID để phòng ban hiển thị đúng dù
  `person/list` không trả metadata tổ chức.
- Cho phép bỏ phòng ban khỏi nhân viên và thêm route
  `PUT /api/people/{id}/department` cho automation.
- Audit catalog 100 endpoint; ghi nhận CRUD biển số và thống kê chấm công nâng cao
  là ưu tiên tiếp theo vì schema mutation chưa được xác minh trên thiết bị thật.

## 0.9.3 - 2026-08-22

- Rotate the built-in dashboard password hash without exposing the password in
  the UI, source documentation or regression tests.
- Migrate both previous built-in hash records to the new record and re-enable
  the dashboard lock while preserving custom passwords and saved lock state.
- Refresh the Ingress dashboard with a brighter, smoother Liquid Glass visual
  system and accessible light color contrast.

## 0.9.2 - 2026-08-22

- Require the built-in dashboard password on first use, then allow the
  authenticated user to change it or persistently disable/re-enable the lock.

## 0.9.1 - 2026-08-22

- Split employee FaceID and visitor FaceID into independent identity tabs.
- Fix FaceID deletion with compatible identifier payload fallbacks and a
  dedicated local delete route.
- Accept JPEG, PNG, WebP, GIF, BMP, TIFF, HEIC, HEIF and AVIF uploads, converting
  non-JPEG/PNG images to cloud-compatible JPEG through bundled FFmpeg.
- Fix close and cancel controls in dialogs containing required fields.

## 0.9.0 - 2026-07-29

- Add a separate dashboard password lock without coupling it to HANET Cloud or
  the custom integration.
- Store the built-in password as a PBKDF2-SHA256 hash and persist custom hashes
  in `/data/ui_auth.json` with owner-only permissions.
- Add 12-hour `HttpOnly` sessions, password rotation, logout and temporary
  lockout after repeated failed attempts.
- Require a minimum of four characters for replacement dashboard passwords.
- Redesign the Ingress dashboard with an Aurora/Glass visual system, responsive
  metric cards, a dedicated unlock screen and a security settings panel.
- Stop accepting webhook secrets in query strings so they cannot enter access
  logs; the `X-HANET-Webhook-Secret` header is now required.
- Bind persisted HANET refresh tokens to the configured username so switching
  add-on accounts cannot silently continue the previous cloud session.
- Expand Vietnamese installation, usage, feature, security, API and
  troubleshooting documentation.

## 0.8.0

- Bundle the multi-architecture TUTK runtime in the custom component so Home
  Assistant opens camera P2P video directly without an add-on URL or media key.
- Bundle Alpine's per-architecture gcompat runtime for the isolated custom P2P
  worker, allowing the glibc TUTK SDK to load inside Home Assistant Core's musl
  container without changing or preloading the main Home Assistant process.
- Implement the APK's native PTZ protocol using IOCTRL `4097` and the exact
  direction codes, with a reusable control session and an automatic stop guard.
- Prefer native P2P PTZ in both packages while retaining cloud command fallbacks
  for cameras or accounts that do not expose P2P credentials.
- Verify every camera setting mutation by reading it back from HANET before the
  UI reports success; failed or ignored changes now return a useful error.
- Synchronize camera status/settings and cloud event history every five seconds
  in the add-on when HANET's SSE route is unavailable, and update open setting
  panels from WebSocket state.
- Simplify custom component setup to its own HANET username/password and polling
  interval, with automatic migration away from the retired add-on media proxy.

## 0.7.0

- Fix PTZ with the mobile app's `start_ptz`/`stop_ptz` command lifecycle,
  press-and-hold controls and a legacy firmware fallback.
- Let Home Assistant Core reach P2P media through the internal port 9091 path;
  migrate old media URLs, expose bridge connectivity and keep optional key
  validation for external URLs.
- Add familiar/stranger detection entities, recognition timestamps, per-person
  FaceID images and richer Vietnamese event names.
- Turn discovered writable boolean and numeric camera settings into native
  Home Assistant controls while retaining every scalar diagnostic sensor.
- Replace the Ingress interface with a responsive camera operations dashboard
  and verify camera cards and PTZ controls at desktop and mobile sizes.

## 0.6.0

- Fix FaceID image upload by sending HANET's required multipart `file` field
  instead of the incompatible `image` field.
- Prefer a place containing cameras when creating or bulk-importing FaceIDs.
- Make the Home Assistant integration authenticate directly with HANET Cloud;
  the add-on URL and key are now optional and used only for P2P media.
- Expose all model-specific scalar settings as diagnostic sensors and add nested
  setting controls plus aliases for recording, detection, security and PTZ.
- Preserve online state and placement while merging partial device-detail
  responses.

## 0.5.0

- Discover owned and shared places through both HANET mobile APIs and the
  authenticated HANET Connect web inventory; camera IDs are no longer required.
- Expose complete employee and visitor FaceID collections, per-person recognition
  sensors, event entities and latest-event image entities in Home Assistant.
- Add Vietnamese entity/action translations plus account, hardware, storage,
  network and recognition sensors.
- Add FaceID create, update, delete and bulk-import actions, with local image path
  validation, and add employee/department management to the Ingress interface.
- Add recording-history actions and reconnect the same MJPEG response when a
  transient P2P session ends.
- Improve desktop/mobile identity filters, quick event/clip review and responsive
  controls while keeping live playback only in the Home Assistant camera entity.

## 0.4.0

- Load and merge both HANET FaceID categories: employees (`type=0`) and visitors
  (`type=1`), instead of showing only the four default employee records.
- Map cloud tracking codes to employee, visitor, stranger, alarm and human events;
  retain the original type code and recognition state.
- Raise the daily event ceiling to 2,000 and add fast filters for date, camera,
  event type, source, search text and recording time period.
- Link event details to cloud clips from the same camera/day and link each clip
  back to its matching event list.
- Remove live viewing from the add-on UI while preserving the P2P/MJPEG gateway
  endpoint used by the Home Assistant camera entity.
- Add per-camera Home Assistant sensors for latest event, latest person and event
  type, including event image, time, place and recognition attributes.

## 0.3.1

- Fix the modern TUTK Linux client output structure used by Home Assistant add-on
  hosts; the old undersized structure could corrupt memory before video arrived.
- Share one native P2P/FFmpeg pipeline per camera across Ingress, Home Assistant
  camera entities and additional browser tabs instead of competing for sessions.
- Keep an idle stream briefly for quick reconnects and retry once with fresh cloud
  credentials when the initial P2P handshake or first frame fails.
- Serve active frames or cloud event images to snapshot polling without opening a
  second P2P session that interrupts live playback.
- Increase the Home Assistant MJPEG proxy read tolerance and explicitly close its
  upstream response when a viewer leaves.

## 0.3.0

- Stream remote HANET cameras through their cloud-issued TUTK P2P session; the
  gateway no longer requires Home Assistant and the camera to share a LAN.
- Add isolated native P2P workers for `amd64`, `aarch64` and `armv7`, HEVC
  keyframe synchronization, FFmpeg MJPEG conversion and clean session shutdown.
- Serialize video sessions per camera so thumbnail requests cannot interrupt live
  playback, while different cameras can still connect in parallel.
- Add a clear per-camera RTSP switch backed by HANET Cloud. RTSP is a firmware
  option and is not used as the gateway's live transport.
- Replace the raw dashboard with focused Camera, Events, Recordings, Identity and
  Settings workspaces, responsive navigation and local Lucide icons.
- Show detection images, playable cloud recordings, Face ID cards, attendance,
  PTZ controls and model-specific settings without exposing raw JSON by default.
- Move the add-on image to glibc-based Debian for the native runtime and fix the
  container healthcheck without adding another system utility.

## 0.2.0

- Replace raw response tables with task-focused camera, event, Face ID, recording,
  license plate and attendance views.
- Load cloud event history with the required case-sensitive `Day` field and display
  HANET detection images through a restricted media proxy.
- Fix truncated image/video responses and avoid sending API Bearer tokens to HANET
  static object-storage hosts.
- Add cloud recording thumbnails and playable MP4 clips for each camera and day.
- Add an FFmpeg RTSP-to-MJPEG bridge with recent-event snapshot fallback.
- Fix the mobile API schemas for device settings and user notification settings.
- Preserve device settings between polls and load hardware/user settings together.
- Normalize webhook, SSE, Face ID, plate and attendance records for readable UI cards.
- Proxy MJPEG through the companion integration without exposing the gateway key in
  a stream URL.

## 0.1.3

- Recover cloud places omitted by `place/list` from optional camera IDs.
- Load every device in a recovered place after resolving its numeric `place_id`.
- Recognize the mobile API's `is_active` field as the camera online state.

## 0.1.2

- Use the verified `POST /stream/checkin` SSE endpoint with numeric `place_ids`.
- Ignore SSE heartbeat events and stop retrying the nonexistent `/event-stream` route.
- Show an explicit gateway notice when HANET Cloud returns zero devices.

## 0.1.1

- Preserve string IDs in Home Assistant while sending numeric database IDs to HANET as `int64`.
- Use the working profile endpoint for account details.
- Change the gateway, Ingress and integration port to `9091`.

## 0.1.0

- Initial HANET Connect 4.1.10 API catalog.
- Ingress dashboard, persistent token refresh and event stream bridge.
- Device settings, commands, media, FaceID, LPR, attendance and raw API access.

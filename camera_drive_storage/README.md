# Camera Drive Storage (add-on)

Record RTSP/ONVIF cameras continuously or on motion, upload to Google Drive,
all configured from a built-in web UI (Home Assistant Ingress panel). MQTT
auto-discovery exposes entities to Home Assistant.

## Install

1. Copy this folder to `/addons/camera_drive_storage/` on the HA host.
2. Settings → Add-ons → Add-on Store → ⋮ → Check for updates → install
   "Camera Drive Storage".
3. Start. Open the panel from the sidebar (icon `mdi:video-vault`).

## Configure in the UI

No YAML editing needed. Config is stored in `/data/runtime_config.json`
(written by the UI). Tabs:

- **Status** — Tổng quan dashboard (cards: đang ghi, clip hoàn tất, chờ tải,
  đã lên Drive) + per-camera table: `state`, `segments_completed`, `pending`,
  `upload_state` (waiting_drive/idle/uploading/error), `uploaded`,
  `last_record_error`, `last_upload_error`, `last_upload_at`.
- **Cameras** — add/edit/delete cameras (RTSP URL, mode, motion source,
  ONVIF creds, sensitivity).
- **Google Drive** — enter OAuth client + authorize, see account/quota.
- **Settings** — global mode, segment length, storage destinations
  (Drive / local HA / mounted NAS), MQTT broker.

## Google auth (in-UI, easiest path)

The **Google Drive** tab defaults to **Quick mode**, which uses rclone's
shared Google OAuth client — you do **not** create a Google Cloud project
and do **not** paste any client_id/secret or token.

1. Open the **Google Drive** tab → **Open Google consent page**.
2. Allow access. The browser then fails to load
   `http://127.0.0.1:53682/...` (expected — that server is not reachable).
3. Copy the full URL from the address bar.
4. Paste it into **Redirected URL or code** → **Exchange for token**. Done.

Scope `drive.file` — the add-on only sees files it creates.

> Note: Google is retiring rclone's shared client during 2026. If Quick mode
> stops working, switch the dropdown to **Custom**, create your own OAuth
> client ("Web application", enable Drive API, add redirect
> `http://localhost`), and paste client_id + secret. The code-paste flow is
> unchanged.

The manual code-paste flow (instead of a callback URL) is used because HA
Ingress is not reachable by Google's OAuth callback servers.

## Add camera by brand (templates)

Cameras tab → **Thêm camera theo hãng**: chọn hãng, nhập IP / user / pass /
channel / stream, add-on tự dựng URL đúng mẫu gốc:

| Hãng | URL sinh ra |
|---|---|
| Dahua / IMOU | `rtsp://user:pass@host:554/cam/realmonitor?channel=1&subtype=0` |
| Hikvision | `rtsp://user:pass@host:554/h264/ch01/main/av_stream` |
| EZVIZ | `rtsp://admin:CODE@host:554/h264/ch1/main/av_stream` |
| Hanet | `rtsp://host:554/user:hanet;pwd:pass` |
| ONVIF | `onvif://user:pass@host:80/onvif/device_service` |
| Manual | tự nhập URL bất kỳ |

Credentials được percent-encode an toàn; ONVIF chỉ cần bấm Authorize/Resolve
sau đó. Template ở `app/web.py:TEMPLATES` — thêm hãng mới chỉ cần thêm 1 dict.

## Supported stream URL formats

Paste any of these into **Cameras → Bulk import**:

| Brand / form | Example shape |
|---|---|
| Dahua / IMOU / EZVIZ (main) | `rtsp://user:pass@host:554/cam/realmonitor?channel=1&subtype=0` |
| Hikvision / Ezviz | `rtsp://user:pass@host:554/h264/ch01/main/av_stream` |
| Hanet | `rtsp://host:554/user:user;pwd:pass` (kept verbatim) |
| ONVIF only | `onvif://user:pass@host:80/onvif/device_service` |

ONVIF-only cameras are resolved to RTSP automatically via
`GetCapabilities → GetProfiles → GetStreamUri` (button **Resolve ONVIF→RTSP**
in the camera card). Credentials inside the URL are extracted automatically.

### Bulk import

Tools → Cameras tab → **Bulk import**. Accepts YAML:

```yaml
streams:
  nhaduoi:
    - rtsp://admin:pass@192.168.5.111:554/cam/realmonitor?channel=1&subtype=0
  aotom:
    - onvif://admin:pass@192.168.5.159:80/onvif/device_service
```

or one line per camera `name: rtsp://...`. Existing names are updated.

## Camera test & live view

- **Cameras** tab → **Test kết nối** runs `ffprobe` against the RTSP URL and
  reports codec / resolution / fps, or the exact error. **Snapshot** grabs a
  single JPEG frame.
- **Live** tab is opt-in per camera (max 2 concurrent MJPEG streams, fps
  1/2/5, width 480/640/960) so it never starves HA. Streams pause when the
  browser tab is hidden and auto-stop after 120s (`/api/camera/stream/cancel`
  for instant stop).

## Flow

```
RTSP ──► ffmpeg segment muxer ──► /data/spool/<cam>/<Y>/<M>/<D>/seg.mp4
                                        │  motion? keep only overlapping segments
                                        ▼
                                   upload queue ──► Drive /<root>/<cam>/<Y>/<M>/<D>/
                                        │           local /media/…/<cam>/<Y>/<M>/<D>/
                                        │           NAS  /media/<name>/…/<cam>/…
                                        ▼
                        Drive retention (drive_keep_days / drive_max_gb)
                        local/NAS archives kept until removed manually
```

## Motion detection

Per camera `motion_source`:

- `onvif` — PullPoint subscription (needs ONVIF URL + credentials)
- `scene` — ffmpeg `select=gt(scene,TH)` on 2fps grayscale (no OpenCV)
- `auto` — tries ONVIF, falls back to scene

## MQTT entities (auto-discovery)

- `binary_sensor.cam_<name>_motion`
- `binary_sensor.cam_<name>_recording`
- `sensor.cam_<name>_last_clip`
- `sensor.cam_<name>_uploaded`
- `sensor.cam_<name>_upload_errors`

## Live view

Add a `generic`/`onvif` camera in HA pointing at the same RTSP URL. This
add-on records; it does not replace `camera.*` entities.

## Storage destinations (Drive, local HA, NAS)

Each clip can be delivered to any combination of targets, chosen per clip when
it is queued. A source clip is removed from the spool only after **every**
selected target has a durable receipt.

- **Google Drive** — cloud archive (unchanged; default target).
- **Local HA** — a dedicated folder under `/media` (default
  `/media/camera_drive_storage`), optionally under `/share`.
- **NAS** — a mounted NFS/CIFS share. Home Assistant mounts network storage
  itself: **Settings → System → Storage → Add network storage**, choose usage
  **Media** (appears at `/media/<name>`) or **Share** (`/share/<name>`), then
  point the add-on at a dedicated subfolder (e.g. `/media/nas_name/camera_drive_storage`).
  The add-on never mounts the NAS and never stores NAS credentials.

The add-on refuses a NAS path that is not a subdirectory of a mounted NFS/CIFS
share, so a disconnected share can never silently fall back to HA storage.
Local and NAS archives are **not** auto-pruned: they are kept until you remove
them. A low-space reserve (256 MiB) pauses new copies and keeps recordings in
the spool instead of deleting them. `keep_days` remains a legacy spool setting,
not an archive retention policy.

## Cloud playback & themes

The **Xem lại** tab replays stored clips like a vendor app: choose a source
(Google Drive, local HA, NAS), a camera and a day, then play a clip in the
browser (HTTP Range streaming) or download it. Dark/light themes are available
from the workspace bar toggle and follow the system preference by default.

## Drive HTTP 403 troubleshooting

`Drive folder lookup failed (HTTP 403)` means Google refused a request; it does
**not** by itself mean the OAuth connection was lost. The add-on now keeps the
Google `reason` and shows it:

- `rateLimitExceeded` / `userRateLimitExceeded` — transient. The add-on backs
  off and retries automatically (shared cooldown across upload, playback and
  retention); clips stay queued.
- `insufficientPermissions` / `insufficientFilePermissions` /
  `appNotAuthorizedToFile` — a permission or sharing issue. Review the Drive
  account/scopes; other files keep working.
- `domainPolicy` / `SERVICE_DISABLED` / `accessNotConfigured` /
  `ACCESS_TOKEN_SCOPE_INSUFFICIENT` — project or admin configuration. Enable the
  Drive API and check the OAuth client/scopes in Google Cloud.
- `storageQuotaExceeded` — the Drive account is full.
- `invalid_grant` — the authorization was revoked or expired (Custom OAuth in
  "Testing" expires the refresh token after ~7 days). Re-authorize Drive.

Unconfirmed clips are never deleted; they stay in the spool and retry. Do not
disconnect OAuth just because of a 403. Changing the OAuth client can hide older
clips because `drive.file` only shows files created by the current client.

## Recording pipeline notes

- A segment is uploaded only after it is **closed** (after
  `segment_seconds`, plus keyframe delay), and only when Drive credentials
  are present. Before that, status shows `waiting_drive`/`pending`.
- **A successful "Test kết nối" does not mean clips are being uploaded.**
  Watch `state` = `recording`, `segments_completed` and `uploaded` in Status.
- Credentials are added to the RTSP URL automatically (Hanet `user:…;pwd:…`
  kept verbatim). ONVIF-only cameras resolve to RTSP in the recorder, with
  retry/backoff, so the UI is never blocked.
- Invalid configuration (e.g. `upload_workers: 0`, duplicate camera names,
  bad range) is rejected with a safe 400 instead of silently disabling
  recording/upload.
- Local buffer never deletes segments that have not been confirmed on Drive;
  recording pauses (`paused_buffer_full`) when the buffer limit or disk space
  is reached.
- `upload_errors` counts each clip once (not once per retry). A clean FFmpeg
  exit returns `state` to `connecting`, not `error`.
- Drive retention reuses the root folder already created by uploads; before
  the first upload it reports `retention_state=waiting_for_first_upload`
  instead of a folder-lookup error.

## License activation

This is an enforced release (`ENFORCE=True`). The add-on requires an activated
License Key before it starts new recording. Existing uploads, the web UI, the
local buffer and MQTT stay available, so already-recorded clips are not lost.

One key activates exactly one add-on installation (Home Assistant). Moving to
another installation needs an admin reset.

1. Open the **License** tab and follow the portal link.
2. Register with email + password (phone optional).
3. Claim the 24-hour trial (one per account and installation, starting at
   first activation) or buy a plan:
   weekly 50,000 VND or lifetime 200,000 VND, paid by PayOS QR.
4. The key appears in the dashboard once PayOS confirms payment.
5. Paste the `CC-...` key into the add-on and activate.

The portal signs a short-lived lease. Without a network connection the add-on
keeps working on the verified lease for up to 72 hours, never past the plan
expiration. Expiry or revocation stops new recording safely; activation resumes
it without restarting Home Assistant. Keep `/data/license_identity.json` in
private backups; do not delete it during updates or share it. Payment and server
credentials never enter the add-on.

## Test status

339 add-on tests pass (2 skip without FFmpeg). Coverage includes multi-target
storage delivery/retry, filesystem path and mount safety, local/NAS playback
ranges and resource cleanup, plus the compiled runtime. Ruff, Pyright and
JavaScript syntax checks pass. Browser tests cover the storage settings, License
and existing dashboard/Drive forms on mobile and desktop. License/PayOS/Drive
network responses are mocked in tests; a separate production smoke run validated
activation, lock/unlock, reset and PayOS checkout creation against the live
portal. No real transfer, NAS mount or production Home Assistant upgrade was
performed. Runtime recorder, motion, uploader, Drive and MQTT implementation is
preserved relative to the stable input copy.

The published image contains compiled first-party modules and no first-party
`.py` source; base-image and third-party Python remains. A determined operator
with root on the Home Assistant host can still reverse engineer native code, so
this is not absolute copy protection.
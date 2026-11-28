# AI Proxy Router

**Phiên bản 1.23.0** · Home Assistant OS / Supervised · `amd64`, `aarch64`

AI Proxy Router gom nhiều nguồn AI vào một API tương thích OpenAI, tự xoay API key, chuyển nguồn khi lỗi và định tuyến Text/Vision tự động. Dashboard chỉ mở qua Home Assistant Ingress; ứng dụng bên ngoài gọi `/v1/*` bằng Proxy Key.

Hướng dẫn đầy đủ song ngữ nằm trong `README.md`. Trang này là bản tóm tắt dùng trong Add-on Store.

**Ngôn ngữ:** [Tiếng Việt](#tiếng-việt) · [English](#english)

---

## Tiếng Việt

### 1. Cài đặt

1. Mở **Settings → Add-ons → Add-on Store**.
2. Mở menu ba chấm → **Repositories**.
3. Thêm:

   ```text
   https://github.com/trankhanhduy2929-beep/my_hass_addon_public
   ```

4. Tìm **AI Proxy Router → Install**.
5. Bật **Start on boot**, **Watchdog** và **Show in sidebar** nếu cần.
6. Nhấn **Start**, mở **Web UI**.

Port `1236` mặc định không publish. Chỉ bật trong **Network** khi client LAN cần gọi trực tiếp `/v1/*`. Dashboard và `/api/*` vẫn chỉ truy cập qua Ingress.

### 2. Bắt đầu nhanh

1. Mở tab **Nguồn & Key**.
2. Chọn provider hoặc **Custom Endpoint**, dán API key thật, bấm **Thêm & tự dò model**.
3. Mở **Quản lý Proxy Keys**, tạo key cho ứng dụng.
4. Mở **Test AI**, chạy Chat/Vision để kiểm tra.
5. Mở **Endpoint**, sao chép Base URL.
6. Cấu hình ứng dụng:

   ```text
   Base URL: http://HOME_ASSISTANT_IP:1236/v1
   API Key: sk-proxy-...
   Model: auto-ai
   ```

7. Nếu dùng từ xa, xem mục **Truy cập từ Internet** bên dưới.

### 3. Truy cập từ Internet

Không dùng URL Ingress của Home Assistant làm Base URL API.

#### Reverse proxy HTTPS

Chỉ forward `/v1/*` tới add-on, giữ dashboard và `/api/*` nội bộ. Nếu reverse proxy chạy cùng Docker network, dùng hostname nội bộ của add-on; nếu chạy trên host/LAN, publish port `1236` rồi trỏ tới IP LAN.

Sau khi có URL:

1. Mở **Endpoint → Kết nối bên ngoài**.
2. Nhập **Public Base URL**, ví dụ `https://ai.example.com/v1`.
3. Lưu và kiểm tra bằng request thật.

#### Cloudflare Tunnel

1. Cài add-on **Cloudflared**.
2. Thêm hostname public một cấp, ví dụ `ai.example.com`.
3. Trỏ service tới AI Proxy Router:

   ```yaml
   additional_hosts:
     - hostname: ai.example.com
       service: http://<ai-proxy-container>:1236
   ```

4. Restart Cloudflared và chờ tunnel kết nối lại.
5. Kiểm tra:

   ```bash
   curl -i "https://ai.example.com/health"
   curl -i "https://ai.example.com/v1/models" \
     -H "Authorization: Bearer sk-proxy-YOUR_KEY"
   ```

6. Nhập `https://ai.example.com/v1` vào **Public Base URL**.

Lưu ý:

- Cloudflare Universal SSL thường chỉ phủ `example.com` và `*.example.com`. Dùng `ai.example.com`, không dùng `ai.ha.example.com` nếu không có chứng chỉ phù hợp.
- Lỗi TLS thường gặp: `sslv3 alert handshake failure` hoặc `SSL alert number 40`.
- Restart Cloudflared có thể gây `530`/`error code: 1033` tạm thời.
- Không public dashboard, `/api/*` hoặc Ingress URL.
- Nếu bật Cloudflare Access cho API, client phải gửi service token; nhiều ứng dụng không hỗ trợ.

### 4. Proxy Key và bảo mật

- Tạo Proxy Key riêng cho từng ứng dụng.
- Không đưa API key gốc của provider cho ứng dụng bên ngoài.
- Đặt hạn mức, rate limit và ngày hết hạn.
- Tạo lại key ngay nếu bị lộ.
- Backup chứa bí mật; hãy mã hóa và không chia sẻ.
- Chỉ dùng HTTPS khi truy cập từ xa.
- Giữ `/`, `/api/*`, `/docs`, `/redoc`, `/openapi.json` ngoài Internet.

Từ `1.23.0`:

- Hỗ trợ nguồn **OpenCode** và **Command Code**.
- Tự lọc model theo endpoint và lưu khả năng Vision từ metadata.
- Có gợi ý chọn nhanh nguồn có model ảnh miễn phí.

Từ `1.22.0`:

- `/docs` và `/redoc` bị tắt.
- `/openapi.json` chỉ mở qua Home Assistant Ingress.
- Response có thêm `X-Content-Type-Options: nosniff` và `Referrer-Policy: no-referrer`.

### 5. Kiểm tra và xử lý sự cố

| Hiện tượng | Cách xử lý |
|---|---|
| Dashboard không mở | Mở từ **Web UI** hoặc sidebar Home Assistant |
| Client LAN không kết nối | Publish port `1236` trong **Network** |
| `401` | Kiểm tra `Authorization: Bearer sk-proxy-...` |
| `402`/`403`/`429` | Kiểm tra hạn mức, trạng thái key, ngày hết hạn, rate limit |
| `503` | Kiểm tra nguồn, model, key và log |
| `530`/`1033` | Cloudflared chưa kết nối; chờ 1–2 phút và xem log |
| Lỗi TLS `alert 40` | Dùng hostname một cấp hoặc chứng chỉ phù hợp |
| Public Base URL báo Đã cấu hình nhưng lỗi | Kiểm tra DNS, TLS, tunnel, firewall; gọi thử `/health` |
| Voice `503` | Thêm nguồn có model STT/TTS và đồng bộ |
| Headroom offline | Chạy dịch vụ `/v1/compress` và kiểm tra URL |

Kiểm tra nhanh:

```bash
curl -i "https://ai.example.com/health"

curl -i "https://ai.example.com/v1/models" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY"
```

### 6. Nâng cấp

1. Tải backup trong **Hệ thống**.
2. Cập nhật add-on từ Add-on Store.
3. Kiểm tra phiên bản, `/health`, `/v1/models` và một request chat.
4. Nếu lỗi, xem **Log** và khôi phục backup khi cần.

### 7. Liên kết

- Kho add-on: `https://github.com/trankhanhduy2929-beep/my_hass_addon_public`
- Hướng dẫn đầy đủ: `README.md`
- API: `/v1/models`, `/v1/chat/completions`, `/v1/responses`, `/v1/audio/transcriptions`, `/v1/audio/speech`
- Health check: `/health`

---

## English

### 1. Install

1. Open **Settings → Add-ons → Add-on Store**.
2. Open the top-right menu → **Repositories**.
3. Add:

   ```text
   https://github.com/trankhanhduy2929-beep/my_hass_addon_public
   ```

4. Find **AI Proxy Router → Install**.
5. Enable **Start on boot**, **Watchdog**, and **Show in sidebar** if desired.
6. Select **Start**, then open **Web UI**.

Port `1236` is not published by default. Enable it in **Network** only when a LAN client must call `/v1/*` directly. Dashboard and `/api/*` remain Ingress-only.

### 2. Quick start

1. Open **Sources & Keys**.
2. Choose a provider or **Custom Endpoint**, paste a provider API key, and click **Add and discover models**.
3. Open **Manage Proxy Keys** and create a key for the app.
4. Open **Test AI** and run a Chat/Vision test.
5. Open **Endpoint** and copy the Base URL.
6. Configure the app:

   ```text
   Base URL: http://HOME_ASSISTANT_IP:1236/v1
   API Key: sk-proxy-...
   Model: auto-ai
   ```

7. For remote access, see **Internet access** below.

### 3. Internet access

Never use the Home Assistant Ingress URL as an API Base URL.

#### HTTPS reverse proxy

Forward only `/v1/*` to the add-on and keep the dashboard and `/api/*` internal. If the proxy shares the add-on Docker network, use the add-on's internal hostname. If the proxy runs on the host/LAN, publish port `1236` and use the LAN address.

After the public URL works:

1. Open **Endpoint → External access**.
2. Enter the **Public Base URL**, for example `https://ai.example.com/v1`.
3. Save and verify with a real request.

#### Cloudflare Tunnel

1. Install the **Cloudflared** add-on.
2. Add a one-level public hostname such as `ai.example.com`.
3. Point the service at AI Proxy Router:

   ```yaml
   additional_hosts:
     - hostname: ai.example.com
       service: http://<ai-proxy-container>:1236
   ```

4. Restart Cloudflared and wait for the tunnel to reconnect.
5. Test:

   ```bash
   curl -i "https://ai.example.com/health"
   curl -i "https://ai.example.com/v1/models" \
     -H "Authorization: Bearer sk-proxy-YOUR_KEY"
   ```

6. Enter `https://ai.example.com/v1` as the **Public Base URL**.

Notes:

- Cloudflare Universal SSL normally covers `example.com` and `*.example.com`. Use `ai.example.com`, not `ai.ha.example.com` without a suitable certificate.
- Common TLS errors: `sslv3 alert handshake failure` or `SSL alert number 40`.
- A Cloudflared restart can cause temporary `530`/`error code: 1033` responses.
- Do not expose the dashboard, `/api/*`, or the Ingress URL.
- Cloudflare Access requires service tokens; many OpenAI-compatible clients do not support them.

### 4. Proxy Keys and security

- Create a separate Proxy Key for each app.
- Never give provider API keys to external apps.
- Set budgets, rate limits, and expiration dates.
- Regenerate a key immediately if it leaks.
- Backups contain secrets; encrypt and protect them.
- Use HTTPS for remote access.
- Keep `/`, `/api/*`, `/docs`, `/redoc`, and `/openapi.json` off the Internet.

From `1.23.0`:

- Added **OpenCode** and **Command Code** sources.
- Models are filtered by endpoint, and Vision capability is stored from metadata.
- Free image-model source quick picks are available in Sources & Keys.

From `1.22.0`:

- `/docs` and `/redoc` are disabled.
- `/openapi.json` is available only through Home Assistant Ingress.
- Responses include `X-Content-Type-Options: nosniff` and `Referrer-Policy: no-referrer`.
- Public `/health` returns only status, name, version, and uptime; use `/health` or `/api/health` through Ingress for full details.

### 5. Troubleshooting

| Symptom | Fix |
|---|---|
| Dashboard does not open | Open **Web UI** or the Home Assistant sidebar |
| LAN client cannot connect | Publish port `1236` in **Network** |
| `401` | Check `Authorization: Bearer sk-proxy-...` |
| `402`/`403`/`429` | Check budget, key state, expiration, and rate limit |
| `503` | Check sources, models, keys, and logs |
| `530`/`1033` | Cloudflared is not connected; wait 1–2 minutes and check logs |
| TLS `alert 40` | Use a one-level hostname or a suitable certificate |
| Public Base URL says Configured but fails | Check DNS, TLS, tunnel, firewall, and `/health` |
| Voice `503` | Add an STT/TTS source and sync |
| Headroom offline | Run the `/v1/compress` service and check its URL |

Quick checks:

```bash
curl -i "https://ai.example.com/health"

curl -i "https://ai.example.com/v1/models" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY"
```

### 6. Upgrade

1. Download a backup from **System**.
2. Update the add-on from the Add-on Store.
3. Check the version, `/health`, `/v1/models`, and a chat request.
4. If something fails, check **Log** and restore the backup when needed.

### 7. Links

- Add-on repository: `https://github.com/trankhanhduy2929-beep/my_hass_addon_public`
- Full guide: `README.md`
- API: `/v1/models`, `/v1/chat/completions`, `/v1/responses`, `/v1/audio/transcriptions`, `/v1/audio/speech`
- Health check: `/health`

# AI Proxy Router cho Home Assistant

**Phiên bản 1.22.0** · Home Assistant OS / Supervised · `amd64`, `aarch64`

AI Proxy Router gom nhiều nguồn AI vào một API tương thích OpenAI, tự xoay API key, chuyển nguồn khi lỗi và định tuyến riêng cho yêu cầu Text/Vision. Dashboard chạy trong Home Assistant; ứng dụng bên ngoài chỉ gọi API `/v1/*` bằng Proxy Key.

> Điểm quan trọng: **Dashboard dùng Home Assistant Ingress**, còn **API dùng Base URL `/v1`**. Không dùng URL Ingress của Home Assistant làm Base URL cho ứng dụng.

**Ngôn ngữ:** [Tiếng Việt](#tiếng-việt) · [English](#english)

---

## Tiếng Việt

### Mục lục

1. [Giới thiệu](#1-giới-thiệu)
2. [Yêu cầu](#2-yêu-cầu)
3. [Cài đặt và nâng cấp](#3-cài-đặt-và-nâng-cấp)
4. [Bắt đầu nhanh trong 5 phút](#4-bắt-đầu-nhanh-trong-5-phút)
5. [Các tab trên dashboard](#5-các-tab-trên-dashboard)
6. [Thêm nguồn AI và API key](#6-thêm-nguồn-ai-và-api-key)
7. [Tạo và quản lý Proxy Key](#7-tạo-và-quản-lý-proxy-key)
8. [Endpoint, LAN và truy cập từ Internet](#8-endpoint-lan-và-truy-cập-từ-internet)
9. [Kết nối ứng dụng và Home Assistant](#9-kết-nối-ứng-dụng-và-home-assistant)
10. [Gọi API OpenAI-compatible](#10-gọi-api-openai-compatible)
11. [Voice: Speech-to-Text và Text-to-Speech](#11-voice-speech-to-text-và-text-to-speech)
12. [Token Saver](#12-token-saver)
13. [Usage, Quota, nhật ký và Telegram](#13-usage-quota-nhật-ký-và-telegram)
14. [Backup, khôi phục và nâng cấp](#14-backup-khôi-phục-và-nâng-cấp)
15. [Bảo mật](#15-bảo-mật)
16. [Xử lý sự cố](#16-xử-lý-sự-cố)
17. [Câu hỏi thường gặp](#17-câu-hỏi-thường-gặp)
18. [Thông tin kỹ thuật](#18-thông-tin-kỹ-thuật)

### 1. Giới thiệu

AI Proxy Router là add-on Home Assistant dùng để:

- gom nhiều API key của nhiều nhà cung cấp AI vào một chỗ;
- cấp cho từng ứng dụng một Proxy Key riêng, có hạn mức và rate limit;
- tự chuyển sang key/nguồn khác khi nguồn hiện tại lỗi, hết quota hoặc bị rate limit;
- cung cấp một Base URL duy nhất cho các ứng dụng hỗ trợ OpenAI API.

```text
Ứng dụng / Home Assistant / CLI
              |
              |  /v1/*  +  Proxy Key
              v
      AI Proxy Router (add-on)
              |
              |  xoay key, failover, auto-ai
              v
  Groq / Gemini / OpenAI / OpenRouter / DeepSeek / Custom Endpoint
```

Các trường hợp sử dụng phổ biến:

| Nhu cầu | Cách dùng |
|---|---|
| Một Base URL cho nhiều ứng dụng | Tạo Proxy Key riêng cho từng ứng dụng, dùng chung `/v1` |
| Tiết kiệm chi phí | Ưu tiên nguồn free ở trên, nguồn trả phí ở dưới |
| Dùng model tự động | Chọn model `auto-ai` |
| Dùng ảnh | Gửi nội dung Vision; router tự chọn nguồn hỗ trợ ảnh |
| Dùng từ xa | Cloudflare Tunnel hoặc reverse proxy HTTPS, chỉ public `/v1/*` |
| Kiểm soát ngân sách | Đặt hạn mức cho nguồn và Proxy Key |
| Giảm token | Bật Token Saver |

Tính năng chính:

- `/v1/models`, `/v1/chat/completions`, `/v1/responses`, `/v1/audio/transcriptions`, `/v1/audio/speech`.
- SSE streaming, function tools, `tool_choice`, `parallel_tool_calls`, `function_call_output`.
- Structured Output dạng JSON Object/JSON Schema, có kiểm tra và failover khi output sai schema.
- Model `auto-ai` tự chọn nguồn Text/Vision còn hoạt động.
- Tự dò model từ một API key; tự đồng bộ model mỗi 6 giờ.
- Token Saver gồm RTK, Headroom, Caveman và Ponytail.
- Proxy Key theo từng ứng dụng, có hạn mức, rate limit, ngày hết hạn và trạng thái bật/tắt.
- Dashboard song ngữ Việt/Anh, tối ưu cho desktop và điện thoại.
- Thống kê token/chi phí, kiểm tra nguồn, Telegram, backup/restore và debug bundle đã che bí mật.

### 2. Yêu cầu

- Home Assistant OS hoặc Home Assistant Supervised có Add-on Store.
- Kiến trúc `amd64` hoặc `aarch64`. Add-on không khai báo `armv7`.
- Kết nối Internet để gọi nhà cung cấp AI và tự dò model.
- Ít nhất một API key của nhà cung cấp AI.
- Với truy cập từ Internet: một tên miền và HTTPS. Cloudflare Tunnel là cách được khuyến nghị trong tài liệu này.

Không cần mở port `1236` nếu chỉ dùng dashboard hoặc Cloudflared cùng Home Assistant. Port `1236` chỉ cần khi một ứng dụng bên ngoài gọi thẳng vào IP LAN của Home Assistant.

### 3. Cài đặt và nâng cấp

#### Cài từ kho add-on

1. Mở **Settings → Add-ons → Add-on Store**.
2. Mở menu ba chấm ở góc phải, chọn **Repositories**.
3. Thêm URL:

   ```text
   https://github.com/trankhanhduy2929-beep/my_hass_addon_public
   ```

4. Tìm **AI Proxy Router**, chọn **Install**.
5. Bật **Start on boot** và **Watchdog** nếu muốn add-on tự khởi động và tự phục hồi.
6. Bật **Show in sidebar** để mở nhanh từ thanh bên Home Assistant.
7. Nhấn **Start**, sau đó mở **Web UI**.

#### Cài thủ công từ thư mục add-on

Nếu bạn nhận được file ZIP hoặc thư mục nguồn:

1. Giải nén thư mục `ai_proxy_router` vào thư mục add-on cục bộ, thường là `/addons/ai_proxy_router`.
2. Vào **Settings → Add-ons → Add-on Store**.
3. Mở menu ba chấm và chọn **Check for updates** hoặc tải lại trang.
4. Chọn **AI Proxy Router → Install → Start**.

#### Bật port LAN cho API

Port `1236` mặc định không được publish.

1. Mở add-on **AI Proxy Router**.
2. Vào tab **Configuration** hoặc **Network**.
3. Ở phần port, gán host port `1236` cho container port `1236/tcp`.
4. Lưu và khởi động lại add-on.

Chỉ bật port này khi client LAN cần gọi trực tiếp. Dashboard và `/api/*` vẫn bị chặn nếu không đi qua Home Assistant Ingress.

#### Nâng cấp add-on

1. Vào **Hệ thống** trên dashboard, tải một bản backup mới.
2. Trong Add-on Store, mở **AI Proxy Router** và chọn **Update**.
3. Chờ add-on khởi động lại, mở dashboard và kiểm tra số phiên bản ở góc giao diện.
4. Kiểm tra `/health`, `/v1/models` và một request chat ngắn.
5. Nếu có lỗi, xem **Log** của add-on trước khi khôi phục backup.

Bản `1.22.0` thay đổi tài liệu và siết API docs:

- `/docs` và `/redoc` bị tắt.
- `/openapi.json` chỉ mở qua Home Assistant Ingress.
- Response được thêm `X-Content-Type-Options: nosniff` và `Referrer-Policy: no-referrer`.

### 4. Bắt đầu nhanh trong 5 phút

| Bước | Việc cần làm | Kết quả |
|---|---|---|
| 1 | Mở **AI Proxy → Web UI** | Dashboard mở qua Ingress |
| 2 | Vào **Nguồn & Key**, chọn provider, dán API key, bấm **Thêm & tự dò model** | Có ít nhất một nguồn và danh sách model |
| 3 | Vào **Nguồn & Key → Quản lý Proxy Keys**, tạo key cho ứng dụng | Có key dạng `sk-proxy-...` |
| 4 | Vào **Test AI**, chạy Chat/Vision | Kiểm tra routing, key và model |
| 5 | Vào **Endpoint**, sao chép Base URL LAN hoặc Public Base URL | Có URL để cấu hình ứng dụng |
| 6 | Cấu hình ứng dụng với Base URL, Proxy Key và model `auto-ai` | Ứng dụng gọi được API |

Nếu bước 4 báo lỗi, xử lý theo mục [Xử lý sự cố](#16-xử-lý-sự-cố) trước khi cấu hình ứng dụng bên ngoài.

### 5. Các tab trên dashboard

| Tab | Công dụng |
|---|---|
| **Tổng quan** | Trạng thái hệ thống, nguồn đang dùng, Base URL, lối tắt |
| **Nguồn & Key** | Thêm/xóa nguồn, kho key, Proxy Key, thứ tự ưu tiên, đồng bộ model |
| **Endpoint** | Base URL nội bộ, endpoint Chat/Responses/Models, Public Base URL |
| **Usage** | Token, chi phí ước tính, tỉ trọng provider, request gần đây |
| **Quota** | Hạn mức còn lại của nguồn và Proxy Key |
| **Token Saver** | Bật/tắt RTK, Headroom, Caveman, Ponytail |
| **Test AI** | Chat, Vision, Tool Calling và JSON Schema test |
| **Voice** | Kiểm tra STT/TTS bằng Proxy Key |
| **CLI Tools** | Snippet cURL, Python SDK, biến môi trường và CLI |
| **Hệ thống** | Cài đặt, backup/restore, Telegram, log, debug bundle |

Dashboard có bộ chọn **Tiếng Việt / English** trên thanh điều hướng. Lựa chọn được lưu trong trình duyệt. Giao diện hỗ trợ light/dark, thao tác chạm và bàn phím.

### 6. Thêm nguồn AI và API key

1. Mở **Nguồn & Key**.
2. Chọn một provider dựng sẵn hoặc **Custom Endpoint**.
3. Dán API key thật, hoặc chọn key đã lưu trong **Kho key & nhập nhiều key**.
4. Với Custom Endpoint, nhập tên nguồn và Base URL tương thích OpenAI, thường kết thúc bằng `/v1`.
5. Nhấn **Thêm & tự dò model**.
6. Add-on gọi `/models`, chỉ giữ model chat/audio dùng được và lưu key vào kho.
7. Dùng **Đồng bộ** để dò lại, **Tạm tắt/Bật lại** để ngưng cả nguồn, hoặc **Xóa nguồn** để bỏ các model của nguồn đó.

Lưu ý:

- Key gốc vẫn được giữ trong kho khi xóa nguồn.
- Nguồn nằm càng cao càng được ưu tiên.
- `auto-ai` ưu tiên nguồn còn hoạt động và thử nguồn dự phòng khi gặp lỗi xác thực, quota, rate limit hoặc lỗi mạng.
- Hạn mức của nguồn là hạn mức bạn đặt trong add-on, không phải số dư thật trên trang nhà cung cấp.
- Với Ollama hoặc LM Studio, dùng **Custom Endpoint** trỏ tới `/v1` của dịch vụ đó và đảm bảo Home Assistant truy cập được địa chỉ mạng tương ứng.
- Không dán key gốc vào ứng dụng bên ngoài. Hãy tạo Proxy Key.

Ví dụ Custom Endpoint:

```text
Tên: DeepSeek
Base URL: https://api.deepseek.com/v1
API key: sk-...
```

### 7. Tạo và quản lý Proxy Key

Proxy Key là chìa khóa cho ứng dụng bên ngoài. Key này khác hoàn toàn API key của nhà cung cấp.

1. Mở **Nguồn & Key → Quản lý Proxy Keys**.
2. Nhập tên ứng dụng, ví dụ `Open WebUI`, `LobeChat`, `Dify` hoặc `Điện thoại`.
3. Đặt hạn mức chi phí, rate limit, tag và ngày hết hạn nếu cần.
4. Nhấn tạo mới.
5. Sao chép key dạng `sk-proxy-...` và dán vào ứng dụng.

Bạn có thể:

- tắt tạm một key mà không xóa;
- hiện lại key khi cần;
- tạo lại key nếu nghi ngờ bị lộ;
- xóa key không còn dùng.

Nếu ứng dụng báo `401`, kiểm tra header:

```http
Authorization: Bearer sk-proxy-YOUR_KEY
```

Nếu báo `402`, `403` hoặc `429`, kiểm tra key có đang bật, còn hạn, còn hạn mức và không vượt rate limit.

> Không gửi Proxy Key qua chat công khai, ảnh chụp màn hình hoặc log. Nếu key bị lộ, tạo lại ngay.

### 8. Endpoint, LAN và truy cập từ Internet

#### Ba loại URL cần phân biệt

| Loại | Ví dụ | Dùng cho |
|---|---|---|
| Ingress | `https://ha.example.com/api/hassio_ingress/...` | Dashboard và `/api/*` |
| LAN API | `http://HOME_ASSISTANT_IP:1236/v1` | Ứng dụng trong cùng mạng LAN |
| Public API | `https://ai.example.com/v1` | Ứng dụng ngoài Internet |

Không dùng URL Ingress làm Base URL API. URL này phụ thuộc phiên Home Assistant, yêu cầu đăng nhập/CSRF và có thể thay đổi.

#### Dùng trong LAN

1. Bật port `1236` như mục [Cài đặt](#3-cài-đặt-và-nâng-cấp).
2. Mở **Endpoint**, sao chép Base URL dạng `http://HOME_ASSISTANT_IP:1236/v1`.
3. Dùng Proxy Key khi gọi `/v1/*`.

Nếu chỉ dùng dashboard, không cần bật port.

#### Dùng reverse proxy HTTPS

Kiến trúc khuyến nghị:

```text
Internet → HTTPS reverse proxy → http://ai-proxy-router:1236
```

Yêu cầu:

- Chỉ forward `/v1/*` (và `/health` nếu cần health check).
- Giữ dashboard `/` và `/api/*` trong mạng nội bộ hoặc chỉ cho phép qua Home Assistant Ingress.
- Bật TLS, giới hạn IP/rate limit nếu có.
- Không forward header nội bộ không cần thiết; giữ `Authorization`.
- Nếu reverse proxy chạy trong cùng Docker network với add-on, dùng hostname nội bộ của add-on, ví dụ `http://011a0c26-ai-proxy-router:1236`.
- Nếu reverse proxy chạy trên host/LAN, publish port `1236` rồi trỏ tới IP LAN của Home Assistant.

Sau khi có URL public:

1. Mở **Endpoint → Kết nối bên ngoài**.
2. Nhập **Public Base URL**, thường là `https://ai.example.com/v1`.
3. Nhấn **Lưu URL**.
4. Kiểm tra trạng thái **Đã cấu hình**.
5. Chạy các lệnh kiểm tra bên dưới.

Trạng thái **Đã cấu hình** chỉ có nghĩa là URL đã được lưu. Nó không đảm bảo tên miền, DNS, tunnel hoặc TLS đang hoạt động. Phải kiểm tra bằng request thật.

#### Cloudflare Tunnel

Cloudflare Tunnel phù hợp khi Home Assistant không có IP public hoặc không muốn mở port. Có hai cách: dùng add-on **Cloudflared** cùng Home Assistant, hoặc dùng một tunnel/cloudflared trên máy khác.

**Điều kiện về tên miền và chứng chỉ**

Cloudflare Universal SSL thường cấp chứng chỉ cho domain gốc và một cấp wildcard:

```text
example.com
*.example.com
```

Vì vậy:

- `ai.example.com` dùng được.
- `ai.ha.example.com` có thể lỗi TLS vì nằm dưới hai cấp.
- Lỗi thường gặp: `sslv3 alert handshake failure` hoặc `SSL alert number 40`.

Nếu cần tên miền nhiều cấp, phải dùng Advanced Certificate Manager hoặc chứng chỉ phù hợp. Cách đơn giản nhất là dùng tên miền con một cấp như `ai.example.com`.

**Các bước với add-on Cloudflared**

1. Cài và cấu hình add-on **Cloudflared** cho Home Assistant.
2. Chọn hostname public, ví dụ `ai.example.com`.
3. Trỏ service tới add-on AI Proxy Router, không trỏ tới dashboard Ingress:

   ```yaml
   additional_hosts:
     - hostname: ai.example.com
       service: http://<ai-proxy-container>:1236
   ```

   `<ai-proxy-container>` là hostname nội bộ của container AI Proxy Router. Trong một số bản cài đặt, tên này có dạng `011a0c26-ai-proxy-router`. Nếu Cloudflared không truy cập được hostname nội bộ, publish port `1236` và dùng địa chỉ LAN của Home Assistant.

4. Lưu cấu hình và khởi động lại Cloudflared.
5. Chờ 1–2 phút. Cloudflared có thể tự tạo bản ghi DNS CNAME cho hostname mới.
6. Kiểm tra:

   ```bash
   curl -i "https://ai.example.com/health"
   curl -i "https://ai.example.com/v1/models" \
     -H "Authorization: Bearer sk-proxy-YOUR_KEY"
   ```

7. Trong dashboard AI Proxy, mở **Endpoint → Kết nối bên ngoài**, nhập `https://ai.example.com/v1` và lưu.

Lưu ý khi dùng Cloudflared:

- Không tạo service trỏ tới `/api/hassio_ingress/...`.
- Không public dashboard hoặc `/api/*` qua tunnel nếu không thật sự cần.
- App đã chặn `/` và `/api/*` từ bên ngoài, nhưng nên đặt thêm Cloudflare WAF/rate limit cho `/v1/*` nếu có thể.
- Nếu bật Cloudflare Access cho hostname API, ứng dụng client phải gửi service token. Nhiều ứng dụng không hỗ trợ header này; chỉ bật Access khi client của bạn đáp ứng được.
- Restart Cloudflared có thể làm tunnel mất kết nối tạm thời. Lỗi `530` hoặc `error code: 1033` trong vài phút thường do tunnel chưa kết nối lại.
- Khi đổi hostname, xóa hostname cũ khỏi cấu hình Cloudflared và xóa DNS record cũ trong Cloudflare nếu không còn dùng.

**Nếu Home Assistant đã có tên miền public**

Vẫn nên tạo một hostname riêng cho API, ví dụ `ai.example.com`, thay vì dùng chung hostname Home Assistant. Cách này tách dashboard Home Assistant khỏi API AI và dễ giới hạn quyền hơn.

Nếu buộc phải dùng chung hostname, phải cấu hình reverse proxy theo path và đảm bảo:

- path public được strip hoặc giữ đúng như Base URL;
- chỉ forward `/v1/*`;
- dashboard và `/api/*` vẫn được bảo vệ;
- không dùng Ingress URL làm Base URL.

Cách này phức tạp hơn và dễ lỗi với client không hỗ trợ Base URL có path. Hostname riêng là lựa chọn an toàn hơn.

#### Mở port trực tiếp

Chỉ dùng khi không có cách nào khác:

```text
Internet → router/firewall → HOME_ASSISTANT_IP:1236/v1
```

Cách này không có TLS và dễ bị quét. Nếu dùng, phải có firewall, rate limit, giám sát và cân nhắc IP allowlist. Không khuyến nghị cho lâu dài.

#### Kiểm tra nhanh endpoint

Thay `https://ai.example.com` bằng URL của bạn:

```bash
curl -i "https://ai.example.com/health"

curl -i "https://ai.example.com/v1/models" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY"

curl -i "https://ai.example.com/v1/chat/completions" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"auto-ai","messages":[{"role":"user","content":"Xin chào"}]}'
```

Kết quả mong đợi:

- `/health`: `200`.
- `/v1/models` có key: `200` và danh sách model.
- `/v1/chat/completions` có key: `200`.
- Không có key: `401`.
- `/`, `/api/stats`, `/api/*` từ Internet: `403`.
- `/docs`, `/redoc`: `404`.
- `/openapi.json` từ Internet: `403`; qua Ingress: `200`.

### 9. Kết nối ứng dụng và Home Assistant

Trong ứng dụng hỗ trợ OpenAI-compatible, nhập:

| Trường | Giá trị |
|---|---|
| Base URL | `https://ai.example.com/v1` hoặc `http://HOME_ASSISTANT_IP:1236/v1` |
| API Key | Proxy Key dạng `sk-proxy-...` |
| Model | `auto-ai` hoặc tên model đã lưu |

Không nhập API key gốc của Groq/Gemini/OpenAI vào ứng dụng. Chỉ nhập Proxy Key.

#### Biến môi trường cho CLI

```bash
export OPENAI_BASE_URL="https://ai.example.com/v1"
export OPENAI_API_KEY="sk-proxy-YOUR_KEY"
```

Một số công cụ dùng `OPENAI_API_BASE` thay cho `OPENAI_BASE_URL`. Kiểm tra tài liệu của công cụ hoặc dùng snippet trong **CLI Tools**.

#### Open WebUI, LobeChat, Dify, Chatbox

1. Chọn provider **OpenAI** hoặc **OpenAI-compatible**.
2. Base URL: `https://ai.example.com/v1`.
3. API Key: Proxy Key.
4. Model: `auto-ai` hoặc model đã lưu.
5. Tắt chế độ yêu cầu API key gốc nếu ứng dụng có tùy chọn đó.

#### Python SDK

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-proxy-YOUR_KEY",
    base_url="https://ai.example.com/v1",
)

response = client.chat.completions.create(
    model="auto-ai",
    messages=[{"role": "user", "content": "Xin chào"}],
)
print(response.choices[0].message.content)
```

#### Home Assistant

Tích hợp OpenAI mặc định của Home Assistant có thể không cho đổi Base URL. Hãy dùng một trong các cách sau:

- dùng tích hợp/custom component hỗ trợ OpenAI-compatible Base URL;
- gọi bằng `rest_command` hoặc `shell_command`;
- dùng Node-RED, AppDaemon hoặc một script bên ngoài.

Ví dụ `rest_command`:

```yaml
rest_command:
  ai_proxy_chat:
    url: "https://ai.example.com/v1/chat/completions"
    method: POST
    headers:
      Authorization: !secret ai_proxy_authorization
      Content-Type: "application/json"
    payload: >-
      {"model":"auto-ai","messages":[{"role":"user","content":{{ prompt | tojson }}}]}
```

Trong `secrets.yaml`:

```yaml
ai_proxy_authorization: "Bearer sk-proxy-YOUR_KEY"
```

Gọi từ automation/script:

```yaml
action: rest_command.ai_proxy_chat
data:
  prompt: "Tóm tắt trạng thái nhà."
response_variable: ai_result
```

Sau đó đọc JSON:

```jinja
{{ (ai_result.content | from_json).choices[0].message.content }}
```

Đây là ví dụ tối giản. Nếu cần hội thoại nhiều lượt, streaming hoặc tool calling, nên dùng một client chuyên dụng hoặc custom integration.

### 10. Gọi API OpenAI-compatible

Base URL luôn kết thúc bằng `/v1`. Các endpoint:

| Phương thức | Endpoint | Mô tả |
|---|---|---|
| `GET` | `/v1/models` | Danh sách model |
| `POST` | `/v1/chat/completions` | Chat Completions, hỗ trợ stream |
| `POST` | `/v1/responses` | Responses API |
| `POST` | `/v1/audio/transcriptions` | Speech-to-Text |
| `POST` | `/v1/audio/speech` | Text-to-Speech |
| `GET` | `/health` | Health check công khai (bản rút gọn); chi tiết đầy đủ qua Ingress |

Mọi endpoint `/v1/*` đều yêu cầu:

```http
Authorization: Bearer sk-proxy-YOUR_KEY
```

#### Chat cơ bản

```bash
curl "https://ai.example.com/v1/chat/completions" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "auto-ai",
    "messages": [
      {"role": "user", "content": "Tóm tắt trạng thái ngôi nhà."}
    ]
  }'
```

#### Vision

```bash
curl "https://ai.example.com/v1/chat/completions" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "auto-ai",
    "messages": [{
      "role": "user",
      "content": [
        {"type": "text", "text": "Mô tả ảnh này."},
        {"type": "image_url", "image_url": {"url": "https://example.com/camera.jpg"}}
      ]
    }]
  }'
```

Ảnh có thể là URL `http(s)` hoặc data URI `data:image/...`.

#### Streaming

```bash
curl -N "https://ai.example.com/v1/chat/completions" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "auto-ai",
    "stream": true,
    "messages": [{"role": "user", "content": "Xin chào"}]
  }'
```

- Không có `stream` hoặc `stream: false`: trả JSON đầy đủ.
- Có `stream: true`: trả SSE.
- Router chỉ failover trước khi event SSE đầu tiên được gửi. Sau khi stream bắt đầu, lỗi được trả trong stream hiện tại để tránh ghép nội dung từ hai provider.
- Một số nguồn không stream token-level sẽ được tổng hợp thành SSE từ nội dung hoàn chỉnh.

#### Responses API

```bash
curl "https://ai.example.com/v1/responses" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"auto-ai","input":"Tóm tắt trạng thái ngôi nhà."}'
```

#### Function tools

```bash
curl "https://ai.example.com/v1/chat/completions" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model":"auto-ai",
    "messages":[{"role":"user","content":"Kiểm tra trạng thái phòng khách"}],
    "tools":[{
      "type":"function",
      "function":{
        "name":"get_home_status",
        "description":"Đọc trạng thái phòng",
        "parameters":{
          "type":"object",
          "properties":{"room":{"type":"string"}},
          "required":["room"],
          "additionalProperties":false
        }
      }
    }],
    "tool_choice":"required",
    "parallel_tool_calls":false
  }'
```

Router chỉ trả về tên function và arguments do model tạo ra. Router không tự thực thi function, không tự chạy shell, web, file hay computer tool. Ứng dụng của bạn phải kiểm tra và thực thi function, sau đó gửi kết quả lại bằng `function_call_output` với đúng `call_id`.

Với Responses API, function tool dùng định dạng phẳng:

```json
{"type":"function","name":"get_home_status","parameters":{"type":"object"}}
```

#### Structured Output

```bash
curl "https://ai.example.com/v1/responses" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model":"auto-ai",
    "input":"Trả về trạng thái ngắn gọn",
    "text":{
      "format":{
        "type":"json_schema",
        "name":"home_status",
        "strict":true,
        "schema":{
          "type":"object",
          "properties":{"status":{"type":"string"}},
          "required":["status"],
          "additionalProperties":false
        }
      }
    }
  }'
```

Nếu output không đúng schema, router có thể thử nguồn khác. Không phải provider nào cũng hỗ trợ JSON Schema; router sẽ bỏ qua nguồn không phù hợp.

#### Lỗi thường gặp

| Mã | Ý nghĩa | Việc cần kiểm tra |
|---|---|---|
| `400` | Request sai | JSON, model, định dạng ảnh/audio, schema |
| `401` | Thiếu hoặc sai Proxy Key | Header `Authorization`, key còn tồn tại |
| `402` | Hết hạn mức | Hạn mức Proxy Key hoặc nguồn |
| `403` | Bị chặn | Key bị tắt, hết hạn, sai quyền hoặc gọi `/api/*` từ ngoài Ingress |
| `404` | Sai đường dẫn/model | Base URL phải có `/v1`; model phải tồn tại |
| `429` | Rate limit | Rate limit Proxy Key hoặc provider |
| `503` | Không có nguồn phù hợp | Kiểm tra nguồn, model, key, quota, log |

Router trả lỗi dạng JSON:

```json
{"detail":"Mô tả lỗi"}
```

### 11. Voice: Speech-to-Text và Text-to-Speech

Voice dùng cùng Proxy Key và cùng Base URL `/v1`.

1. Thêm nguồn có model audio (STT/TTS) và đồng bộ model.
2. Tạo Proxy Key cho ứng dụng voice.
3. Mở tab **Voice** để kiểm tra nhanh.

#### Speech-to-Text

```bash
curl "https://ai.example.com/v1/audio/transcriptions" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY" \
  -F "file=@audio.mp3" \
  -F "model=WHISPER_MODEL"
```

Trường `file` là bắt buộc. Các trường khác như `language`, `prompt`, `response_format` được chuyển tiếp nếu provider hỗ trợ.

#### Text-to-Speech

```bash
curl "https://ai.example.com/v1/audio/speech" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "TTS_MODEL",
    "input": "Xin chào từ Home Assistant",
    "voice": "alloy"
  }' --output speech.mp3
```

Tên model và voice phụ thuộc provider. Chỉ model đã dò thấy và đang bật mới được dùng. Nếu không có nguồn audio phù hợp, API trả `503`.

### 12. Token Saver

Bật master **Token Saver** trong tab **Token Saver**, sau đó chọn module:

| Module | Tác dụng |
|---|---|
| **RTK** | Nén output dài của tool/lệnh như `git`, `grep`, `ls`, `tree`, log/build output |
| **Headroom** | Gọi dịch vụ `/v1/compress` để nén context trước khi routing |
| **Caveman** | Yêu cầu model trả lời ngắn theo mức Lite/Full/Ultra, vẫn giữ code, lệnh, đường dẫn, lỗi và cảnh báo |
| **Ponytail** | Hướng model theo YAGNI, ưu tiên xóa/reuse/stdlib/native trước khi thêm abstraction hoặc dependency |

RTK bật sẵn trong cấu hình module nhưng chỉ chạy khi master Token Saver được bật. Headroom, Caveman và Ponytail là tùy chọn độc lập.

Bỏ qua Token Saver cho một request:

```http
X-AI-Proxy-Token-Saver: off
```

Response có thể trả:

```text
X-AI-Proxy-Token-Saver
X-AI-Proxy-Input-Chars-Saved
X-AI-Proxy-Estimated-Tokens-Saved
```

Headroom phải chạy như dịch vụ riêng, có endpoint `/v1/compress`. Nhập URL vào dashboard và kiểm tra trạng thái trước khi bật. Nếu Headroom lỗi, timeout hoặc trả dữ liệu không hợp lệ, router dùng context gốc.

### 13. Usage, Quota, nhật ký và Telegram

- **Usage** hiển thị token, chi phí ước tính, tỉ trọng provider và request gần đây.
- **Quota** hiển thị hạn mức còn lại của từng nguồn và từng Proxy Key.
- **Nhật ký** giúp xem lỗi gần đây và tình trạng nguồn.
- **Telegram** gửi cảnh báo khi nguồn/key gặp sự cố. Cấu hình trong **Hệ thống**, sau đó dùng nút test.
- **Kiểm tra nguồn** chạy lại kiểm tra provider/key đang hoạt động.
- **Debug bundle** tạo gói chẩn đoán đã che bí mật để gửi khi cần hỗ trợ.

Chi phí trong dashboard là ước tính dựa trên token và bảng giá đã cấu hình. Hóa đơn thật của nhà cung cấp là nguồn chính xác cuối cùng.

### 14. Backup, khôi phục và nâng cấp

#### Backup

1. Mở **Hệ thống**.
2. Chọn **Tải backup**.
3. Lưu file JSON ở nơi an toàn.

File backup đầy đủ chứa API key nguồn, Proxy Key và cấu hình nhạy cảm. Hãy mã hóa hoặc lưu trong thư mục riêng, không đăng công khai.

#### Khôi phục

1. Mở **Hệ thống**.
2. Chọn **Khôi phục backup**.
3. Chọn file JSON hợp lệ.
4. Add-on tự tạo safety backup trước khi ghi đè.
5. Kiểm tra lại nguồn, Proxy Key, model và endpoint sau khi khôi phục.

`data.json` và file backup được đặt quyền `600`. File JSON lỗi được giữ thành bản `.corrupt-*` thay vì ghi đè.

#### Nâng cấp

- Tải backup trước khi nâng cấp.
- Cập nhật add-on từ Add-on Store.
- Kiểm tra số phiên bản, `/health`, `/v1/models` và chat.
- Nếu lỗi, xem **Log**; khôi phục backup nếu cần.

Dùng **Masked preview** hoặc **Debug bundle** khi cần gửi thông tin chẩn đoán mà không lộ API key.

### 15. Bảo mật

Checklist tối thiểu:

- Dashboard và `/api/*` chỉ truy cập qua Home Assistant Ingress.
- Mọi thao tác thay đổi dữ liệu qua `/api/*` phải có header `X-CSRF-Token` do dashboard tự gắn.
- Port `1236` mặc định tắt. Nếu bật, chỉ dùng cho `/v1/*` có Proxy Key.
- Không public dashboard hoặc API quản trị ra Internet.
- Dùng HTTPS cho mọi kết nối từ xa.
- Chỉ forward `/v1/*` ở reverse proxy; giữ `/`, `/api/*`, `/docs`, `/redoc` và `/openapi.json` ngoài Internet.
- Tạo Proxy Key riêng cho từng ứng dụng; đặt hạn mức, rate limit và ngày hết hạn.
- Không chia sẻ API key gốc hoặc Proxy Key.
- Tạo lại Proxy Key ngay nếu nghi ngờ bị lộ.
- Giữ backup ở nơi an toàn, mã hóa nếu có thể.
- Kiểm tra log và cảnh báo Telegram định kỳ.
- Xóa DNS record và hostname cũ khi đổi tên miền public.

Từ `1.22.0`:

- `/docs` và `/redoc` bị tắt.
- `/openapi.json` chỉ trả qua Home Assistant Ingress.
- Response có thêm `X-Content-Type-Options: nosniff` và `Referrer-Policy: no-referrer`.
- `/health` công khai chỉ trả trạng thái, tên, phiên bản và uptime; dùng `/health` hoặc `/api/health` qua Ingress để xem chi tiết đầy đủ.

Nếu cần xem OpenAPI schema để phát triển tích hợp, mở qua Ingress hoặc dùng công cụ đã đăng nhập Home Assistant. Không mở `/openapi.json` ra Internet.

### 16. Xử lý sự cố

| Hiện tượng | Nguyên nhân thường gặp | Cách xử lý |
|---|---|---|
| Không mở được dashboard | Truy cập thẳng `IP:1236` | Mở từ **Web UI** hoặc sidebar Home Assistant |
| Dashboard mở nhưng trắng | Cache/JS lỗi | Tải lại không cache, xem Console/Network |
| Client LAN không kết nối | Port `1236` chưa publish | Bật port trong **Network** của add-on |
| `401` | Thiếu/sai Proxy Key | Kiểm tra `Authorization: Bearer sk-proxy-...` |
| `403` | Key tắt/hết hạn/sai quyền | Kiểm tra Proxy Key; không gọi `/api/*` từ ngoài Ingress |
| `402` | Hết hạn mức | Tăng hạn mức key/nguồn hoặc tạo key mới |
| `429` | Rate limit | Giảm tần suất hoặc tăng rate limit |
| `503` | Không có nguồn phù hợp | Kiểm tra nguồn, model, key, quota, log |
| `404` | Sai Base URL | Base URL phải kết thúc bằng `/v1` |
| `530` / `1033` | Cloudflare Tunnel chưa kết nối | Chờ 1–2 phút, xem log Cloudflared, restart tunnel |
| TLS `alert 40` | Hostname quá nhiều cấp | Dùng `ai.example.com`, không dùng `ai.ha.example.com` |
| Public `/health` 200 nhưng `/v1` lỗi | Key/nguồn/model | Kiểm tra Proxy Key và nguồn trên dashboard |
| Public Base URL báo Đã cấu hình nhưng không gọi được | URL đã lưu nhưng DNS/TLS/tunnel lỗi | Kiểm tra DNS, tunnel, firewall, chứng chỉ |
| Không có model Vision | Chưa có nguồn Vision | Thêm nguồn/model hỗ trợ ảnh |
| Tool không chạy | Router không thực thi tool | Ứng dụng phải tự thực thi function |
| JSON Schema lỗi | Provider không hỗ trợ | Dùng nguồn/model hỗ trợ structured output |
| Headroom offline | Dịch vụ chưa chạy | Kiểm tra URL/port và nút test |
| Voice `503` | Chưa có model STT/TTS | Thêm nguồn audio và đồng bộ model |
| Telegram không gửi | Token/chat ID sai | Kiểm tra cấu hình và dùng nút test |
| Đổi ngôn ngữ không lưu | `localStorage` bị chặn | Cho phép lưu trữ hoặc tải lại trang |

Kiểm tra từ ngoài:

```bash
curl -i "https://ai.example.com/health"

curl -i "https://ai.example.com/v1/models" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY"
```

Kiểm tra từ trong LAN:

```bash
curl -i "http://HOME_ASSISTANT_IP:1236/health"
```

Kiểm tra DNS:

```bash
dig +short ai.example.com
```

Nếu `curl` báo lỗi chứng chỉ, kiểm tra:

- hostname có đúng một cấp dưới domain gốc không;
- Cloudflare SSL/TLS mode có phải **Full** hoặc **Full (strict)** không;
- origin có chứng chỉ hợp lệ nếu dùng Full (strict);
- DNS đã trỏ đúng tunnel chưa.

Nếu Cloudflared báo lỗi, xem **Log** của add-on Cloudflared. Lỗi cấu hình `additional_hosts` thường do sai hostname hoặc service không truy cập được.

### 17. Câu hỏi thường gặp

**Add-on này có miễn phí không?**
Add-on miễn phí. Chi phí phát sinh từ nhà cung cấp AI theo API key của bạn.

**Dữ liệu của tôi có bị gửi lên cloud không?**
Cấu hình, log và thống kê được lưu cục bộ trong add-on. Nội dung request được gửi tới nhà cung cấp AI mà bạn cấu hình. Không có dịch vụ trung gian của add-on.

**Có dùng được Ollama hoặc LM Studio không?**
Có. Dùng **Custom Endpoint** trỏ tới địa chỉ `/v1` của dịch vụ và đảm bảo Home Assistant truy cập được địa chỉ đó.

**Có thể public API ra Internet không?**
Có. Dùng HTTPS reverse proxy hoặc Cloudflare Tunnel, chỉ public `/v1/*`, luôn dùng Proxy Key và đặt rate limit/WAF nếu có thể.

**Có cần mở port 1236 không?**
Không, nếu chỉ dùng dashboard hoặc Cloudflared cùng Home Assistant. Chỉ bật khi client LAN gọi trực tiếp.

**Vì sao dashboard không mở được bằng IP:1236?**
Theo thiết kế, dashboard và `/api/*` chỉ nhận request từ Home Assistant Ingress.

**Vì sao `/docs` trả 404?**
Từ `1.22.0`, Swagger/ReDoc bị tắt để giảm bề mặt tấn công. `/openapi.json` chỉ mở qua Ingress.

**Vì sao Public Base URL báo Đã cấu hình nhưng vẫn lỗi?**
Trạng thái đó chỉ xác nhận URL đã lưu. Hãy kiểm tra DNS, TLS, tunnel, firewall và gọi thử `/health`.

**Vì sao dùng `ai.ha.example.com` bị lỗi TLS?**
Cloudflare Universal SSL thường chỉ phủ `*.example.com`, không phủ tên miền hai cấp. Dùng `ai.example.com` hoặc chứng chỉ phù hợp.

**Router có tự thực thi function tool không?**
Không. Router chỉ trả về function name và arguments. Ứng dụng client phải thực thi và gửi kết quả lại.

**Làm sao xóa hostname/DNS cũ?**
Xóa hostname khỏi cấu hình Cloudflared và xóa bản ghi DNS tương ứng trong Cloudflare Dashboard nếu không còn dùng.

### 18. Thông tin kỹ thuật

- Add-on slug: `ai_proxy_router`.
- Ingress port: `1236`.
- Kiến trúc: `amd64`, `aarch64`.
- API: FastAPI, tương thích OpenAI.
- Dữ liệu: `/data/data.json`; quyền file `600`.
- Dashboard: HTML/CSS/JS đóng gói trong add-on, không cần CDN.
- Health check: `/health`.
- OpenAPI schema: `/openapi.json`, chỉ qua Ingress từ `1.22.0`.
- Kho add-on công khai: `https://github.com/trankhanhduy2929-beep/my_hass_addon_public`.
- Mã nguồn phát hành được quản lý trong kho private của chủ dự án.

Cấu trúc chính:

```text
ai_proxy_router/
  config.yaml
  Dockerfile
  main.py
  token_saver.py
  ui_i18n.js
  dashboard.css
  vendor/
  README.md
  DOCS.md
```

Quy trình phát hành:

1. Cập nhật `config.yaml` và `APP_VERSION` trong `main.py`.
2. Chạy compile, smoke test và kiểm tra UI.
3. Đóng gói ZIP, tạo SHA-256.
4. Cập nhật ghi chú phát hành.
5. Build/push image và cập nhật metadata kho add-on.

---

## English

### Contents

1. [Overview](#1-overview)
2. [Requirements](#2-requirements)
3. [Install and upgrade](#3-install-and-upgrade)
4. [Five-minute quick start](#4-five-minute-quick-start)
5. [Dashboard tabs](#5-dashboard-tabs)
6. [Add AI sources](#6-add-ai-sources)
7. [Proxy Keys](#7-proxy-keys)
8. [Endpoints, LAN, and Internet access](#8-endpoints-lan-and-internet-access)
9. [Connect apps and Home Assistant](#9-connect-apps-and-home-assistant)
10. [OpenAI-compatible API](#10-openai-compatible-api)
11. [Voice](#11-voice)
12. [Token Saver](#12-token-saver)
13. [Usage, quota, logs, and Telegram](#13-usage-quota-logs-and-telegram)
14. [Backup, restore, and upgrade](#14-backup-restore-and-upgrade)
15. [Security](#15-security)
16. [Troubleshooting](#16-troubleshooting)
17. [FAQ](#17-faq)
18. [Technical notes](#18-technical-notes)

### 1. Overview

AI Proxy Router combines multiple AI providers behind one OpenAI-compatible API. It rotates API keys, fails over between sources, and routes Text/Vision requests automatically.

```text
App / Home Assistant / CLI
            |
            |  /v1/*  +  Proxy Key
            v
    AI Proxy Router (add-on)
            |
            |  key rotation, failover, auto-ai
            v
  Groq / Gemini / OpenAI / OpenRouter / DeepSeek / Custom Endpoint
```

Key points:

- The dashboard is available only through Home Assistant Ingress.
- External apps use `/v1/*` with a Proxy Key.
- Never use the Home Assistant Ingress URL as an API Base URL.
- Provider API keys stay inside the add-on. External apps receive Proxy Keys.

Main features:

- `/v1/models`, `/v1/chat/completions`, `/v1/responses`, `/v1/audio/transcriptions`, `/v1/audio/speech`.
- SSE streaming, function tools, `tool_choice`, `parallel_tool_calls`, and `function_call_output`.
- JSON Object/JSON Schema structured output with validation and failover.
- `auto-ai` model selection based on healthy Text/Vision sources.
- Automatic model discovery and six-hour model sync.
- Token Saver: RTK, Headroom, Caveman, and Ponytail.
- Per-app Proxy Keys with budgets, rate limits, expiration, and enable/disable controls.
- Token/cost statistics, provider checks, Telegram alerts, backup/restore, and masked diagnostics.
- Vietnamese/English dashboard for desktop and mobile.

### 2. Requirements

- Home Assistant OS or Home Assistant Supervised with the Add-on Store.
- `amd64` or `aarch64`. `armv7` is not declared.
- Internet access for AI providers and model discovery.
- At least one provider API key.
- For Internet access: a domain and HTTPS. Cloudflare Tunnel is the recommended approach in this guide.

Port `1236` is not required for the dashboard or for Cloudflared running next to Home Assistant. Enable it only when a LAN client must call the add-on directly.

### 3. Install and upgrade

#### Install from the add-on repository

1. Open **Settings → Add-ons → Add-on Store**.
2. Open the top-right menu and select **Repositories**.
3. Add:

   ```text
   https://github.com/trankhanhduy2929-beep/my_hass_addon_public
   ```

4. Find **AI Proxy Router** and select **Install**.
5. Enable **Start on boot** and **Watchdog** if desired.
6. Enable **Show in sidebar** for quick access.
7. Select **Start**, then open **Web UI**.

#### Install from a local folder

1. Extract `ai_proxy_router` into the local add-ons directory, usually `/addons/ai_proxy_router`.
2. Open **Settings → Add-ons → Add-on Store**.
3. Use the top-right menu and select **Check for updates**, or reload the page.
4. Select **AI Proxy Router → Install → Start**.

#### Enable the LAN API port

1. Open the **AI Proxy Router** add-on.
2. Open **Configuration** or **Network**.
3. Map host port `1236` to container port `1236/tcp`.
4. Save and restart.

The dashboard and `/api/*` remain protected by Home Assistant Ingress.

#### Upgrade

1. Download a backup from **System**.
2. In the Add-on Store, open **AI Proxy Router** and select **Update**.
3. Wait for the add-on to restart, then check the version in the dashboard.
4. Test `/health`, `/v1/models`, and a short chat request.
5. If something fails, check the add-on log before restoring the backup.

Version `1.22.0` changes:

- `/docs` and `/redoc` are disabled.
- `/openapi.json` is available only through Home Assistant Ingress.
- Responses include `X-Content-Type-Options: nosniff` and `Referrer-Policy: no-referrer`.

### 4. Five-minute quick start

| Step | Action | Result |
|---|---|---|
| 1 | Open **AI Proxy → Web UI** | Dashboard opens through Ingress |
| 2 | Open **Sources & Keys**, choose a provider, paste a key, click **Add and discover models** | At least one source and model list |
| 3 | Open **Sources & Keys → Manage Proxy Keys**, create a key | A key like `sk-proxy-...` |
| 4 | Open **Test AI** and run Chat/Vision | Validates routing, key, and model |
| 5 | Open **Endpoint** and copy the LAN Base URL or Public Base URL | URL for your app |
| 6 | Configure the app with Base URL, Proxy Key, and `auto-ai` | App calls the API |

If step 4 fails, use [Troubleshooting](#16-troubleshooting) before exposing the API.

### 5. Dashboard tabs

| Tab | Purpose |
|---|---|
| **Overview** | System status, active source, Base URL, shortcuts |
| **Sources & Keys** | Sources, key vault, Proxy Keys, priority, model sync |
| **Endpoint** | LAN Base URL, Chat/Responses/Models endpoints, Public Base URL |
| **Usage** | Tokens, estimated cost, provider mix, recent requests |
| **Quota** | Remaining source and Proxy Key budgets |
| **Token Saver** | RTK, Headroom, Caveman, Ponytail controls |
| **Test AI** | Chat, Vision, Tool Calling, and JSON Schema tests |
| **Voice** | STT/TTS checks with a Proxy Key |
| **CLI Tools** | cURL, Python SDK, environment, and CLI snippets |
| **System** | Settings, backup/restore, Telegram, logs, diagnostics |

The dashboard supports Vietnamese/English, light/dark mode, touch, and keyboard navigation.

### 6. Add AI sources

1. Open **Sources & Keys**.
2. Choose a built-in provider or **Custom Endpoint**.
3. Paste a provider API key or select a saved key from the key vault.
4. For a custom source, enter a name and an OpenAI-compatible Base URL, usually ending in `/v1`.
5. Click **Add and discover models**.
6. The add-on calls `/models`, keeps usable chat/audio models, and stores the key in the vault.
7. Use **Sync**, **Disable/Enable**, or **Delete source** on the source card.

Notes:

- Deleting a source keeps its key in the vault.
- Sources higher in the list have higher priority.
- `auto-ai` prefers healthy sources and tries fallbacks on auth, quota, rate-limit, or network errors.
- Source budgets are add-on limits, not the provider's real account balance.
- For Ollama or LM Studio, use **Custom Endpoint** with that service's `/v1` URL and make sure Home Assistant can reach it.
- Never give a provider API key to an external app. Create a Proxy Key.

### 7. Proxy Keys

1. Open **Sources & Keys → Manage Proxy Keys**.
2. Enter an app name, for example `Open WebUI`, `LobeChat`, `Dify`, or `Phone`.
3. Set a budget, rate limit, tags, and expiration if needed.
4. Create the key.
5. Copy the `sk-proxy-...` value into the app.

You can disable, reveal, regenerate, or delete each key.

Use this header:

```http
Authorization: Bearer sk-proxy-YOUR_KEY
```

A `401` means the key is missing or invalid. `402`, `403`, and `429` usually mean budget, permission, expiration, or rate-limit problems.

### 8. Endpoints, LAN, and Internet access

| Type | Example | Use |
|---|---|---|
| Ingress | `https://ha.example.com/api/hassio_ingress/...` | Dashboard and `/api/*` |
| LAN API | `http://HOME_ASSISTANT_IP:1236/v1` | Apps on the same LAN |
| Public API | `https://ai.example.com/v1` | Apps on the Internet |

Never use the Ingress URL as an API Base URL.

#### LAN

1. Publish port `1236`.
2. Open **Endpoint** and copy `http://HOME_ASSISTANT_IP:1236/v1`.
3. Use a Proxy Key for `/v1/*`.

#### HTTPS reverse proxy

Recommended architecture:

```text
Internet → HTTPS reverse proxy → http://ai-proxy-router:1236
```

- Forward only `/v1/*` and optionally `/health`.
- Keep `/` and `/api/*` internal or behind Home Assistant Ingress.
- Enable TLS and rate limiting where possible.
- If the proxy shares the add-on Docker network, use the add-on's internal hostname.
- If the proxy runs on the host/LAN, publish port `1236`.

After the public URL works:

1. Open **Endpoint → External access**.
2. Enter the **Public Base URL**, for example `https://ai.example.com/v1`.
3. Save and confirm the status shows **Configured**.
4. Run real requests to verify DNS, TLS, tunnel, and routing.

**Configured** only means the URL was saved. It does not prove reachability.

#### Cloudflare Tunnel

Cloudflare Tunnel is useful when Home Assistant has no public IP or you do not want to open ports.

**TLS hostname rule**

Cloudflare Universal SSL normally covers:

```text
example.com
*.example.com
```

Use `ai.example.com`. A nested host such as `ai.ha.example.com` can fail with:

```text
sslv3 alert handshake failure
SSL alert number 40
```

Use Advanced Certificate Manager if you truly need nested names.

**Cloudflared add-on steps**

1. Install and configure the **Cloudflared** add-on.
2. Choose a public hostname such as `ai.example.com`.
3. Point the service at AI Proxy Router, not at the Ingress URL:

   ```yaml
   additional_hosts:
     - hostname: ai.example.com
       service: http://<ai-proxy-container>:1236
   ```

   `<ai-proxy-container>` is the add-on's internal hostname, sometimes similar to `011a0c26-ai-proxy-router`. If Cloudflared cannot resolve it, publish port `1236` and use the Home Assistant LAN address.

4. Save and restart Cloudflared.
5. Wait 1–2 minutes. Cloudflared usually creates the DNS CNAME automatically.
6. Test:

   ```bash
   curl -i "https://ai.example.com/health"
   curl -i "https://ai.example.com/v1/models" \
     -H "Authorization: Bearer sk-proxy-YOUR_KEY"
   ```

7. In AI Proxy, open **Endpoint → External access**, enter `https://ai.example.com/v1`, and save.

Cloudflare notes:

- Do not route the tunnel to `/api/hassio_ingress/...`.
- Do not expose the dashboard or `/api/*` unless required.
- The app blocks `/` and `/api/*` externally, but add Cloudflare WAF/rate limits for `/v1/*` if possible.
- If Cloudflare Access is enabled for the API hostname, clients must send a service token. Many OpenAI-compatible apps do not support that.
- A Cloudflared restart can cause temporary `530` or `error code: 1033` responses while the tunnel reconnects.
- Remove old hostnames and DNS records when changing domains.

#### Direct port forwarding

Not recommended:

```text
Internet → router/firewall → HOME_ASSISTANT_IP:1236/v1
```

It has no TLS and is easy to scan. Use only with firewall rules, rate limits, monitoring, and an IP allowlist.

#### Endpoint checks

```bash
curl -i "https://ai.example.com/health"

curl -i "https://ai.example.com/v1/models" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY"

curl -i "https://ai.example.com/v1/chat/completions" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"auto-ai","messages":[{"role":"user","content":"Hello"}]}'
```

Expected:

- `/health`: `200`.
- `/v1/models` with a key: `200`.
- Chat with a key: `200`.
- No key: `401`.
- `/`, `/api/stats`, `/api/*` from the Internet: `403`.
- `/docs`, `/redoc`: `404`.
- `/openapi.json` from the Internet: `403`; through Ingress: `200`.

### 9. Connect apps and Home Assistant

| Field | Value |
|---|---|
| Base URL | `https://ai.example.com/v1` or `http://HOME_ASSISTANT_IP:1236/v1` |
| API Key | Proxy Key `sk-proxy-...` |
| Model | `auto-ai` or a saved model |

Environment variables for CLIs:

```bash
export OPENAI_BASE_URL="https://ai.example.com/v1"
export OPENAI_API_KEY="sk-proxy-YOUR_KEY"
```

Some tools use `OPENAI_API_BASE` instead. Check the tool documentation or use the **CLI Tools** snippets.

Python SDK:

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-proxy-YOUR_KEY",
    base_url="https://ai.example.com/v1",
)

response = client.chat.completions.create(
    model="auto-ai",
    messages=[{"role": "user", "content": "Hello"}],
)
print(response.choices[0].message.content)
```

The built-in Home Assistant OpenAI integration may not support a custom Base URL. Use a custom integration, a `rest_command`/`shell_command`, or Node-RED/AppDaemon instead.

Example `rest_command`:

```yaml
rest_command:
  ai_proxy_chat:
    url: "https://ai.example.com/v1/chat/completions"
    method: POST
    headers:
      Authorization: !secret ai_proxy_authorization
      Content-Type: "application/json"
    payload: >-
      {"model":"auto-ai","messages":[{"role":"user","content":{{ prompt | tojson }}}]}
```

`secrets.yaml`:

```yaml
ai_proxy_authorization: "Bearer sk-proxy-YOUR_KEY"
```

The router does not execute tools. Your app must run functions and send `function_call_output` back with the matching `call_id`.

### 10. OpenAI-compatible API

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/v1/models` | Model list |
| `POST` | `/v1/chat/completions` | Chat Completions, streaming supported |
| `POST` | `/v1/responses` | Responses API |
| `POST` | `/v1/audio/transcriptions` | Speech-to-Text |
| `POST` | `/v1/audio/speech` | Text-to-Speech |
| `GET` | `/health` | Health check, no key required |

All `/v1/*` endpoints require:

```http
Authorization: Bearer sk-proxy-YOUR_KEY
```

Basic chat:

```bash
curl "https://ai.example.com/v1/chat/completions" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"auto-ai","messages":[{"role":"user","content":"Hello"}]}'
```

Streaming:

```bash
curl -N "https://ai.example.com/v1/chat/completions" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"auto-ai","stream":true,"messages":[{"role":"user","content":"Hello"}]}'
```

Failover happens before the first SSE event. After a stream starts, errors are reported in that stream to avoid mixing content from two providers.

Response errors use:

```json
{"detail":"Error description"}
```

Common codes: `400` invalid request, `401` missing/invalid Proxy Key, `402` budget exhausted, `403` blocked/disabled, `404` wrong path/model, `429` rate limit, `503` no healthy source.

Structured output uses `text.format` with `json_schema` on `/v1/responses`. JSON Schema support depends on the provider; the router skips sources that cannot satisfy the request.

### 11. Voice

1. Add a source with STT/TTS models and sync models.
2. Create a Proxy Key.
3. Use the **Voice** tab for a quick test.

Speech-to-Text:

```bash
curl "https://ai.example.com/v1/audio/transcriptions" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY" \
  -F "file=@audio.mp3" \
  -F "model=WHISPER_MODEL"
```

Text-to-Speech:

```bash
curl "https://ai.example.com/v1/audio/speech" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"TTS_MODEL","input":"Hello from Home Assistant","voice":"alloy"}' \
  --output speech.mp3
```

Model and voice names depend on the provider. If no audio source is available, the API returns `503`.

### 12. Token Saver

Enable the main **Token Saver** switch, then choose modules:

- **RTK**: compresses long tool output such as `git`, `grep`, `ls`, `tree`, logs, and build output.
- **Headroom**: calls a `/v1/compress` service before routing; falls back to the original context on errors.
- **Caveman**: asks for terse answers at Lite/Full/Ultra levels while preserving code, commands, paths, errors, and safety warnings.
- **Ponytail**: guides the model toward YAGNI, deletion, reuse, stdlib, and native features before new abstractions or dependencies.

Bypass one request:

```http
X-AI-Proxy-Token-Saver: off
```

Responses may include:

```text
X-AI-Proxy-Token-Saver
X-AI-Proxy-Input-Chars-Saved
X-AI-Proxy-Estimated-Tokens-Saved
```

Headroom must run as a separate service with `/v1/compress`.

### 13. Usage, quota, logs, and Telegram

- **Usage** shows tokens, estimated cost, provider mix, and recent requests.
- **Quota** shows remaining source and Proxy Key budgets.
- Logs show recent errors and source status.
- Telegram alerts can be configured in **System** and tested from the dashboard.
- Provider checks verify active keys and models.
- The debug bundle masks secrets before sharing.

Dashboard cost is an estimate based on tokens and configured pricing. The provider invoice is the source of truth.

### 14. Backup, restore, and upgrade

- Download a backup from **System** before major changes.
- A full backup contains provider API keys, Proxy Keys, and sensitive settings. Encrypt it and keep it private.
- Restore creates a safety backup before writing data.
- `data.json` and backup files use mode `600`; corrupt JSON is kept as `.corrupt-*`.
- After an upgrade, check the version, `/health`, `/v1/models`, and a chat request.
- Use the masked preview or debug bundle when sharing diagnostics.

### 15. Security

- Dashboard and `/api/*` are available only through Home Assistant Ingress.
- State-changing `/api/*` calls require `X-CSRF-Token`.
- Port `1236` is disabled by default. If enabled, use it only for Proxy Key-protected `/v1/*`.
- Do not expose the dashboard or admin API to the Internet.
- Use HTTPS for remote access.
- Forward only `/v1/*` at the reverse proxy. Keep `/`, `/api/*`, `/docs`, `/redoc`, and `/openapi.json` off the Internet.
- Use a separate Proxy Key for each app with budget, rate limit, and expiration.
- Never share provider keys or Proxy Keys.
- Regenerate a Proxy Key immediately if it leaks.
- Keep backups encrypted and private.
- Remove old DNS records and tunnel hostnames after changing domains.
- From `1.22.0`, `/docs` and `/redoc` are disabled, `/openapi.json` is Ingress-only, and responses include `X-Content-Type-Options: nosniff` and `Referrer-Policy: no-referrer`.
- Public `/health` returns only status, name, version, and uptime; use `/health` or `/api/health` through Ingress for full details.

### 16. Troubleshooting

| Symptom | Common cause | Fix |
|---|---|---|
| Dashboard does not open | Direct `IP:1236` access | Open **Web UI** or the Home Assistant sidebar |
| Blank dashboard | Cache/JS error | Hard reload and check Console/Network |
| LAN client cannot connect | Port `1236` not published | Publish the port in **Network** |
| `401` | Missing/invalid Proxy Key | Check `Authorization: Bearer sk-proxy-...` |
| `403` | Key disabled/expired or wrong endpoint | Check the Proxy Key; do not call `/api/*` externally |
| `402` | Budget exhausted | Raise the key/source budget or create a new key |
| `429` | Rate limit | Slow down or raise the limit |
| `503` | No healthy source | Check sources, models, keys, quota, and logs |
| `404` | Wrong Base URL | Base URL must end with `/v1` |
| `530` / `1033` | Cloudflare Tunnel not connected | Wait 1–2 minutes, check Cloudflared logs, restart |
| TLS `alert 40` | Nested hostname | Use `ai.example.com`, not `ai.ha.example.com` |
| Public `/health` works but `/v1` fails | Key/source/model issue | Check the Proxy Key and source |
| Public Base URL says Configured but fails | URL saved, but DNS/TLS/tunnel is broken | Check DNS, tunnel, firewall, and certificate |
| Vision request fails | No Vision source | Add a source/model that supports images |
| Tool does not run | The router does not execute tools | The client must run the function |
| JSON Schema fails | Provider lacks support | Use a compatible source/model |
| Headroom offline | Service is not running | Check the URL/port and test button |
| Voice `503` | No STT/TTS model | Add an audio source and sync |
| Telegram does not send | Wrong token/chat ID | Check settings and use the test button |

Check from the Internet:

```bash
curl -i "https://ai.example.com/health"

curl -i "https://ai.example.com/v1/models" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY"
```

Check DNS:

```bash
dig +short ai.example.com
```

Check Cloudflare SSL/TLS mode, certificate coverage, and Cloudflared logs if TLS or tunnel errors occur.

### 17. FAQ

**Is the add-on free?**
The add-on is free. AI provider usage is billed by your provider.

**Is my data sent to a cloud service?**
Configuration, logs, and statistics stay in the add-on. Request content goes to the AI providers you configure. There is no add-on intermediary service.

**Can I use Ollama or LM Studio?**
Yes. Use **Custom Endpoint** with the service's `/v1` URL, and make sure Home Assistant can reach it.

**Can I expose the API to the Internet?**
Yes. Use an HTTPS reverse proxy or Cloudflare Tunnel, expose only `/v1/*`, always require Proxy Keys, and add rate limits/WAF where possible.

**Do I need port 1236?**
No, not for the dashboard or Cloudflared running next to Home Assistant. Enable it only for direct LAN clients.

**Why is port 1236 blocked for the dashboard?**
Dashboard and `/api/*` are designed to be reachable only through Home Assistant Ingress.

**Why does `/docs` return 404?**
Swagger and ReDoc are disabled in `1.22.0` to reduce attack surface. `/openapi.json` is Ingress-only.

**Why does a nested hostname fail TLS?**
Cloudflare Universal SSL normally covers `*.example.com`, not `ai.ha.example.com`. Use a one-level hostname or a suitable certificate.

**Does the router execute function tools?**
No. It returns function names and arguments; the client must execute them and send results back.

### 18. Technical notes

- Add-on slug: `ai_proxy_router`.
- Ingress/API port: `1236`.
- Architectures: `amd64`, `aarch64`.
- API server: FastAPI with OpenAI-compatible routes.
- Data: `/data/data.json` with mode `600`.
- Dashboard assets are bundled; no CDN required.
- Health check: `/health`.
- OpenAPI schema: `/openapi.json`, Ingress-only from `1.22.0`.
- Public add-on repository: `https://github.com/trankhanhduy2929-beep/my_hass_addon_public`.
- Release sources are maintained in the project's private repository.

```text
ai_proxy_router/
  config.yaml
  Dockerfile
  main.py
  token_saver.py
  ui_i18n.js
  dashboard.css
  vendor/
  README.md
  DOCS.md
```

Release process:

1. Update `config.yaml` and `APP_VERSION` in `main.py`.
2. Run compile, smoke, and UI checks.
3. Build the ZIP and SHA-256.
4. Update release notes.
5. Build/push the image and update add-on repository metadata.

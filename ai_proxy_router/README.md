# AI Proxy Router for Home Assistant

AI Proxy Router gom nhiều nguồn AI vào một API tương thích OpenAI, tự xoay API key, chuyển nguồn khi lỗi và định tuyến riêng cho yêu cầu Text/Vision.

AI Proxy Router combines multiple AI providers behind one OpenAI-compatible API, rotates API keys, fails over between sources, and routes Text/Vision requests automatically.

- [Tiếng Việt](#tiếng-việt)
- [English](#english)

---

## Tiếng Việt

### 1. Tính năng chính

- Xoay vòng nhiều API key và tự chuyển nguồn khi provider lỗi, hết quota hoặc đang cooldown.
- Endpoint tương thích OpenAI: `/v1/models`, `/v1/chat/completions` và `/v1/responses`.
- Hỗ trợ SSE streaming opt-in với `stream: true`; request không có `stream` vẫn trả JSON đầy đủ.
- Hỗ trợ function tools, `tool_choice`, `parallel_tool_calls`, streaming tool-call events và vòng lặp `function_call_output`.
- Hỗ trợ Structured Output dạng JSON Object/JSON Schema, có kiểm tra kết quả và tự chuyển nguồn khi output sai schema.
- Model `auto-ai` tự chọn nguồn Text/Vision phù hợp theo tình trạng thực tế.
- Hỗ trợ nguồn dựng sẵn, Custom Endpoint và OpenAI Codex OAuth.
- Codex OAuth có thể xử lý cả văn bản và ảnh qua cùng endpoint proxy.
- Bolt Token Saver gồm RTK, Headroom, Caveman và Ponytail.
- Proxy Key riêng cho từng ứng dụng, có hạn mức, rate limit, ngày hết hạn và bật/tắt nhanh.
- Dashboard song ngữ Việt/Anh, tối ưu thao tác chạm và chỉ mở qua Home Assistant Ingress.
- Thống kê token/chi phí, kiểm tra nguồn, Telegram, backup/restore và debug bundle đã che bí mật.

### 2. Cài đặt trên Home Assistant

1. Giải nén thư mục `ai_proxy_router` vào thư mục add-on cục bộ của Home Assistant, thường là `/addons/ai_proxy_router`.
2. Vào **Settings → Add-ons → Add-on Store**.
3. Mở menu góc phải và chọn **Check for updates** hoặc tải lại trang.
4. Chọn **AI Proxy Router**, nhấn **Install**, sau đó **Start**.
5. Bật **Show in sidebar** nếu muốn mở nhanh từ thanh bên.
6. Mở **Web UI** để cấu hình.

Cổng API LAN `1236` mặc định không được publish. Nếu ứng dụng trên thiết bị khác cần gọi proxy, mở tab **Network** của add-on và gán host port `1236` cho container port `1236/tcp`.

Kiến trúc được khai báo trong add-on: `amd64` và `aarch64`.

### 3. Mở dashboard và chọn ngôn ngữ

- Add-on mở thẳng dashboard qua Home Assistant Ingress, không còn màn hình đăng nhập, tài khoản hay mật khẩu nội bộ.
- Bộ chọn **Tiếng Việt / English** nằm trên thanh điều hướng và dùng được ngay khi mở addon.
- Nếu chưa từng chọn, trình duyệt tiếng Việt dùng Tiếng Việt; các ngôn ngữ khác dùng English.
- Lựa chọn được lưu trong trình duyệt và có thể đổi lại trên thanh điều hướng dashboard.

Truy cập trực tiếp `http://HOME_ASSISTANT_IP:1236/` sẽ bị từ chối. Cổng LAN, nếu được bật, chỉ dùng cho API `/v1/*`; dashboard và API quản trị `/api/*` yêu cầu Home Assistant Ingress.

### 4. Thêm nguồn AI/API key

1. Mở tab **API Các Nguồn**.
2. Chọn provider hoặc chọn **Custom Endpoint**.
3. Nhập API key thật của provider.
4. Với Custom Endpoint, nhập tên nguồn và Base URL tương thích OpenAI, ví dụ `https://api.example.com/v1`.
5. Nhấn **Tải Model**, chọn model rồi đặt hạn mức chi phí nếu cần.
6. Nhấn **Lưu Nguồn**.
7. Dùng nút `▲`/`▼` để sắp xếp ưu tiên nguồn.

Khi dùng `auto-ai`, router ưu tiên nguồn còn hoạt động và tự thử nguồn dự phòng khi gặp lỗi xác thực, quota, rate limit hoặc lỗi mạng.

### 5. Tạo và dùng Proxy Key

Không đưa API key gốc cho ứng dụng bên ngoài. Hãy tạo Proxy Key riêng:

1. Mở **Quản lý Proxy Keys**.
2. Nhập tên ứng dụng, hạn mức, rate limit, tag hoặc ngày hết hạn nếu cần.
3. Nhấn tạo mới và sao chép key dạng `sk-proxy-...`.
4. Có thể tắt, hiện lại, tạo lại hoặc xóa từng Proxy Key trên dashboard.

Thẻ **📡 Base URL Connect** tự hiển thị IP Home Assistant thực tế, Base URL, endpoint Chat Completions và endpoint Responses API. Mỗi dòng có nút sao chép một chạm.

Base URL dùng cho client:

```text
http://HOME_ASSISTANT_IP:1236/v1
```

Địa chỉ này chỉ hoạt động sau khi bật port `1236` trong cấu hình **Network** của add-on. `/v1/models`, `/v1/chat/completions` và `/v1/responses` đều yêu cầu Proxy Key.

Chat completions endpoint đầy đủ:

```text
http://HOME_ASSISTANT_IP:1236/v1/chat/completions
```

Responses API endpoint:

```text
http://HOME_ASSISTANT_IP:1236/v1/responses
```

### 6. Kiểm tra nhanh trên dashboard

Tab kiểm tra không yêu cầu nhập token. Khi nhấn kiểm tra, add-on tự chọn một Proxy Key hợp lệ đang bật. Hãy tạo ít nhất một Proxy Key trước khi chạy test.

Có ba chế độ: **Chat / Vision**, **Tool Calling** và **JSON Schema**. Tool mode chỉ hiển thị tên function cùng arguments do model tạo ra; add-on không thực thi function. JSON mode cho phép dán schema để kiểm tra failover structured output.

### 7. Gọi API tương thích OpenAI

Liệt kê model:

```bash
curl "http://HOME_ASSISTANT_IP:1236/v1/models" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY"
```

Chat văn bản:

```bash
curl "http://HOME_ASSISTANT_IP:1236/v1/chat/completions" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "auto-ai",
    "messages": [
      {"role": "user", "content": "Tóm tắt trạng thái ngôi nhà."}
    ]
  }'
```

Chat Vision bằng URL ảnh:

```bash
curl "http://HOME_ASSISTANT_IP:1236/v1/chat/completions" \
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

Ảnh có thể là URL `http(s)` hoặc data URI `data:image/...`. Với Chat Completions, thêm `"stream": true` để nhận SSE; Responses API hỗ trợ cả JSON và các event SSE như `response.output_text.delta` và `response.completed`.

Chat streaming:

```bash
curl -N "http://HOME_ASSISTANT_IP:1236/v1/chat/completions" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"auto-ai","stream":true,"messages":[{"role":"user","content":"Xin chào"}]}'
```

Responses API:

```bash
curl "http://HOME_ASSISTANT_IP:1236/v1/responses" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"auto-ai","input":"Tóm tắt trạng thái ngôi nhà."}'
```

Function tool qua Chat Completions:

```bash
curl "http://HOME_ASSISTANT_IP:1236/v1/chat/completions" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model":"auto-ai",
    "messages":[{"role":"user","content":"Kiểm tra trạng thái phòng khách"}],
    "tools":[{"type":"function","function":{"name":"get_home_status","description":"Đọc trạng thái phòng","parameters":{"type":"object","properties":{"room":{"type":"string"}},"required":["room"],"additionalProperties":false}}}],
    "tool_choice":"required",
    "parallel_tool_calls":false
  }'
```

Function tool qua Responses dùng định dạng phẳng `{"type":"function","name":...}`. Sau khi ứng dụng tự kiểm tra và thực thi function, gửi kết quả lại bằng item `function_call_output` có cùng `call_id`. Router không tự chạy web/file/computer hoặc bất kỳ function nào.

Structured Output JSON Schema:

```bash
curl "http://HOME_ASSISTANT_IP:1236/v1/responses" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model":"auto-ai",
    "input":"Trả về trạng thái ngắn gọn",
    "text":{"format":{"type":"json_schema","name":"home_status","strict":true,"schema":{"type":"object","properties":{"status":{"type":"string"}},"required":["status"],"additionalProperties":false}}}
  }'
```

Khi stream tool calls qua Responses, client nhận các event `response.output_item.added`, `response.function_call_arguments.delta`, `response.function_call_arguments.done`, `response.output_item.done` và `response.completed`. Router tự bỏ qua nguồn không hỗ trợ tính năng yêu cầu. Codex OAuth vẫn dùng Text/Vision nhưng bị loại khỏi request tools/JSON Schema và không bao giờ thực thi tool.

Router chỉ chuyển nguồn dự phòng trước khi event SSE đầu tiên được gửi. Sau khi stream đã bắt đầu, lỗi được trả trong stream hiện tại để tránh ghép nội dung từ hai provider. Codex OAuth dùng fallback SSE tổng hợp từ nội dung hoàn chỉnh vì app-server không luôn cung cấp stream token-level ổn định.

### 8. Cấu hình client/Home Assistant

Trong ứng dụng hoặc tích hợp hỗ trợ OpenAI Custom Base URL, nhập:

| Trường | Giá trị |
|---|---|
| Base URL | `http://HOME_ASSISTANT_IP:1236/v1` |
| API Key | Proxy Key dạng `sk-proxy-...` |
| Model | `auto-ai` hoặc tên model đã lưu |

Ví dụ Python dùng OpenAI SDK:

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-proxy-YOUR_KEY",
    base_url="http://HOME_ASSISTANT_IP:1236/v1",
)

response = client.chat.completions.create(
    model="auto-ai",
    messages=[{"role": "user", "content": "Xin chào"}],
)
print(response.choices[0].message.content)
```

Nếu client chạy trên thiết bị khác, bật port `1236`, sau đó thay `HOME_ASSISTANT_IP` bằng địa chỉ LAN của máy Home Assistant. Không dùng URL Ingress làm Base URL cho ứng dụng API bên ngoài.

### 9. Đăng nhập OpenAI Codex OAuth

1. Mở phần **OpenAI Codex OAuth** trên dashboard.
2. Nhấn **Đăng nhập Codex**.
3. Sao chép mã thiết bị và mở liên kết xác thực được hiển thị.
4. Đăng nhập tài khoản ChatGPT/OpenAI và xác nhận mã.
5. Quay lại dashboard; trạng thái sẽ tự cập nhật và nguồn `codex-auto` được bật tự động.
6. Có thể tải danh sách model và chọn model cụ thể, hoặc giữ `codex-auto` để tự chọn Text/Vision.

Thông tin OAuth được Codex CLI lưu trong vùng dữ liệu bền vững `/data/codex`. AI Proxy Router không hiển thị access token và không đưa token Codex vào file backup của router.

### 10. Dùng Codex Vision

- Giữ model `codex-auto` để bridge tự chọn model phù hợp khi message có ảnh.
- Gửi ảnh bằng `image_url`, `input_image`, URL `http(s)` hoặc data URI.
- Có thể thử trực tiếp trong tab test bằng cách tải ảnh lên; không cần nhập token test.
- Nếu Vision lỗi, kiểm tra trạng thái OAuth, model đã chọn và định dạng ảnh.

### 11. Bolt Token Saver

Bật master **Bolt Token Saver** trong phần cài đặt, sau đó chọn các module cần dùng:

- **RTK — Compress tool output:** nén đầu ra dài của `git`, `grep`, `ls`, `tree`, log/build output và dữ liệu tương tự trước khi gửi model.
- **Headroom — Compress context:** gọi `/v1/compress` của dịch vụ Headroom trước khi routing. Nếu lỗi, timeout hoặc dữ liệu trả về không hợp lệ, router tự dùng context gốc.
- **Caveman — Compress LLM output:** thêm chỉ dẫn trả lời ngắn theo mức Lite/Full/Ultra nhưng vẫn giữ code, lệnh, đường dẫn, lỗi và cảnh báo an toàn.
- **Ponytail — Lazy senior dev:** hướng model theo YAGNI, ưu tiên xóa/reuse/stdlib/native trước khi thêm abstraction hoặc dependency.

RTK bật sẵn trong cấu hình module nhưng chỉ chạy khi master Token Saver được bật. Headroom, Caveman và Ponytail là tùy chọn độc lập.

Để bỏ qua Token Saver cho một request:

```http
X-AI-Proxy-Token-Saver: off
```

Response có thể trả các header:

```text
X-AI-Proxy-Token-Saver
X-AI-Proxy-Input-Chars-Saved
X-AI-Proxy-Estimated-Tokens-Saved
```

Headroom phải chạy như dịch vụ riêng có endpoint `/v1/compress`. Nhập URL dịch vụ vào dashboard và dùng nút kiểm tra trạng thái trước khi bật.

### 12. Backup và khôi phục

- Dùng **Tải backup** để xuất cấu hình JSON.
- Dùng **Khôi phục backup** để nhập lại file JSON hợp lệ.
- Trước khi restore, add-on tự tạo safety backup và giữ các bản gần nhất.
- Dùng masked preview/debug bundle khi cần gửi thông tin chẩn đoán mà không lộ API key.

> File backup đầy đủ có chứa API key nguồn, Proxy Key và cấu hình nhạy cảm. Hãy mã hóa hoặc lưu ở nơi an toàn, không đăng công khai.

### 13. Xử lý sự cố

- **Không mở được dashboard:** mở từ **Open Web UI** hoặc sidebar Home Assistant; truy cập trực tiếp bằng `IP:1236` bị chặn theo thiết kế.
- **Client LAN không kết nối:** mở cấu hình **Network** và publish container port `1236/tcp` ra host port `1236`.
- **Client báo 401:** kiểm tra header `Authorization: Bearer sk-proxy-...` và Proxy Key còn tồn tại.
- **Client báo 403/402/429:** Proxy Key có thể đang tắt, hết hạn, hết hạn mức hoặc vượt rate limit.
- **Không có nguồn phù hợp:** bật ít nhất một nguồn, tải đúng model và dùng model hỗ trợ Vision nếu request có ảnh.
- **Custom Endpoint lỗi:** Base URL phải trỏ đến API tương thích OpenAI; thường kết thúc bằng `/v1`.
- **Codex OAuth lỗi:** đăng xuất rồi đăng nhập lại, xác nhận mã thiết bị còn hạn và xem log add-on.
- **Headroom báo Not installed/offline:** chạy Headroom riêng, kiểm tra URL/port và nút kiểm tra trên dashboard.
- **Test không chạy:** tạo ít nhất một Proxy Key hợp lệ; ô test không còn nhận token thủ công.
- **Ngôn ngữ không đổi:** tải lại trang và cho phép `localStorage`; lựa chọn được lưu riêng theo trình duyệt.

### 14. Lưu ý bảo mật

- Dashboard và API quản trị chỉ nhận request từ Home Assistant Ingress.
- Mọi thao tác thay đổi dữ liệu qua `/api/*` yêu cầu header `X-CSRF-Token` do dashboard tự gắn.
- `data.json` và file backup được đặt quyền `600`; file JSON lỗi được giữ thành bản `.corrupt-*` thay vì ghi đè.
- Port `1236` mặc định tắt; nếu bật, chỉ dùng cho API `/v1/*` có Proxy Key và không nên mở trực tiếp ra Internet.
- Không chia sẻ API key nguồn; cấp Proxy Key riêng cho từng ứng dụng và đặt hạn mức/rate limit.
- Tạo lại Proxy Key ngay nếu nghi ngờ bị lộ.
- Kiểm tra kỹ file backup trước khi sao chép hoặc gửi cho người khác.

---

## English

### 1. Main features

- Rotates multiple API keys and fails over when a provider is unavailable, out of quota, or cooling down.
- OpenAI-compatible endpoints: `/v1/models`, `/v1/chat/completions`, and `/v1/responses`.
- Opt-in SSE streaming with `stream: true`; requests without `stream` remain normal JSON responses.
- Function tools with `tool_choice`, `parallel_tool_calls`, streaming tool-call events, and `function_call_output` follow-ups.
- JSON Object/JSON Schema structured output with validation and automatic fallback after invalid output.
- The `auto-ai` model selects a healthy Text/Vision source automatically.
- Supports built-in providers, Custom Endpoints, and OpenAI Codex OAuth.
- Codex OAuth supports both text and image requests through the same proxy endpoint.
- Bolt Token Saver includes RTK, Headroom, Caveman, and Ponytail.
- Per-application Proxy Keys with budgets, rate limits, expiration dates, and enable/disable controls.
- Vietnamese/English dashboard with touch-friendly navigation, restricted to Home Assistant Ingress.
- Token/cost statistics, provider checks, Telegram alerts, backup/restore, and a masked debug bundle.

### 2. Install on Home Assistant

1. Extract the `ai_proxy_router` directory into the Home Assistant local add-ons directory, usually `/addons/ai_proxy_router`.
2. Open **Settings → Add-ons → Add-on Store**.
3. Open the top-right menu and select **Check for updates**, or reload the page.
4. Select **AI Proxy Router**, click **Install**, then **Start**.
5. Enable **Show in sidebar** for quick access if desired.
6. Open the **Web UI** to configure the router.

LAN API port `1236` is not published by default. If a client on another device needs the proxy, open the add-on **Network** settings and map host port `1236` to container port `1236/tcp`.

The add-on currently declares `amd64` and `aarch64` architectures.

### 3. Open the dashboard and select a language

- The add-on opens the dashboard directly through Home Assistant Ingress; there is no built-in login screen, username, or password.
- The **Tiếng Việt / English** selector is on the navigation bar and works immediately when the add-on opens.
- On first use, Vietnamese browsers default to Vietnamese; other browser languages default to English.
- The selection is stored in the browser and can be changed again from the dashboard navigation bar.

Direct access to `http://HOME_ASSISTANT_IP:1236/` is denied. If the LAN port is enabled, it is only for `/v1/*`; the dashboard and `/api/*` administration endpoints require Home Assistant Ingress.

### 4. Add an AI provider/API key

1. Open the **API Sources** tab.
2. Select a provider or choose **Custom Endpoint**.
3. Enter the provider's real API key.
4. For a Custom Endpoint, enter a display name and an OpenAI-compatible Base URL such as `https://api.example.com/v1`.
5. Click **Load Models**, select a model, and optionally set a cost budget.
6. Click **Save Source**.
7. Use the `▲`/`▼` controls to change source priority.

With `auto-ai`, the router prefers healthy sources and automatically tries fallbacks after authentication, quota, rate-limit, or network failures.

### 5. Create and use a Proxy Key

Do not distribute upstream provider keys. Create a separate Proxy Key for each client:

1. Open **Proxy Key Management**.
2. Enter an application name and optional budget, rate limit, tag, or expiration date.
3. Create the key and copy the generated `sk-proxy-...` value.
4. Each Proxy Key can be disabled, revealed, regenerated, or deleted from the dashboard.

The **📡 Base URL Connect** card automatically shows the Home Assistant IP, Base URL, Chat Completions endpoint, and Responses API endpoint. Each row has a one-click copy button.

Client Base URL:

```text
http://HOME_ASSISTANT_IP:1236/v1
```

Full chat completions endpoint:

```text
http://HOME_ASSISTANT_IP:1236/v1/chat/completions
```

Responses API endpoint:

```text
http://HOME_ASSISTANT_IP:1236/v1/responses
```

These addresses work only after port `1236` is enabled in the add-on **Network** settings. `/v1/models`, `/v1/chat/completions`, and `/v1/responses` require a Proxy Key.

### 6. Dashboard quick test

The test tab no longer asks for a token. When you click Test, the add-on automatically selects an enabled, valid Proxy Key. Create at least one Proxy Key before running a test.

Three modes are available: **Chat / Vision**, **Tool Calling**, and **JSON Schema**. Tool mode displays the function name and generated arguments but never executes the function. JSON mode accepts a schema for structured-output failover testing.

### 7. Call the OpenAI-compatible API

List models:

```bash
curl "http://HOME_ASSISTANT_IP:1236/v1/models" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY"
```

Text chat:

```bash
curl "http://HOME_ASSISTANT_IP:1236/v1/chat/completions" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "auto-ai",
    "messages": [
      {"role": "user", "content": "Summarize the current home status."}
    ]
  }'
```

Vision chat using an image URL:

```bash
curl "http://HOME_ASSISTANT_IP:1236/v1/chat/completions" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "auto-ai",
    "messages": [{
      "role": "user",
      "content": [
        {"type": "text", "text": "Describe this image."},
        {"type": "image_url", "image_url": {"url": "https://example.com/camera.jpg"}}
      ]
    }]
  }'
```

Images may use an `http(s)` URL or a `data:image/...` URI. Set `stream: true` for Chat Completions SSE. The Responses endpoint emits events including `response.output_text.delta` and `response.completed`.

Chat streaming:

```bash
curl -N "http://HOME_ASSISTANT_IP:1236/v1/chat/completions" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"auto-ai","stream":true,"messages":[{"role":"user","content":"Hello"}]}'
```

Responses API:

```bash
curl "http://HOME_ASSISTANT_IP:1236/v1/responses" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"auto-ai","input":"Summarize the current home status."}'
```

Function tool with Chat Completions:

```bash
curl "http://HOME_ASSISTANT_IP:1236/v1/chat/completions" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model":"auto-ai",
    "messages":[{"role":"user","content":"Check the living room status"}],
    "tools":[{"type":"function","function":{"name":"get_home_status","description":"Read room status","parameters":{"type":"object","properties":{"room":{"type":"string"}},"required":["room"],"additionalProperties":false}}}],
    "tool_choice":"required",
    "parallel_tool_calls":false
  }'
```

Responses function tools use the flat `{"type":"function","name":...}` format. After the client validates and executes the function, send a `function_call_output` item with the matching `call_id`. The Router never runs hosted web/file/computer tools or client functions.

JSON Schema structured output:

```bash
curl "http://HOME_ASSISTANT_IP:1236/v1/responses" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model":"auto-ai",
    "input":"Return a short home status",
    "text":{"format":{"type":"json_schema","name":"home_status","strict":true,"schema":{"type":"object","properties":{"status":{"type":"string"}},"required":["status"],"additionalProperties":false}}}
  }'
```

Responses tool streaming emits `response.output_item.added`, `response.function_call_arguments.delta`, `response.function_call_arguments.done`, `response.output_item.done`, and `response.completed`. Unsupported providers are skipped automatically. Codex OAuth remains available for Text/Vision but is excluded from tools/JSON Schema requests and never executes tools.

The router can fail over before the first SSE event is sent. After streaming starts, an error stays in the current stream so output from two providers is never merged. Codex OAuth uses synthesized SSE chunks from its completed answer because token-level app-server streaming is not consistently available.

### 8. Configure a client/Home Assistant

For an application or Home Assistant integration that supports a custom OpenAI Base URL, use:

| Field | Value |
|---|---|
| Base URL | `http://HOME_ASSISTANT_IP:1236/v1` |
| API Key | A Proxy Key such as `sk-proxy-...` |
| Model | `auto-ai` or a saved model name |

Python example using the OpenAI SDK:

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-proxy-YOUR_KEY",
    base_url="http://HOME_ASSISTANT_IP:1236/v1",
)

response = client.chat.completions.create(
    model="auto-ai",
    messages=[{"role": "user", "content": "Hello"}],
)
print(response.choices[0].message.content)
```

If the client runs on another device, enable port `1236`, then replace `HOME_ASSISTANT_IP` with the Home Assistant host's LAN address. Do not use the Ingress URL as an external API Base URL.

### 9. Sign in with OpenAI Codex OAuth

1. Open **OpenAI Codex OAuth** on the dashboard.
2. Click **Sign in to Codex**.
3. Copy the device code and open the displayed verification link.
4. Sign in to your ChatGPT/OpenAI account and confirm the code.
5. Return to the dashboard; the status updates automatically and the `codex-auto` source is enabled.
6. Load and select a specific model, or keep `codex-auto` for automatic Text/Vision selection.

OAuth credentials are stored by the Codex CLI in persistent `/data/codex` storage. AI Proxy Router does not expose the access token or include the Codex token in router backups.

### 10. Use Codex Vision

- Keep `codex-auto` selected so the bridge can choose an appropriate model when an image is present.
- Send images as `image_url` or `input_image` parts using an `http(s)` URL or data URI.
- You can also upload an image in the dashboard test tab; no test token is required.
- If Vision fails, verify OAuth status, the selected model, and the image format.

### 11. Bolt Token Saver

Enable the main **Bolt Token Saver** switch, then choose the required modules:

- **RTK — Compress tool output:** reduces long `git`, `grep`, `ls`, `tree`, log/build, and similar tool output before it reaches the model.
- **Headroom — Compress context:** calls a Headroom `/v1/compress` service before routing. On errors, timeouts, or invalid responses, the router safely falls back to the original context.
- **Caveman — Compress LLM output:** injects a Lite/Full/Ultra terse-style instruction while preserving code, commands, paths, errors, and safety warnings.
- **Ponytail — Lazy senior dev:** biases coding responses toward YAGNI, deletion, reuse, standard-library, and native solutions before new abstractions or dependencies.

RTK is selected by default at the module level but only runs when the main Token Saver switch is enabled. Headroom, Caveman, and Ponytail are independent options.

Bypass Token Saver for one request:

```http
X-AI-Proxy-Token-Saver: off
```

Responses may include:

```text
X-AI-Proxy-Token-Saver
X-AI-Proxy-Input-Chars-Saved
X-AI-Proxy-Estimated-Tokens-Saved
```

Headroom must run as a separate service exposing `/v1/compress`. Enter its service URL on the dashboard and test the connection before enabling it.

### 12. Backup and restore

- Use **Download Backup** to export the complete JSON configuration.
- Use **Restore Backup** to import a valid JSON backup.
- Before restoration, the add-on creates a safety backup and retains recent copies.
- Use the masked preview/debug bundle when sharing diagnostics without exposing API keys.

> A full backup contains upstream API keys, Proxy Keys, and other sensitive configuration. Encrypt it or keep it in secure storage; never publish it.

### 13. Troubleshooting

- **Dashboard does not open:** use **Open Web UI** or the Home Assistant sidebar; direct `IP:1236` dashboard access is blocked by design.
- **LAN client cannot connect:** map container port `1236/tcp` to host port `1236` in the add-on **Network** settings.
- **Client returns 401:** verify `Authorization: Bearer sk-proxy-...` and confirm that the Proxy Key still exists.
- **Client returns 403/402/429:** the Proxy Key may be disabled, expired, over budget, or rate-limited.
- **No suitable source:** enable at least one source, load a valid model, and use a Vision-capable model for image requests.
- **Custom Endpoint fails:** the Base URL must expose an OpenAI-compatible API and usually ends in `/v1`.
- **Codex OAuth fails:** sign out and sign in again, verify that the device code is still valid, and inspect add-on logs.
- **Headroom shows Not installed/offline:** run Headroom separately and verify its URL, port, and dashboard status check.
- **Dashboard test fails:** create at least one valid Proxy Key; the test form no longer accepts a manually entered token.
- **Language does not change:** reload the page and allow `localStorage`; the preference is stored per browser.

### 14. Security notes

- The dashboard and administration APIs accept requests only through Home Assistant Ingress.
- Every data-changing `/api/*` call requires an `X-CSRF-Token` header added automatically by the dashboard.
- `data.json` and backup files are written with mode `600`; corrupt JSON is preserved as a `.corrupt-*` copy instead of being overwritten.
- Port `1236` is disabled by default; if enabled, use it only for Proxy Key-protected `/v1/*` APIs and do not expose it directly to the Internet.
- Never share upstream API keys; issue a separate Proxy Key per application and apply budgets/rate limits.
- Regenerate a Proxy Key immediately if it may have leaked.
- Treat full backup files as secrets before copying or sharing them.

---

## Phiên bản / Version

Tài liệu này áp dụng cho AI Proxy Router `1.14.1`.

This guide applies to AI Proxy Router `1.14.1`.

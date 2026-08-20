# 🚀 AI Proxy Router Add-on

**Ngôn ngữ / Language:** [Tiếng Việt](#hướng-dẫn-tiếng-việt) · [English](#english-guide)

README song ngữ đầy đủ nằm trong file `README.md` của add-on. Phần tiếng Việt hiện có được giữ bên dưới; phần hướng dẫn English nằm ở cuối tài liệu.

The complete bilingual README is included as `README.md`. The existing Vietnamese guide remains below, followed by an English guide at the end.

## Hướng dẫn Tiếng Việt

Chào mừng bạn đến với AI Proxy Router! Add-on này biến Home Assistant của bạn thành một trạm trung chuyển (Proxy) AI siêu mạnh mẽ, giúp bạn gom chung tất cả API Keys từ các nhà cung cấp (Groq, Gemini, OpenRouter, OpenAI, và cả Các Nguồn Custom) vào một chỗ và tự động định tuyến thông minh.

Dưới đây là hướng dẫn từ A-Z để bạn làm chủ hệ thống này.

🌟 TÍNH NĂNG NỔI BẬT

Smart Routing (Định tuyến thông minh): Gửi chữ thì gọi LLM (Llama, Claude), gửi ảnh thì tự động bẻ lái sang model Vision (Gemini, GPT-4o).

Key Rotation (Xoay vòng): Add-on sẽ tự chuyển sang API Key khác nếu Key đang dùng bị lỗi mạng hoặc hết tiền (Quota Exceeded).

Auto-AI: Tính năng chọn model tự động theo thứ tự ưu tiên mà bạn sắp xếp.

Custom Endpoints: Hỗ trợ cấu hình thêm API từ DeepSeek, Together AI, Mistral hoặc thậm chí mô hình Local (LM Studio, Ollama).

Quản lý Hạn mức (Quota Limits): Bảo vệ túi tiền của bạn bằng cách giới hạn số USD tối đa mà mỗi Client được xài.

Thống kê: Theo dõi Token, dự tính chi phí.

Tool Calling & Structured Output: Hỗ trợ function tools trên Chat Completions/Responses, streaming arguments, JSON Object/JSON Schema và failover khi output sai schema. Function chỉ được trả về cho client; Router không tự thực thi.

🛠️ HƯỚNG DẪN CÀI ĐẶT & CẤU HÌNH

Bước 1: Mở Dashboard

Sau khi nhấn Start Add-on, bạn hãy nhấn vào nút Open Web UI (hoặc tích chọn Show in sidebar rồi nhấn vào thanh menu bên trái). Add-on mở thẳng dashboard qua Home Assistant Ingress, không có tài khoản/mật khẩu nội bộ.

Dashboard và API quản trị `/api/*` chỉ hoạt động qua Home Assistant Ingress. Cổng LAN `1236` mặc định tắt; nếu client ngoài Home Assistant cần kết nối, hãy publish `1236/tcp` trong mục Network của add-on. Proxy Key được yêu cầu cho `/v1/models`, `/v1/chat/completions` và `/v1/responses`.

Bước 2: Thêm API Key Gốc (Nguồn cấp)

Đây là nơi bạn khai báo các Key thật từ các hãng AI.

Tại mục API Các Nguồn, chọn tên nhà cung cấp (Ví dụ: Groq).

Mẹo: Nếu bạn muốn thêm hãng khác (như DeepSeek), hãy chọn 🌐 Custom Endpoint. Lúc này bảng sẽ hiện thêm 2 ô để bạn điền Tên hiển thị và Base URL của hãng đó (Ví dụ: https://api.deepseek.com/v1).

Dán API Key thật của bạn vào ô kế bên.

Nhấn nút Tải Model. Lúc này Add-on sẽ tự động liên hệ máy chủ để lấy danh sách các model có sẵn (giúp bạn không phải gõ tay dễ sai sót).

Chọn Model bạn muốn dùng từ Menu xổ xuống.

Thiết lập Quota ($) (Hạn mức): Nếu bạn mua Key đó 5$, hãy nhập số 5. Khi xài hết 5$, Proxy sẽ khóa Key đó lại. (Nếu xài Free, hãy để là 0).

Nhấn Lưu Nguồn.

Bước 3: Sắp xếp Ưu tiên

Hệ thống sẽ chạy từ trên xuống dưới danh sách Nguồn bạn đã thêm.

Sử dụng các nút mũi tên ▲ / ▼ để thay đổi vị trí ưu tiên.

Ví dụ: Bạn xếp Groq (miễn phí) ở trên cùng, Custom DeepSeek ở giữa, OpenRouter (trả phí) ở dưới. Khi các nguồn free bị sập, hệ thống mới tự chuyển sang dùng OpenRouter để tiết kiệm.

Bước 4: Tạo Proxy Key (Giấy thông hành)

Thay vì dùng Key gốc đem đi phân phát dễ bị lộ, bạn sẽ cấp Proxy Key cho các ứng dụng.

Đến mục Quản lý Proxy Keys.

Đặt tên cho ứng dụng (VD: LobeChat).

Nhập giới hạn ngân sách $ muốn cấp cho app đó (Nhập 0 nếu cho xài thả ga). Nhấn Tạo mới.

Nhấn nút 📋 để copy mã Proxy Key (có dạng sk-proxy-...).

🔗 KẾT NỐI VỚI ỨNG DỤNG BÊN NGOÀI

Bây giờ bạn đã có Base URL (xem trên Dashboard) và Proxy Key. Hãy mở các ứng dụng như Dify, LobeChat, ChatGPT Next Web, hoặc Home Assistant OpenAI Conversation và cấu hình như sau:

API Endpoint / Base URL / Custom Endpoint: Sau khi bật port `1236` trong mục Network, dùng đường dẫn có dạng http://<IP_HASS_CỦA_BẠN>:1236/v1

API Key: Dán mã sk-proxy-... bạn vừa tạo ở Bước 4.

Custom Model: * Gõ chữ auto-ai (Đây là tính năng độc quyền: Add-on sẽ tự động tìm và dùng model đang rảnh nhất trên hệ thống của bạn).

Hoặc gõ chính xác tên model (VD: gpt-4o hoặc deepseek-chat) nếu bạn chỉ muốn "bắt" nó dùng đúng model đó.

❓ XỬ LÝ SỰ CỐ THƯỜNG GẶP

Dashboard hiện IP lỗi homeassistant.local: Bạn chưa cấp quyền mạng cho Add-on. Hãy đảm bảo bạn đã chèn dòng hassio_api: true vào file cấu hình config.yaml và Rebuild lại Add-on.

Quét Lỗi Key báo đỏ:
Nhà cung cấp đã xóa (deprecated) cái model đó, hoặc API Key của bạn đã bị khóa. Hãy tạo/cập nhật Key khác!

Lỗi khi thêm Custom Endpoint:
Hãy chắc chắn rằng Base URL của hãng đó chuẩn định dạng OpenAI và phải kết thúc bằng /v1 (Ví dụ: https://api.together.xyz/v1).

---

## Cập nhật 1.0.4

- Tạo Proxy Key mặc định ngẫu nhiên thay vì dùng key cố định
- Session đăng nhập dùng token ngẫu nhiên thay cho cookie tĩnh
- Đổi mật khẩu tài khoản sẽ được lưu dạng hash SHA-256 có salt
- Ẩn API key gốc khi trả dữ liệu dashboard `/api/stats`
- Ghi `data.json` theo kiểu atomic write để an toàn hơn khi có nhiều request
- Thêm endpoint kiểm tra sống `/health`
- Tự ép `stream=false` để tương thích ổn định hơn với client/Home Assistant ở bản này
- Bổ sung OpenRouter headers cho request chat completion
- Normalize custom base URL tốt hơn cho endpoint `/models` và `/chat/completions`
- Cải thiện nhận diện Vision input


## Cập nhật 1.0.5

- Thêm CSRF protection cho toàn bộ API thay đổi dữ liệu (POST/DELETE quản trị)
- Dashboard tự gửi `X-CSRF-Token` từ cookie đăng nhập
- Siết CORS mặc định: không mở `*`; dùng same-origin/Ingress là chính
- Có thể mở CORS có kiểm soát qua biến `ALLOWED_ORIGINS` (danh sách URL, cách nhau dấu phẩy)
- Tự migrate mật khẩu plaintext cũ sang hash SHA-256 + salt khi boot


## Cập nhật 1.0.6

- Thêm rate limit cho đăng nhập (giới hạn số lần sai và khóa tạm thời)
- Thêm session idle timeout (hết phiên nếu không hoạt động)
- Cookie đăng nhập/CSRF có `max_age`, tự bật `secure` khi truy cập HTTPS qua reverse proxy
- `/api/stats` không còn trả full proxy key, chỉ trả key đã mask
- Thêm endpoint quản trị Proxy Key:
  - `POST /api/proxy_keys/{index}/reveal` để lấy full key khi cần
  - `POST /api/proxy_keys/{index}/regenerate` để tạo key mới và vô hiệu key cũ
- Dashboard cập nhật nút copy theo cơ chế reveal + thêm nút regenerate key


## OpenAI Codex OAuth (v1.3.0)

Bản 1.3.0 cho phép dùng OpenAI Codex qua tài khoản ChatGPT mà không phải nhập API key thủ công.

1. Mở giao diện Add-on.
2. Tại thẻ **OpenAI Codex — đăng nhập không cần API Key**, bấm **Đăng nhập Codex**.
3. Mở trang `https://auth.openai.com/codex/device` bằng nút trong giao diện.
4. Nhập mã một lần được Add-on hiển thị và hoàn thành đăng nhập ChatGPT.
5. Quay lại Add-on, chọn model rồi bấm **Bật nguồn Codex**.

Thông tin xác thực được Codex CLI chính thức lưu trong `/data/codex`, tồn tại qua lần khởi động lại Add-on và được Codex tự làm mới. AI Proxy Router không đọc hoặc đưa access token ra giao diện/backup. Nguồn Codex chạy ở sandbox chỉ đọc, approval `never`, đồng thời client từ chối các yêu cầu chạy công cụ để phù hợp chế độ proxy trả lời văn bản.

Lưu ý: Codex sử dụng hạn mức của gói ChatGPT/Codex đang đăng nhập. Khả năng truy cập model và giới hạn sử dụng phụ thuộc tài khoản, workspace và chính sách hiện hành của OpenAI.


## Cập nhật 1.5.0 — Tự phục hồi nguồn

- Thêm nút **Tự phục hồi nguồn** trong khu vực Chat test nhanh.
- Hệ thống kiểm tra đồng thời các provider đã lưu và chỉ kích hoạt lại nguồn khi endpoint phản hồi thành công.
- Nguồn phục hồi thành công được xóa số lần lỗi, cooldown và thông báo lỗi cũ.
- Thêm tùy chọn **Tự đổi model khi model cũ không còn**. Tùy chọn này mặc định tắt để tránh tự thay đổi cấu hình ngoài ý muốn.
- Khi bật tự đổi model, Router ưu tiên model cùng họ với model cũ; nếu không tìm thấy mới chọn model phổ biến phù hợp từ danh sách provider trả về.
- Bảng nguồn hiển thị thêm độ trễ, thời điểm kiểm tra và dấu hiệu lỗi gần nhất.
- Mọi lần tự phục hồi đều được ghi vào Audit log.
- Giữ nguyên định tuyến dự phòng thông minh và các sửa lỗi ổn định từ v1.4.0.


## Cập nhật 1.6.0 — Giám sát tự động, Telegram và backup an toàn

- Thêm kiểm tra provider định kỳ chạy nền nhẹ, chu kỳ tối thiểu 5 phút và có thể tắt hoàn toàn.
- Có tùy chọn tự kích hoạt lại nguồn sau khi kiểm tra xác nhận nguồn đã hoạt động tốt.
- Thêm nút **Kiểm tra ngay** và phần tổng quan vận hành: số nguồn khỏe/lỗi, tỉ lệ request thành công và nhóm lỗi xác thực, hạn mức, model, mạng/timeout.
- Thêm cảnh báo Telegram khi toàn bộ nguồn lỗi, hệ thống suy giảm hoặc tự phục hồi thành công.
- Telegram có thời gian chống gửi trùng; Bot Token và Chat ID được cấu hình ngay trong giao diện quản trị.
- Thêm nút gửi thử Telegram để kiểm tra cấu hình.
- Trước khi Restore JSON, Router tự tạo một bản sao an toàn trong `/data` và giữ tối đa 5 bản gần nhất.
- Giữ nguyên toàn bộ tính năng v1.5.0: tự phục hồi nguồn, tùy chọn sửa model, failover thông minh, Codex OAuth và kiểm tra đồng loạt provider.


## Cập nhật 1.7.3 — Tùy chọn bỏ mật khẩu

- Thêm tùy chọn **Tắt yêu cầu mật khẩu khi mở addon** trong tab Cài đặt.
- Khi bật tùy chọn này, mở Web UI sẽ vào thẳng dashboard. Chỉ nên dùng khi addon chạy qua Home Assistant Ingress hoặc mạng tin cậy.

## Cập nhật 1.8.1 — Tối ưu thao tác vuốt trên điện thoại

- Tăng khoảng vuốt tối thiểu để tránh chạm nhẹ làm chuyển tab ngoài ý muốn.
- Chỉ chuyển tab khi cử chỉ vuốt ngang đủ rõ và có chủ ý.
- Tự hủy nhận diện swipe khi người dùng đang cuộn dọc.
- Không nhận swipe trên nút, liên kết, ô nhập, biểu đồ, bảng cuộn và vùng chọn nội dung.
- Bỏ qua cử chỉ bắt đầu sát mép màn hình để không xung đột thao tác quay lại của điện thoại.

## Cập nhật 1.8.2 — Test nhanh và Codex Vision

- Loại bỏ hoàn toàn giao diện Quota Tracker Codex để dashboard gọn hơn.
- Chat test tự chọn Proxy Key đang hoạt động, không cần dán token thủ công.
- Đăng nhập Codex thành công sẽ tự bật nguồn `codex-auto`.
- Request có ảnh được chuyển sang input Vision của Codex app-server.
- Codex tự ưu tiên model có `inputModalities` hỗ trợ ảnh; danh sách model hiển thị nhãn **Vision**.

## Cập nhật 1.9.0 — Bolt Token Saver

Dashboard có thêm khối **⚡ Bolt Token Saver** với bốn module độc lập:

- **RTK:** tự nhận dạng và nén các `tool`/`tool_result` dạng `git diff`, `git status`, `grep`, `find`, `ls`, `tree`, log và output build. Nếu bộ lọc lỗi hoặc kết quả không nhỏ hơn, Router giữ nguyên output ban đầu.
- **Headroom:** gửi `{messages, model}` tới endpoint `/v1/compress` trước khi chọn provider. Nếu Headroom không chạy, timeout hoặc trả dữ liệu sai, Router fail-open và tiếp tục bằng context gốc.
- **Caveman:** chèn system prompt trả lời ngắn theo mức Lite/Full/Ultra. Code, command, đường dẫn, URL, lỗi và cảnh báo an toàn vẫn phải giữ rõ ràng.
- **Ponytail:** hướng model làm code tối thiểu theo YAGNI, ưu tiên xóa/reuse/stdlib/native trước khi thêm abstraction hoặc dependency.

Các tùy chọn mặc định không tự bật master Token Saver để giữ tương thích với cấu hình cũ. Khi bật master, RTK được chọn mặc định; Headroom, Caveman và Ponytail bật riêng theo nhu cầu.

### Chạy Headroom riêng

Headroom là dịch vụ tùy chọn. Có thể chạy trong container/máy khác rồi nhập URL tại dashboard:

```bash
pip install "headroom-ai[proxy,code,ml]"
headroom proxy --port 8787
```

Ví dụ URL: `http://headroom:8787`. Nút **Kiểm tra** sẽ gọi `/health` để hiển thị trạng thái. Không nên cài trực tiếp thủ công vào container Add-on vì thay đổi sẽ mất khi rebuild/update image.

### Bỏ qua theo từng request

Gửi header sau để không áp dụng Token Saver cho một request cụ thể:

```http
X-AI-Proxy-Token-Saver: off
```

Response thành công có các header `X-AI-Proxy-Token-Saver`, `X-AI-Proxy-Input-Chars-Saved` và `X-AI-Proxy-Estimated-Tokens-Saved`. Dashboard lưu tổng request, ký tự context giảm, token input ước tính, số lần RTK/Headroom/Caveman/Ponytail hoạt động và lỗi Headroom gần nhất.

## Cập nhật 1.10.0 — Giao diện song ngữ Việt/Anh

- Thêm lựa chọn **Tiếng Việt / English** ở khu vực đầu giao diện, dùng được ngay khi mở dashboard.
- Dashboard cũng có bộ chọn ngôn ngữ trên thanh điều hướng để đổi lại bất cứ lúc nào.
- Nếu chưa từng chọn, trình duyệt có ngôn ngữ `vi` sẽ dùng tiếng Việt; các ngôn ngữ khác mặc định dùng English.
- Lựa chọn được lưu trong `localStorage` của trình duyệt và tiếp tục được dùng sau khi tải lại trang.
- Dịch các tab, form, placeholder, tooltip, trạng thái Codex, Token Saver, bảng nguồn, test chat, Telegram, backup, diagnostics, toast và hộp xác nhận.
- Nội dung tạo động sau khi gọi API được dịch bằng `MutationObserver`; nội dung AI trả lời, code, command, URL và dữ liệu trong khối `pre/code` không bị tự động dịch.
- Script i18n được phục vụ nội bộ qua `/ui-i18n.js`, tương thích Home Assistant Ingress và không phụ thuộc dịch vụ dịch bên ngoài.

## Cập nhật 1.10.1 — Tài liệu hướng dẫn song ngữ

- Thêm `README.md` hướng dẫn đầy đủ bằng Tiếng Việt và English.
- Bổ sung hướng dẫn cài đặt, đăng nhập, chọn ngôn ngữ, thêm provider, tạo Proxy Key và kết nối API tương thích OpenAI.
- Bổ sung ví dụ Text/Vision, Codex OAuth/Vision, Bolt Token Saver, backup/restore, xử lý sự cố và lưu ý bảo mật.
- Thêm phần English Guide ngay trong `DOCS.md` để người dùng nước ngoài đọc được từ trang tài liệu của Home Assistant.

## Cập nhật 1.10.2 — Sửa treo khi đổi ngôn ngữ

- Sửa vòng lặp `MutationObserver` do ghi lại `nodeValue` dù nội dung dịch không thay đổi.
- Chỉ cập nhật text và thuộc tính khi giá trị mới thực sự khác giá trị hiện tại.
- Tạm ngắt observer khi dịch toàn trang rồi bật lại sau khi hoàn tất, tránh observer tự bắt chính thay đổi của nó.
- Giảm tải CPU khi đổi Tiếng Việt/English, đặc biệt khi mở dashboard qua Home Assistant Ingress trên điện thoại.

## Cập nhật 1.11.0 — Mở thẳng dashboard

- Bỏ hoàn toàn màn hình đăng nhập, tài khoản, mật khẩu và session nội bộ của add-on.
- Khi mở Web UI, người dùng vào thẳng dashboard; không còn nút đăng xuất hoặc form đổi tài khoản.
- Giữ Proxy Key cho các client API; đây vẫn là lớp xác thực riêng của endpoint `/v1/chat/completions`.
- Xóa dữ liệu tài khoản cũ khỏi cấu hình runtime và bỏ qua trường legacy khi restore backup.
- Khuyến nghị chỉ expose dashboard qua Home Assistant Ingress hoặc mạng nội bộ tin cậy.

## Cập nhật 1.12.0 — Ingress-only Dashboard

- Dashboard `/`, script giao diện và toàn bộ API quản trị `/api/*` chỉ chấp nhận request qua Home Assistant Ingress.
- Kiểm tra đồng thời `X-Ingress-Path` và địa chỉ gateway Supervisor để request LAN giả header không vượt qua được.
- Truy cập trực tiếp `IP_HOME_ASSISTANT:1236/` trả hướng dẫn mở addon từ sidebar thay vì hiển thị dashboard.
- Port `1236` mặc định không publish; người dùng chủ động bật trong mục Network nếu cần API cho client LAN.
- `/health` vẫn hoạt động cho watchdog; `/v1/models` và `/v1/chat/completions` đều yêu cầu Proxy Key.
- Thêm `watchdog`, mô tả port, `panel_admin`, `boot`, `startup` và `stage` vào cấu hình add-on.

## Cập nhật 1.12.1 — Base URL hiện IP HASS

- Thẻ **📡 Base URL Connect** lấy IP Home Assistant thực tế từ Supervisor và hiển thị ngay khi render dashboard.
- Tách rõ ba dòng: IP HASS, Base URL `/v1` và endpoint LLM Vision `/v1/chat/completions`.
- Mỗi dòng có nút copy một chạm, hỗ trợ clipboard chuẩn và fallback cho WebView/HTTP.
- Bỏ placeholder `IP Hass` và cách ghép URL theo hostname trình duyệt dễ sai khi chạy qua Ingress.

## Cập nhật 1.13.0 — Streaming SSE + Responses API

- `/v1/chat/completions` hỗ trợ SSE khi request gửi `"stream": true`; mặc định vẫn trả JSON để không phá client cũ.
- Thêm `/v1/responses` cho `input` dạng chuỗi, message/content arrays, `input_text`, `input_image`, URL ảnh và `data:image/...` URI.
- Responses streaming phát các event chính: `response.created`, `response.output_text.delta`, `response.output_text.done` và `response.completed`.
- Token Saver được áp dụng trước routing cho cả Chat Completions và Responses, đồng thời giữ nguyên dữ liệu Vision.
- Router có thể retry/chuyển nguồn trước event SSE đầu tiên. Sau khi stream bắt đầu, lỗi được gửi trong stream hiện tại và không ghép nội dung từ provider khác.
- Codex OAuth giữ Vision và dùng SSE tổng hợp từ câu trả lời hoàn chỉnh khi app-server không cung cấp token stream ổn định.
- Thẻ **📡 Base URL Connect** có thêm dòng `/v1/responses` với nút copy một chạm.

## Cập nhật 1.14.0 — Tool Calling + Structured Output

- `/v1/chat/completions` và `/v1/responses` hỗ trợ function tools, `tool_choice` và `parallel_tool_calls`.
- Responses nhận tool định dạng phẳng, `function_call`, `function_call_output` và phát event arguments khi streaming.
- Structured Output hỗ trợ JSON Object/JSON Schema; output sai JSON/schema sẽ bị loại và Router thử nguồn tương thích tiếp theo.
- Router tự bỏ qua provider không hỗ trợ tools/JSON Schema. Có thể đặt `supports_tools` hoặc `supports_json_schema` trên nguồn để override khả năng tương thích.
- Dashboard có ba chế độ test: Chat/Vision, Tool Calling và JSON Schema; test tự dùng Proxy Key đang hoạt động.
- Tool arguments chỉ được trả cho client, không ghi vào request log/CSV/test history. Client phải tự xác thực, cấp quyền và thực thi function.
- Hosted web/file/computer tools bị từ chối. Codex OAuth không được chọn cho request tools/JSON Schema và không bao giờ thực thi tools.

## Version 1.10.2 — Language switch freeze fix

- Fixed a `MutationObserver` loop caused by rewriting unchanged text nodes.
- Text and attributes are now updated only when the translated value is different.
- The observer is temporarily disconnected during a full-page language update and safely reconnected afterward.
- Reduced CPU load when switching Vietnamese/English, especially in Home Assistant Ingress on mobile devices.

## Version 1.11.0 — Direct dashboard access

- Removed the add-on's internal login screen, username, password, and session layer.
- The Web UI now opens directly on the dashboard; logout and account-change controls are gone.
- Proxy Keys remain required for client API calls to `/v1/chat/completions`.
- Legacy account data is removed from runtime configuration and ignored during backup restore.
- Expose the dashboard only through Home Assistant Ingress or a trusted local network.

## Version 1.12.0 — Ingress-only Dashboard

- Restricted `/`, UI assets, and all `/api/*` administration endpoints to Home Assistant Ingress.
- Validates both `X-Ingress-Path` and the Supervisor ingress gateway address to reject spoofed LAN requests.
- Direct `HOME_ASSISTANT_IP:1236/` access returns instructions instead of the dashboard.
- Port `1236` is not published by default and can be enabled manually for LAN API clients.
- `/health` remains available for the watchdog; `/v1/models` and `/v1/chat/completions` both require a Proxy Key.
- Added watchdog, port description, `panel_admin`, boot/startup, and release-stage metadata.

## Version 1.12.1 — Home Assistant IP in Base URL

- The **📡 Base URL Connect** card now displays the actual Home Assistant IP obtained from Supervisor data.
- Shows separate Home Assistant IP, `/v1` Base URL, and `/v1/chat/completions` LLM Vision endpoint rows.
- Each row provides one-click copying with clipboard and WebView/HTTP fallback support.
- Removed the `IP Hass` placeholder and browser-hostname URL construction that could be incorrect through Ingress.

## Version 1.13.0 — Streaming SSE + Responses API

- `/v1/chat/completions` supports opt-in SSE with `"stream": true`; existing requests remain non-streaming JSON by default.
- Added `/v1/responses` with string input, message/content arrays, `input_text`, `input_image`, image URLs, and `data:image/...` URIs.
- Responses streaming emits core events including `response.created`, `response.output_text.delta`, `response.output_text.done`, and `response.completed`.
- Token Saver runs before routing for both APIs while preserving Vision content.
- Retry/failover is available before the first SSE event. Once streaming starts, errors stay in the current stream and output from different providers is never merged.
- Codex OAuth keeps Vision support and synthesizes SSE chunks from the completed answer when stable token-level app-server streaming is unavailable.
- The **📡 Base URL Connect** card adds a one-click `/v1/responses` endpoint row.

## Version 1.14.0 — Tool Calling + Structured Output

- `/v1/chat/completions` and `/v1/responses` support function tools, `tool_choice`, and `parallel_tool_calls`.
- Responses accepts flat function definitions, `function_call`, `function_call_output`, and streamed argument events.
- JSON Object/JSON Schema structured output is validated; invalid JSON/schema output triggers fallback to the next compatible source.
- Providers without tools/JSON Schema support are skipped automatically. Per-source `supports_tools` and `supports_json_schema` overrides are supported.
- The dashboard adds Chat/Vision, Tool Calling, and JSON Schema test modes and automatically uses an active Proxy Key.
- Tool arguments are returned to the client but excluded from request logs, CSV exports, and test history. The client must validate, authorize, and execute functions safely.
- Hosted web/file/computer tools are rejected. Codex OAuth is excluded from tools/JSON Schema requests and never executes tools.

---

## English Guide

### Overview

AI Proxy Router combines multiple AI providers behind one OpenAI-compatible API. It rotates API keys, automatically fails over when a source is unavailable, supports Text/Vision routing, and provides separate Proxy Keys for client applications.

Main features:

- OpenAI-compatible `/v1/models`, `/v1/chat/completions`, and `/v1/responses` endpoints.
- Function tools, streamed tool-call arguments, and `function_call_output` follow-ups.
- JSON Object/JSON Schema structured output with validation and compatible-provider fallback.
- Automatic routing through the `auto-ai` model.
- Built-in providers, OpenAI-compatible Custom Endpoints, and OpenAI Codex OAuth.
- Text and Vision support, including Codex Vision.
- Bolt Token Saver with RTK, Headroom, Caveman, and Ponytail.
- Per-client budgets, rate limits, expiration dates, statistics, provider checks, Telegram alerts, backup/restore, and masked diagnostics.
- Vietnamese/English dashboard with a language selector on the navigation bar.

### Installation

1. Extract the `ai_proxy_router` folder into the Home Assistant local add-ons directory, usually `/addons/ai_proxy_router`.
2. Open **Settings → Add-ons → Add-on Store**.
3. Use **Check for updates** from the top-right menu or reload the page.
4. Select **AI Proxy Router**, click **Install**, then **Start**.
5. Open the **Web UI** and optionally enable **Show in sidebar**.

Supported add-on architectures are `amd64` and `aarch64`.

### Direct dashboard access and language

- The add-on opens the dashboard directly; there is no built-in login screen, username, or password.
- Select **Tiếng Việt** or **English** from the navigation bar.
- Vietnamese browsers default to Vietnamese; other browser languages default to English on first use.
- The language is stored in the browser and can be changed again from the dashboard navigation bar.

The Web UI and administration endpoints are available only through Home Assistant Ingress. Proxy Keys remain required for client API calls.

### Add an AI source

1. Open **API Sources**.
2. Select a built-in provider or **Custom Endpoint**.
3. Enter the upstream provider API key.
4. For a Custom Endpoint, enter a name and an OpenAI-compatible Base URL such as `https://api.example.com/v1`.
5. Click **Load Models**, select a model, and optionally set a budget.
6. Save the source and use `▲`/`▼` to change priority.

When the requested model is `auto-ai`, the router selects a healthy source and tries fallback sources after quota, authentication, rate-limit, or network failures.

### Create a Proxy Key

Create one Proxy Key per application instead of sharing upstream API keys:

1. Open **Proxy Key Management**.
2. Enter the client name and optional budget, rate limit, tag, or expiration date.
3. Create and copy the generated `sk-proxy-...` key.
4. Use the dashboard to disable, reveal, regenerate, or delete the key.

Client configuration:

| Field | Value |
|---|---|
| Base URL | `http://HOME_ASSISTANT_IP:1236/v1` |
| API Key | `sk-proxy-YOUR_KEY` |
| Model | `auto-ai` or a saved model name |

Port `1236` is disabled by default. Enable the `1236/tcp` mapping in the add-on Network settings before using this Base URL. Do not use the Home Assistant Ingress URL as an external API Base URL.

### Dashboard test

The test tab does not require a manually entered token. It automatically uses an enabled, valid Proxy Key. Create at least one Proxy Key before testing. Choose **Chat / Vision**, **Tool Calling**, or **JSON Schema**. Tool mode displays generated arguments without executing the function; JSON mode validates structured output and provider failover.

### API examples

Text request:

```bash
curl "http://HOME_ASSISTANT_IP:1236/v1/chat/completions" \
  -H "Authorization: Bearer sk-proxy-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "auto-ai",
    "messages": [{"role": "user", "content": "Summarize the home status."}]
  }'
```

Vision request:

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

Images may use an `http(s)` URL or a `data:image/...` URI. Add `"stream": true` to Chat Completions for SSE.

Streaming chat:

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
  -d '{"model":"auto-ai","input":"Summarize the home status."}'
```

Function tool:

```json
{
  "model": "auto-ai",
  "messages": [{"role": "user", "content": "Check the kitchen"}],
  "tools": [{
    "type": "function",
    "function": {
      "name": "get_home_status",
      "parameters": {
        "type": "object",
        "properties": {"room": {"type": "string"}},
        "required": ["room"],
        "additionalProperties": false
      }
    }
  }],
  "tool_choice": "required",
  "parallel_tool_calls": false
}
```

Responses uses flat function definitions and accepts `function_call_output` items with the matching `call_id`. Structured output uses `text.format.type=json_schema` or Chat Completions `response_format`. Responses tool streams emit `response.output_item.added`, `response.function_call_arguments.delta`, `response.function_call_arguments.done`, `response.output_item.done`, and `response.completed`.

The client is responsible for validating and authorizing tool arguments before execution. Hosted web/file/computer tools are rejected, arguments are excluded from logs, and Codex OAuth never executes tools.

Set `"stream": true` on the Responses request to receive events such as `response.output_text.delta` and `response.completed`. Failover is available before the first SSE event; after streaming starts, errors remain in the current stream. Codex OAuth synthesizes SSE chunks from its completed answer when token-level streaming is unavailable.

### OpenAI Codex OAuth and Vision

1. Open **OpenAI Codex OAuth** on the dashboard.
2. Click **Sign in to Codex**.
3. Copy the device code and open the displayed verification link.
4. Sign in to your ChatGPT/OpenAI account and confirm the code.
5. Return to the dashboard. The status updates automatically and `codex-auto` is enabled.
6. Keep `codex-auto` for automatic Text/Vision selection, or load and select a specific model.

Codex credentials are stored by the Codex CLI in persistent `/data/codex` storage. AI Proxy Router does not expose the access token or include the Codex token in router backups. Vision accepts `image_url` and `input_image` message parts.

### Bolt Token Saver

Enable the main **Bolt Token Saver** switch and then configure the required modules:

- **RTK:** compresses long `git`, `grep`, `ls`, `tree`, logs, and build output before sending it to the model.
- **Headroom:** calls a separate `/v1/compress` service before routing. Errors and timeouts fail open to the original context.
- **Caveman:** adds a terse Lite/Full/Ultra response instruction while preserving code, commands, paths, errors, and safety warnings.
- **Ponytail:** biases coding answers toward YAGNI, deletion, reuse, standard-library, and native solutions.

RTK is selected by default at the module level but only runs after the main Token Saver switch is enabled. Headroom, Caveman, and Ponytail are optional.

Bypass Token Saver for one request:

```http
X-AI-Proxy-Token-Saver: off
```

Headroom must run as a separate service that exposes `/v1/compress`. Enter its URL on the dashboard and test the connection before enabling it.

### Backup and restore

- **Download Backup** exports the complete JSON configuration.
- **Restore Backup** validates and imports a backup file.
- A safety backup is created automatically before restoration.
- Masked preview and debug bundle output can be used for diagnostics without exposing API keys.

A full backup contains upstream API keys, Proxy Keys, and sensitive settings. Store it securely and never publish it.

### Troubleshooting

- **Dashboard unavailable:** open it through **Open Web UI** or the Home Assistant sidebar; direct `IP:1236` dashboard access is blocked.
- **LAN API unavailable:** publish container port `1236/tcp` in the add-on Network settings.
- **401:** verify `Authorization: Bearer sk-proxy-...` and confirm the key still exists.
- **402/403/429:** check key status, expiration, budget, and rate limit.
- **No suitable source:** enable a valid source and choose a Vision-capable model for image requests.
- **Custom Endpoint failure:** use an OpenAI-compatible Base URL, usually ending in `/v1`.
- **Codex OAuth failure:** sign out, start a new device login, and inspect add-on logs.
- **Headroom offline:** verify the separate service URL and port.
- **Dashboard test failure:** create at least one enabled Proxy Key; the test no longer accepts a manual token.
- **Language does not change:** reload the page and allow browser `localStorage`.

### Security

- The dashboard and administration APIs are restricted to Home Assistant Ingress.
- Port `1236` is disabled by default; if enabled, use it only for Proxy Key-protected `/v1/*` requests and do not expose it directly to the Internet.
- Use a separate Proxy Key with budgets/rate limits for each client.
- Regenerate any Proxy Key that may have leaked.
- Treat full backup files as secrets.

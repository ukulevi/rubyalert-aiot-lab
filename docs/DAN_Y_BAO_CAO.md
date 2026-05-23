# DÀN Ý BÁO CÁO ĐỒ ÁN ĐA NGÀNH
## HỆ THỐNG GIÁM SÁT MÔI TRƯỜNG PHÒNG THÍ NGHIỆM THÔNG MINH TÍCH HỢP AI
### (RubyAlert: AIoT Alarm System)

---

## CHƯƠNG 1: TỔNG QUAN ĐỀ TÀI (~3 trang)

### 1.1. Lý do chọn đề tài
- Thực trạng an toàn phòng thí nghiệm tại Việt Nam (rò rỉ khí gas, cháy nổ, thiếu hệ thống giám sát tự động).
- Xu hướng AIoT (Artificial Intelligence of Things): Kết hợp AI vào IoT để tạo hệ thống thông minh, tự trị.
- Nhu cầu thực tế: Giám sát từ xa qua điện thoại, nhận cảnh báo tức thì, điều khiển thiết bị bằng ngôn ngữ tự nhiên.

### 1.2. Mục tiêu đề tài
1. Xây dựng hệ thống IoT thu thập dữ liệu môi trường thời gian thực (Nhiệt độ, Độ ẩm, Khí Gas).
2. Phát triển Dashboard giám sát trực quan, responsive trên cả PC và Mobile.
3. Tích hợp cảnh báo thông minh qua Telegram Bot với khả năng điều khiển thiết bị hai chiều (Bidirectional Control).
4. **Tích hợp AI (Google Gemini)** để nâng cấp hệ thống lên 3 cấp độ: Trợ lý → Hành động → Tự trị.

### 1.3. Phạm vi và giới hạn
- Phạm vi: 1 phòng Lab, 3 loại cảm biến (DHT22, MQ-2), 1 thiết bị điều khiển (Quạt thông gió).
- Giới hạn: Sử dụng MQTT Broker công cộng (broker.emqx.io), MQ-2 là cảm biến bán định lượng.

### 1.4. Ý nghĩa khoa học và thực tiễn
- Khoa học: Đề xuất mô hình AIoT 3 cấp độ cho ứng dụng an toàn phòng Lab.
- Thực tiễn: Hệ thống có thể triển khai chi phí thấp, dễ mở rộng.

---

## CHƯƠNG 2: CƠ SỞ LÝ THUYẾT (~6 trang)

### 2.1. Internet of Things (IoT)
- Khái niệm, kiến trúc phân tầng (Perception → Network → Application).
- So sánh giao thức truyền thông: **MQTT** vs HTTP vs CoAP (lý do chọn MQTT: nhẹ, real-time, publish/subscribe).

### 2.2. Giao thức MQTT
- Mô hình Publish/Subscribe, khái niệm Broker, Topic, QoS.
- Topic thiết kế cho hệ thống: `rubyalert/lab_1/telemetry` (JSON), `rubyalert/lab_1/fan` (Control).

### 2.3. Vi điều khiển ESP32
- Đặc điểm: Dual-core, tích hợp Wi-Fi/Bluetooth, GPIO đa năng, ADC 12-bit.
- So sánh ESP32 vs Arduino Uno (lý do chọn ESP32: tích hợp sẵn Wi-Fi, xử lý nhanh hơn, giá tương đương).

### 2.4. Cảm biến sử dụng
| Cảm biến | Chức năng | Thông số kỹ thuật |
|---|---|---|
| **DHT22** | Đo nhiệt độ & độ ẩm | Sai số: ±0.5°C, ±2-5% RH |
| **MQ-2** | Phát hiện khí gas/khói | Phát hiện: LPG, CO, Methane. Ngõ ra: Analog (0-4095) |

### 2.5. Trí tuệ nhân tạo trong IoT (AIoT)
- Khái niệm AIoT: Sự hội tụ của AI và IoT.
- **Generative AI (Google Gemini):** Mô hình ngôn ngữ lớn (LLM), khả năng hiểu ngữ cảnh và ra quyết định.
- **Function Calling (Gọi hàm):** Cơ chế cho phép AI thực thi hành động thực tế (bật/tắt thiết bị) thay vì chỉ trả lời văn bản.
- **3 cấp độ AI trong IoT** (đề xuất của đề tài):
  - Cấp 1: **AI Thụ động (Reactive)** — Trả lời câu hỏi khi được yêu cầu.
  - Cấp 2: **AI Hành động (Agentic)** — Hiểu ý định người dùng bằng ngôn ngữ tự nhiên và thực thi lệnh điều khiển.
  - Cấp 3: **AI Tự trị (Autonomous)** — Chủ động phân tích dữ liệu, phát hiện rủi ro sớm và tự ra quyết định can thiệp.

### 2.6. Telegram Bot API
- Cơ chế Long Polling, gửi/nhận tin nhắn, xử lý lệnh (Command Handling).

---

## CHƯƠNG 3: THIẾT KẾ HỆ THỐNG (~10 trang)

### 3.1. Kiến trúc tổng quan (Block Diagram)

```
┌──────────────┐    MQTT (JSON)    ┌──────────────────────┐
│   ESP32 +    │ ──────────────►   │   Backend Python     │
│   DHT22      │   broker.emqx.io  │   (smart_lab_system) │
│   MQ-2       │ ◄──────────────   │                      │
│   Relay+Quạt │   Lệnh Fan 0/1   │  ┌────────────────┐  │
└──────────────┘                   │  │ AIoT Logic     │  │
                                   │  │ (Rule Engine)  │  │
                                   │  └────────────────┘  │
                                   │  ┌────────────────┐  │
                                   │  │ Gemini AI      │  │
                                   │  │ (Function Call) │  │
                                   │  └────────────────┘  │
                                   │  ┌────────────────┐  │
                                   │  │ Telegram Bot   │  │
                                   │  │ (Bidirectional)│  │
                                   │  └────────────────┘  │
                                   └──────────────────────┘
                                            │
                                   MQTT (WSS:8084)
                                            │
                                   ┌──────────────────────┐
                                   │   Web Dashboard      │
                                   │   (Single-file HTML) │
                                   │   Responsive PC/Mobile│
                                   └──────────────────────┘
```

### 3.2. Thiết kế phần cứng
- Sơ đồ nguyên lý đấu nối (Fritzing/Draw.io).
- Bảng kết nối chân:

| Cảm biến/Thiết bị | Chân cảm biến | Chân ESP32 |
|---|---|---|
| DHT22 - DATA | Pin 2 | GPIO 0 (D3) |
| MQ-2 - Analog Out | A0 | GPIO 1 (ADC) |
| Relay - Signal | IN | GPIO 2 |
| Quạt DC | +/- | Relay NO/GND |

### 3.3. Thiết kế phần mềm

#### 3.3.1. Firmware ESP32 (`main_esp32.py`)
- Ngôn ngữ: MicroPython.
- Chức năng: Đọc cảm biến → Đóng gói JSON → Publish MQTT → Nhận lệnh điều khiển quạt (Subscribe).
- Định dạng dữ liệu gửi đi:
```json
{
  "temperature": 28.5,
  "humidity": 65.0,
  "gas": 850
}
```

#### 3.3.2. Backend thông minh (`smart_lab_system.py`)
- Ngôn ngữ: Python 3.
- Thư viện: `paho-mqtt`, `requests`, `google-genai`.
- Các module chính:

| Module | Chức năng |
|---|---|
| **MQTT Handler** | Kết nối Broker, nhận/gửi dữ liệu cảm biến và lệnh điều khiển |
| **AIoT Logic Engine** | Xử lý ngưỡng, phát hiện đột biến, điều khiển tự động |
| **Gemini AI Module** | Chat thông minh, Function Calling, AI tự trị |
| **Telegram Bot** | Long Polling, xử lý lệnh, gửi cảnh báo |

#### 3.3.3. Thuật toán AIoT thông minh (Flowchart)

**a) Rate of Change Detection (Phát hiện tăng đột biến):**
- So sánh giá trị nhiệt độ hiện tại với chu kỳ trước.
- Nếu chênh lệch ≥ 3°C/chu kỳ → Cảnh báo tăng đột biến.

**b) Hysteresis Control (Điều khiển trễ):**
- Ngưỡng BẬT quạt: Nhiệt độ > 35°C.
- Ngưỡng TẮT quạt: Nhiệt độ < 32°C (cách 3°C để tránh bật/tắt liên tục).

**c) Message Aggregation (Gom nhóm cảnh báo):**
- Nếu xảy ra đồng thời nhiều sự kiện (nhiệt độ cao + gas rò rỉ), hệ thống gom thành **1 tin nhắn duy nhất** thay vì spam nhiều tin riêng lẻ.
- Cơ chế Cooldown: Tối đa 1 tin nhắn Telegram mỗi 60 giây.

**d) AI Autonomous Intervention (AI Tự động can thiệp sớm — Cấp độ 3):**
- Ngưỡng kích hoạt: Khí gas > 60% ngưỡng nguy hiểm (tức > 1200 ppm khi ngưỡng đỏ là 2000 ppm).
- Khi đạt ngưỡng phòng ngừa, AI Gemini được kích hoạt để phân tích tình huống và tự động bật quạt.
- Cơ chế Cooldown cho AI: Tối đa 1 lần phân tích mỗi 5 phút (300 giây). Nếu đang trong thời gian hồi chiêu, hệ thống Local tự xử lý (không tốn Token AI).

**e) Sensor Fault Detection & Hardware-Safe Logic (Phát hiện lỗi cảm biến):**
- Hệ thống có khả năng tự động nhận diện cảm biến bị lỗi hoặc đứt kết nối (Ví dụ: DHT22 trả về giá trị 0.0 hoặc không có dữ liệu).
- Khi phát hiện lỗi, hệ thống lập tức vô hiệu hóa các quy tắc tự động hóa liên quan đến cảm biến đó để tránh lỗi điều khiển sai (Hardware-Safe), đồng thời gửi cảnh báo SOS qua Telegram cho quản trị viên.

**f) Manual Override (Bảo vệ quyền điều khiển thủ công):**
- Cờ `manual_override` được thiết kế để giải quyết xung đột giữa điều khiển thủ công và tự động hóa. 
- Khi người dùng chủ động điều khiển quạt (qua Dashboard/Telegram), hệ thống sẽ tạm ngưng các logic can thiệp tự động để tôn trọng quyết định của con người.

#### 3.3.4. Tích hợp AI (Google Gemini)

**Kiến trúc 3 cấp độ AI:**

| Cấp độ | Tên gọi | Mô tả | Ví dụ |
|---|---|---|---|
| **1** | Reactive (Thụ động) | AI trả lời câu hỏi về dữ liệu Lab | Hỏi: "Khí gas bao nhiêu?" → AI: "Gas hiện tại 614 ppm, an toàn." |
| **2** | Agentic (Hành động) | AI hiểu ý định & thực thi lệnh qua Function Calling | Hỏi: "Nóng quá, bật quạt đi" → AI gọi `set_fan_state("ON")` → Quạt bật |
| **3** | Autonomous (Tự trị) | AI tự phát hiện rủi ro sớm & tự can thiệp | Gas = 1300 ppm → AI tự phân tích → Tự bật quạt → Gửi tin giải thích |

**Chiến lược tối ưu Token:**

| Chiến lược | Mô tả | Hiệu quả |
|---|---|---|
| **Hybrid Processing** | Xử lý từ khóa phổ biến ("bật quạt", "trạng thái") tại Local, không gọi AI | Tiết kiệm ~70% lượt gọi API |
| **Compact Prompt** | Nén System Instruction từ ~200 chữ xuống ~40 chữ | Giảm ~60% Input Token mỗi lần gọi |
| **Max Output Tokens** | Giới hạn AI trả lời tối đa 150 token | Tránh phản hồi dài dòng |
| **AI Cooldown** | AI tự trị chỉ kích hoạt 1 lần/5 phút, phần còn lại Local xử lý | Giảm chi phí khi chạy 24/7 |
| **Fallback 429** | Nếu AI bị quá tải (Rate Limit), hệ thống tự trả về dữ liệu thô | Đảm bảo không bị gián đoạn |

**Bộ lọc phạm vi (Scope Filter):**
- System Instruction ép AI chỉ trả lời về an toàn phòng Lab, thiết bị, và tình huống khẩn cấp.
- Nếu người dùng hỏi ngoài lề (nấu ăn, giải trí...), AI lịch sự từ chối.

#### 3.3.5. Web Dashboard (`dashboard.html`)
- Kiến trúc: Single-file HTML (bao gồm cả CSS + JS).
- Công nghệ: Tailwind CSS, Chart.js, MQTT.js (WebSocket), Lucide Icons.
- Phong cách thiết kế: **Editorial Minimalist** (tối giản, tập trung vào dữ liệu).
- Kết nối MQTT: WebSocket Secure (WSS) qua cổng 8084.
- Responsive: Hỗ trợ đồng thời PC và Mobile.
- Tính năng:
  - Hiển thị thời gian thực: Nhiệt độ, Độ ẩm, Gas, Trạng thái quạt.
  - Biểu đồ lịch sử (Live Telemetry History) — tối đa 30 điểm dữ liệu gần nhất.
  - Điều khiển quạt trực tiếp trên Dashboard (Toggle Switch).
  - Cảnh báo trực quan: Card chuyển viền đỏ + nền hồng khi vượt ngưỡng.
  - Đồng bộ thời gian thực (Last Sync) giữa các thiết bị theo dõi.

#### 3.3.6. Telegram Bot (Bidirectional Control)
- Các lệnh hỗ trợ:

| Lệnh | Chức năng |
|---|---|
| `/status` | Xem toàn bộ thông số hiện tại |
| `/fan_on` | Bật quạt thông gió |
| `/fan_off` | Tắt quạt thông gió |
| `/report` | AI tổng hợp báo cáo đánh giá an toàn chuyên sâu |
| *"Bật quạt đi"* | AI hiểu ngôn ngữ tự nhiên → thực thi lệnh (Cấp độ 2) |
| *"Phòng có an toàn không?"* | AI phân tích dữ liệu → trả lời có ngữ cảnh (Cấp độ 1) |

### 3.4. Cấu hình hệ thống (`config.py`)
- Quản lý tập trung: API Key, Token, MQTT Server/Topic.
- Dễ dàng chuyển đổi giữa các môi trường (Development/Production).

---

## CHƯƠNG 4: KẾT QUẢ THỰC NGHIỆM (~5 trang)

### 4.1. Môi trường thử nghiệm
- **Chế độ mô phỏng (Simulation Mode):** Dữ liệu ngẫu nhiên trong khoảng thực tế.
- **Phần cứng thật (Hardware Mode):** ESP32 + DHT22 + MQ-2 + Relay + Quạt DC.
- **Đánh giá Baseline (Cơ sở so sánh):** Hệ thống có sử dụng module `lab_analytics_backend.py` đóng vai trò là một hệ thống giám sát IoT truyền thống (không tích hợp AI) để làm cơ sở (baseline) nhằm so sánh và làm nổi bật sức mạnh tự động hóa/trợ lý của module `smart_lab_system.py` có AI.

### 4.2. Kết quả giám sát thời gian thực
- Screenshot Dashboard trên PC (hiển thị 4 card + biểu đồ).
- Screenshot Dashboard trên Mobile (Responsive layout).
- Bảng số liệu thu thập (ít nhất 10 chu kỳ đo).

### 4.3. Kết quả cảnh báo Telegram
- Screenshot tin nhắn cảnh báo khi nhiệt độ vượt ngưỡng.
- Screenshot tin nhắn cảnh báo khi khí gas vượt ngưỡng.
- Screenshot tin nhắn gom nhóm (khi 2 sự kiện xảy ra đồng thời).

### 4.4. Kết quả tích hợp AI (Google Gemini)
- **Cấp độ 1:** Screenshot AI trả lời câu hỏi về dữ liệu phòng Lab.
- **Cấp độ 1 (Scope Filter):** Screenshot AI từ chối câu hỏi ngoài lề.
- **Cấp độ 2:** Screenshot AI hiểu lệnh "Bật quạt đi" bằng ngôn ngữ tự nhiên và thực thi.
- **Cấp độ 3:** Screenshot/Log AI tự động phát hiện Gas cao và chủ động bật quạt phòng ngừa.
- **Lệnh `/report`:** Screenshot AI xuất báo cáo đánh giá an toàn chuyên sâu.

### 4.5. Bảng kiểm thử (Test Cases)

| ID | Tình huống | Hành động | Kết quả mong đợi | Kết quả thực tế | Đạt/Không |
|---|---|---|---|---|---|
| TC01 | Khởi động hệ thống | Chạy `smart_lab_system.py` | Kết nối MQTT thành công | | |
| TC02 | Nhiệt độ > 35°C | Mô phỏng T=38°C | Quạt tự bật + Telegram cảnh báo | | |
| TC03 | Nhiệt độ < 32°C | Mô phỏng T=30°C | Quạt tự tắt (Hysteresis) | | |
| TC04 | Gas > 2000 ppm | Mô phỏng G=2200 | Quạt tự bật + Cảnh báo Gas | | |
| TC05 | Gas > 1200 ppm (60%) | Mô phỏng G=1300 | AI tự trị phân tích + Bật quạt phòng ngừa | | |
| TC06 | Telegram `/status` | Gửi lệnh | Nhận đúng thông số hiện tại | | |
| TC07 | Telegram `/fan_on` | Gửi lệnh | Quạt bật + Dashboard đồng bộ | | |
| TC08 | Telegram "Bật quạt" | Gửi tin nhắn NLP | AI hiểu ý định → Quạt bật | | |
| TC09 | Telegram "Nấu phở thế nào?" | Gửi câu ngoài lề | AI từ chối trả lời | | |
| TC10 | Telegram `/report` | Gửi lệnh | AI xuất báo cáo đánh giá an toàn | | |
| TC11 | Dashboard Toggle Fan | Click nút trên Web | Quạt bật + Telegram/Backend đồng bộ | | |
| TC12 | API bị quá tải (429) | Gửi liên tục nhiều lần | Hệ thống trả dữ liệu thô (Fallback) | | |

---

## CHƯƠNG 5: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN (~2 trang)

### 5.1. Kết luận
- Đã xây dựng thành công hệ thống AIoT giám sát phòng Lab với đầy đủ tính năng:
  - Thu thập dữ liệu thời gian thực qua MQTT.
  - Dashboard trực quan, responsive.
  - Cảnh báo Telegram thông minh (gom nhóm, chống spam).
  - Điều khiển thiết bị hai chiều (Dashboard ↔ Telegram ↔ Backend).
  - **AI 3 cấp độ** (Reactive → Agentic → Autonomous) — Điểm nhấn khác biệt của đề tài.
- Hệ thống hoạt động ổn định trên cả chế độ mô phỏng và phần cứng thật.

### 5.2. Tổng hợp các Điểm sáng (Highlights / Đóng góp chính)
1. **Kiến trúc AIoT 3 cấp độ (Reactive -> Agentic -> Autonomous):** Là điểm nhấn khác biệt lớn nhất của đề tài, biến hệ thống IoT từ việc chỉ hiển thị dữ liệu sang khả năng tự tương tác, tự hiểu ngữ nghĩa điều khiển và tự ra quyết định độc lập.
2. **Cơ chế Fault-Tolerant & Hardware-Safe:** Phát hiện sớm tình trạng hỏng hóc hoặc ngắt kết nối cảm biến (vd: DHT22 trả về 0.0), lập tức vô hiệu hóa AI/Logic bị phụ thuộc để bảo vệ thiết bị phần cứng, đồng thời gửi thông báo SOS.
3. **Quản lý xung đột điều khiển (Manual Override):** Giải quyết bài toán xung đột cơ bản trong tự động hóa, luôn tôn trọng lệnh thao tác thủ công của con người thay vì cứng nhắc theo logic máy móc.
4. **Tích hợp linh hoạt với chi phí thấp:** Xây dựng giải pháp tổng thể (Backend + Mobile/Web Dashboard + Chatbot Telegram) với các thành phần phần cứng chi phí thấp nhưng có độ hoàn thiện ở phần mềm cực kỳ cao.
5. **Chiến lược tối ưu tài nguyên (Token Optimization):** Thiết kế Hybrid Processing, Cooldown, Micro-prompt giúp AI (Gemini) chạy mượt mà 24/7 mà không lo vượt giới hạn API miễn phí.

### 5.3. Tổng hợp các Hạn chế (Limitations)
1. **Sự phụ thuộc vào MQTT Broker công cộng (broker.emqx.io):** Gây ra độ trễ hoặc rủi ro gián đoạn dịch vụ, đồng thời gói tin hiện tại ở dạng bản rõ (Unencrypted JSON) và chưa có mã hóa TLS/SSL, có nguy cơ lộ thông tin nội bộ.
2. **Tính chất bán định lượng của thiết bị đầu cuối:** Cảm biến MQ-2 là cảm biến bán định lượng, có độ nhạy với nhiều loại khí khác nhau thay vì chuyên biệt, nên khó cung cấp giá trị ppm chính xác tuyệt đối mà cần qua quá trình Calibration (hiệu chuẩn) chuyên sâu.
3. **Phụ thuộc kết nối Internet (Wi-Fi local):** Nếu mạng Wi-Fi tại phòng Lab bị rớt, ESP32 sẽ mất kết nối với Backend, hệ thống sẽ rơi vào trạng thái mù (dù có thể bổ sung xử lý Local tại ESP32 nhưng hiện đề tài chủ yếu xử lý tại Server).
4. **Cơ sở dữ liệu (Database):** Hệ thống đang tập trung vào thời gian thực (Real-time telemetry), chưa có database kiên cố (như SQLite/InfluxDB/PostgreSQL) nên bị giới hạn trong việc xuất báo cáo thống kê dài hạn và huấn luyện lại AI từ lịch sử lâu dài.

### 5.4. Hướng phát triển
1. **Bổ sung màn hình OLED** trên ESP32 để hiển thị dữ liệu tại chỗ.
2. **Lưu trữ dữ liệu** vào Database (SQLite/InfluxDB) để phân tích xu hướng dài hạn.
3. **AI dự báo** (Predictive AI): Sử dụng dữ liệu lịch sử để dự đoán ngưỡng nguy hiểm trước khi xảy ra.
4. **Mở rộng quy mô:** Giám sát nhiều phòng Lab đồng thời (Multi-room Monitoring).
5. **Triển khai MQTT Broker riêng** với bảo mật TLS/SSL và xác thực người dùng.

---

## PHỤ LỤC

### A. Cấu trúc thư mục dự án
```
DADN/
├── config.py               # Cấu hình tập trung (API Key, MQTT, Telegram)
├── smart_lab_system.py     # Backend chính (AIoT Logic + Gemini AI + Telegram Bot)
├── esp32_simulator.py      # Trình mô phỏng ESP32 (Chế độ phát triển)
├── main_esp32.py           # Firmware ESP32 (MicroPython — Chế độ phần cứng thật)
├── dashboard.html          # Web Dashboard (Single-file, Responsive)
├── lab_analytics_backend.py # Module phân tích bổ sung (dự phòng)
└── requirements.txt        # Danh sách thư viện Python
```

### B. Danh sách thư viện sử dụng
| Thư viện | Phiên bản | Chức năng |
|---|---|---|
| `paho-mqtt` | 1.6+ | Kết nối MQTT Broker |
| `requests` | 2.31+ | HTTP Client (Telegram API) |
| `google-genai` | 1.x | Google Gemini AI SDK (thế hệ mới) |
| Tailwind CSS | 3.x (CDN) | Styling Dashboard |
| Chart.js | 4.x (CDN) | Biểu đồ trực quan |
| MQTT.js | 5.x (CDN) | Kết nối MQTT qua WebSocket |
| Lucide Icons | Latest (CDN) | Icon cho Dashboard |

### C. Cấu hình MQTT Topics
| Topic | Hướng | Payload | Mô tả |
|---|---|---|---|
| `rubyalert/lab_1/telemetry` | ESP32 → Backend/Dashboard | `{"temperature": T, "humidity": H, "gas": G}` | Dữ liệu cảm biến |
| `rubyalert/lab_1/fan` | Backend/Dashboard → ESP32 | `"1"` (ON) hoặc `"0"` (OFF) | Điều khiển quạt |

### D. Tài liệu tham khảo (gợi ý)
1. Google Gemini API Documentation — https://ai.google.dev/docs
2. Eclipse Paho MQTT Python Client — https://github.com/eclipse/paho.mqtt.python
3. ESP32 MicroPython Reference — https://docs.micropython.org/en/latest/esp32/
4. Chart.js Documentation — https://www.chartjs.org/docs/
5. Telegram Bot API — https://core.telegram.org/bots/api

---

> [!IMPORTANT]
> **Ghi chú cho sinh viên:**
> - Chương 3 (Thiết kế) là chương quan trọng nhất, cần có Block Diagram, Flowchart, và bảng mô tả chi tiết.
> - Chương 4 (Kết quả) cần chụp screenshot thực tế từ Telegram và Dashboard.
> - Phần AI 3 cấp độ (mục 3.3.4) là **điểm nhấn khác biệt** so với các đồ án IoT thông thường — hãy trình bày kỹ phần này.

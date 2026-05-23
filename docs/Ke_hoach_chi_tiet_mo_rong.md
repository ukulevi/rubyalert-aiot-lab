# KẾ HOẠCH CHI TIẾT MỞ RỘNG
## Đồ Án Đa Ngành: Hệ Thống Giám Sát Môi Trường Phòng Lab Thông Minh (IoT)

---

## GIAI ĐOẠN 1: PHẦN CỨNG & FIRMWARE (17/05 – 21/05)

### Ngày 1 – Thứ Bảy 17/05: Mua sắm & Khởi tạo môi trường

**Mục tiêu:** Kit ESP32 nháy LED thành công, môi trường dev sẵn sàng.

#### ✅ Checklist buổi sáng (Mua linh kiện)
- [x] In bảng dự toán ra giấy, mang đi mua tại khu Bắc Hải / Lý Thường Kiệt
- [x] Kiểm tra từng linh kiện ngay tại quầy (xin thử nguồn nếu có thể)
- [x] Mua thêm 2-3 LED + trở 220Ω (rẻ, dùng để test chân GPIO)

#### ✅ Checklist buổi chiều (Cài môi trường)
- [x] Tải Arduino IDE 2.x từ arduino.cc
- [x] Trong Arduino IDE → Preferences → thêm URL Board: `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
- [x] Board Manager → tìm `esp32` by Espressif → cài version 2.x
- [x] Cài driver USB-UART: thử cắm ESP32, nếu không nhận → tải CP210x hoặc CH340
- [x] Cài thư viện: **DHT sensor library** (Adafruit) + **Adafruit Unified Sensor**

#### ✅ Checklist buổi tối (Test kit)
- [x] File → Examples → 01.Basics → Blink → Upload thành công → LED nháy
- [x] Ghi lại cổng COM nhận diện ESP32 (VD: COM3)

---

### Ngày 2 – Thứ Hai 18/05: Đọc dữ liệu cảm biến

**Mục tiêu:** Serial Monitor hiển thị giá trị Nhiệt độ, Độ ẩm, Khói.

#### Sơ đồ đấu nối nhanh
| Cảm biến | Chân cảm biến | Chân ESP32 |
|---|---|---|
| DHT22 | VCC | 3.3V |
| DHT22 | GND | GND |
| DHT22 | DATA | GPIO 4 (+ trở 10kΩ lên 3.3V) |
| MQ-2 | VCC | 5V (chân VIN) |
| MQ-2 | GND | GND |
| MQ-2 | A0 | GPIO 34 (ADC) |
| MQ-2 | D0 | GPIO 35 (Digital) |

> [!WARNING]
> MQ-2 cần **làm nóng (preheat) 60 giây** sau khi cấp nguồn mới cho số liệu ổn định. Thêm `delay(60000)` ở đầu `setup()` lần chạy đầu tiên.

#### Code mẫu cốt lõi
```cpp
#include <DHT.h>
#define DHTPIN 4
#define DHTTYPE DHT22
#define MQ2_PIN 34

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();
  delay(2000);
}

void loop() {
  float temp = dht.readTemperature();
  float humi = dht.readHumidity();
  int gas  = analogRead(MQ2_PIN);
  Serial.printf("Temp: %.1f°C | Humi: %.1f%% | Gas: %d\n", temp, humi, gas);
  delay(2000);
}
```

#### ✅ Checklist
- [x] Đấu nối đúng theo bảng trên
- [x] Giá trị Temp và Humi hợp lý (nhiệt độ phòng ~26-30°C)
- [x] Giá trị Gas thay đổi khi thở gần cảm biến

---

### Ngày 3 – Thứ Ba 19/05: Điều khiển Buzzer & Relay

**Mục tiêu:** Hệ thống tự động bật Còi + Quạt khi vượt ngưỡng.

#### Sơ đồ đấu nối
| Thiết bị | Chân | ESP32 |
|---|---|---|
| Buzzer `+` | — | GPIO 26 |
| Buzzer `-` | — | GND |
| Relay IN | Signal | GPIO 27 |
| Relay | VCC | 5V (VIN) |
| Quạt DC `+` | — | Relay NO |
| Quạt DC `-` | — | GND |

#### Logic cảnh báo
```cpp
#define BUZZER_PIN  26
#define RELAY_PIN   27
#define TEMP_THRESH  35.0
#define GAS_THRESH   2000

void handleAlert(float temp, int gas) {
  bool alert = (temp > TEMP_THRESH) || (gas > GAS_THRESH);
  digitalWrite(BUZZER_PIN, alert ? HIGH : LOW);
  digitalWrite(RELAY_PIN,  alert ? LOW  : HIGH); // Relay Active LOW
}
```

> [!NOTE]
> Module Relay Opto-cách ly thường là **Active LOW** (LOW = bật relay). Kiểm tra nhãn trên module để xác nhận.

#### ✅ Checklist
- [x] Buzzer kêu khi che tay vào MQ-2 hoặc thở mạnh
- [x] Relay click, quạt quay
- [x] Hệ thống tự tắt khi không khí sạch trở lại

---

### Ngày 4 – Thứ Tư 20/05: Kết nối Wi-Fi

**Mục tiêu:** ESP32 kết nối Wi-Fi, in IP ra Serial Monitor.

```cpp
#include <WiFi.h>
const char* ssid     = "TEN_WIFI_CUA_BAN";
const char* password = "MAT_KHAU_WIFI";

void setupWiFi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); Serial.print(".");
  }
  Serial.println("\nIP: " + WiFi.localIP().toString());
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    WiFi.reconnect();
    delay(5000);
  }
}
```

> [!IMPORTANT]
> **Hotspot 4G dự phòng:** Tạo sẵn Hotspot điện thoại với SSID/Pass cố định và lưu vào code. Dùng khi Wifi trường bị chặn Portal.

---

### Ngày 5 – Thứ Năm 21/05: Tối ưu Firmware (Non-blocking)

**Mục tiêu:** Xóa toàn bộ `delay()`, dùng `millis()` để đa nhiệm.

```cpp
unsigned long lastSensorRead = 0;
const long SENSOR_INTERVAL = 2000;

void loop() {
  unsigned long now = millis();
  if (now - lastSensorRead >= SENSOR_INTERVAL) {
    lastSensorRead = now;
    float temp = dht.readTemperature();
    float humi = dht.readHumidity();
    int   gas  = analogRead(MQ2_PIN);
    handleAlert(temp, gas);
    sendToCloud(temp, humi, gas);
  }
  Blynk.run(); // Chạy liên tục không bị block
}
```

---

## GIAI ĐOẠN 2: PHẦN MỀM & KẾT NỐI (22/05 – 25/05)

### Ngày 6 – Thứ Sáu 22/05: Thiết lập Blynk IoT

#### Datastreams cần tạo
| Virtual Pin | Tên | Data Type | Unit |
|---|---|---|---|
| V0 | Nhiệt độ | Double | °C |
| V1 | Độ ẩm | Double | % |
| V2 | Khói (Gas) | Integer | ADC |
| V3 | Trạng thái Alert | Integer | 0/1 |
| V4 | Điều khiển Relay | Integer | 0/1 |

```cpp
#define BLYNK_TEMPLATE_ID   "TMPLxxxxxxxx"
#define BLYNK_AUTH_TOKEN    "xxxxxxxxxxxx"
#include <BlynkSimpleEsp32.h>

void sendToCloud(float temp, float humi, int gas, bool alert) {
  Blynk.virtualWrite(V0, temp);
  Blynk.virtualWrite(V1, humi);
  Blynk.virtualWrite(V2, gas);
  Blynk.virtualWrite(V3, alert ? 1 : 0);
}

BLYNK_WRITE(V4) { // Nhận lệnh điều khiển từ xa
  digitalWrite(RELAY_PIN, param.asInt() == 1 ? LOW : HIGH);
}
```

---

### Ngày 7 – Thứ Bảy 23/05: Thiết kế Dashboard

#### Layout Dashboard gợi ý
```
┌──────────────────────────────────────┐
│  🌡️ Gauge Nhiệt độ  💧 Gauge Độ ẩm  │
├──────────────────────────────────────┤
│  💨 Chart Gas       🚨 LED Cảnh báo  │
├──────────────────────────────────────┤
│  📈 SuperChart Lịch sử (1h/1d/1w)   │
├──────────────────────────────────────┤
│       [Button ON/OFF Quạt - V4]      │
└──────────────────────────────────────┘
```

#### ✅ Checklist
- [ ] Tất cả widget hiển thị đúng dữ liệu thực
- [ ] Button V4 điều khiển được Relay từ xa
- [ ] Chụp screenshot Dashboard để đưa vào báo cáo

---

### Ngày 8 – Chủ Nhật 24/05: Cấu hình Telegram Bot

#### Các bước tạo Bot
1. Tìm `@BotFather` → `/newbot` → đặt tên `LabMonitor_Bot`
2. Lấy `BOT_TOKEN` (dạng `123456789:AAHxxxx...`)
3. Tìm `@userinfobot` → lấy `CHAT_ID`

```cpp
#include <UniversalTelegramBot.h>
#include <WiFiClientSecure.h>

WiFiClientSecure client;
UniversalTelegramBot bot("BOT_TOKEN", client);
bool alertSent = false;

void sendTelegramAlert(float temp, int gas) {
  if (!alertSent) {
    String msg = "🚨 CẢNH BÁO PHÒNG LAB!\n";
    msg += "🌡️ Nhiệt độ: " + String(temp) + "°C\n";
    msg += "💨 Gas: " + String(gas);
    bot.sendMessage("CHAT_ID", msg, "");
    alertSent = true;
  }
}

void clearAlert() {
  if (alertSent) {
    bot.sendMessage("CHAT_ID", "✅ Môi trường đã an toàn!", "");
    alertSent = false;
  }
}
```

> [!NOTE]
> Thêm `client.setInsecure()` vào `setup()` để bỏ qua SSL certificate verification.

---

### Ngày 9 – Thứ Hai 25/05: Kiểm thử End-to-End

#### Bảng Test Cases
| Test Case | Hành động | Kết quả mong đợi |
|---|---|---|
| TC01 | Cắm nguồn ESP32 | Kết nối Wifi trong 15 giây |
| TC02 | Thổi nhẹ vào MQ-2 | Gas ADC tăng trên Dashboard |
| TC03 | Đặt ngón tay vào DHT22 | Nhiệt độ tăng nhẹ |
| TC04 | Bật lửa gần MQ-2 | Còi kêu + Relay bật + Telegram nhận tin |
| TC05 | Đưa bật lửa ra xa | Còi tắt + Relay tắt + Telegram báo an toàn |
| TC06 | Tắt Wi-Fi 30 giây | ESP32 tự reconnect |
| TC07 | Nhấn nút Relay trên Dashboard | Quạt bật/tắt từ xa |

#### ✅ Checklist đóng gói mô hình
- [ ] Cố định breadboard trong hộp nhựa bằng băng keo 2 mặt
- [ ] Đục lỗ cho DHT22 và MQ-2 nhô ra ngoài
- [ ] Dán nhãn tên các cảm biến lên hộp
- [ ] Kiểm tra toàn bộ dây cắm chắc chắn

---

## GIAI ĐOẠN 3: BÁO CÁO & BẢO VỆ (26/05 – 30/05)

### Ngày 10-11 – 26-27/05: Viết Báo cáo

#### Cấu trúc báo cáo đề xuất

| Chương | Nội dung | Số trang |
|---|---|---|
| **Chương 1** | Mở đầu, lý do chọn đề tài, mục tiêu, phạm vi | ~2 trang |
| **Chương 2** | Tổng quan: IoT, ESP32, MQTT vs HTTP, Blynk, Telegram | ~5 trang |
| **Chương 3** | Thiết kế: Block Diagram, sơ đồ đấu nối, Flowchart, Dashboard | ~8 trang |
| **Chương 4** | Kết quả thực nghiệm: bảng số liệu, test cases, ảnh chụp | ~4 trang |
| **Chương 5** | Kết luận, hạn chế, hướng phát triển | ~1 trang |

#### ✅ Checklist nội dung kỹ thuật cần có
- [ ] **Block Diagram** kiến trúc hệ thống (vẽ bằng draw.io)
- [ ] **Sơ đồ đấu nối** Fritzing hoặc ảnh thực tế rõ nét
- [ ] **Flowchart** thuật toán firmware (draw.io)
- [ ] **Bảng kết quả đo** ít nhất 10 lần đo
- [ ] **Screenshot** Dashboard Blynk
- [ ] **Screenshot** tin nhắn Telegram nhận được

---

### Ngày 12 – 28/05: Hoàn chỉnh & Nộp

#### ✅ Checklist trước khi nộp báo cáo
- [ ] Trang bìa đúng mẫu trường (tên đề tài, MSSV, lớp, GVHD)
- [ ] Mục lục tự động (Table of Contents của Word)
- [ ] Font chữ: **Times New Roman 13**, dãn dòng **1.5**
- [ ] Căn lề: Trái 3cm, Phải 2cm, Trên 2.5cm, Dưới 2.5cm
- [ ] Đánh số trang từ Chương 1
- [ ] Tất cả hình có chú thích: *Hình X.Y: Tên hình*
- [ ] Xuất PDF, kiểm tra font không bị lỗi
- [ ] **Gửi email** đến `binh@hcmut.edu.vn`
  - Subject: `[Báo cáo ĐAĐN] MSSV - Tên đề tài`

---

### Ngày 13 – 29/05: Slide thuyết trình (14 slide)

| Slide | Nội dung |
|---|---|
| 1 | Trang bìa |
| 2 | Mục lục |
| 3 | Đặt vấn đề |
| 4 | Mục tiêu & Phạm vi |
| 5 | Kiến trúc hệ thống (Block Diagram) |
| 6 | Linh kiện sử dụng (ảnh thực tế) |
| 7 | Sơ đồ đấu nối phần cứng |
| 8 | Lưu đồ thuật toán phần mềm |
| 9 | **Demo Live** hoặc Video demo |
| 10 | Giao diện Dashboard Blynk |
| 11 | Kết quả cảnh báo Telegram |
| 12 | Bảng kết quả kiểm thử |
| 13 | Kết luận & Hướng phát triển |
| 14 | Cảm ơn & Q&A |

#### Phân bổ 15 phút
- Slide 1-4: **2 phút** (giới thiệu nhanh)
- Slide 5-8: **4 phút** (phần kỹ thuật)
- Slide 9-12: **6 phút** (demo + kết quả — quan trọng nhất)
- Slide 13-14: **3 phút** (kết luận + Q&A buffer)

---

### Ngày 14 – 30/05: Demo & Chấm điểm

#### ✅ Checklist mang theo
- [ ] Laptop đã sạc đầy + dây sạc
- [ ] Mô hình phần cứng đóng gói gọn
- [ ] Cáp Micro-USB dự phòng
- [ ] Điện thoại 4G hotspot sẵn sàng
- [ ] Mở sẵn Blynk Dashboard trên trình duyệt
- [ ] Telegram mở sẵn để thầy thấy thông báo real-time

#### Câu hỏi thầy hay hỏi & gợi ý trả lời
| Câu hỏi | Gợi ý trả lời |
|---|---|
| "Tại sao chọn ESP32 không dùng Arduino Uno?" | ESP32 tích hợp Wi-Fi/BT, xử lý nhanh hơn, giá tương đương |
| "Giao thức truyền thông dùng gì?" | HTTP qua thư viện Blynk, dữ liệu đẩy mỗi 2 giây |
| "Mất mạng thì hệ thống xử lý thế nào?" | Tự reconnect; cảnh báo Buzzer tại chỗ vẫn hoạt động độc lập |
| "Độ chính xác cảm biến?" | DHT22: ±0.5°C, ±2-5%RH. MQ-2 bán định lượng, cần calibration |
| "Hướng phát triển?" | Thêm OLED, lưu DB, AI dự báo ngưỡng nguy hiểm |

---

## PHỤ LỤC: QUẢN TRỊ RỦI RO MỞ RỘNG

| Rủi ro | Xác suất | Phương án dự phòng |
|---|---|---|
| Linh kiện hỏng (DHT22) | Thấp | Mua 2 cái từ đầu (chỉ +45k) |
| Wifi trường bị chặn | Cao | 4G Hotspot điện thoại |
| Blynk server down | Rất thấp | Quay video demo trước làm bằng chứng |
| Code lỗi trước demo | Trung bình | Lưu bản code ổn định lên Google Drive |
| Relay/Buzzer không hoạt động | Thấp | Dùng LED sáng/tắt để minh họa logic |

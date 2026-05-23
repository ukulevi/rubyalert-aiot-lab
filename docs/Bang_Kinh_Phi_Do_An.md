# BẢNG KINH PHÍ CHI TIẾT & DỰ TOÁN ĐỒ ÁN ĐA NGÀNH
## ĐỀ TÀI: HỆ THỐNG GIÁM SÁT MÔI TRƯỜNG VÀ CẢNH BÁO PHÒNG LAB THÔNG MINH (IoT)

> **Lưu ý:** Bảng dự toán kinh phí dưới đây được thiết kế tối ưu cho sinh viên thực hiện đồ án đa ngành. Các thiết bị được lựa chọn dựa trên tiêu chí: **Đúc sẵn, có độ bền cao, dễ dàng lắp đặt nhanh và giá thành hợp lý nhất tại TP.HCM**.

---

### I. BẢNG TỔNG HỢP KINH PHÍ DỰ TOÁN

| STT | Nhóm Chi Phí | Chi Phí Dự Kiến (VND) | Tỷ Trọng (%) | Ghi Chú |
| :--- | :--- | :---: | :---: | :--- |
| **1** | Phần cứng & Cảm biến (Core Hardware) | 260.000 | 44.8% | ESP32, các cảm biến DHT22, MQ-2, còi, dây cắm,... |
| **2** | Thiết bị đóng gói & Mô hình (Chassis) | 120.000 | 20.7% | Hộp mica, quạt tản nhiệt, module relay, nguồn cấp |
| **3** | Phần mềm & Dịch vụ Cloud (Software) | 0 | 0.0% | Sử dụng gói Free của Blynk IoT, Gemini API và Telegram |
| **4** | Chi phí tài liệu, in ấn & Slide (Materials) | 100.000 | 17.2% | In ấn báo cáo chuẩn quy cách, slide thuyết trình |
| **5** | Dự phòng phát sinh & Rủi ro (Contingency) | 100.000 | 17.2% | Mua linh kiện thay thế nếu hỏng hóc hoặc ship hỏa tốc |
| **--** | **TỔNG KINH PHÍ DỰ TOÁN** | **580.000 VND** | **100%** | *Bằng chữ: Năm trăm tám mươi ngàn đồng chẵn.* |

---

### II. CHI TIẾT CÁC HẠNG MỤC CHI PHÍ

#### 1. Nhóm 1: Phần cứng & Cảm biến chính (Core Hardware)

| STT | Tên Thiết Bị / Linh Kiện | Thông Số Kỹ Thuật | SL | Đơn Giá (VND) | Thành Tiền (VND) | Nơi Mua Tham Khảo (TP.HCM) |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| 1.1 | **NodeMCU ESP32** | Kit phát triển 38 chân, tích hợp Wi-Fi + Bluetooth | 1 | 85.000 | 85.000 | Thế Giới IC / Linh Kiện Thủ Đức |
| 1.2 | **Cảm biến DHT22** | Đo nhiệt độ (-40 to 80°C) & độ ẩm (0-100%), độ chính xác cao | 1 | 45.000 | 45.000 | Hshop / Linh Kiện 3M |
| 1.3 | **Cảm biến Gas MQ-2** | Phát hiện khí ga LPG, propan, metan, khói | 1 | 30.000 | 30.000 | Hshop / Cửa hàng Tự Động Hóa |
| 1.4 | **Còi Buzzer Active 5V** | Phát âm thanh cảnh báo tại chỗ dạng bíp-bíp liên tục | 2 | 5.000 | 10.000 | Linh Kiện Điện Tử BK |
| 1.5 | **Breadboard MB-102** | Bo test mạch cỡ lớn 830 lỗ, không cần hàn | 1 | 25.000 | 25.000 | Hshop / Linh Kiện BK |
| 1.6 | **Bó dây cắm Breadboard** | 40 sợi 20cm, đủ loại Đực-Cái, Cái-Cái, Đực-Đực | 1 | 20.000 | 20.000 | Hshop / Cửa hàng LK gần trường |
| 1.7 | **Trở kéo lên 4.7kΩ / 10kΩ** | Phục vụ kết nối đường truyền tín hiệu của DHT22 | 1 túi | 5.000 | 5.000 | Tiệm điện tử Nhật Tảo |
| 1.8 | **Cáp kết nối Micro-USB** | Cáp truyền dữ liệu loại tốt để nạp code và cấp nguồn | 1 | 40.000 | 40.000 | Các cửa hàng phụ kiện điện thoại |
| **Cộng**| | | | | **260.000 VND** | |

#### 2. Nhóm 2: Thiết bị cơ cấu & Hộp đóng gói mô hình (Chassis & Actuators)

| STT | Tên Thiết Bị / Vật Tư | Mục Đích Sử Dụng | SL | Đơn Giá (VND) | Thành Tiền (VND) | Nơi Mua Tham Khảo |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| 2.1 | **Module Relay 1 Kênh 5V** | Điều khiển bật tắt quạt hút/thiết bị điện 220V cách ly | 1 | 20.000 | 20.000 | Hshop / Thế Giới IC |
| 2.2 | **Quạt tản nhiệt DC 5V** | Mô phỏng quạt thông gió tự động bật khi có cảnh báo | 1 | 15.000 | 15.000 | Linh Kiện Nhật Tảo |
| 2.3 | **Hộp nhựa kỹ thuật chứa mạch** | Hộp nhựa ABS chống nước cỡ 120x80x50mm làm vỏ bọc thẩm mỹ | 1 | 35.000 | 35.000 | Hshop / Tiệm đồ điện |
| 2.4 | **Bộ nguồn adapter 5V-2A** | Cấp nguồn ổn định dài lâu cho ESP32 và quạt lúc chạy thử nghiệm | 1 | 50.000 | 50.000 | Hshop / Cửa hàng máy tính |
| **Cộng**| | | | | **120.000 VND** | |

#### 3. Nhóm 3: Phần mềm, API & Dịch vụ Cloud (Software & Cloud Services)

| STT | Tên Dịch Vụ / Nền Tảng | Mục Đích Sử Dụng | Chi Phí (VND) | Trạng Thái Gói | Ghi Chú |
| :---: | :--- | :--- | :---: | :---: | :--- |
| 3.1 | **Blynk IoT Cloud Platform** | Đẩy data cảm biến lên Cloud & hiển thị Dashboard | 0 | Free Plan | Đủ dùng cho 1 thiết bị & 5 Datastreams |
| 3.2 | **Gemini AI Developer Key** | Nhận diện sự cố, đề xuất giải pháp thông minh trong Chatbot | 0 | Free Tier | Đủ lượng yêu cầu mỗi phút cho đồ án |
| 3.3 | **Telegram Bot API** | Gửi thông báo khẩn cấp & tương tác điều khiển thiết bị | 0 | Free | Không giới hạn lượng tin nhắn |
| **Cộng**| | | | **0 VND** | |

#### 4. Nhóm 4: Chi phí Học thuật, In ấn & Slide (Materials & Academic Costs)

| STT | Tên Hạng Mục | Chi Tiết | SL | Đơn Giá (VND) | Thành Tiền (VND) | Ghi Chú |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| 4.1 | **In ấn báo cáo Đồ án** | In Laser 2 bản (1 bản nộp thầy, 1 bản lưu), đóng bìa kính | 2 | 35.000 | 70.000 | Tiệm Photocopy cổng trường ĐH |
| 4.2 | **Thiết kế & in Slide tóm tắt** | Phục vụ buổi thuyết trình bảo vệ trước hội đồng | -- | 30.000 | 30.000 | Tự thiết kế Canva, chỉ tốn phí in |
| **Cộng**| | | | | **100.000 VND** | |

---

### III. CÁC MẸO TIẾT KIỆM KINH PHÍ CHO SINH VIÊN

* **Mua chung để giảm ship:** Nếu bạn có bạn học làm đề tài IoT tương tự, hãy gom đơn mua chung cảm biến, dây cắm, breadboard trên các sàn Shopee/Lazada để được miễn phí vận chuyển hoặc áp mã giảm giá tối đa.
* **Tận dụng cáp sạc cũ:** ESP32 sử dụng cáp Micro-USB thông dụng. Bạn hoàn toàn có thể tận dụng cáp sạc điện thoại cũ ở nhà thay vì mua mới 40.000 VND.
* **In ấn ghép đôi:** Khi đi in báo cáo, nên ghép file chung với các bạn để in số lượng trang lớn, các tiệm Photocopy quanh trường ĐH Bách Khoa thường giảm giá mạnh từ trang thứ 100 trở đi.

---

### IV. PHƯƠNG ÁN DỰ PHÒNG KHI CÓ SỰ CỐ (Dành cho 100.000 VND dự phòng)

1. **Hỏng cảm biến bất chợt:** Các dòng MQ-2 hoặc DHT22 cực kỳ nhạy cảm với việc cắm ngược nguồn (`GND` vào `VCC`). Nếu vô tình làm cháy cảm biến, khoản dự phòng 100.000 VND sẽ giúp bạn mua ngay linh kiện thay thế tại tiệm linh kiện gần trường trong vòng 30 phút mà không làm gián đoạn tiến độ.
2. **Cần giao hàng hỏa tốc:** Trong giai đoạn cuối, nếu phát hiện thiếu dây cắm hay thiếu một linh kiện nhỏ, bạn có thể đặt đơn Grab/Shopee Express giao ngay để nhận hàng trong vòng 1-2 tiếng, đảm bảo kịp hạn nộp của giáo viên hướng dẫn.

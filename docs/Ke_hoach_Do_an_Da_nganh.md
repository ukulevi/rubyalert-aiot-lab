# KẾ HOẠCH TRIỂN KHAI CHI TIẾT & DỰ TOÁN CHI PHÍ
## ĐỒ ÁN ĐA NGÀNH: HỆ THỐNG GIÁM SÁT MÔI TRƯỜNG VÀ CẢNH BÁO PHÒNG LAB THÔNG MINH (IoT)

---

## 1. DỰ TOÁN CHI PHÍ LINH KIỆN (BẢNG GIÁ THAM KHẢO TẠI TP.HCM)

Vì đặc thù triển khai nhanh trong vòng 2 tuần và làm độc lập, toàn bộ linh kiện dưới đây đều là các module đúc sẵn, có độ bền cao, dễ dàng kết nối qua dây cắm breadboard mà không cần hàn mạch phức tạp.

| STT | Tên Linh Kiện / Thiết Bị | Số Lượng | Giá Dự Kiến (VND) | Ghi Chú / Nơi Mua (Tham khảo) |
| :--- | :--- | :---: | :---: | :--- |
| **1** | **NodeMCU ESP32 (Wifi + Bluetooth)** | 1 | 85.000 | Kit phát triển chính, điều khiển toàn hệ thống |
| **2** | **Cảm biến nhiệt độ & độ ẩm DHT22** | 1 | 45.000 | Độ chính xác cao hơn dòng DHT11, kèm trở treo |
| **3** | **Cảm biến khí gas / khói MQ-2** | 1 | 30.000 | Đầu ra cả Analog và Digital, có biến trở chỉnh độ nhạy |
| **4** | **Module Relay 1 Kênh 5V Opto Cách Ly** | 1 | 20.000 | Dùng kích hoạt quạt hút mô phỏng cảnh báo |
| **5** | **Quạt tản nhiệt DC 5V (Mô phỏng quạt thông gió)** | 1 | 15.000 | Kết nối qua Relay để làm cơ cấu chấp hành |
| **6** | **Còi chíp báo động (Buzzer Active 5V)** | 1 | 5.000 | Kêu tại chỗ khi phát hiện vượt ngưỡng |
| **7** | **Mạch nạp / Cáp Micro-USB loại tốt** | 1 | 15.000 | Kết nối ESP32 với máy tính để nạp code và cấp nguồn |
| **8** | **Test board (Breadboard) MB-102** | 1 | 25.000 | Bo cắm thử nghiệm mạch, không cần hàn |
| **9** | **Dây cắm Breadboard (Đực-Cái, Cái-Cái, Đực-Đực)** | 1 bó | 20.000 | Bó 40 sợi dài 20cm phục vụ đấu nối nhanh |
| **10** | **Hộp nhựa kỹ thuật chứa mạch (Mô hình)** | 1 | 30.000 | Dùng để cố định phần cứng thẩm mỹ khi đi demo |
| -- | **TỔNG CHI PHÍ DỰ KIẾN** | -- | **290.000 VND** | *Chưa bao gồm phí vận chuyển hỏa tốc (nếu có)* |

*Mẹo tối ưu thời gian:* Bạn có thể chạy ra các cửa hàng linh kiện điện tử gần trường Đại học Bách Khoa (khu Bắc Hải, Lý Thường Kiệt) hoặc đặt Shopee/Lazada chọn giao hàng hỏa tốc trong ngày để có ngay linh kiện làm việc.

---

## 2. KẾ HOẠCH TRIỂN KHAI CHI TIẾT TỪNG NGÀY (17/05 - 30/05)

### GIAI ĐOẠN 1: NGHIÊN CỨU & THIẾT KẾ PHẦN CỨNG (Day 1 - Day 5)
* **Ngày 1 (Chủ Nhật - 17/05): Mua sắm & Khởi tạo môi trường**
    * *Sáng:* Mua đầy đủ linh kiện theo bảng dự toán.
    * *Chiều:* Cài đặt Arduino IDE (hoặc VS Code + PlatformIO). Cài đặt Driver kết nối USB-UART (CP210x hoặc CH340 tùy loại kit ESP32).
    * *Tối:* Viết chương trình "Blink LED" huyền thoại để đảm bảo kit ESP32 hoạt động bình thường.
* **Ngày 2 (Thứ Hai - 18/05): Đọc dữ liệu Cảm biến độc lập**
    * Kết nối cảm biến DHT22 và MQ-2 vào ESP32 trên breadboard.
    * Cài đặt thư viện `DHT sensor library` từ Adafruit. Viết code đọc giá trị Nhiệt độ, Độ ẩm, Khói hiển thị lên Serial Monitor. Ngưỡng cảnh báo tạm thời thiết lập trong code.
* **Ngày 3 (Thứ Ba - 19/05): Kiểm soát cơ cấu chấp hành tại chỗ**
    * Đấu nối Còi chip (Buzzer) và Module Relay (kèm quạt 5V) vào chân GPIO của ESP32.
    * Bổ sung logic vào code: Nếu Nhiệt độ > 35°C hoặc Khói > Ngưỡng thiết lập -> Bật Còi + Bật Relay (Quạt quay). Ngược lại tắt. Test thực tế bằng cách dùng bật lửa mồi khói gần cảm biến.
* **Ngày 4 (Thứ Tư - 20/05): Kết nối mạng (Wi-Fi)**
    * Tìm hiểu thư viện `WiFi.h` trên ESP32. Viết chương trình kết nối ESP32 vào mạng Wi-Fi nhà/phòng lab.
    * Đảm bảo ESP32 tự động kết nối lại nếu bị mất mạng vật lý. In địa chỉ IP nội mạng ra Serial Monitor để kiểm tra.
* **Ngày 5 (Thứ Năm - 21/05): Đóng gói tầng Firmware**
    * Tối ưu hóa mã nguồn phần cứng sử dụng cơ chế Non-blocking (dùng `millis()` thay vì lệnh `delay()`) giúp cảm biến đọc liên tục không bị trễ khi hệ thống thực thi tác vụ khác.

### GIAI ĐOẠN 2: XÂY DỰNG TẦNG PHẦN MỀM & KẾT NỐI HỆ THỐNG (Day 6 - Day 9)
* **Ngày 6 (Thứ Sáu - 22/05): Thiết lập nền tảng Backend / Cloud**
    * *Lựa chọn tối ưu tốc độ:* Tạo tài khoản và cấu hình Datastream trên **Blynk IoT Platform** (hoặc Firebase). Định nghĩa các biến: `V1` (Nhiệt độ), `V2` (Độ ẩm), `V3` (Khói), `V4` (Trạng thái Relay/Quạt).
    * Tải thư viện Blynk về Arduino IDE. Nạp mã Token cấu hình vào ESP32 để đẩy dữ liệu lên Cloud.
* **Ngày 7 (Thứ Bảy - 23/05): Thiết kế Dashboard Giao diện Người dùng**
    * Tùy chỉnh giao diện trên Web Dashboard và Mobile App của Blynk.
    * Sử dụng các widget dạng đồ thị (Chart), đồng hồ đo (Gauge), nút nhấn điều khiển quạt từ xa để tạo nên một giao diện sạch sẽ, trực quan theo đúng tinh thần "Minimalist".
* **Ngày 8 (Chủ Nhật - 24/05): Cấu hình Cảnh báo tự động qua Telegram**
    * Tạo một Telegram Bot cá nhân thông qua `@BotFather`, lấy `Token API` và `Chat ID` của bạn.
    * *Giải pháp 1:* Dùng tính năng Webhook/Automation trực tiếp của Blynk để bắn thông báo sang Telegram khi giá trị cảm biến vượt ngưỡng.
    * *Giải pháp 2:* Code trực tiếp thư viện `UniversalTelegramBot` vào ESP32 để tự gửi tin nhắn khẩn cấp.
* **Ngày 9 (Thứ Hai - 25/05): Kiểm thử tích hợp toàn diện (End-to-End Test)**
    * Chạy thử nghiệm hệ thống liên tục trong 3-4 tiếng. Theo dõi xem dữ liệu trên Web có bị mất gói hay không.
    * Đóng gói toàn bộ mạch điện gọn gàng vào hộp nhựa kỹ thuật, đục các lỗ nhỏ để cảm biến nhô ra ngoài đón không khí, đảm bảo mô hình mang đi chấm điểm nhìn chuyên nghiệp.

### GIAI ĐOẠN 3: VIẾT BÁO CÁO & CHUẨN BỊ BẢO VỆ (Day 10 - Day 14)
* **Ngày 10 (Thứ Ba - 26/05): Soạn thảo cấu trúc Báo cáo Đồ án**
    * Viết Chương 1 (Mở đầu, Lý do chọn đề tài), Chương 2 (Tổng quan công nghệ: ESP32, Giao thức truyền thông, Nền tảng Cloud áp dụng).
    * Vẽ sơ đồ khối tổng thể kiến trúc hệ thống (Block Diagram) chèn vào báo cáo.
* **Ngày 11 (Thứ Tư - 27/05): Hoàn thiện nội dung kỹ thuật chi tiết**
    * Viết Chương 3 (Thiết kế chi tiết): Sơ đồ đấu nối chân phần cứng, Sơ đồ thuật toán xử lý của phần phần mềm.
    * Chụp ảnh thực tế mô hình phần cứng hoàn thiện và ảnh chụp màn hình giao diện Dashboard đưa vào Chương 4 (Kết quả thực nghiệm).
* **Ngày 12 (Thứ Năm - 28/05): ĐÁNH GIÁ CUỐI CÙNG & NỘP BÁO CÁO**
    * Đọc rà soát lại toàn bộ lỗi chính tả, định dạng căn lề văn bản báo cáo theo đúng phông chuẩn quy định. Xuất file báo cáo sang định dạng **PDF**.
    * Soạn và **Gửi email nộp báo cáo** đến địa chỉ thầy Bình: `binh@hcmut.edu.vn` trước thời hạn quy định (2 ngày trước buổi chấm).
* **Ngày 13 (Thứ Sáu - 29/05): Thiết kế Slide Thuyết trình**
    * Xây dựng slide bảo vệ giới hạn từ 12 - 15 slide ngắn gọn. Tập trung vào hình ảnh sơ đồ khối, hình thực tế hệ thống và biểu đồ kết quả thay vì chèn nhiều chữ.
    * Tự thuyết trình thử tại nhà bằng đồng hồ bấm giờ, đảm bảo bài nói mạch lạc và gói gọn trong khoảng **15 phút**.
* **Ngày 14 (Thứ Bảy - 30/05): BUỔI DEMO VÀ CHẤM ĐIỂM TRỰC TIẾP**
    * Sạc đầy pin laptop, mang theo mô hình phần cứng, dây cáp nguồn dự phòng. Đột phá tự tin để hoàn thành xuất sắc đồ án đa ngành!

---

## 3. QUẢN TRỊ RỦI RO & PHƯƠNG ÁN DỰ PHÒNG

Vì bạn làm một mình, bất kỳ lỗi phần cứng nào cũng có thể gây nghẽn tiến độ. Hãy lưu ý các nguyên tắc "sống còn" sau:
1.  **Rủi ro cháy linh kiện:** Khi cấp nguồn cho ESP32 hoặc cảm biến, phải kiểm tra cực âm/dương (`GND`/`VCC`) thật kỹ. Cắm nhầm nguồn 5V vào chân tín hiệu IO có thể làm hỏng chân vi điều khiển ngay lập tức.
2.  **Mạng Wifi trường học bị chặn:** Wifi tại trường Bách Khoa thường yêu cầu đăng nhập trang Portal (Web Authentication), ESP32 sẽ không tự kết nối được. **Phương án dự phòng:** Sử dụng tính năng Phát di động (4G Hotspot) từ điện thoại cá nhân của bạn, cấu hình SSID và Password của ESP32 trùng với mạng 4G này để chạy Demo mượt mà lúc chấm điểm.
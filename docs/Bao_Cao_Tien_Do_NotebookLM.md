# BÁO CÁO TIẾN ĐỘ ĐỒ ÁN ĐA NGÀNH: DỰ ÁN RUBYALERT SMART LAB
## CẬP NHẬT TRẠNG THÁI MỚI NHẤT (NGÀY 21/05/2026)

> **Lưu ý:** Tài liệu này được thiết kế để đồng bộ hóa và tải trực tiếp lên Google NotebookLM làm nguồn tri thức (Source) chính thức của dự án. NotebookLM có thể sử dụng tài liệu này để tóm tắt, giải đáp câu hỏi, hoặc tạo Podcast thảo luận về đồ án.

---

### I. CÁC CHECKPOINT ĐÃ HOÀN THÀNH XUẤT SẮC

#### 1. Lắp ráp hoàn chỉnh phần cứng 100% (Hardware Assembled)
*   **Vi điều khiển chính:** Kit phát triển NodeMCU ESP32.
*   **Cảm biến thu thập dữ liệu:**
    *   **DHT22 (Nhiệt độ & Độ ẩm):** Đã kết nối vào chân `GPIO 0` (được bảo vệ bằng trở kéo lên 4.7kΩ).
    *   **MQ-2 (Khói & Khí Gas):** Đã kết nối vào cổng `Analog ADC` (chân đầu vào tương tự để đọc chính xác nồng độ gas).
*   **Cơ cấu chấp hành và cảnh báo:**
    *   **Module Relay 5V (Opto cách ly):** Được kết nối với chân điều khiển `GPIO 2`.
    *   **Quạt hút thông gió (DC 5V):** Đấu nối qua tiếp điểm Thường Mở (NO) của Relay, sẵn sàng tự động kích hoạt khi có sự cố.
    *   **Còi chíp báo động (Buzzer Active 5V):** Kết nối để phát âm thanh cảnh báo tại chỗ tức thời.
*   **Bảng cắm thử nghiệm (Breadboard MB-102):** Toàn bộ dây dẫn (Đực - Cái, Cái - Cái) đã được đấu nối an toàn, gọn gàng, cố định chắc chắn.

#### 2. Kết nối vật lý với Máy tính (PC USB Connection)
*   **Cáp kết nối:** Đã sử dụng cáp Micro-USB truyền tín hiệu tốt nối ESP32 với cổng USB máy tính.
*   **Cổng COM nhận diện trên Windows:** **`COM3`** *(Đã được kiểm tra và nhận diện chính xác qua trình điều khiển USB-to-UART)*.

---

### II. TRẠNG THÁI PHẦN MỀM & KẾT NỐI HIỆN TẠI

1.  **Firmware trên ESP32 (`main_esp32.py`):**
    *   Sử dụng ngôn ngữ **MicroPython** tối ưu, nạp thư viện kết nối nhanh `umqtt.simple`.
    *   Tần suất đo đạc và đẩy dữ liệu lên MQTT Broker: 10 giây/lần.
    *   Định dạng dữ liệu gửi: Gói JSON chuẩn gồm `{ "temperature", "humidity", "gas" }`.
    *   Lắng nghe lệnh điều khiển quạt từ xa trên kênh: `rubyalert/lab_1/fan`.

2.  **Hệ thống Backend trung tâm (`smart_lab_system.py`):**
    *   Đã hoàn thiện việc xử lý dữ liệu, lưu lịch sử đo đạc.
    *   **Trí tuệ nhân tạo Gemini AI:** Tích hợp thành công SDK GenAI mới nhất, sẵn sàng phân tích dữ liệu, tự động viết báo cáo an toàn chuyên sâu (`/report`) và trò chuyện tư vấn phòng lab thông minh.
    *   **Telegram Chatbot:** Đã tối ưu hóa nội dung thông báo khẩn cấp cực kỳ gọn gàng, tiết chế icon, tự động gợi ý câu lệnh `/` khi người dùng nhập ký tự và tích hợp **tự động kiểm tra trạng thái HTTP Server (port 8000)** để gợi ý link Dashboard cho cả Máy tính và Điện thoại.

---

### III. KẾ HOẠCH BƯỚC TIẾP THEO (GIAI ĐOẠN 2: PHẦN MỀM & KẾT NỐI)

Từ ngày mai (22/05/2026), chúng ta sẽ tiến hành đồng bộ hóa phần cứng thật vào phần mềm theo các bước:

1.  **Nạp mã nguồn MicroPython lên ESP32:**
    *   Mở phần mềm **Thonny IDE** (hoặc dùng extension MicroPython trên VS Code).
    *   Chọn cổng kết nối là **`COM3`**.
    *   Cấu hình thông tin Wi-Fi nhà/phòng lab vào file code trên ESP32.
    *   Lưu và chạy file `main_esp32.py` để ESP32 bắt đầu đo dữ liệu thật.

2.  **Khởi động các dịch vụ mạng trên Laptop:**
    *   **Mosquitto MQTT Broker:** Chạy để làm cầu nối truyền nhận tin nhắn giữa ESP32 và máy tính.
    *   **Python HTTP Server (Port 8000):** Chạy lệnh `python -m http.server 8000` để phát sóng Web Dashboard.

3.  **Kích hoạt Hệ thống Giám sát Realtime:**
    *   Chạy chương trình chính `python smart_lab_system.py` với chế độ dữ liệu thật từ cổng COM/MQTT thay vì chế độ mô phỏng (`SIMULATION_MODE = False`).
    *   Mở Dashboard trên Điện thoại/Máy tính để tận hưởng thành quả giám sát thời gian thực!

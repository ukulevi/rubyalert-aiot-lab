# DÀN Ý CHI TIẾT BÁO CÁO ĐỒ ÁN ĐA NGÀNH
**Đề tài:** Xây dựng hệ thống IoT giám sát môi trường phòng Lab thời gian thực tích hợp cảnh báo qua Telegram.

---

## CHƯƠNG 1: GIỚI THIỆU CHUNG
### 1.1. Lý do chọn đề tài
*   Tầm quan trọng của việc giám sát môi trường (Nhiệt độ, độ ẩm, khí gas) trong phòng Lab để đảm bảo an toàn thiết bị và con người.
*   Hạn chế của các phương pháp giám sát thủ công.
### 1.2. Mục tiêu đề tài
*   Xây dựng hệ thống tự động đo đạc thông số môi trường.
*   Hiển thị dữ liệu trực quan trên Dashboard Web.
*   Gửi cảnh báo tức thời qua Telegram khi có sự cố.
### 1.3. Phạm vi nghiên cứu
*   Sử dụng vi điều khiển ESP32 (Yolo UNO).
*   Giao thức truyền tin MQTT qua Server OhStem/Core IoT.
*   Ứng dụng Telegram làm kênh nhận thông báo.

---

## CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ
### 2.1. Tổng quan về IoT (Internet of Things)
### 2.2. Phần cứng sử dụng
*   **ESP32/Yolo UNO:** Đặc điểm, thông số kỹ thuật.
*   **Cảm biến DHT22:** Nguyên lý đo nhiệt độ, độ ẩm.
*   **Cảm biến MQ-2:** Nguyên lý phát hiện khí Gas/Khói.
*   **Module Relay:** Cách điều khiển thiết bị công suất cao (quạt).
### 2.3. Giao thức MQTT
*   Khái niệm Publish/Subscribe.
*   Tại sao chọn MQTT cho hệ thống IoT.
### 2.4. Nền tảng Core IoT và Telegram Bot API

---

## CHƯƠNG 3: THIẾT KẾ VÀ KIẾN TRÚC HỆ THỐNG
### 3.1. Mô hình kiến trúc tổng quát
*   Sơ đồ khối: Sensor -> ESP32 -> MQTT Broker -> Dashboard/Backend -> Telegram.
### 3.2. Thiết kế sơ đồ đấu nối (Wiring Diagram)
*   *(Chèn sơ đồ Mermaid/Fritzing mà tôi đã cung cấp)*.
### 3.3. Thiết kế luồng dữ liệu (Flowchart)
*   Quy trình đọc dữ liệu, kiểm tra ngưỡng và gửi lệnh điều khiển quạt.

---

## CHƯƠNG 4: TRIỂN KHAI VÀ THỰC NGHIỆM
### 4.1. Cài đặt môi trường phần mềm
*   Cấu hình MQTT trên Core IoT Platform.
*   Tạo Bot Telegram và lấy Token/Chat ID.
### 4.2. Xây dựng chương trình giả lập (Simulation)
*   Giới thiệu script Python giả lập thiết bị (Digital Twin).
*   Mục đích: Kiểm thử logic hệ thống trước khi lắp đặt phần cứng.
### 4.3. Kết quả thực nghiệm
*   Hình ảnh Dashboard hiển thị số liệu.
*   Hình ảnh Terminal chạy script xử lý.
*   Hình ảnh tin nhắn cảnh báo nhận được trên điện thoại qua Telegram.

---

## CHƯƠNG 5: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
### 5.1. Kết quả đạt được
*   Hệ thống chạy ổn định, độ trễ thấp.
*   Cảnh báo chính xác theo ngưỡng cài đặt.
### 5.2. Hạn chế
*   Phụ thuộc vào kết nối Internet.
### 5.3. Hướng phát triển
*   Tích hợp thêm Camera giám sát.
*   Xây dựng ứng dụng di động riêng (App Mobile).

---

## TÀI LIỆU THAM KHẢO
1. Tài liệu kỹ thuật ESP32/Yolo UNO.
2. Tài liệu giao thức MQTT (mqtt.org).
3. Hướng dẫn lập trình Python/MicroPython cho IoT.

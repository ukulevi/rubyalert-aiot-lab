import os
from dotenv import load_dotenv

# Nạp biến môi trường từ file .env (nếu tồn tại)
load_dotenv()

# --- CẤU HÌNH TELEGRAM & GEMINI AI (Đọc từ file .env) ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")  # Lấy tại aistudio.google.com


# --- CHỌN SERVER MQTT ---
# Đang dùng Mosquitto Broker cục bộ trên máy Edge Server
MQTT_SERVER = "192.168.1.91" 
MQTT_PORT = 1884
OHSTEM_USERNAME = ""  # Để trống khi dùng Broker cục bộ không xác thực
OHSTEM_KEY = ""       # Để trống khi dùng Broker cục bộ không xác thực

# Topic chính thức của RubyAlert
MQTT_TOPIC_TELEMETRY = "rubyalert/lab_1/telemetry"
FEED_FAN = "rubyalert/lab_1/fan"

# Các Feed phụ
FEED_TEMP = "temperature"
FEED_HUMI = "humidity"
FEED_GAS  = "gas"


# --- PHẦN CORE IOT (TẠM THỜI ĐỂ ĐÂY, KHI NÀO SERVER HẾT LỖI THÌ ĐỔI LẠI) ---
# MQTT_SERVER = "app.coreiot.io" (Device: RubyAlert AIoT Alarm Node)
# OHSTEM_USERNAME = "2YitXJMGPgFqZGtcF7w5" 
# MQTT_TOPIC_TELEMETRY = "v1/devices/me/telemetry"

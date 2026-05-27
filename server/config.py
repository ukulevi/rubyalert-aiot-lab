import os
from dotenv import load_dotenv

# Nạp biến môi trường từ file .env (nếu tồn tại)
load_dotenv()

# --- CẤU HÌNH TELEGRAM & GEMINI AI (Đọc từ file .env) ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")  # Lấy tại aistudio.google.com

# --- HỖ TRỢ ĐA MODEL (FREE POLLINATIONS, GEMINI, GROQ, OLLAMA) ĐỂ TĂNG QUOTA FREE ---
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "free").lower()  # "free" (Pollinations AI - Không cần key, quota cực lớn), "gemini", "groq", "ollama"
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")  # qwen2.5:3b, llama3, gemma2



# --- CHỌN SERVER MQTT ---
# Đang dùng Mosquitto Broker cục bộ trên máy Edge Server
MQTT_SERVER = "127.0.0.1" 
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

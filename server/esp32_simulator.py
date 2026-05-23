import paho.mqtt.client as mqtt
import time
import random
import json
import config
import sys

# Đảm bảo console Windows hỗ trợ in unicode không bị crash
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# Cấu hình MQTT
# Đặt Client ID riêng cho thiết bị giả lập
client = mqtt.Client("ESP32_Device")
client.username_pw_set(config.OHSTEM_USERNAME, config.OHSTEM_KEY)

def log_sim(msg):
    try:
        print(msg)
    except UnicodeEncodeError:
        safe_msg = msg.encode('ascii', errors='replace').decode('ascii')
        print(safe_msg)

def connect_mqtt():
    try:
        # Kết nối tới Broker
        client.connect(config.MQTT_SERVER, config.MQTT_PORT, 60)
        log_sim("[SIMULATOR] Đã kết nối thành công tới MQTT Broker!")
    except Exception as e:
        log_sim(f"[SIMULATOR-ERROR] Lỗi kết nối: {e}")

def simulate_data():
    while True:
        # Giả lập dữ liệu ngẫu nhiên
        temp = round(random.uniform(25.0, 40.0), 1)
        humi = round(random.uniform(50.0, 90.0), 1)
        gas  = random.randint(300, 2500) # Giả lập nồng độ khí gas

        log_sim(f"[SIMULATOR] Đang gửi dữ liệu: Temp={temp}°C, Humi={humi}%, Gas={gas}")
        
        # Đóng gói dữ liệu thành JSON chuẩn RubyAlert
        payload = {
            "temperature": temp,
            "humidity": humi,
            "gas": gas
        }
        
        # Gửi lên Topic Telemetry tổng hợp
        try:
            client.publish(config.MQTT_TOPIC_TELEMETRY, json.dumps(payload))
        except Exception as e:
            log_sim(f"[SIMULATOR-ERROR] Không thể gửi dữ liệu: {e}")
        
        time.sleep(5) # Đợi 5 giây trước khi gửi tiếp

if __name__ == "__main__":
    if config.OHSTEM_USERNAME == "Dien_Username_Cua_Ban":
        log_sim("[SIMULATOR-WARNING] Bạn chưa điền MQTT Username trong file config.py!")
    else:
        connect_mqtt()
        client.loop_start()
        simulate_data()

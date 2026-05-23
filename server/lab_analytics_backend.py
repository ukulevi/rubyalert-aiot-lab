import paho.mqtt.client as mqtt
import requests
import config
import time

# Ngưỡng cảnh báo
TEMP_THRESHOLD = 35.0
GAS_THRESHOLD = 2000

def send_telegram(message):
    url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": config.TELEGRAM_CHAT_id if hasattr(config, 'TELEGRAM_CHAT_id') else config.TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("🔔 Đã gửi cảnh báo qua Telegram!")
        else:
            print(f"❌ Lỗi gửi Telegram: {response.text}")
    except Exception as e:
        print(f"❌ Exception Telegram: {e}")

def on_connect(client, userdata, flags, rc):
    print("✅ Backend: Đã kết nối với MQTT Broker")
    # Subscribe vào tất cả mọi thứ để tìm đúng Topic
    client.subscribe("#")
    print("🔍 Đang dò tìm dữ liệu từ Simulator...")

def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        payload = msg.payload.decode()
        print(f"📡 DÒ THẤY: Topic: [{topic}] -> Dữ liệu: {payload}")

        # Hỗ trợ định dạng JSON tổng hợp (như của esp32_simulator.py / main_esp32.py)
        if topic == config.MQTT_TOPIC_TELEMETRY:
            import json
            data = json.loads(payload)
            
            # Kiểm tra Nhiệt độ
            if "temperature" in data:
                temp = float(data["temperature"])
                if temp > TEMP_THRESHOLD:
                    msg_alert = (
                        f"🚨 **[RubyAlert] CẢNH BÁO NHIỆT ĐỘ**\n"
                        f"Sự cố: Nhiệt độ vượt ngưỡng an toàn!\n"
                        f"- Nhiệt độ: `{temp}°C` (Ngưỡng: {TEMP_THRESHOLD}°C)\n"
                        f"Hành động: Đã bật quạt thông gió tự động."
                    )
                    send_telegram(msg_alert)
                    client.publish(config.FEED_FAN, "1")
            
            # Kiểm tra Khí Gas
            if "gas" in data:
                gas = float(data["gas"])
                if gas > GAS_THRESHOLD:
                    msg_alert = (
                        f"🚨 **[RubyAlert] CẢNH BÁO KHÍ GAS**\n"
                        f"Sự cố: Phát hiện rò rỉ khí Gas/Khói!\n"
                        f"- Khí Gas: `{gas} ppm` (Ngưỡng: {GAS_THRESHOLD} ppm)\n"
                        f"Hành động: Đã bật quạt thông gió tự động."
                    )
                    send_telegram(msg_alert)
                    client.publish(config.FEED_FAN, "1")
                    
        # Hỗ trợ định dạng Feed đơn lẻ (nếu có)
        elif config.FEED_TEMP in topic:
            value = float(payload)
            if value > TEMP_THRESHOLD:
                msg_alert = (
                    f"🚨 **[RubyAlert] CẢNH BÁO NHIỆT ĐỘ**\n"
                    f"Sự cố: Nhiệt độ vượt ngưỡng an toàn!\n"
                    f"- Nhiệt độ: `{value}°C` (Ngưỡng: {TEMP_THRESHOLD}°C)\n"
                    f"Hành động: Đã bật quạt thông gió tự động."
                )
                send_telegram(msg_alert)
                client.publish(config.FEED_FAN, "1")

        elif config.FEED_GAS in topic:
            value = float(payload)
            if value > GAS_THRESHOLD:
                msg_alert = (
                    f"🚨 **[RubyAlert] CẢNH BÁO KHÍ GAS**\n"
                    f"Sự cố: Phát hiện rò rỉ khí Gas/Khói!\n"
                    f"- Khí Gas: `{value} ppm` (Ngưỡng: {GAS_THRESHOLD} ppm)\n"
                    f"Hành động: Đã bật quạt thông gió tự động."
                )
                send_telegram(msg_alert)
                client.publish(config.FEED_FAN, "1")
    except Exception as e:
        print(f"❌ Lỗi xử lý tin nhắn: {e}")

if __name__ == "__main__":
    # Đặt Client ID riêng cho Backend
    client = mqtt.Client("Backend_Server")
    client.username_pw_set(config.OHSTEM_USERNAME, config.OHSTEM_KEY)
    client.on_connect = on_connect
    client.on_message = on_message

    if config.OHSTEM_USERNAME == "Dien_Username_Cua_Ban":
        print("⚠️ CẢNH BÁO: Bạn chưa điền MQTT Username trong file config.py!")
    else:
        try:
            client.connect(config.MQTT_SERVER, config.MQTT_PORT, 60)
            client.loop_forever()
        except Exception as e:
            print(f"❌ Lỗi Backend: {e}")

from machine import Pin, ADC
import dht
import time
import json
import network
from umqtt.simple import MQTTClient

# ==================== CẤU HÌNH HỆ THỐNG ====================
# 1. Cấu hình WiFi (Thay đổi thông tin WiFi của bạn ở đây)
WIFI_SSID = "Ruby"
WIFI_PASS = "abc12345"

# 2. Cấu hình MQTT Broker (Theo Edge Server cục bộ của bạn)
MQTT_SERVER = "192.168.1.91"
MQTT_PORT   = 1884
CLIENT_ID   = "RubyAlert_ESP32_Real"

TOPIC_TELEMETRY = b"rubyalert/lab_1/telemetry"
TOPIC_FAN       = b"rubyalert/lab_1/fan"

# 3. Cấu hình chân phần cứng (Pins) theo sơ đồ đấu nối chuẩn của đồ án
sensor_dht = dht.DHT22(Pin(4))     # Sử dụng DHT22 nối chân GPIO 4 (Phát hiện phần cứng chuẩn xác)
sensor_mq2 = ADC(Pin(34))          # MQ-2 nối chân GPIO 34 (Analog A0)
sensor_mq2.atten(ADC.ATTN_11DB)   # Cấu hình thang đo 0 - 3.6V cho MQ-2 (Đọc giá trị 0-4095)
relay_fan  = Pin(27, Pin.OUT)      # Relay quạt nối chân GPIO 27
buzzer     = Pin(26, Pin.OUT)      # Còi Buzzer nối chân GPIO 26

# Mặc định tắt các thiết bị ngoại vi lúc khởi động (Đối với Relay Active HIGH)
relay_fan.off() # Gọi .off() để tắt quạt lúc khởi động (nếu là Active LOW thì đổi thành .on())
buzzer.off()
# ==========================================================

# Trạng thái quạt
fan_state = 0

def connect_wifi():
    """Hàm kết nối WiFi tự động"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("🔌 Đang kết nối WiFi: " + WIFI_SSID + " ...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        # Chờ tối đa 15 giây
        count = 0
        while not wlan.isconnected() and count < 30:
            time.sleep(0.5)
            count += 1
            print(".", end="")
    
    if wlan.isconnected():
        print("\n✅ WiFi ĐÃ KẾT NỐI!")
        print("📌 Địa chỉ IP của ESP32:", wlan.ifconfig()[0])
        return True
    else:
        print("\n❌ Không thể kết nối WiFi. Vui lòng kiểm tra lại SSID/Password.")
        return False

def on_receive_message(topic, msg):
    """Callback nhận lệnh từ Dashboard hoặc Bot Telegram"""
    global fan_state
    print("📥 Nhận lệnh từ Server MQTT:", topic, "->", msg)
    if msg == b'1':
        relay_fan.on() # Đổi thành .off() nếu dùng Relay Active LOW
        fan_state = 1
        print("-> 🟢 Đã BẬT quạt thông gió")
    else:
        relay_fan.off() # Đổi thành .on() nếu dùng Relay Active LOW
        fan_state = 0
        print("-> 🔴 Đã TẮT quạt thông gió")

def connect_mqtt():
    """Hàm kết nối MQTT Broker"""
    client = MQTTClient(CLIENT_ID, MQTT_SERVER, port=MQTT_PORT)
    client.set_callback(on_receive_message)
    try:
        client.connect()
        client.subscribe(TOPIC_FAN)
        print("✅ Đã kết nối MQTT Broker thành công và subscribe:", TOPIC_FAN)
        return client
    except Exception as e:
        print("❌ Lỗi kết nối MQTT Broker:", e)
        return None

def run_real_hardware():
    # 1. Kết nối WiFi trước
    if not connect_wifi():
        print("🚨 Không có kết nối WiFi, thử lại sau 10s...")
        time.sleep(10)
        import machine
        machine.reset()

    # 2. Kết nối MQTT
    client = connect_mqtt()
    while client is None:
        print("⏳ Thử kết nối lại MQTT sau 5 giây...")
        time.sleep(5)
        client = connect_mqtt()

    print("🚀 Hệ thống telemetry bắt đầu hoạt động!")
    
    last_send = time.time()
    
    while True:
        try:
            # Luôn kiểm tra kết nối WiFi, nếu mất thì reconnect
            wlan = network.WLAN(network.STA_IF)
            if not wlan.isconnected():
                print("🚨 Mất kết nối WiFi! Tiến hành kết nối lại...")
                if connect_wifi():
                    client = connect_mqtt()
                time.sleep(2)
                continue

            # Kiểm tra xem có tin nhắn (lệnh điều khiển quạt) đến không (non-blocking)
            try:
                client.check_msg()
            except Exception as e:
                print("⚠️ Lỗi kiểm tra tin nhắn MQTT (Có thể Broker mất kết nối):", e)
                print("🔄 Đang kết nối lại MQTT...")
                client = connect_mqtt()
                time.sleep(2)
                continue

            # Đọc cảm biến mỗi 10 giây
            now = time.time()
            if now - last_send >= 10 or now < last_send: # Tránh trường hợp overflow
                last_send = now
                
                # Đọc cảm biến DHT22
                temp = 0.0
                humi = 0.0
                try:
                    sensor_dht.measure()
                    temp = round(sensor_dht.temperature(), 1)
                    humi = round(sensor_dht.humidity(), 1)
                except Exception as e:
                    print("❌ Lỗi đọc cảm biến DHT22:", e)
                
                # Đọc cảm biến MQ-2 (Gas)
                gas = 0
                try:
                    gas = sensor_mq2.read() # Giá trị 0-4095 trên ESP32
                except Exception as e:
                    print("❌ Lỗi đọc cảm biến MQ-2:", e)

                print("📊 [Data] Temp: {}°C | Humi: {}% | Gas: {}".format(temp, humi, gas))

                # Đóng gói dữ liệu định dạng JSON
                payload = json.dumps({
                    "temperature": temp,
                    "humidity": humi,
                    "gas": gas
                })

                # Gửi lên Broker MQTT
                try:
                    client.publish(TOPIC_TELEMETRY, payload.encode('utf-8'))
                    print("📤 Đã gửi dữ liệu thành công lên MQTT Topic:", TOPIC_TELEMETRY)
                except Exception as e:
                    print("❌ Gửi dữ liệu MQTT thất bại:", e)
            
            time.sleep(0.1) # Tốc độ kiểm tra lệnh từ Telegram cực nhạy
            
        except KeyboardInterrupt:
            print("👋 Dừng hệ thống.")
            break
        except Exception as e:
            print("🚨 Lỗi vòng lặp chính:", e)
            time.sleep(2)

if __name__ == "__main__":
    run_real_hardware()

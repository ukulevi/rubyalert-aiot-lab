import paho.mqtt.client as mqtt
import time
import random
import requests
import json
import config
import threading
import socket
from google import genai
from google.genai import types

def is_http_server_active():
    try:
        with socket.create_connection(("127.0.0.1", 8000), timeout=0.2):
            return True
    except Exception:
        return False

# Cấu hình Gemini AI (SDK mới)
try:
    client_ai = genai.Client(api_key=config.GEMINI_API_KEY)
    AI_ENABLED = True
except Exception:
    AI_ENABLED = False



# Cấu hình ngưỡng báo động RubyAlert
TEMP_LIMIT = 35.0
TEMP_SAFE = 32.0 # Ngưỡng an toàn để tắt quạt (Hysteresis)
GAS_LIMIT = 2000

# Biến trạng thái hệ thống (State)
SIMULATION_MODE = False # Đổi thành False nếu dùng ESP32 thật

fan_on = False
last_temp = None
last_humi = None
last_gas = None
last_telegram_time = 0
last_update_id = 0
TELEGRAM_COOLDOWN = 60 # 60 giây chống spam tin nhắn

def log(tag, msg):
    try:
        print(f"[{tag}] {msg}")
    except Exception:
        try:
            # Thay thế ký tự không in được bằng dấu hỏi để không bao giờ bị crash
            safe_msg = msg.encode('ascii', errors='replace').decode('ascii')
            print(f"[{tag}] {safe_msg}")
        except Exception:
            pass

def send_telegram(message, ignore_cooldown=False):
    global last_telegram_time
    now = time.time()
    
    # Logic Cooldown: Chỉ áp dụng cho cảnh báo tự động
    if not ignore_cooldown and (now - last_telegram_time < TELEGRAM_COOLDOWN):
        log("NOTIFY", "Telegram alert skipped (Cooldown active ⏳)")
        return
        
    url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": config.TELEGRAM_CHAT_ID, 
        "text": message, 
        "parse_mode": "Markdown"
    }
    try:
        r = requests.post(url, json=payload, timeout=5)
        if r.status_code == 200:
            log("NOTIFY", "Telegram message sent successfully 📱")
            if not ignore_cooldown:
                last_telegram_time = now
        else:
            log("ERROR", f"Telegram fail: {r.status_code}")
    except Exception as e:
        log("ERROR", f"Connection to Telegram failed: {e}")

# --- MODULE AI: PHÂN TÍCH VỚI GEMINI (SDK MỚI) ---
def ask_gemini_ai(user_question):
    if not AI_ENABLED or config.GEMINI_API_KEY == "DIEN_API_KEY_CUA_BAN_VAO_DAY":
        return "⚠️ Chưa cấu hình API Key."
    
    # Prompt nén gọn để tiết kiệm Token
    sys_instruction = f"""Hệ thống RubyAlert. T:{last_temp}C, H:{last_humi}%, G:{last_gas}ppm, Quạt:{"ON" if fan_on else "OFF"}.
    Quy tắc: 1. Chỉ trả lời về an toàn Lab/thiết bị. 2. Từ chối câu hỏi ngoài lề. 3. Ngắn gọn, dùng icon, in đậm số."""


    
    try:
        # Gọi Gemini với khả năng sử dụng công cụ (Function Calling)
        response = client_ai.models.generate_content(
            model='gemini-2.0-flash',
            contents=user_question,
            config=types.GenerateContentConfig(
                system_instruction=sys_instruction,
                tools=tools_list,
                max_output_tokens=150 # Giới hạn độ dài để tiết kiệm Token
            )
        )

        
        # Nếu AI quyết định gọi hàm (ví dụ: bật quạt)
        if response.candidates[0].content.parts[0].function_call:
            fn = response.candidates[0].content.parts[0].function_call
            if fn.name == "set_fan_state":
                # Thực thi hàm và lấy kết quả
                s = fn.args["state"]
                result = set_fan_state(s)
                return f"✅ {result}"

        return response.text.strip()
    except Exception as e:

        if "429" in str(e):
            return f"🚀 **AI đang bận (Quá tải)**.\n\n📊 **Dữ liệu thô:**\n- T: {last_temp}°C\n- H: {last_humi}%\n- G: {last_gas} ppm\n\n(Vui lòng đợi vài giây rồi thử lại câu hỏi của bạn)"
        return f"❌ Lỗi AI: {str(e)}"


# --- CÁC HÀM THỰC THI (TOOLS) CHO AI ---
def set_fan_state(state: str):
    """Bật hoặc tắt quạt thông gió. state chỉ có thể là 'ON' hoặc 'OFF'."""
    global fan_on
    if state == "ON":
        client.publish(config.FEED_FAN, "1")
        fan_on = True
        log("AI_ACTION", "AI đã thực hiện BẬT QUẠT 🟢")
        return "Đã bật quạt thông gió thành công."
    else:
        client.publish(config.FEED_FAN, "0")
        fan_on = False
        log("AI_ACTION", "AI đã thực hiện TẮT QUẠT 🔴")
        return "Đã tắt quạt thông gió thành công."

# Danh sách công cụ để AI sử dụng
tools_list = [set_fan_state]


def handle_telegram_cmd(text, chat_id):

    global fan_on
    text = text.lower().strip()
    reply = ""
    
    if text == "/status":
        t_str = f"{last_temp}°C" if last_temp else "--°C"
        h_str = f"{last_humi}%" if last_humi else "--%"
        g_str = f"{last_gas} ppm" if last_gas else "-- ppm"
        fan_str = "Đang BẬT 🟢" if fan_on else "Đang TẮT 🔴"
        reply = f"📊 THÔNG SỐ HIỆN TẠI:\n- Nhiệt độ: {t_str}\n- Độ ẩm: {h_str}\n- Khí Gas: {g_str}\n- Quạt: {fan_str}"
    elif text == "/fan_on":
        client.publish(config.FEED_FAN, "1")
        fan_on = True
        reply = "Đã BẬT quạt từ xa 🟢"
        log("ACTION", "Telegram Command: Fan ACTIVATED 🟢")
    elif text == "/report":
        # AI tổng hợp báo cáo chuyên sâu
        reply = ask_gemini_ai(f"Hãy viết một báo cáo đánh giá an toàn phòng lab chuyên sâu dựa trên thông số hiện tại: T={last_temp}C, H={last_humi}%, G={last_gas}ppm. Nêu rõ rủi ro và khuyến nghị.")
    elif text == "/fan_off":
        reply = set_fan_state("OFF")
    elif text == "/dashboard":
        server_active = is_http_server_active()
        status_msg = "🟢 Đang hoạt động (Bạn có thể truy cập ngay!)" if server_active else "🔴 Chưa hoạt động (Vui lòng chạy `python -m http.server 8000` trên Laptop trước)"
        reply = (
            "🖥️ **HỆ THỐNG GIÁM SÁT LAB - DASHBOARD**\n\n"
            "**1. Trên Máy Tính (Offline File):**\n"
            "Mở đường dẫn sau bằng trình duyệt:\n"
            "`file:///C:/Users/PC/Downloads/ĐAĐN/ĐAĐN/dashboard/dashboard.html`\n\n"
            "**2. Trên Điện Thoại (Web Server local):**\n"
            f"Trạng thái Server: {status_msg}\n"
            "👉 Đường dẫn truy cập: `http://192.168.1.91:8000/dashboard/dashboard.html`\n"
            "*(Lưu ý: Điện thoại và Laptop cần bắt cùng mạng Wi-Fi)*"
        )
    else:
        # TỐI ƯU: Xử lý các câu lệnh phổ biến tại Local (Không tốn Token)
        quick_replies = {
            "bật quạt": lambda: set_fan_state("ON"),
            "mở quạt": lambda: set_fan_state("ON"),
            "tắt quạt": lambda: set_fan_state("OFF"),
            "trạng thái": lambda: f"📊 T:{last_temp}C | H:{last_humi}% | G:{last_gas}ppm | Quạt: {'BẬT' if fan_on else 'TẮT'}"
        }
        
        found_local = False
        for kw, func in quick_replies.items():
            if kw in text:
                reply = f"⚡ [Local] {func()}"
                found_local = True
                break
        
        if not found_local:
            # Chỉ khi không khớp từ khóa local mới gọi AI (Tiết kiệm Token tối đa)
            log("AI", f"Hỏi Gemini: {text}")
            reply = ask_gemini_ai(text)
        
    send_telegram(reply, ignore_cooldown=True)



def register_telegram_commands():
    url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/setMyCommands"
    commands = [
        {"command": "status", "description": "Xem thông số môi trường hiện tại 📊"},
        {"command": "dashboard", "description": "Lấy link mở giao diện Dashboard Web 🖥️"},
        {"command": "fan_on", "description": "Bật quạt thông gió từ xa 🟢"},
        {"command": "fan_off", "description": "Tắt quạt thông gió từ xa 🔴"},
        {"command": "report", "description": "AI phân tích và lập báo cáo an toàn phòng lab 🤖"}
    ]
    try:
        r = requests.post(url, json={"commands": commands}, timeout=5)
        if r.status_code == 200:
            log("SYSTEM", "Đã đăng ký danh sách lệnh gợi ý với Telegram! 📜")
        else:
            log("ERROR", f"Lỗi đăng ký lệnh với Telegram: {r.status_code}")
    except Exception as e:
        log("ERROR", f"Không thể đăng ký lệnh với Telegram: {e}")

def telegram_polling():
    global last_update_id
    
    # Tự động đăng ký danh sách câu lệnh khi khởi động chatbot
    register_telegram_commands()
    
    url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/getUpdates"
    
    while True:
        try:
            payload = {"offset": last_update_id + 1, "timeout": 30}
            r = requests.get(url, params=payload, timeout=35)
            if r.status_code == 200:
                data = r.json()
                for item in data.get("result", []):
                    last_update_id = item["update_id"]
                    msg = item.get("message", {})
                    text = msg.get("text", "")
                    chat_id = msg.get("chat", {}).get("id")
                    
                    if str(chat_id) == config.TELEGRAM_CHAT_ID:
                        handle_telegram_cmd(text, chat_id)
        except Exception:
            pass
        time.sleep(2)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        log("SYSTEM", "RubyAlert Node Online.")
        client.subscribe(config.FEED_FAN)
        client.subscribe(config.MQTT_TOPIC_TELEMETRY) # Lắng nghe cả dữ liệu cảm biến
    else:
        log("ERROR", f"Auth Failed (RC:{rc})")

def process_aiot_logic(t, h, g):
    global fan_on, last_temp, last_humi, last_gas
    
    last_humi = h
    last_gas = g

    log("MONITOR", f"{time.strftime('%H:%M:%S')} | T:{t}°C | H:{h}% | G:{g}")

    # --- BẮT ĐẦU LOGIC AIoT THÔNG MINH ---
    temp_spike = False
    temp_high = t > TEMP_LIMIT
    gas_high = g > GAS_LIMIT
    
    # Tính năng 1: Rate of Change (Phát hiện tăng đột biến)
    if last_temp is not None:
        temp_diff = t - last_temp
        if temp_diff >= 3.0:
            log("AIoT", f"TĂNG ĐỘT BIẾN (+{temp_diff:.1f}°C) 📈")
            temp_spike = True
    last_temp = t

    # Điều khiển quạt dựa trên Hysteresis và cảnh báo Gas
    if temp_high or gas_high:
        if not fan_on:
            client.publish(config.FEED_FAN, "1")
            fan_on = True
    elif t < TEMP_SAFE and g < (GAS_LIMIT * 0.6) and fan_on:
        log("SYSTEM", "Môi trường an toàn. Tự động tắt quạt ❄️")
        client.publish(config.FEED_FAN, "0")
        fan_on = False

    # --- TẠO THÔNG BÁO KHẨN CẤP ĐỒNG BỘ ĐẸP MẮT ---
    if temp_high and gas_high:
        msg = (
            f"🚨 **[RubyAlert] CẢNH BÁO NGUY HIỂM KÉP**\n"
            f"Sự cố: Nhiệt độ quá cao & Rò rỉ khí Gas!\n"
            f"- Nhiệt độ: `{t}°C` (Ngưỡng: {TEMP_LIMIT}°C)\n"
            f"- Khí Gas: `{g} ppm` (Ngưỡng: {GAS_LIMIT} ppm)\n"
            f"Hành động: Đã bật quạt thông gió tự động."
        )
        send_telegram(msg)
        
    elif temp_high:
        msg = (
            f"🚨 **[RubyAlert] CẢNH BÁO NHIỆT ĐỘ**\n"
            f"Sự cố: Nhiệt độ vượt ngưỡng an toàn!\n"
            f"- Nhiệt độ: `{t}°C` (Ngưỡng: {TEMP_LIMIT}°C)\n"
            f"Hành động: Đã bật quạt thông gió tự động."
        )
        if temp_spike:
            msg += "\n⚠️ *Lưu ý: Phát hiện nhiệt độ tăng đột biến!*"
        send_telegram(msg)
        
    elif gas_high:
        msg = (
            f"🚨 **[RubyAlert] CẢNH BÁO KHÍ GAS**\n"
            f"Sự cố: Phát hiện rò rỉ khí Gas/Khói!\n"
            f"- Khí Gas: `{g} ppm` (Ngưỡng: {GAS_LIMIT} ppm)\n"
            f"Hành động: Đã bật quạt thông gió tự động."
        )
        send_telegram(msg)
        
    # Tính năng 3: CẤP ĐỘ 3 - AI Tự động can thiệp sớm (Có Cooldown)
    elif g > (GAS_LIMIT * 0.6) and not fan_on:
        global last_ai_proactive_time
        if 'last_ai_proactive_time' not in globals():
            last_ai_proactive_time = 0
            
        now = time.time()
        # COOLDOWN 5 phút (300 giây): AI chỉ tự phân tích 1 lần mỗi 5 phút
        if now - last_ai_proactive_time > 300:
            log("AI_PROACTIVE", f"Khí Gas mức rủi ro ({g} ppm). Kích hoạt AI tự trị...")
            # Ép AI trả lời cực ngắn để tiết kiệm Token
            ai_eval = ask_gemini_ai(f"Gas={g}ppm (Mức nguy hiểm). Hãy gọi tool bật quạt và trả lời < 15 chữ lý do.")
            
            msg = (
                f"⚠️ **[RubyAlert] TỰ ĐỘNG BẢO VỆ (AI)**\n"
                f"Trạng thái: Khí gas tăng nhẹ (`{g} ppm`)\n"
                f"Hành động: Bật quạt thông gió phòng ngừa.\n"
                f"AI phân tích: {ai_eval}"
            )
            send_telegram(msg)
            last_ai_proactive_time = now
        else:
            # Nếu đang trong thời gian Cooldown AI, Local tự xử lý (Free Token)
            client.publish(config.FEED_FAN, "1")
            fan_on = True
            log("LOCAL_PROACTIVE", "Bật quạt phòng ngừa (Local Fallback - Tiết kiệm Token)")
            
            msg = (
                f"⚠️ **[RubyAlert] TỰ ĐỘNG BẢO VỆ**\n"
                f"Trạng thái: Khí gas tăng nhẹ (`{g} ppm`)\n"
                f"Hành động: Tự động bật quạt phòng ngừa."
            )
            send_telegram(msg)

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    
    if topic == config.FEED_FAN:
        status = "ACTIVATED 🟢" if payload=="1" else "DEACTIVATED 🔴"
        log("ACTION", f"External Command: Fan {status}")
    
    elif topic == config.MQTT_TOPIC_TELEMETRY:
        try:
            data = json.loads(payload)
            if isinstance(data, dict) and "temperature" in data:
                # Xử lý logic AIoT
                process_aiot_logic(data["temperature"], data["humidity"], data["gas"])
            else:
                log("DEBUG", f"Nhận dữ liệu không đúng định dạng JSON RubyAlert: {payload}")
        except Exception as e:
            log("ERROR", f"Lỗi xử lý dữ liệu từ {topic}: {e}")


client = mqtt.Client("RubyAlert_AIoT_Node")
client.username_pw_set(config.OHSTEM_USERNAME, config.OHSTEM_KEY)
client.on_connect = on_connect
client.on_message = on_message

def simulator_loop():
    while True:
        t = round(random.uniform(25, 40), 1)
        h = round(random.uniform(50, 90), 1)
        g = random.randint(300, 2500)

        # Đã sửa: Sử dụng phím chuỗi trực tiếp để tránh lỗi parse
        payload = {"temperature": t, "humidity": h, "gas": g}
        client.publish(config.MQTT_TOPIC_TELEMETRY, json.dumps(payload))
        time.sleep(10)


def run_system():
    # Bắt đầu luồng lắng nghe Telegram
    tg_thread = threading.Thread(target=telegram_polling, daemon=True)
    tg_thread.start()

    # Bắt đầu luồng giả lập nếu đang ở chế độ mô phỏng
    if SIMULATION_MODE:
        sim_thread = threading.Thread(target=simulator_loop, daemon=True)
        sim_thread.start()

    try:
        client.connect(config.MQTT_SERVER, config.MQTT_PORT, 60)
        
        print("\n" + "="*50)
        print(f"   RUBYALERT: AIoT ALARM SYSTEM ACTIVE")
        print(f"   MODE: {'SIMULATION' if SIMULATION_MODE else 'HARDWARE (ESP32)'}")
        print("="*50 + "\n")
        
        # Gửi tin nhắn khởi động kèm đường dẫn Dashboard Web
        server_active = is_http_server_active()
        status_msg = "🟢 Đang hoạt động" if server_active else "🔴 Chưa hoạt động *(chạy `python -m http.server 8000` để bật)*"
        
        send_telegram(
            "🚀 **Hệ thống giám sát phòng Lab RubyAlert đã ONLINE!**\n\n"
            "🖥️ **Dashboard Web:**\n"
            "- **PC:** `file:///C:/Users/PC/Downloads/ĐAĐN/ĐAĐN/dashboard/dashboard.html`\n"
            f"- **Mobile:** `http://192.168.1.91:8000/dashboard/dashboard.html` ({status_msg})\n\n"
            "💬 Gõ `/status` để xem thông số, `/dashboard` để lấy lại link, hoặc chat tự do bằng tiếng Việt để hỏi mình nhé!", 
            ignore_cooldown=True
        )
        
        client.loop_forever() # Hàm này sẽ block thread chính để lắng nghe MQTT

    except KeyboardInterrupt:
        log("EXIT", "RubyAlert System Offline.")
        client.disconnect()
    except Exception as e:
        log("CRASH", str(e))

if __name__ == "__main__":
    run_system()

import serial
import pyautogui
import time
import pyperclip
import threading

# تنظیمات پورت
SERIAL_PORT = 'COM2'  
BAUD_RATE = 9600

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    print(f"Connected to {SERIAL_PORT}")
except Exception as e:
    print(f"Error: {e}")
    exit()

def send_data_to_mcu(text):
    print(f">> Sending to MCU: {text}")
    for char in text:
        ser.write(char.encode())
        # *** تغییر مهم: افزایش تاخیر به 100 میلی ثانیه ***
        # این به میکروکنترلر فرصت میدهد تا کاراکتر را پردازش و در آرایه ذخیره کند
        time.sleep(0.1) 
    
    ser.write(b'\n') # پایان خط
    time.sleep(0.1)

def listen_to_serial():
    buffer = ""
    print("Waiting for commands...")
    while True:
        try:
            if ser.in_waiting > 0:
                char = ser.read().decode('utf-8', errors='ignore')
                
                if char == '\n':
                    command = buffer.strip()
                    buffer = ""
                    process_command(command)
                else:
                    buffer += char
        except Exception as e:
            print(f"Error: {e}")

def process_command(cmd):
    print(f"Received: {cmd}")
    
    if cmd.startswith("CMD:RUN"):
        pyautogui.hotkey('win', 'r')
        
    elif cmd.startswith("TYPE:"):
        text = cmd[5:]
        pyautogui.write(text, interval=0.01)
        
    elif cmd.startswith("KEY:ENTER"):
        pyautogui.press('enter')
        
    elif cmd.startswith("ACTION:GET_CLIP"):
        print("Waiting for valid IP in clipboard...")
        
        # حلقه تلاش برای خواندن کلیپ بورد
        # حداکثر 10 ثانیه صبر میکند
        max_retries = 20
        content = ""
        
        for i in range(max_retries):
            content = pyperclip.paste().strip()
            # شرط: متن خالی نباشد AND داخلش نقطه باشد (فرمت IP)
            if content and "." in content and "python" not in content:
                break
            
            time.sleep(0.5)
            print(f"Attempt {i+1}: Clipboard empty or invalid, waiting...")
            
        if not content:
            content = "IP_NOT_FOUND" # اگر پیدا نشد این را بفرست

        print(f"Clipboard content: {content}")
        send_data_to_mcu(content)


if __name__ == "__main__":
    # پاک کردن کلیپ بورد قبل از شروع برای جلوگیری از ارسال دیتای قدیمی
    pyperclip.copy("") 
    listen_to_serial()

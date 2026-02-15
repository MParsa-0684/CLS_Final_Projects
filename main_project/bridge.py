import serial
import pyautogui
import time
import pyperclip
import sys

# تنظیمات پورت
SERIAL_PORT = 'COM2'  
BAUD_RATE = 4800

print("--- Bridge Started ---")

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    print(f"Connected to {SERIAL_PORT}")
except Exception as e:
    print(f"Error opening serial port: {e}")
    sys.exit()

def send_to_mcu(text):
    print(f">> [TX] Sending: {text}")
    for char in text:
        ser.write(char.encode())
        time.sleep(0.05) # <--- افزایش تاخیر از 0.02 به 0.05 برای اطمینان بیشتر
    ser.write(b'\n')
    time.sleep(0.1)

def process_command(cmd):
    # چاپ دستورات برای دیباگ
    if cmd.startswith("DEBUG:"):
        print(f"@@ [MCU LOG]: {cmd[6:]}")
        return

    print(f"<< [RX] CMD: {cmd}")
    
    if cmd == "CMD:RUN":
        pyautogui.hotkey('win', 'r')
        
    elif cmd.startswith("TYPE:"):
        text = cmd[5:]
        pyautogui.write(text, interval=0.005)
        
    elif cmd == "KEY:ENTER":
        pyautogui.press('enter')
        
    elif cmd == "ACTION:GET_CLIP":
        print("   -> MCU requested Clipboard.")
        time.sleep(1) # صبر کوتاه برای اطمینان از پر شدن کلیپ بورد توسط سیستم عامل
        
        content = "IP_NOT_FOUND"
        for _ in range(10): # 10 بار تلاش
            temp = pyperclip.paste().strip()
            if temp and "." in temp and "python" not in temp:
                content = temp
                break
            time.sleep(0.5)
            
        print(f"   -> Found in Clip: {content}")
        send_to_mcu(content)

def main_loop():
    buffer = ""
    while True:
        try:
            if ser.in_waiting > 0:
                # خواندن کاراکتر به کاراکتر برای دقت بیشتر
                char = ser.read().decode('utf-8', errors='ignore')
                
                if char == '\n':
                    cmd = buffer.strip()
                    buffer = ""
                    if cmd:
                        process_command(cmd)
                else:
                    buffer += char
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    pyperclip.copy("") 
    main_loop()

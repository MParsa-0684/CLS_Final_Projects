import serial
import pyautogui
import time
import threading
import sys

# تنظیمات: این پورت باید جفت پورت پروتئوس باشد
SERIAL_PORT = 'COM2' 
BAUD_RATE = 9600

def handle_incoming_data(ser):
    """داده‌ها را از پروتئوس می‌خواند و اجرا می‌کند"""
    print(f"[*] Listening for BadUSB commands on {SERIAL_PORT}...")
    buffer = ""
    
    while True:
        try:
            if ser.in_waiting > 0:
                # خواندن کاراکتر به کاراکتر
                char = ser.read().decode('utf-8', errors='ignore')
                
                # تشخیص پایان دستور (Enter یا کاراکتر خاص)
                if char == '\n' or char == '\r':
                    if not buffer: continue
                    
                    print(f"[>] Command Received: {buffer}")
                    
                    if buffer.startswith("CMD:RUN"):
                        # باز کردن Run ویندوز
                        pyautogui.hotkey('win', 'r')
                        time.sleep(0.5)
                        
                    elif buffer.startswith("TYPE:"):
                        # تایپ کردن متن
                        text_to_type = buffer[5:] # حذف TYPE: از اول رشته
                        pyautogui.write(text_to_type, interval=0.01)
                        
                    elif buffer.startswith("KEY:ENTER"):
                        pyautogui.press('enter')
                        
                    buffer = "" # خالی کردن بافر
                else:
                    buffer += char
        except Exception as e:
            print(f"Error reading: {e}")
            break

def send_led_status(ser):
    """وضعیت CapsLock را به پروتئوس می‌فرستد (برای فاز استخراج)"""
    # در ویندوز برای خواندن وضعیت LED نیاز به کتابخانه‌های خاص است
    # اینجا برای سادگی فرض می‌کنیم اگر CapsLock روشن باشد کاراکتر '1' میفرستد
    import ctypes
    
    last_caps = -1
    
    while True:
        hllDll = ctypes.WinDLL("User32.dll")
        VK_CAPITAL = 0x14
        caps_on = hllDll.GetKeyState(VK_CAPITAL) & 1
        
        if caps_on != last_caps:
            if caps_on:
                ser.write(b'1') # ارسال به پروتئوس
                print("[<] Sent CapsLock ON to MCU")
            else:
                ser.write(b'0')
                print("[<] Sent CapsLock OFF to MCU")
            last_caps = caps_on
            
        time.sleep(0.2)

if __name__ == "__main__":
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
        # اجرای تردها برای خواندن و نوشتن همزمان
        t1 = threading.Thread(target=handle_incoming_data, args=(ser,))
        t2 = threading.Thread(target=send_led_status, args=(ser,))
        t1.start()
        t2.start()
        t1.join()
    except serial.SerialException:
        print(f"Error: Could not open {SERIAL_PORT}. Make sure com0com is running.")

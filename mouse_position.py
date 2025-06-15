import pyautogui
import time

print("กรุณาเลื่อนเมาส์ไปยังตำแหน่งที่ต้องการดูพิกัด (Ctrl+C เพื่อหยุด)")

try:
    while True:
        x, y = pyautogui.position()
        position_str = f"ตำแหน่งเมาส์: ({x}, {y})"
        print(position_str, end='\r')
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nหยุดการแสดงผลแล้ว")

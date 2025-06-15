import pyautogui
import threading
import time
import tkinter as tk

# ข้อมูลลำดับการกด: (label, x, y, wait_time)
steps = [
    # Step 1
    ("รีเซ็ตแผนที่", 442, 265, 4),
    ("ยืนยัน", 896, 466, 4),
    ("เลือกด่าน 1", 573, 563, 4),
    ("เข้าสู่ด่าน 1", 1166, 586, 40),  # เวลาจริง 36
    ("ยืนยันด่าน 1", 1076, 525, 4),
    ("เลือกอวยพรด่าน 1", 832, 582, 4),

    # Step 2
    ("เลือกด่าน 2", 673, 481, 4),
    ("เข้าสู่ด่าน 2", 1166, 586, 4),  
    ("ยืนยันเข้าสู่ด่าน 2", 889, 464, 70), # เวลาจริง 53
    ("ยืนยันด่าน 2", 1076, 525, 4),
    ("เลือกอวยพรด่าน 2", 832, 582, 4),

    # Step 3
    ("เลือกด่าน 3", 914, 534, 4),
    ("เข้าสู่ด่าน 3", 1166, 586, 4),
    ("ยืนยันด่าน 3", 1076, 525, 30),
]

running = False

def bot_loop():
    global running
    while running:
        for label, x, y, wait in steps:
            if not running:
                break
            print(f"👉 กด: {label} ที่ ({x}, {y}) แล้วรอ {wait} วินาที")
            pyautogui.click(x, y)
            time.sleep(wait)
        print("🌀 รอโหลดก่อนเริ่มรอบใหม่...")
        time.sleep(15)  # เพิ่มเวลารอโหลดก่อนเริ่มรอบใหม่


def start_bot():
    status_label.config(text="สลับไปเปิดเจอเกมเลย... และรอ 20 วิ")
    time.sleep(20)
    global running
    if not running:
        running = True
        threading.Thread(target=bot_loop, daemon=True).start()
        status_label.config(text="กำลังเก็บเห็ดด...")

def stop_bot():
    global running
    running = False
    status_label.config(text="หยุดทำงานแล้ว")

# GUI
root = tk.Tk()
root.title("แชมป์นักเก็บเห็ด")
root.geometry("300x180")

start_button = tk.Button(root, text="▶ Start", command=start_bot, font=("Arial", 14), width=12)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="⏹ Stop", command=stop_bot, font=("Arial", 14), width=12)
stop_button.pack(pady=5)

status_label = tk.Label(root, text="ยังไม่เริ่มทำงาน", font=("Arial", 12))
status_label.pack(pady=10)

note_label = tk.Label(root, text="ESC เพื่อหยุดฉุกเฉิน", font=("Arial", 10), fg="gray")
note_label.pack()

root.mainloop()

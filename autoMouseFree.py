import tkinter as tk
from tkinter import ttk, messagebox
from pynput import mouse
import pyautogui
import threading
import time
from datetime import datetime

click_steps = []
recording = False
last_time = None
running = False
round_count = 0
recording_active = False

expiry_date = datetime.strptime("2025-07-15", "%Y-%m-%d")

def check_expiry():
    today = datetime.now()
    if today > expiry_date:
        messagebox.showerror("หมดอายุ", f"โปรแกรมนี้หมดอายุการใช้งานตั้งแต่วันที่ {expiry_date.strftime('%d/%m/%Y')}")
        return False
    return True

def on_click(x, y, button, pressed):
    global last_time
    if pressed and recording and recording_active:
        now = time.time()
        wait_time = 4.0 if len(click_steps) == 0 else round(now - last_time, 2)
        last_time = now
        step_number = len(click_steps) + 1
        step = {'label': f'Step {step_number}', 'x': x, 'y': y, 'wait': wait_time}
        click_steps.append(step)
        tree.insert('', 'end', values=(step['label'], f"{wait_time:.2f}"))

def start_recording():
    global recording, last_time, click_steps, recording_active
    clear_all_steps()
    recording = True
    recording_active = True
    last_time = None
    status_label.config(text="🎥 กำลังบันทึก... คลิกเมาส์เพื่อบันทึกตำแหน่ง")

def stop_recording():
    global recording, recording_active
    recording = False
    recording_active = False
    status_label.config(text="⏹ หยุดบันทึกแล้ว สามารถแก้ไขเวลาได้")

def run_bot():
    global running, round_count
    if not running and click_steps:
        if not check_expiry():
            return
        running = True
        round_count = 0
        threading.Thread(target=countdown_and_run, daemon=True).start()

def countdown_and_run():
    for i in range(20, 0, -1):
        status_label.config(text=f"⏳ รอสลับหน้าจอเกม... ({i})")
        time.sleep(1)
    save_wait_times()
    status_label.config(text="🚀 เริ่มทำงานแล้ว...")
    time.sleep(1)
    bot_loop()

def stop_bot():
    global running
    running = False
    status_label.config(text="⏸ หยุดทำงานแล้ว สามารถแก้ไขเวลาได้")

def bot_loop():
    global running, round_count
    while running:
        for i, step in enumerate(click_steps):
            if not running:
                break
            x, y = step.get('x'), step.get('y')
            wait = step.get('wait', 0)
            print(f"👉 Step {i+1}: Click at ({x}, {y}) then wait {wait} sec")
            pyautogui.click(x, y)
            time.sleep(wait)
        round_count += 1
        status_label.config(text=f"🔁 ทำงานสำเร็จไปแล้ว {round_count} รอบ รอก่อนเริ่มรอบใหม่...")
        time.sleep(10)

def delete_selected():
    selected = tree.selection()
    for sel in reversed(selected):
        idx = tree.index(sel)
        tree.delete(sel)
        del click_steps[idx]
    update_labels()

def clear_all_steps():
    global click_steps
    for item in tree.get_children():
        tree.delete(item)
    click_steps = []
    status_label.config(text="🧹 ล้างขั้นตอนทั้งหมดแล้ว")

def update_labels():
    for i, step in enumerate(click_steps):
        step['label'] = f'Step {i+1}'
        tree.item(tree.get_children()[i], values=(step['label'], f"{step['wait']:.2f}"))

def save_wait_times():
    items = tree.get_children()
    for i, item in enumerate(items):
        try:
            new_wait = float(tree.item(item, 'values')[1])
            click_steps[i]['wait'] = new_wait
        except ValueError:
            pass
        except IndexError:
            continue
    update_labels()
    status_label.config(text="💾 บันทึกเวลาเรียบร้อยแล้ว")

def on_double_click(event):
    if running:
        return
    item_id = tree.focus()
    if not item_id:
        return
    col = tree.identify_column(event.x)
    if col != '#2':
        return

    x, y, width, height = tree.bbox(item_id, column=col)
    entry = tk.Entry(tree)
    entry.place(x=x, y=y, width=width, height=height)
    entry.insert(0, tree.item(item_id, 'values')[1])
    entry.focus()

    def on_enter(event):
        new_value = entry.get()
        try:
            float(new_value)
            tree.set(item_id, column=col, value=new_value)
        except ValueError:
            pass
        entry.destroy()

    entry.bind("<Return>", on_enter)
    entry.bind("<FocusOut>", lambda e: entry.destroy())

# GUI
root = tk.Tk()
root.title("🍄 Bot Auto Mouse By ChampChamp ฟรีห้ามซื้อขาย(ตัวทดลอง)")
root.geometry("520x510")

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="🎥 เริ่มบันทึก", command=start_recording, bg="lightgreen").grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="⏹ หยุดบันทึก", command=stop_recording, bg="tomato").grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="🗑 ลบ Step", command=delete_selected, bg="orange").grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="🧹 ล้างทั้งหมด", command=clear_all_steps, bg="lightgray").grid(row=0, column=3, padx=5)

tree = ttk.Treeview(root, columns=('label', 'wait'), show='headings', height=13)
tree.heading('label', text='ขั้นตอน')
tree.heading('wait', text='เวลารอ (วินาที)')
tree.column('label', width=250)
tree.column('wait', width=100)
tree.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
tree.bind('<Double-1>', on_double_click)

scrollbar = ttk.Scrollbar(root, orient='vertical', command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side='right', fill='y')

save_frame = tk.Frame(root)
save_frame.pack(pady=5)

tk.Button(save_frame, text="💾 บันทึกเวลา", command=save_wait_times).pack(side=tk.LEFT, padx=10)
tk.Button(save_frame, text="▶ เริ่มรัน", command=run_bot, bg="deepskyblue").pack(side=tk.LEFT, padx=10)
tk.Button(save_frame, text="⏸ หยุดรัน", command=stop_bot).pack(side=tk.LEFT, padx=10)

status_label = tk.Label(root, text="พร้อมทำงาน", font=("Arial", 10))
status_label.pack(pady=5)

listener = mouse.Listener(on_click=on_click)
listener.start()

root.mainloop()

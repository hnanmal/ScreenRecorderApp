import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap import ttk
from ttkbootstrap.constants import *
import pyautogui
import cv2
import numpy as np
import threading
import datetime


class ScreenRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("화면 녹화기")
        self.root.geometry("300x200")
        self.style = Style("cyborg")

        self.recording = False

        self.start_button = ttk.Button(
            root, text="녹화 시작", bootstyle="success", command=self.start_recording
        )
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(
            root,
            text="녹화 중지",
            bootstyle="danger",
            command=self.stop_recording,
            state=tk.DISABLED,
        )
        self.stop_button.pack(pady=10)

        self.status_label = ttk.Label(root, text="대기 중...", bootstyle="info")
        self.status_label.pack(pady=20)

    def start_recording(self):
        self.recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="녹화 중...")

        self.thread = threading.Thread(target=self.record_screen)
        self.thread.start()

    def stop_recording(self):
        self.recording = False
        self.stop_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)
        self.status_label.config(text="저장 완료")

    def record_screen(self):
        screen_size = pyautogui.size()
        filename = datetime.datetime.now().strftime("recording_%Y%m%d_%H%M%S.avi")
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(filename, fourcc, 10.0, screen_size)

        while self.recording:
            img = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            out.write(frame)

        out.release()


if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenRecorderApp(root)
    root.mainloop()

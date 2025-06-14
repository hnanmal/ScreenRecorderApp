# src/views/main_view.py
import tkinter as tk
from ttkbootstrap import ttk
from src.viewmodels.screen_vm import ScreenRecorderViewModel
from src.views.region_selector import RegionSelector  # 👈 추가

class ScreenRecorderView:
    def __init__(self, root):
        self.root = root
        self.root.title("화면 녹화기")
        self.root.geometry("300x250")

        self.vm = ScreenRecorderViewModel()

        # 📦 영역 선택 버튼
        self.select_button = ttk.Button(root, text="영역 선택", bootstyle="secondary", command=self.select_region)
        self.select_button.pack(pady=10)

        # ▶️ 녹화 시작
        self.start_button = ttk.Button(root, text="녹화 시작", bootstyle="success", command=self.start)
        self.start_button.pack(pady=10)

        # ⏹️ 녹화 중지
        self.stop_button = ttk.Button(root, text="녹화 중지", bootstyle="danger", command=self.stop, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.status_label = ttk.Label(root, text="대기 중...", bootstyle="info")
        self.status_label.pack(pady=20)

    def select_region(self):
        selector = RegionSelector()
        region = selector.select_region()
        if region:
            self.vm.set_region(region)
            self.status_label.config(text=f"영역: {region[0]}, {region[1]}, {region[2]}×{region[3]}")

    def start(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="녹화 중...")
        self.vm.start_recording(on_done=self.recording_finished)

    def stop(self):
        self.vm.stop_recording()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="저장 완료")

    def recording_finished(self):
        pass

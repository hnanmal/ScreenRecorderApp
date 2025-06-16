# src/views/main_view.py
import tkinter as tk
from tkinter import ttk

# from ttkbootstrap import ttk
from src.viewmodels.screen_vm import ScreenRecorderViewModel
from src.views.region_selector import RegionSelector
from src.views.overlay_box import OverlayBox  # 👈 추가


class ScreenRecorderView:
    def __init__(self, root):
        self.root = root
        self.root.title("화면 녹화기")
        self.root.geometry("300x250")
        self.overlay = None  # 반드시 추가

        self.vm = ScreenRecorderViewModel()

        # 📦 영역 선택 버튼
        self.select_button = ttk.Button(
            root,
            text="영역 선택",
            # bootstyle="secondary",
            command=self.select_region,
        )
        self.select_button.pack(pady=10)

        # ▶️ 녹화 시작
        self.start_button = ttk.Button(
            root,
            text="녹화 시작",
            # bootstyle="success",
            command=self.start,
        )
        self.start_button.pack(pady=10)

        # ⏹️ 녹화 중지
        self.stop_button = ttk.Button(
            root,
            text="녹화 중지",
            # bootstyle="danger",
            command=self.stop,
            state=tk.DISABLED,
        )
        self.stop_button.pack(pady=10)

        self.status_label = ttk.Label(
            root,
            text="대기 중...",
            # bootstyle="info",
        )
        self.status_label.pack(pady=20)

    def select_region(self):
        print("[DEBUG] select_region() called")
        selector = RegionSelector()
        region = selector.select_region()  # mainloop 종료 후 여기 실행됨
        selector.root.destroy()  # ✅ 이제 안전하게 창 닫기
        self.vm.set_region(region)
        print(f"[DEBUG] region from selector: {region}")

        if region:
            x, y, w, h = map(int, region)
            print("[DEBUG] OverlayBox 생성 예약")
            self.root.after(10, lambda: self.create_overlay_box(x, y, w, h))

    def create_overlay_box(self, x, y, w, h):
        print(f"[OverlayBox] 진짜 생성 시작")
        self.overlay = OverlayBox(x, y, w, h)

    def start(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="녹화 중...")

        # ✅ 녹화 중 Overlay 유지 – 아무것도 하지 않음
        self.vm.start_recording(on_done=self.recording_finished)

    def stop(self):
        self.vm.stop_recording()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="저장 완료")

        # ✅ 녹화 중이 끝났을 때에만 Overlay 제거
        if hasattr(self, "overlay") and self.overlay:
            self.overlay.close()
            self.overlay = None

    def recording_finished(self):
        pass

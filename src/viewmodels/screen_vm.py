# src/viewmodels/screen_vm.py
import threading
from tkinter import messagebox
from src.services.recorder import ScreenRecorder
from src.views.overlay_box import OverlayBox  # 👈 추가


class ScreenRecorderViewModel:
    def __init__(self, root):
        self.root = root  # Tk 인터페이스 객체 저장
        self.recorder = ScreenRecorder(root)
        self.is_recording = False
        self.region = None
        self.overlay = None
        self.output_path = None

    def set_region(self, region):
        self.region = region

    def start_recording(self, on_done=None):
        self.is_recording = True

        # # ✅ 녹화 영역 오버레이 표시
        # if self.region:
        #     x, y, w, h = map(int, self.region)
        #     self.overlay = OverlayBox(x, y, w, h)

        self.thread = threading.Thread(target=self._record_and_notify, args=(on_done,))
        self.thread.start()

    # def _record_and_notify(self, on_done):
    #     self.recorder.start(region=self.region, output_path=self.output_path)  # ✅ 수정
    #     if on_done:
    #         on_done()
    #         # self.root.after(0, on_done)

    def _record_and_notify(self, on_done):
        self.recorder.start(region=self.region, output_path=self.output_path)
        if on_done:
            # 🔽 root.after가 메인 스레드에서 호출되도록 안전하게 래핑
            def safe_notify():
                print(f"[Thread] 현재 스레드: {threading.current_thread().name}")
                print(f"[Mainloop Running?] {self.root.tk.call('info', 'exists', '.')}")
                on_done()

            try:
                self.root.after(0, safe_notify)
            except RuntimeError as e:
                print("[ERROR] Tkinter mainloop not running:", e)

    def stop_recording(self):
        self.recorder.stop()
        self.is_recording = False

        # ✅ 오버레이 제거
        if self.overlay:
            self.overlay.close()
            self.overlay = None

    def set_output_path(self, path):
        self.output_path = path

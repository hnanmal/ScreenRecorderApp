# src/viewmodels/screen_vm.py
import threading
from src.services.recorder import ScreenRecorder
from src.views.overlay_box import OverlayBox  # 👈 추가


class ScreenRecorderViewModel:
    def __init__(self):
        self.recorder = ScreenRecorder()
        self.is_recording = False
        self.region = None
        self.overlay = None

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

    def _record_and_notify(self, on_done):
        self.recorder.start(region=self.region, output_path=self.output_path)  # ✅ 수정
        if on_done:
            on_done()

    def stop_recording(self):
        self.recorder.stop()
        self.is_recording = False

        # ✅ 오버레이 제거
        if self.overlay:
            self.overlay.close()
            self.overlay = None

    def set_output_path(self, path):
        self.output_path = path

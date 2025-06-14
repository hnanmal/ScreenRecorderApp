# src/viewmodels/screen_vm.py
import threading
from src.services.recorder import ScreenRecorder


class ScreenRecorderViewModel:
    def __init__(self):
        self.recorder = ScreenRecorder()
        self.is_recording = False
        self.region = None

    def start_recording(self, on_done=None):
        self.is_recording = True
        self.thread = threading.Thread(target=self._record_and_notify, args=(on_done,))
        self.thread.start()

    def _record_and_notify(self, on_done):
        # ✅ region 정보를 넘겨줌
        self.recorder.start(region=self.region)
        if on_done:
            on_done()

    def stop_recording(self):
        self.recorder.stop()
        self.is_recording = False

    def set_region(self, region):
        self.region = region

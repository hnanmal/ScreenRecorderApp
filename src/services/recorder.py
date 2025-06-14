# src/services/recorder.py
import mss
import cv2
import numpy as np
import datetime


class ScreenRecorder:
    def __init__(self):
        self.recording = False
        self.out = None

    def start(self, region=None):
        if region:
            x, y, w, h = map(int, region)
            monitor = {"top": y, "left": x, "width": w, "height": h}
            screen_size = (w, h)
            print(f"[DEBUG] 녹화 영역: {monitor}")
        else:
            with mss.mss() as sct:
                monitor = sct.monitors[1]  # 전체 모니터
                screen_size = (monitor["width"], monitor["height"])
                print(f"[DEBUG] 전체 화면 녹화: {screen_size}")

        filename = datetime.datetime.now().strftime("recording_%Y%m%d_%H%M%S.avi")
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.out = cv2.VideoWriter(filename, fourcc, 10.0, screen_size)
        self.recording = True

        with mss.mss() as sct:
            while self.recording:
                try:
                    sct_img = sct.grab(monitor)
                    frame = np.array(sct_img)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                    self.out.write(frame)
                except Exception as e:
                    print(f"[ERROR] 캡처 오류: {e}")
                    break

        self.out.release()
        print("[INFO] 녹화 완료:", filename)

    def stop(self):
        self.recording = False

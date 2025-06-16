# src/services/recorder.py
import mss
import cv2
import numpy as np
import datetime


class ScreenRecorder:
    def __init__(self):
        self.recording = False
        self.out = None
        self.monitor = None

    def start(self, region=None):
        with mss.mss() as sct:
            if region:
                x, y, w, h = map(int, region)
                # 💡 다중 모니터 환경 고려
                for monitor in sct.monitors[1:]:  # monitors[0]은 전체, [1:]은 개별
                    mx, my, mw, mh = (
                        monitor["left"],
                        monitor["top"],
                        monitor["width"],
                        monitor["height"],
                    )
                    if mx <= x < mx + mw and my <= y < my + mh:
                        # 보정된 전체 좌표로 변환
                        abs_x = x
                        abs_y = y
                        monitor_dict = {
                            "top": abs_y,
                            "left": abs_x,
                            "width": w,
                            "height": h,
                        }
                        print(f"[DEBUG] 선택 영역 모니터: {monitor}")
                        break
                else:
                    print(
                        "[WARNING] 선택 영역이 어떤 모니터에도 속하지 않음. 기본 모니터 사용"
                    )
                    monitor_dict = {"top": y, "left": x, "width": w, "height": h}

                screen_size = (w, h)
            else:
                monitor = sct.monitors[1]
                monitor_dict = monitor
                screen_size = (monitor["width"], monitor["height"])
                print(f"[DEBUG] 전체 화면 녹화 시작: {monitor}")

            # 🔴 VideoWriter 설정
            filename = datetime.datetime.now().strftime("recording_%Y%m%d_%H%M%S.avi")
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            self.out = cv2.VideoWriter(filename, fourcc, 10.0, screen_size)
            self.recording = True

            while self.recording:
                try:
                    sct_img = sct.grab(monitor_dict)
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

    def _detect_monitor(self, x, y):
        with mss.mss() as sct:
            for i, m in enumerate(sct.monitors[1:], start=1):
                if (m["left"] <= x < m["left"] + m["width"]) and (
                    m["top"] <= y < m["top"] + m["height"]
                ):
                    print(f"[DEBUG] Region starts on monitor {i}: {m}")
                    return i, m
        print("[WARN] Monitor not detected, fallback to primary")
        return 1, sct.monitors[1]

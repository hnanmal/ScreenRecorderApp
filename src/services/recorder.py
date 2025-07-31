# src/services/recorder.py
import mss
import cv2
import numpy as np
import datetime
import win32api
import win32gui
from PIL import Image, ImageDraw


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
            # filename = datetime.datetime.now().strftime("recording_%Y%m%d_%H%M%S.avi")
            # fourcc = cv2.VideoWriter_fourcc(*"XVID")
            filename = datetime.datetime.now().strftime("recording_%Y%m%d_%H%M%S.mp4")
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")

            self.out = cv2.VideoWriter(filename, fourcc, 10.0, screen_size)
            self.recording = True

            while self.recording:
                try:
                    sct_img = sct.grab(monitor_dict)
                    frame = np.array(sct_img)  # BGRA

                    # ✅ PIL 이미지로 변환하여 커서 합성
                    pil_img = Image.fromarray(frame)

                    # 마우스 커서 좌표
                    cx, cy = win32api.GetCursorPos()

                    # 모니터 좌상단 기준으로 상대좌표로 변환
                    rel_x = cx - monitor_dict["left"]
                    rel_y = cy - monitor_dict["top"]

                    if (
                        0 <= rel_x < monitor_dict["width"]
                        and 0 <= rel_y < monitor_dict["height"]
                    ):
                        draw = ImageDraw.Draw(pil_img)
                        draw.ellipse(
                            (rel_x - 5, rel_y - 5, rel_x + 5, rel_y + 5), fill="red"
                        )

                    # 다시 numpy로 변환 후 BGR 색공간으로 변환
                    frame_with_cursor = cv2.cvtColor(
                        np.array(pil_img), cv2.COLOR_RGBA2BGR
                    )

                    self.out.write(frame_with_cursor)

                except Exception as e:
                    print(f"[ERROR] 캡처 오류: {e}")
                    break

            # while self.recording:
            #     try:
            #         sct_img = sct.grab(monitor_dict)
            #         frame = np.array(sct_img)
            #         frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            #         self.out.write(frame)
            #     except Exception as e:
            #         print(f"[ERROR] 캡처 오류: {e}")
            #         break

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

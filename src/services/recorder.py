import sys
import mss
import cv2
import numpy as np
import datetime
import time
import os
import subprocess
import win32api
from PIL import Image, ImageDraw


def get_ffmpeg_path():
    if getattr(sys, "frozen", False):  # PyInstaller 패키징된 실행파일
        base_path = sys._MEIPASS
        return os.path.join(base_path, "resources", "bin", "ffmpeg.exe")
    else:
        return os.path.join("resources", "bin", "ffmpeg.exe")


class ScreenRecorder:
    def __init__(self):
        self.recording = False
        self.out = None
        self.monitor = None

    def set_output_path(self, path):
        self.output_path = path

    def start_recording(self):
        self.recorder.start(region=self.region, output_path=self.output_path)

    def start(self, region=None, output_path=None):
        with mss.mss() as sct:
            if region:
                x, y, w, h = map(int, region)
                for monitor in sct.monitors[1:]:
                    mx, my, mw, mh = (
                        monitor["left"],
                        monitor["top"],
                        monitor["width"],
                        monitor["height"],
                    )
                    if mx <= x < mx + mw and my <= y < my + mh:
                        abs_x, abs_y = x, y
                        offset = 2
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

            # 파일명 및 코덱 설정
            filename = output_path  # ✅ output_path는 파일 전체 경로!

            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            self.out = cv2.VideoWriter(filename, fourcc, 10.0, screen_size)
            self.recording = True

            fps = 10.0

            while self.recording:
                start_time = time.time()
                try:
                    sct_img = sct.grab(monitor_dict)
                    frame = np.array(sct_img)  # BGRA → PIL

                    pil_img = Image.fromarray(frame)
                    cx, cy = win32api.GetCursorPos()
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

                    frame_with_cursor = cv2.cvtColor(
                        np.array(pil_img), cv2.COLOR_RGBA2BGR
                    )
                    self.out.write(frame_with_cursor)

                except Exception as e:
                    print(f"[ERROR] 캡처 오류: {e}")
                    break

                # 일정한 프레임 간격 유지
                elapsed = time.time() - start_time
                time.sleep(max(0, 1.0 / fps - elapsed))

            self.out.release()
            print("[INFO] 녹화 완료:", filename)

            # 🔁 ffmpeg로 재인코딩 (PowerPoint 최적화)
            self.reencode_with_ffmpeg(filename)

    def reencode_with_ffmpeg(self, input_path):
        # output_path = input_path.replace(".mp4", "_fixed.mp4")
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_fixed{ext}"
        cmd = [
            get_ffmpeg_path(),
            "-y",
            "-i",
            input_path,
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-r",
            "30",
            output_path,
        ]
        try:
            subprocess.run(cmd, check=True)
            os.remove(input_path)
            os.rename(output_path, input_path)
            print(f"[INFO] ffmpeg 재인코딩 완료 및 저장: {input_path}")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] ffmpeg 인코딩 실패: {e}")

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

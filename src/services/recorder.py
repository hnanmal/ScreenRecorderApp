# src/services/recorder.py
import pyautogui
import cv2
import numpy as np
import datetime


class ScreenRecorder:
    def __init__(self):
        self.recording = False
        self.out = None

    def start(self):
        screen_size = pyautogui.size()
        filename = datetime.datetime.now().strftime("recording_%Y%m%d_%H%M%S.avi")
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.out = cv2.VideoWriter(filename, fourcc, 10.0, screen_size)
        self.recording = True

        while self.recording:
            img = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            self.out.write(frame)

        self.out.release()

    def stop(self):
        self.recording = False

# src/views/overlay_box.py
import tkinter as tk


class OverlayBox:
    def __init__(self, x, y, w, h):
        print(f"[OverlayBox] 생성 at {x}, {y}, {w}, {h}")
        self.root = tk.Toplevel()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

        # ✅ 배경을 '투명색상'으로 설정
        self.root.configure(bg="magenta")
        self.root.attributes("-transparentcolor", "magenta")  # Windows only

        # ✅ 창 위치 및 크기 지정
        self.root.geometry(f"{w}x{h}+{x}+{y}")

        # ✅ 캔버스도 같은 투명색 사용
        self.canvas = tk.Canvas(
            self.root, width=w, height=h, bg="magenta", highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # ✅ 빨간 테두리만 남김
        self.canvas.create_rectangle(2, 2, w - 2, h - 2, outline="red", width=3)

    def close(self):
        print("[OverlayBox] 닫기")
        self.root.destroy()

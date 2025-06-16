# src/views/region_selector.py
import tkinter as tk


class RegionSelector:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.3)
        self.root.configure(bg="black")
        self.root.attributes("-topmost", True)
        self.root.title("녹화 영역 선택")
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.root.withdrawn = False  # 추가
        self.selected_region = None

        self.start_x = self.start_y = 0
        self.rect_id = None

        self.canvas = tk.Canvas(self.root, bg="black", cursor="crosshair")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_start)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.selected_region = None

    def on_start(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.rect_id = self.canvas.create_rectangle(
            self.start_x,
            self.start_y,
            self.start_x,
            self.start_y,
            outline="red",
            width=2,
        )

    def on_drag(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect_id, self.start_x, self.start_y, cur_x, cur_y)

    def on_release(self, event):
        x1 = int(self.start_x)
        y1 = int(self.start_y)
        x2 = int(self.canvas.canvasx(event.x))
        y2 = int(self.canvas.canvasy(event.y))
        x = min(x1, x2)
        y = min(y1, y2)
        w = abs(x2 - x1)
        h = abs(y2 - y1)

        self.selected_region = (x, y, w, h)
        self.region_selected = True
        print(f"Selected region: {self.selected_region}")
        self.root.quit()  # ✅ mainloop를 먼저 종료

        self.root.destroy()  # 반드시 닫기

    def select_region(self):
        self.root.mainloop()
        print(f"[DEBUG] return self.selected_region: {self.selected_region}")
        return self.selected_region

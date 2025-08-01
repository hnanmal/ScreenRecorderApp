import tkinter as tk

# from ttkbootstrap import Style
from src.views.main_view import ScreenRecorderView, check_thread
from src.views.overlay_box import OverlayBox

if __name__ == "__main__":
    root = tk.Tk()
    # style = Style("cosmo")
    app = ScreenRecorderView(root)
    root.mainloop()
    check_thread()


# if __name__ == "__main__":
#     root = tk.Tk()
#     root.withdraw()

#     ob = OverlayBox(100, 100, 400, 300)  # ✅ 이게 실행되면 무조건 보임
#     root.mainloop()

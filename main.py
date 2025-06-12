import tkinter as tk
from ttkbootstrap import Style
from src.views.main_view import ScreenRecorderView

if __name__ == "__main__":
    root = tk.Tk()
    style = Style("cosmo")
    app = ScreenRecorderView(root)
    root.mainloop()

import tkinter as tk

root = tk.Tk()
root.withdraw()  # 숨김

win = tk.Toplevel()
win.overrideredirect(True)
win.attributes("-topmost", True)

win.configure(bg="magenta")
win.attributes("-transparentcolor", "magenta")  # Windows only

win.geometry("400x300+300+200")

canvas = tk.Canvas(win, width=400, height=300, bg="magenta", highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

canvas.create_rectangle(2, 2, 398, 298, outline="red", width=4)

root.mainloop()

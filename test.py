import tkinter as tk
import threading
from tkinter import messagebox


def background_task(root):
    def show_message():
        messagebox.showinfo("완료", "작업이 끝났습니다.")

    # 안전하게 main thread에서 실행
    root.after(0, show_message)


root = tk.Tk()
tk.Button(
    root,
    text="작업 시작",
    command=lambda: threading.Thread(target=background_task, args=(root,)).start(),
).pack()
root.mainloop()

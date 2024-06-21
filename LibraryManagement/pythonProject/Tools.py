"""
@Author:     
@Time:      2024/5/13 17:25
@What:      函数集合
"""
from tkinter import Frame
import tkinter as tk


def set_frame(root: tk.Tk, frame: Frame):
    frame.grid(row=0, column=0, sticky='nsew')
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)


def frame_set(frame: Frame, infos: tuple, row):
    i = 0
    for info in infos:
        lb = tk.Label(frame, text=info, font=('Arial', 16), highlightthickness=1, highlightbackground='black')
        if i == 2:
            lb.grid(row=row, column=i, ipadx=10, ipady=5, sticky='news', columnspan=5)
            i += 4
        else:
            lb.grid(row=row, column=i, ipadx=10, ipady=5, sticky='news')
        i += 1


def create_scrollable_text(canvas: tk.Canvas, title: tuple, text_list):
    canvas.delete('all')
    scroll_frame = tk.Frame(canvas)
    frame_set(scroll_frame, title, 0)
    row = 1
    for text in text_list:
        frame_set(scroll_frame, text, row)
        row += 1
    canvas.create_window((100, 0), window=scroll_frame, anchor='nw')

    def on_mousewheel(event):
        if canvas.winfo_height() >= scroll_frame.winfo_reqheight():
            return
        if event.delta < 0:
            canvas.yview_scroll(1, "units")
        else:
            canvas.yview_scroll(-1, "units")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scroll_frame.bind('<Configure>', on_configure)
    canvas.bind_all('<MouseWheel>', lambda event: on_mousewheel(event))
    canvas.bind('<Destroy>', lambda event: canvas.unbind_all('<MouseWheel>'))


def singleton(cls):
    instances = {}

    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return getinstance

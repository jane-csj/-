"""
@Author:     
@Time:      2024/4/29 18:20
@What:      控制界面
"""
from tkinter import Frame, Tk
import tkinter as tk
from PIL import Image, ImageTk
from pythonProject.LibraryManage import FindBook
from pythonProject.ManagerUser import UserManagementView
from pythonProject.LendBook import RANK
from pythonProject.BookInfo import SEARCH
from searchUserOrReturn import UserFrame, ReturnFrame
from ModifyUser import Modify
from LendBook import LendInfo
from DataSolve import Data
from AddBook import AddBookSystem
from OutBook import CheckoutBookSystem

global top_frame


class WINDOWS:
    width, height = 0, 0

    def __init__(self):
        if self.width == 0 and self.height == 0:
            self.get_screen_size()

    def get_screen_size(self):
        win = Tk()
        win.state('zoomed')
        self.width = win.winfo_screenwidth()
        self.height = win.winfo_screenheight()
        win.destroy()


def frame_set_background(root, path):
    image = Image.open(path)
    image = image.resize((WINDOWS().width, WINDOWS().height))
    bg_image = ImageTk.PhotoImage(image)

    frame = tk.Frame(root)
    bg_label = tk.Label(frame, image=bg_image, bg='blue')
    bg_label.image = bg_image
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    return frame


def welcome_frame(self):
    path = 'picture\\cbe769a523095d18c6c11252415cc065.png'
    frame = frame_set_background(self, path)
    set_frame(self, frame)
    global top_frame
    top_frame = frame


# desc：展示某个frame
# return：void
def show_frame(root: Tk, frame: int):
    # frame.tkraise()
    global top_frame
    top_frame.destroy()
    if frame == 1:
        top_frame = UserFrame(root).get_user_frame()
    elif frame == 2:
        top_frame = Data(root).get_top_frame()
    elif frame == 3:
        top_frame = Modify(root)
    elif frame == 4:
        top_frame = SEARCH(root).get_frame()
    elif frame == 5:
        top_frame = RANK(root).get_rank_book()
    elif frame == 6:
        top_frame = LendInfo(root).get_lend_info()
    elif frame == 7:
        top_frame = UserManagementView(root).get_top_frame()
    elif frame == 8:
        top_frame = None
    elif frame == 9:
        top_frame = FindBook(root).get_find_frame()
    elif frame == 10:
        top_frame = AddBookSystem(root).get_top_frame()
    elif frame == 11:
        top_frame = CheckoutBookSystem(root).get_top_frame()
    elif frame == 12:
        top_frame = ReturnFrame(root).get_return_frame()


def set_frame(root, frame: Frame):
    frame.grid(row=0, column=0, sticky='nsew')
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)


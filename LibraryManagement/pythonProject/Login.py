"""
@Author:     陈世杰
@Time:      2024/4/29 18:19
@What:      登录界面
"""

from tkinter import messagebox, Tk, Frame, font
import tkinter as tk
from Control import WINDOWS, welcome_frame, frame_set_background
from SqlOperate import SQL
from Menu import Menubar


# desc：密码错误弹窗
# return：void
def pwd_error(title, message):
    messagebox.showinfo(title, message)


# desc：给frame添加图片
# return：void


class LOGIN(Tk):
    root = None
    win = None

    # desc：登录主界面
    # return：void
    def __init__(self, master=None):
        super().__init__(master)
        self.title("登录界面")
        self.state("zoomed")
        self.master = master

        frame = Frame(self)
        frame.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        width = WINDOWS().width
        height = WINDOWS().height
        path = 'picture\\img.png'
        self.frame = frame_set_background(frame, path)
        self.frame.config(bg='blue')
        self.frame.pack(fill='both', expand=True)

        frame_l = tk.Frame(self.frame)
        sx, sy = 400, 400
        lx = 0.5 - sx / (width * 3 // 2)
        ly = 0.5 - sy / (height * 3 // 2)
        frame_l.place(relx=lx, rely=ly, width=sx, height=sy)

        lb_font = font.Font(size=20)
        lb = tk.Label(frame_l, text='欢迎登录图书馆管理系统', font=lb_font)
        lb.pack()

        frm = tk.Frame(frame_l)
        frm.pack(ipady=30)

        lb_account = tk.Label(frm, text='工号：')
        lb_account.pack(side='left', ipadx=10)
        en_account = tk.Entry(frm)
        en_account.pack(side='right')
        en_account.focus_set()

        frm_pwd = tk.Frame(frame_l)
        frm_pwd.pack(ipady=20)
        lb_pwd = tk.Label(frm_pwd, text='密码：')
        lb_pwd.pack(side='left', ipadx=10)
        en_pwd = tk.Entry(frm_pwd, show='*')
        en_pwd.pack(side='right')
        en_account.bind('<Return>', lambda event: en_pwd.focus_set())
        en_pwd.bind('<Return>', lambda event: login_btn.invoke())
        login_btn = tk.Button(frame_l,
                              command=lambda: self.check_id(en_account, en_pwd),
                              text='login', width=30, bg='red')

        login_btn.pack()
        self.mainloop()

    # desc：检查工号密码是否正确
    # return：void
    def check_id(self, en_id, en_pwd):
        pwd = SQL().check_id_pwd(user_id=en_id.get())
        in_pwd = en_pwd.get()
        if pwd is None:
            pwd_error('工号不存在', '工号不存在，请重新输入')
        elif in_pwd == pwd:
            self.destroy()
            Main()
        else:
            pwd_error('密码错误', '密码错误，请重试')


# desc：登录后的主界面
class Main(Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.state('zoomed')
        self.title('图书馆管理系统')
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        mdict = {'用户信息': 1, '数据统计': 2,
                 '修改用户信息': 3, '书籍信息': 4,
                 '借阅排行榜': 5, '借阅历史': 6,
                 '管理用户': 7,
                 '新增书籍数': 8, '修改书籍信息': 9,
                 '新书入库': 10, '书籍出库': 11,
                 '归还信息': 12}

        Menubar(self, mdict).show()
        welcome_frame(self)
        self.mainloop()

    # desc：欢迎界面
    # return：void

    def on_closing(self):
        SQL().conn.close()
        self.destroy()


class Application:
    def __init__(self):
        LOGIN()

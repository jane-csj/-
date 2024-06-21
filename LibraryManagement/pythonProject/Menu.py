"""
@Author:     
@Time:      2024/5/2 14:04
@What:      菜单栏
"""
from tkinter import Menu
from ModifyUser import *
from Control import show_frame


class Menubar:
    menu = None

    def __init__(self, root: Tk, mdict: dict):
        self.mf = ('Arial', 16)
        self.root = root
        self.menu = Menu(root, font=self.mf, tearoff=False)
        query_menu = Menu(self.menu, font=self.mf, tearoff=False)
        # 查询菜单
        query_menu.add_command(label='用户信息',
                               command=lambda: show_frame(self.root, mdict['用户信息']))
        query_menu.add_command(label='书籍信息',
                               command=lambda: show_frame(self.root, mdict['书籍信息']))
        query_menu.add_command(label='归还信息',
                               command=lambda: show_frame(self.root, mdict['归还信息']))
        lend_menu = Menu(query_menu, font=self.mf, tearoff=False)
        lend_menu.add_command(label='借阅排行榜',
                              command=lambda: show_frame(self.root, mdict['借阅排行榜']))
        lend_menu.add_command(label='借阅历史',
                              command=lambda: show_frame(self.root, mdict['借阅历史']))
        query_menu.add_cascade(label='借阅信息', menu=lend_menu)
        manage_menu = Menu(self.menu, font=self.mf, tearoff=False)

        # 管理用户信息
        manage_menu.add_cascade(label='修改用户信息',
                                command=lambda: show_frame(self.root, mdict['修改用户信息']))
        manage_menu.add_cascade(label='管理用户',
                                command=lambda: show_frame(self.root, mdict['管理用户']))

        data_menu = Menu(self.menu, font=self.mf, tearoff=False)
        data_menu.add_command(label='数据统计',
                              command=lambda: show_frame(self.root, mdict['数据统计']))

        hold_menu = Menu(data_menu, font=self.mf, tearoff=False)
        hold_menu.add_command(label='新书入库',
                              command=lambda: show_frame(self.root, mdict['新书入库']))
        hold_menu.add_command(label='书籍出库',
                              command=lambda: show_frame(self.root, mdict['书籍出库']))
        hold_menu.add_command(label='修改书籍信息',
                              command=lambda: show_frame(self.root, mdict['修改书籍信息']))

        # 管理菜单
        self.menu.add_cascade(label='查询', menu=query_menu)
        self.menu.add_cascade(label='管理用户信息', menu=manage_menu)
        self.menu.add_cascade(label='数据统计', menu=data_menu)
        self.menu.add_cascade(label='修改馆藏信息', menu=hold_menu)

    def show(self):
        self.root.config(menu=self.menu)

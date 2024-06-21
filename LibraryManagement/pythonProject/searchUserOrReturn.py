from tkinter import messagebox
from SqlOperate import *
from Control import *
from Tools import *


class UserFrame:
    def __init__(self, master):
        self.user_frame = None
        self.master = master
        self.create_user_info_window()

    def create_user_info_window(self):
        self.user_frame = tk.Frame(self.master)
        set_frame(self.master, self.user_frame)
        # 在新窗口中创建 UserInfoFrame
        user_info_frame = UserInfoFrame(self.user_frame)
        user_info_frame.pack(expand=True, fill='both')

    def get_user_frame(self):
        return self.user_frame


class UserInfoFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = None
        self.root = parent
        self.result_text = None
        self.user_var = None
        self.create_widgets()

    def create_widgets(self):
        sample_frame = tk.Frame(self.root)
        sample_frame.pack()

        wel_label = tk.Label(sample_frame, text='用户查询', font=('Arial', 20))
        wel_label.grid(row=0, column=0, columnspan=2, sticky='news')
        (tk.Label(sample_frame, text="输入工号/学号查看信息:", font=('Arial', 16))
         .grid(row=1, column=0, sticky='news', columnspan=2))
        self.user_var = tk.StringVar()
        user_entry = tk.Entry(sample_frame, font=('Arial', 16), textvariable=self.user_var)
        user_entry.grid(row=2, column=0, sticky='news', columnspan=2)
        btn = tk.Button(sample_frame, text="查询", command=lambda: self.query_info(self.user_var.get()))
        btn.grid(row=3, column=0, sticky='news')
        btn_all = tk.Button(sample_frame, text="查询全部", command=lambda: self.query_info())
        btn_all.grid(row=3, column=1, ipadx=10, sticky='news', columnspan=2)
        user_entry.bind('<Return>', lambda event: btn.invoke())

        self.canvas = tk.Canvas(self)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(self, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        def on_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.canvas.bind('<Configure>', on_configure)

    def query_info(self, username='#'):
        # self.result_text.delete('1.0', tk.END)
        user_info = None
        if username == '#':
            try:
                user_info = SQL().query_user_info()
            except Exception as e:
                tk.messagebox.showinfo("提示", "数据库连接失败！无法查询信息！\n" + str(e))
            if user_info is None:
                tk.messagebox.showinfo("提示", "用户不存在！")
                return
        else:
            try:
                info = SQL().search_reader_by_id(username)
                if info is None:
                    tk.messagebox.showinfo("提示", "用户不存在！")
                    return
                user_info = [(info['user_id'], info['user_name'], info['sex'], info['unit'], info['user_type'])]
            except Exception as e:
                tk.messagebox.showinfo("提示", "数据库连接失败！无法查询信息！\n" + str(e))

        title = ('工号/学号', '姓名', '性别', '单位', '用户类型')
        text_list = self.solve_query_info(user_info)
        create_scrollable_text(self.canvas, title, text_list)

    def solve_query_info(self, result):
        text_list = []
        for row in result:
            user_id, user_name, sex, unit, user_type = row
            if user_type is True:
                user_type = '管理员'
            else:
                user_type = '普通用户'
            text_list.append((user_id, user_name, sex, unit, user_type))

        return text_list


class ReturnFrame:
    def __init__(self, master):
        self.return_frame = None
        self.master = master
        self.create_return_info_window()

    def create_return_info_window(self):
        self.return_frame = tk.Frame(self.master)
        set_frame(self.master, self.return_frame)
        return_info_frame = ReturnInfoFrame(self.return_frame)
        return_info_frame.pack(expand=True, fill='both')

    def get_return_frame(self):
        return self.return_frame


class ReturnInfoFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.scroll_frame = None
        self.canvas = None
        self.result_text = None
        self.book_entry = None
        self.book_isbn = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="输入书籍ISBN查看归还信息:").pack()
        self.book_entry = tk.Entry(self, textvariable=self.book_isbn)
        self.book_entry.pack()
        btn = tk.Button(self, text="查询", command=self.query_return_info, width=20)
        btn.pack()
        self.book_entry.bind('<Return>', lambda event: btn.invoke())
        # self.result_text = tk.Text(self, height=30, width=200)
        # self.result_text.pack()

        self.canvas = tk.Canvas(self)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(self, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        def on_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.canvas.bind('<Configure>', on_configure)
        self.canvas.bind('<Destroy>', lambda event: self.canvas.unbind_all('<MouseWheel>'))

    def query_return_info(self):
        return_info = []
        if self.book_isbn.get() == '':
            try:
                return_info = SQL().get_return_infos()
            except Exception as e:
                tk.messagebox.showinfo("提示", "数据库连接失败！无法查询信息！\n" + str(e))
        else:
            try:
                return_info = SQL().get_return_info_by_book_isbn(isbn=self.book_isbn.get())
            except Exception as e:
                tk.messagebox.showinfo("提示", "数据库连接失败！无法查询信息！\n" + str(e))
        # 格式化和打印每一条归还信息
        result_info = []
        for info in return_info:
            user_id, user_name, book_name, lend_time, return_time = info
            user_id = str(user_id)
            lend_time = lend_time.strftime('%Y-%m-%d')
            if return_time is None:
                return_time = '未归还'
            else:
                return_time = return_time.strftime('%Y-%m-%d')
            result_info.append((user_id, user_name, book_name, lend_time, return_time))
        create_scrollable_text(self.canvas, ('用户ID', '用户名', '书名', '借出时间', '归还时间'), text_list=result_info)

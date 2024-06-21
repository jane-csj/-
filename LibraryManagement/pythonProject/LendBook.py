from tkinter import (Label, BOTTOM, BOTH, Scrollbar,
                     RIGHT, Y, Canvas, NW, TOP, X)
from tkinter import ttk
from PIL import ImageTk, Image
from SqlOperate import SQL
from Tools import *


# 借阅信息类
class LendInfo:
    user_id = None  # 用户账号
    book_id = None  # 图书名称
    lend_name = None  # 借阅人姓名
    lend_time = None  # 借书时间
    return_time = None  # 还书时间
    root = None  # 借阅信息界面
    top_frame = None  # 顶部Frame
    data_array = []  # 借阅信息数组

    # 初始化方法
    def __init__(self, root):
        self.canvas = None
        self.rows = []  # 初始化一个空列表用于存储借阅信息
        self.root = root
        self.top_frame = Frame(self.root)  # 创建顶部Frame
        set_frame(self.root, self.top_frame)
        self.data_array = SQL().get_lend_info()
        self.get_book_info(self.data_array)
        self.showinfo()

    # 获取用户借阅信息，将数据存入 rows 属性中
    def get_book_info(self, data_array):
        for row in data_array:
            lend_info_data = {
                'user_id': row[0],
                'user_name': row[1],
                'book_name': row[2],
                'lend_time': row[3],
                'return_time': row[4]
            }
            self.rows.append(lend_info_data)

    def solve_data(self, data_list):
        for row in self.rows:
            user_id = str(row['user_id'])
            user_name = row['user_name']
            book_name = row['book_name']

            lend_time = row['lend_time']
            if lend_time is None:
                lend_time = "未借阅"
            else:
                lend_time = lend_time.strftime('%Y-%m-%d')
            return_time = row['return_time']
            if return_time is None:
                return_time = "未归还"
            else:
                return_time = return_time.strftime('%Y-%m-%d')
            data_list.append((user_id, user_name, book_name, lend_time, return_time))

    # 展示借阅信息
    def showinfo(self):
        # 创建借阅信息界面
        new_label = Label(self.top_frame, text="用户借阅信息", font=("Arial", 20))
        new_label.pack(side=TOP, fill=X)

        # 写入借阅信息
        self.canvas = Canvas(self.top_frame)
        self.canvas.pack(side=tk.LEFT, fill=BOTH ,expand=True)
        scrollbar = Scrollbar(self.top_frame, command=self.canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        def on_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.bind("<Configure>", on_configure)
        self.canvas.bind('<Destroy>', lambda event: self.canvas.unbind_all("<MouseWheel>"))

        data_list = []
        self.solve_data(data_list)
        title = ('工号/学号',  '借阅人姓名', '图书名称', '借书时间', '还书时间')
        create_scrollable_text(self.canvas, title, data_list)

        self.top_frame.grid_rowconfigure(1, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1)

    def get_lend_info(self):
        return self.top_frame


# 借阅排行榜类
class RANK:
    # 初始化
    def __init__(self, root):
        self.Combo = None
        self.bottom_frame = None
        self.root = root
        self.book_id = []  # 书本名称
        self.publish = []  # 出版社
        self.subject = []  # 书本类型
        self.ISBN = []  # 书本编号
        self.resume = []  # 借阅次数
        self.path = []  # 图片地址
        self.rows = []  # 存储图书信息的列表
        self.rank_book_frame = None  # 借阅排行榜Frame
        self.rank_book_arr = SQL().get_rank_book()  # 存储图书信息的数组
        self.create_rank_gui()

    # 获取数据库中所有的书本信息
    def get_book_info(self, rows):
        for row in rows:
            book_info = {
                '书本名称': row[0],
                '出版社': row[1],
                '书本类型': row[2],
                'ISBN': row[3],
                '图片地址': row[4],
                '借阅次数': row[5]
            }
            self.rows.append(book_info)

    def sort_book(self, sort_type):
        if self.bottom_frame is None:  # 如果底部 Frame 不存在，则创建
            self.bottom_frame = Frame(self.rank_book_frame)
            self.bottom_frame.pack(side=BOTTOM, fill=BOTH, expand=True)
        else:  # 如果底部 Frame 已存在，则清空内容
            for widget in self.bottom_frame.winfo_children():
                widget.destroy()
        # 创建一个滚动条
        my_scroll = Scrollbar(self.bottom_frame)
        my_scroll.pack(side=RIGHT, fill=Y)
        canvas = Canvas(self.bottom_frame, yscrollcommand=my_scroll.set, height=500)  # 创建Canvas组件
        canvas.pack(fill=BOTH, expand=True)
        # 清空旧数据
        self.rows.clear()
        i = 0
        # 导入图书数据
        self.rank_book_arr = SQL().get_rank_book()
        self.get_book_info(self.rank_book_arr)
        # 将图书信息按照借阅次数从小到大重新排序
        sorted_rows = sorted(self.rows, key=lambda x: x['借阅次数'], reverse=sort_type)
        # 打印每本书的信息
        for book_info in sorted_rows:
            label = Label(canvas,
                          text="书本名称： {}\n出版社：{}\n书本类型：{}\nISBN：{}\n借阅次数：{}\n".format(
                              book_info['书本名称'], book_info['出版社'], book_info['书本类型'],
                              book_info['ISBN'], book_info['借阅次数']),
                          font=("Helvetica", 15), justify='left')
            self.label_a.append(label)
            path = book_info['图片地址']
            if path is None:
                path = 'picture/img_1.png'
            try:
                im = Image.open(path)
            except FileNotFoundError:
                im = Image.open('picture/img_1.png')
            im = im.resize((200, 200))
            img = ImageTk.PhotoImage(im)
            label_book = tk.Label(canvas, image=img, width=170, height=200)
            label_book.image = img
            self.label_book_a.append(label_book)
            canvas.create_window(0, i * 200, anchor=NW, window=label_book)  # 在Canvas组件中创建窗口小部件
            canvas.create_window(255, i * 200, anchor=NW, window=label)  # 在Canvas组件中创建窗口小部件
            i = i + 1
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))  # 设置 Canvas 的滚动区域
        my_scroll.config(command=canvas.yview)  # 使用滚动条控制 Canvas 的垂直滚动
        # 绑定鼠标滚轮事件
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))
        canvas.bind('<Destroy>', lambda event: canvas.unbind_all("<MouseWheel>"))

    # 所需变量
    root = None
    label_a = []
    label_book_a = []

    # 生成借阅排行榜底部frame
    def get_selected(self, event):
        selected_value = self.Combo.get()  # 获取获取选择的内容
        # 根据选择内容生成借阅次数按从小到大排序的排行榜
        if selected_value == "按从小到大排序":
            self.sort_book(False)
        # 根据选择内容生成借阅次数按从大到小排序的排行榜
        if selected_value == "按从大到小排序":
            self.sort_book(True)

    # ！！！！！！！实现借阅排行榜全部功能，调用这个函数即可！！！！！！
    def create_rank_gui(self):
        # 创建一个主界面Frame
        self.rank_book_frame = Frame(self.root)
        set_frame(self.root, self.rank_book_frame)

        # 创建一个顶部Frame，用来实现subject检索功能
        top_frame = Frame(self.rank_book_frame)
        top_frame.pack(side=TOP, fill=X)
        # 创建一个label文本，打印“借阅排行榜”放于顶部frame中间
        label1 = Label(top_frame, text="借阅排行榜", font=("Helvetica", 30))
        label1.pack(padx=2, pady=5)
        # 创建一个list列表，用来存放文本类型
        value_list = ["按从小到大排序", "按从大到小排序"]

        self.Combo = ttk.Combobox(top_frame, values=value_list, state="readonly")  # 将list列表的文本类型放进组合箱里面,并设置只读模式
        self.Combo.set("选择按借阅次数排序方式")  # 给组合箱命名
        self.Combo.pack(padx=5, pady=150)
        self.bottom_frame = None  # 创建全局变量，用于保存底部 Frame
        # 绑定事件，当用户选择一个选项时，触发get_selected方法,获取选择的内容
        self.Combo.bind("<<ComboboxSelected>>", self.get_selected)
        self.Combo.current(0)
        self.get_selected(None)

    def get_rank_book(self):
        return self.rank_book_frame

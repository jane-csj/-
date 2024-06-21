import tkinter
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import Pmw
from Control import *
from SqlOperate import *


def set_frame(tk, frame: Frame):
    frame.grid(row=0, column=0, sticky='nsew')
    tk.grid_rowconfigure(0, weight=1)
    tk.grid_columnconfigure(0, weight=1)


class SEARCH:
    root = None
    root_frame = None
    label_a = []
    label_book_a = []

    # 显示查询结果
    def print_info(self, rows, canvas):
        # 滚动条置顶
        canvas.yview_moveto(0)
        # 删除之前查询的项
        for i in self.label_a:
            i.destroy()
        for i in self.label_book_a:
            i.destroy()
        info = "书名：{}\n作者：{}\n出版社：{}\n类型：{}\n学科：{}\nISBN：{}"
        i = 0

        brief_tip = Pmw.Balloon(self.root)

        for row in rows:
            i = i + 1
            label = Label(canvas, text=info.format(row[0], row[1], row[2], row[3], row[4], row[5]),
                          font=("Helvetica", 15), justify='left')
            self.label_a.append(label)
            brief_str = row[6]
            path = row[7]
            im = None
            try:
                if path is not None:
                    im = Image.open(path)
                else:
                    im = Image.open("picture/img_1.png")
            except FileNotFoundError:
                im = Image.open("picture/img_1.png")
            im = im.resize((200, 200))
            img = ImageTk.PhotoImage(im)
            label_book = tkinter.Label(canvas, image=img, width=170, height=200)
            label_book.image = img
            self.label_book_a.append(label_book)
            str_tmp = ""
            cnt = 0
            for j in brief_str:
                str_tmp += j
                cnt += 1
                if cnt == 26:
                    cnt = 0
                    str_tmp += '\n'
            brief_tip.bind(label_book, str_tmp)
            canvas.create_window(0, i * 200, anchor=NW, window=label_book)
            canvas.create_window(255, i * 200, anchor=NW, window=label)
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    # 按下回车查询
    def on_enter(self, event, conn, entry, combo, canvas):
        info = entry.get()
        cursor = conn.cursor()
        same_str = """
        select distinct Book.book_name,AuthorInfo.author,Book.publish,Type.type_name,Book.subject,Book.ISBN,
        Book.resume,Book.image from Book inner join AuthorInfo on Book.book_id=AuthorInfo.book_id inner join BookType on Book.book_id=BookType.book_id inner join Type on BookType.type_id=Type.type_id where"""
        value = combo.get()
        match value:
            case "书名":
                cursor.execute(f"{same_str} Book.book_name ='{info}'")
            case "作者":
                cursor.execute(f"{same_str} AuthorInfo.author='{info}'")
            case "出版社":
                cursor.execute(f"{same_str} Book.publish='{info}'")
            case "类型":
                cursor.execute(f"{same_str} Type.type_name='{info}'")
            case "学科":
                cursor.execute(f"{same_str} Book.subject='{info}'")
            case _:
                cursor.execute(f"{same_str} Book.ISBN='{info}'")
        rows = cursor.fetchall()
        if len(rows) == 0:
            messagebox.showinfo("提示", f"没有{value}\"{info}\"的书")
        self.print_info(rows, canvas)

    # 滚轮事件
    def on_mousewheel(self, event, canvas):
        canvas.yview_scroll(-1 * (int(event.delta / 120)), "units")

    def __init__(self, root):
        conn = SQL().get_conn()
        self.root = root
        self.root_frame = Frame(root)
        set_frame(self.root, self.root_frame)

        frame_0 = self.root_frame

        label_0 = tkinter.Label(frame_0, text="查询方法", font=("Helvetica", 16))
        label_0.pack(pady=20)

        combo_values = ["书名", "作者", "出版社", "类型", "学科", "ISBN"]
        combo = ttk.Combobox(frame_0, values=combo_values, state='readonly', font=("Helvetica", 16))
        combo.pack(pady=10)
        combo.current(0)

        label_1 = tkinter.Label(frame_0, text="输入信息", font=("Helvetica", 16))
        label_1.pack(pady=10)

        entry = tkinter.Entry(frame_0, font=("Helvetica", 18))
        entry.pack(pady=10)
        entry.bind("<Return>", lambda event: self.on_enter(event, conn, entry, combo, canvas))

        frame_1 = Frame(frame_0, height=700)
        frame_1.pack(fill=X, side=BOTTOM)

        scrollbar = Scrollbar(frame_1, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas = Canvas(frame_1, yscrollcommand=scrollbar.set, height=500)
        canvas.pack(fill=BOTH, expand=True)

        scrollbar.config(command=canvas.yview)
        canvas.bind_all("<MouseWheel>", lambda event: self.on_mousewheel(event, canvas))
        canvas.bind('<Destroy>', lambda event: canvas.unbind_all('<MouseWheel>'))

    def get_frame(self):
        return self.root_frame


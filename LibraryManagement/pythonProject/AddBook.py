import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from Tools import set_frame


class AddBookSystem:
    def __init__(self, root):
        self.top_frame = None
        self.root = root
        self.top_frame = tk.Frame(self.root)
        set_frame(self.root, self.top_frame)
        self.main_frame = tk.Frame(self.root)
        self.main_frame.place(relx=0.4, rely=0.4)
        self.conn = None
        self.cursor = None
        self.create_widgets()

    def create_widgets(self):
        m_font = ('Arial', 16)

        ttk.Label(self.main_frame, text="ISBN", font=m_font).grid(row=0, column=0)
        self.isbn_entry = ttk.Entry(self.main_frame)
        self.isbn_entry.grid(row=0, column=1)

        ttk.Label(self.main_frame, text="书名", font=m_font).grid(row=1, column=0)
        self.book_name_entry = ttk.Entry(self.main_frame)
        self.book_name_entry.grid(row=1, column=1)

        ttk.Label(self.main_frame, text="作者", font=m_font).grid(row=2, column=0)
        self.author_entry = ttk.Entry(self.main_frame)
        self.author_entry.grid(row=2, column=1)

        ttk.Label(self.main_frame, text="出版社", font=m_font).grid(row=3, column=0)
        self.publish_entry = ttk.Entry(self.main_frame)
        self.publish_entry.grid(row=3, column=1)

        ttk.Label(self.main_frame, text="简介", font=m_font).grid(row=4, column=0)
        self.resume_entry = ttk.Entry(self.main_frame)
        self.resume_entry.grid(row=4, column=1)

        ttk.Label(self.main_frame, text="学科", font=m_font).grid(row=5, column=0)
        self.subject_entry = ttk.Entry(self.main_frame)
        self.subject_entry.grid(row=5, column=1)

        ttk.Label(self.main_frame, text="语言", font=m_font).grid(row=6, column=0)
        self.language_entry = ttk.Entry(self.main_frame)
        self.language_entry.grid(row=6, column=1)

        ttk.Label(self.main_frame, text="类型", font=m_font).grid(row=7, column=0)
        self.type_name_entry = ttk.Entry(self.main_frame)
        self.type_name_entry.grid(row=7, column=1)

        ttk.Label(self.main_frame, text="馆藏数量", font=m_font).grid(row=8, column=0)
        self.hold_num_entry = ttk.Entry(self.main_frame)
        self.hold_num_entry.grid(row=8, column=1)

        ttk.Label(self.main_frame, text="可借数量", font=m_font).grid(row=9, column=0)
        self.assign_num_entry = ttk.Entry(self.main_frame)
        self.assign_num_entry.grid(row=9, column=1)

        m_style = ttk.Style()
        m_style.configure('TButton', font=m_font)
        (ttk.Button(self.main_frame, text="添加新书", command=self.add_book, style='TButton')
         .grid(row=10, column=0, columnspan=2))

    def connect_database(self):
        try:
            self.conn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=90pn65xq4259.vicp.fun,50889;DATABASE=LibraryManage;UID=lm;PWD=chenshijie')
            self.cursor = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("连接错误", f"数据库连接失败: {e}")
            self.cursor = None

    def add_book(self):
        if not self.cursor:
            self.connect_database()
            if not self.cursor:
                return

        isbn = self.isbn_entry.get()
        hold_num = int(self.hold_num_entry.get())
        assign_num = int(self.assign_num_entry.get())

        try:
            # 查询书籍是否已存在
            self.cursor.execute("SELECT book_id FROM Book WHERE ISBN=?", (isbn,))
            book_result = self.cursor.fetchone()

            if book_result:
                book_id = book_result[0]
                # 更新馆藏信息
                self.cursor.execute("""
                    UPDATE HoldInfo SET
                    hold_num = hold_num + ?,
                    assign_num = assign_num + ?
                    WHERE book_id = ?
                """, (hold_num, assign_num, book_id))
                self.conn.commit()
                messagebox.showinfo("成功", "书籍馆藏数量更新成功")
            else:
                # 添加新书籍
                self.cursor.execute("""
                    INSERT INTO Book (ISBN, publish, language, subject, resume, book_name)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (isbn, self.publish_entry.get(), self.language_entry.get(),
                      self.subject_entry.get(), self.resume_entry.get(), self.book_name_entry.get()))
                # self.cursor.commit()
                book_id = self.cursor.execute(f"SELECT book_id from Book where ISBN = '{isbn}'").fetchone()[0]
                # 插入馆藏信息
                now_time = datetime.datetime.now()
                school = "佛山科学技术学院"
                self.cursor.execute("""
                    INSERT INTO HoldInfo (book_id, hold_num, assign_num,add_time,school)
                    VALUES (?, ?, ?,?,?)
                """, (book_id, hold_num, assign_num, now_time, school))
                self.cursor.commit()
                # 插入作者信息
                self.cursor.execute("""
                                    INSERT INTO AuthorInfo (book_id, author)
                                    VALUES (?, ?)
                                """, (int(book_id), self.author_entry.get()))
                self.cursor.commit()
                self.cursor.execute("SELECT type_id FROM Type WHERE type_name=?", (self.type_name_entry.get()))
                type_result = self.cursor.fetchone()

                if type_result:
                    type_id = type_result[0]
                else:
                    # 插入新类型
                    self.cursor.execute("INSERT INTO Type (type_name) VALUES (?)", (self.type_name_entry.get()))
                    self.cursor.commit()
                    type_id = self.cursor.execute(
                        f"SELECT type_id from Type where type_name = '{self.type_name_entry.get()}'").fetchone()[0]
                # 插入类型信息
                self.cursor.execute("""
                                                   INSERT INTO BookType (book_id, type_id)
                                                   VALUES (?, ?)
                                               """, (int(book_id), int(type_id)))
                self.cursor.commit()
                messagebox.showinfo("成功", "成功添加新书到数据库")
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("数据库错误", f"添加书籍失败: {e}")

    def get_top_frame(self):
        return self.main_frame


if __name__ == '__main__':
    root = tk.Tk()
    root.state('zoomed')
    app = AddBookSystem(root)
    root.mainloop()

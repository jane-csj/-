import tkinter as tk
from SqlOperate import SQL
from datetime import datetime


class Data:
    def __init__(self, master):
        self.master = master

        self.frame1 = tk.Frame(master)
        self.frame1.grid(row=0, column=0, sticky="nsew")

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # 连接数据库并执行数据查询的函数
        def connect_to_database(query_type):
            try:
                # 连接数据库
                conn = SQL().get_conn()
                cursor = conn.cursor()

                # 清空之前显示的信息
                today_add_label.config(text="")
                month_add_label.config(text="")
                year_add_label.config(text="")
                today_lend_label.config(text="")
                month_lend_label.config(text="")
                year_lend_label.config(text="")
                book_info_label.config(text="")
                error_label.config(text="")

                # 获取今天的日期
                today = datetime.now().date()
                today_str = today.strftime("%Y-%m-%d")

                # 获取查询类型
                if query_type == "今日":
                    # 查询今天添加的书籍数量
                    cursor.execute(f"SELECT COUNT(*) FROM HoldInfo WHERE add_time = '{today_str}'")
                    result = cursor.fetchone()[0]
                    today_add_label.config(text=f"{query_type}添加书籍数量: {result}")

                    # 查询今天添加的书籍信息
                    cursor.execute(
                        f"SELECT book_id, ISBN, publish, language, subject , book_name FROM Book WHERE book_id IN ("
                        f"SELECT book_id FROM HoldInfo WHERE add_time LIKE '{today_str}')")
                    book_info = cursor.fetchall()
                    for info in book_info:
                        book_info_label.config(text=book_info_label.cget("text") + f"\n{info}")

                elif query_type == "本月":
                    # 查询本月添加的书籍数量
                    this_month = today.strftime("%Y-%m")
                    cursor.execute(f"SELECT COUNT(*) FROM HoldInfo WHERE add_time LIKE '{this_month}-%'")
                    result = cursor.fetchone()[0]
                    month_add_label.config(text=f"{query_type}添加书籍数量: {result}")

                    # 查询本月添加的书籍信息
                    cursor.execute(
                        f"SELECT book_id, ISBN, publish, language, subject , book_name FROM Book WHERE book_id IN ("
                        f"SELECT book_id FROM HoldInfo WHERE add_time LIKE '{this_month}-%')")
                    book_info = cursor.fetchall()
                    for info in book_info:
                        book_info_label.config(text=book_info_label.cget("text") + f"\n{info}")

                elif query_type == "今年":
                    # 查询今年添加的书籍数量
                    this_year = today.strftime("%Y")
                    cursor.execute(f"SELECT COUNT(*) FROM HoldInfo WHERE add_time LIKE '{this_year}-%'")
                    result = cursor.fetchone()[0]
                    year_add_label.config(text=f"{query_type}添加书籍数量: {result}")

                    # 查询今年添加的书籍信息
                    cursor.execute(
                        f"SELECT book_id, ISBN, publish, language, subject , book_name FROM Book WHERE book_id IN ("
                        f"SELECT book_id FROM HoldInfo WHERE add_time LIKE '{this_year}-%')")
                    book_info = cursor.fetchall()
                    for info in book_info:
                        book_info_label.config(text=book_info_label.cget("text") + f"\n{info}")

                if query_type == "今日借阅次数":
                    # 查询今日借阅次数
                    cursor.execute(f"SELECT COUNT(*) FROM LendInfo WHERE lend_time = '{today_str}'")
                    result = cursor.fetchone()[0]
                    today_lend_label.config(text=f"{query_type}: {result}")

                    # 查询今日借阅的书籍信息
                    cursor.execute(
                        f"SELECT book_id, ISBN, publish, language, subject , book_name FROM Book WHERE book_id IN ("
                        f"SELECT book_id FROM LendInfo WHERE lend_time  LIKE '{today_str}')")
                    book_info = cursor.fetchall()
                    for info in book_info:
                        book_info_label.config(text=book_info_label.cget("text") + f"\n{info}")

                elif query_type == "本月借阅次数":
                    # 查询本月借阅次数
                    this_month = today.strftime("%Y-%m")
                    cursor.execute(f"SELECT COUNT(*) FROM LendInfo WHERE lend_time LIKE '{this_month}-%'")
                    result = cursor.fetchone()[0]
                    month_lend_label.config(text=f"{query_type}: {result}")

                    # 查询本月借阅的书籍信息
                    cursor.execute(
                        f"SELECT book_id, ISBN, publish, language, subject , book_name FROM Book WHERE book_id IN ("
                        f"SELECT book_id FROM LendInfo WHERE lend_time LIKE '{this_month}-%')")
                    book_info = cursor.fetchall()
                    for info in book_info:
                        book_info_label.config(text=book_info_label.cget("text") + f"\n{info}")

                elif query_type == "今年借阅次数":
                    # 查询今年借阅次数
                    this_year = today.strftime("%Y")
                    cursor.execute(f"SELECT COUNT(*) FROM LendInfo WHERE lend_time LIKE '{this_year}-%'")
                    result = cursor.fetchone()[0]
                    year_lend_label.config(text=f"{query_type}: {result}")

                    # 查询今年借阅的书籍信息
                    cursor.execute(
                        f"SELECT book_id, ISBN, publish, language, subject , book_name FROM Book WHERE book_id IN ("
                        f"SELECT book_id FROM LendInfo WHERE lend_time LIKE '{this_year}-%')")
                    book_info = cursor.fetchall()
                    for info in book_info:
                        book_info_label.config(text=book_info_label.cget("text") + f"\n{info}")

                cursor.close()
            except Exception as e:
                error_label.config(text=f"数据库错误: {str(e)}")

        # 创建大标题
        title_label = tk.Label(self.frame1, text="图书馆数据统计系统", font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3)

        # 创建标签用于显示查询结果
        today_add_label = tk.Label(self.frame1, text="")
        today_add_label.grid(row=2, column=0)

        month_add_label = tk.Label(self.frame1, text="")
        month_add_label.grid(row=2, column=1)

        year_add_label = tk.Label(self.frame1, text="")
        year_add_label.grid(row=2, column=2)

        today_lend_label = tk.Label(self.frame1, text="")
        today_lend_label.grid(row=4, column=0)

        month_lend_label = tk.Label(self.frame1, text="")
        month_lend_label.grid(row=4, column=1)

        year_lend_label = tk.Label(self.frame1, text="")
        year_lend_label.grid(row=4, column=2)

        error_label = tk.Label(self.frame1, text="")
        error_label.grid(row=3, column=0, columnspan=3)

        book_info_label = tk.Label(self.frame1, text="")
        book_info_label.grid(row=5, column=0, columnspan=3)

        # 创建按钮函数
        def create_button(text, query_type):
            return tk.Button(self.frame1, text=text, command=lambda: connect_to_database(query_type))

        # 创建新增书籍数查询按钮
        today_add_button = create_button("今日新增书籍数", "今日")
        today_add_button.grid(row=1, column=0)

        month_add_button = create_button("本月新增书籍数", "本月")
        month_add_button.grid(row=1, column=1)

        year_add_button = create_button("今年新增书籍数", "今年")
        year_add_button.grid(row=1, column=2)

        # 创建借阅次数查询按钮
        today_borrow_button = create_button("今日借阅次数", "今日借阅次数")
        today_borrow_button.grid(row=3, column=0)

        month_borrow_button = create_button("本月借阅次数", "本月借阅次数")
        month_borrow_button.grid(row=3, column=1)

        year_borrow_button = create_button("今年借阅次数", "今年借阅次数")
        year_borrow_button.grid(row=3, column=2)

    def get_top_frame(self):
        return self.frame1


if __name__ == '__main__':
    root = tk.Tk()
    root.state("zoomed")
    app = Data(root)
    root.mainloop()

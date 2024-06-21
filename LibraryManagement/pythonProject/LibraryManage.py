import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from SqlOperate import SQL

# 连接到SQL Server数据库
conn = SQL().get_conn()


# 创建函数来打开查找书籍信息窗口
class FindBook:
    root = None

    def __init__(self, root):
        self.frame = None
        self.root = root
        self.create_frame()

    def open_book_search_window(self):
        # 创建函数来查找书籍信息
        def search_book():
            cursor = conn.cursor()
            book_id = entry.get()
            if not book_id:
                messagebox.showerror("错误", "书籍ID不能为空！")
                return

            # 通过书籍ID检索Book表中的信息
            cursor.execute("SELECT * FROM Book WHERE ISBN = ?", book_id)
            book_info = cursor.fetchone()

            # 通过书籍ID检索HoldInfo表中的信息
            cursor.execute("SELECT hold_num, assign_num FROM HoldInfo WHERE book_id = ?", book_id)
            hold_info = cursor.fetchone()

            if book_info:
                self.open_book_update_window(book_info, hold_info)
            else:
                messagebox.showerror("提示", "未找到对应的书籍")
            cursor.close()

        search_window = tk.Toplevel(self.root)
        search_window.title("查找书籍信息")

        # 计算屏幕中心位置
        search_window_width = 500
        search_window_height = 100
        screen_width = search_window.winfo_screenwidth()
        screen_height = search_window.winfo_screenheight()
        x = int((screen_width - search_window_width) / 2)
        y = int((screen_height - search_window_height) / 2)
        search_window.geometry(f"{search_window_width}x{search_window_height}+{x}+{y}")

        label = ttk.Label(search_window, text="请输入书籍ISBN：")
        label.grid(row=0, column=0, pady=10, padx=10)

        entry = ttk.Entry(search_window, width=30)
        entry.grid(row=0, column=1, pady=10, padx=10)

        search_button = ttk.Button(search_window, text="查找", command=search_book)
        search_button.grid(row=1, column=2, pady=5, padx=10)

        search_window.grab_set()

    # 创建函数来打开修改书籍信息窗口
    def open_book_update_window(self, book_info, hold_info):
        # 创建函数来更新书籍信息
        def update_book():
            new_book_ISBN = entries[0].get()
            new_book_publish = entries[1].get()
            new_book_language = entries[2].get()
            new_book_subject = entries[3].get()
            new_book_resume = entries[4].get()
            new_image = entries[5].get()
            new_book_name = entries[6].get()
            new_hold_num = entries[7].get()
            new_assign_num = entries[8].get()

            try:
                cursor = conn.cursor()
                # 更新Book表的信息
                update_book_query = ("UPDATE Book SET book_name=?, publish=?, ISBN=?, language=?, subject=?, resume=?, "
                                     "image=? WHERE book_id = ?")
                cursor.execute(update_book_query, (
                    new_book_name, new_book_publish, new_book_ISBN, new_book_language, new_book_subject,
                    new_book_resume,
                    new_image, book_info[0]))

                if cursor.rowcount > 0:
                    # 更新HoldInfo表的信息
                    update_hold_query = "UPDATE HoldInfo SET hold_num=?, assign_num=? WHERE book_id = ?"
                    cursor.execute(update_hold_query, (new_hold_num, new_assign_num, book_info[0]))

                    conn.commit()
                    if cursor.rowcount > 0:
                        messagebox.showinfo("成功", "书籍信息及馆藏信息已更新！")
                        cursor.close()
                    else:
                        cursor.close()
                        messagebox.showerror("失败", "馆藏信息更新失败！")
                else:
                    cursor.close()
                    messagebox.showerror("失败", "书籍信息修改失败！")
            except Exception as e:
                cursor.close()
                messagebox.showerror("错误", f"更新过程中出现异常：{str(e)}")

            # 恢复小窗口的焦点状态
            update_window.grab_set()

        update_window = tk.Toplevel(self.root)
        update_window.title("修改书籍信息")

        # 计算屏幕中心位置
        update_window_width = 500
        update_window_height = 400
        screen_width = update_window.winfo_screenwidth()
        screen_height = update_window.winfo_screenheight()
        x = int((screen_width - update_window_width) / 2)
        y = int((screen_height - update_window_height) / 2)
        update_window.geometry(f"{update_window_width}x{update_window_height}+{x}+{y}")

        labels = ["ISBN", "出版社", "语言", "主题", "简介", "封面", "书名", "馆藏数", "在馆数"]
        entries = []

        for i, label_text in enumerate(labels):
            label = ttk.Label(update_window, text=label_text)
            label.grid(row=i, column=0, sticky="e", pady=5, padx=(20, 10))
            entry = ttk.Entry(update_window, width=30)
            entry.grid(row=i, column=1, pady=5, padx=(0, 20))
            entries.append(entry)

        # 若有原始书籍信息，则显示在文本框
        if book_info:
            for i, entry in enumerate(entries):
                if i < len(book_info) - 1:
                    entry.delete(0, tk.END)  # 清空文本框
                    if book_info[i + 1] is None:
                        book_info[i + 1] = ""
                    entry.insert(0, book_info[i + 1])  # 显示原始书籍信息

            if hold_info:  # 如果HoldInfo表中有信息
                entries[7].delete(0, tk.END)
                entries[7].insert(0, hold_info[0])
                entries[8].delete(0, tk.END)
                entries[8].insert(0, hold_info[1])
            else:
                entries[7].delete(0, tk.END)
                entries[8].delete(0, tk.END)
        else:
            messagebox.showerror("提示", "未找到对应的书籍")

        update_button = ttk.Button(update_window, text="修改书籍信息", command=update_book)
        update_button.grid(row=len(labels), column=0, columnspan=2, pady=10, padx=(20, 0), sticky="e")
        update_window.grab_set()

    # 创建Frame作为容器
    def create_frame(self):
        self.frame = ttk.Frame(self.root, padding="20")
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # 创建Frame作为容器
        container = ttk.Frame(self.frame, padding="20")
        container.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # 创建按钮来打开小窗口
        open_search_button = ttk.Button(self.frame, text="打开查找窗口", command=self.open_book_search_window)
        open_search_button.grid(row=0, column=0, pady=10)

    def get_find_frame(self):
        return self.frame

import tkinter as tk
from tkinter import ttk, messagebox
from SqlOperate import SQL
from Tools import set_frame

class CheckoutBookSystem:
    """书籍出库系统"""

    def __init__(self, root):
        self.top_frame = tk.Frame(root)
        set_frame(root, self.top_frame)
        # 创建界面元素
        self.create_widgets()
        self.conn = None
        self.cursor = None

    def create_widgets(self):
        frame = ttk.Frame(self.top_frame)
        frame.place(relx=0.4, rely=0.4)
        m_font = ("Arial", 16)
        ttk.Label(frame, text="书籍ID", font=m_font).grid(row=0, column=0, padx=10, pady=10)
        self.book_id_entry = ttk.Entry(frame)
        self.book_id_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(frame, text="出库数量", font=m_font).grid(row=1, column=0, padx=10, pady=10)
        self.quantity_entry = ttk.Entry(frame)
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=10)
        m_style = ttk.Style()
        m_style.configure("TButton", font=m_font)
        ttk.Button(frame, text="出库", command=self.checkout_book, style='TButton').grid(row=2, column=0, columnspan=2, pady=20)

    def connect_database(self):
        """尝试连接数据库"""
        try:
            self.conn = SQL().get_conn()
            self.cursor = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("连接错误", f"数据库连接失败: {e}")

    def checkout_book(self):
        """执行书籍出库操作"""
        if not self.cursor:
            self.connect_database()
            if not self.cursor:
                return

        book_id = self.book_id_entry.get()
        quantity = int(self.quantity_entry.get())
        try:
            self.cursor.execute("SELECT holding_num, assignable_num FROM holdingInfo WHERE book_id=?", (book_id,))
            current_holding = self.cursor.fetchone()
            if current_holding and current_holding[0] >= quantity and current_holding[1] >= quantity:
                new_holding_num = current_holding[0] - quantity
                new_assignable_num = current_holding[1] - quantity
                self.cursor.execute("UPDATE holdingInfo SET holding_num=?, assignable_num=? WHERE book_id=?",
                                    (new_holding_num, new_assignable_num, book_id))
                self.conn.commit()
                messagebox.showinfo("成功", "成功出库书籍")
                self.cursor.close()
            else:
                messagebox.showerror("库存错误", "库存不足或书籍不存在")
        except Exception as e:
            messagebox.showerror("数据库错误", f"出库操作失败: {e}")

    def get_top_frame(self):
        return self.top_frame


if __name__ == '__main__':
    root = tk.Tk()
    root.title("书籍出库系统")
    root.state("zoomed")
    app = CheckoutBookSystem(root)
    root.mainloop()

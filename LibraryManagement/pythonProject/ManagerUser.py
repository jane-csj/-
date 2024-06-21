import tkinter as tk
from tkinter import messagebox
from SqlOperate import SQL

# 连接数据库，并创建游标

conn = SQL().get_conn()
cursor = conn.cursor()


def set_frame(tk, frame: tk.Frame):
    frame.grid(row=0, column=0, sticky='nsew')
    tk.grid_rowconfigure(0, weight=1)
    tk.grid_columnconfigure(0, weight=1)


# 录入用户
class InsertUser:
    def __init__(self, cursor, user_id, user_type, unit, user_name, pwd, sex):
        # 初始化
        self.cursor = cursor
        self.user_id = user_id
        self.user_type = user_type
        self.unit = unit
        self.user_name = user_name
        self.pwd = pwd
        self.sex = sex

        try:
            cursor.execute("INSERT INTO Reader (user_id, user_type, unit, user_name, pwd, sex) VALUES (?,?,?,?,?,?)",
                           (self.user_id, self.user_type, self.unit, self.user_name, self.pwd, self.sex))
            conn.commit()
            messagebox.showinfo("成功", "用户录入成功")
        except Exception as e:
            messagebox.showerror("失败", str(e))
            # 记录错误日志
            print(f"An error occurred: {e}")


# 删除用户
class DeleteUser:
    def __init__(self, cursor, user_id):
        self.cursor = cursor
        self.user_id = user_id

        try:
            cursor.execute("DELETE FROM Reader WHERE user_id = ?", self.user_id)
            conn.commit()
            messagebox.showinfo("成功", "用户删除成功")
        except Exception as e:
            messagebox.showerror("失败", str(e))
            # 记录错误日志
            print(f"An error occurred: {e}")


# 界面  frame = tk.Frame()
class UserManagementView:
    def __init__(self, root):
        self.button_back = None
        self.button_submit = None
        self.entry_sex = None
        self.label_sex = None
        self.entry_pwd = None
        self.label_pwd = None
        self.entry_user_name = None
        self.label_user_name = None
        self.entry_unit = None
        self.label_unit = None
        self.entry_user_type = None
        self.label_user_type = None
        self.entry_user_id = None
        self.label_user_id = None

        self.root = root
        self.top_frame = tk.Frame(self.root)
        set_frame(self.root, self.top_frame)
        self.cursor = cursor
        # 创建框架
        self.frame = tk.Frame(self.top_frame)
        self.frame.pack(padx=10, pady=10)

        # 录入用户按钮
        self.button_insert_user = tk.Button(self.frame, text="录入用户", command=self.show_insert_user_fields,
                                            font=("Helvetica", 20))
        self.button_insert_user.grid(row=0, column=0, pady=20)

        # 删除用户按钮
        self.button_delete_user = tk.Button(self.frame, text="删除用户", command=self.show_delete_user_field,
                                            font=("Helvetica", 20))
        self.button_delete_user.grid(row=1, column=0, pady=20)

    def show_initial_interface(self):
        # 清除当前框架中的所有内容
        for widget in self.frame.winfo_children():
            widget.destroy()

        # 显示初始的按钮界面
        self.button_insert_user = tk.Button(self.frame, text="录入用户", command=self.show_insert_user_fields)
        self.button_insert_user.grid(row=0, column=0, pady=5)

        self.button_delete_user = tk.Button(self.frame, text="删除用户", command=self.show_delete_user_field)
        self.button_delete_user.grid(row=1, column=0, pady=5)

    def show_insert_user_fields(self):
        # 清除当前框架中的所有内容
        for widget in self.frame.winfo_children():
            widget.destroy()

        # 用户ID标签和输入框
        self.label_user_id = tk.Label(self.frame, text="用户工号\学号:")
        self.label_user_id.grid(row=0, column=0, sticky="e")
        self.entry_user_id = tk.Entry(self.frame)
        self.entry_user_id.grid(row=0, column=1)

        self.label_user_type = tk.Label(self.frame, text="用户类型:")
        self.label_user_type.grid(row=1, column=0, sticky="e")
        self.user_type = tk.IntVar(value=1)  # 设置默认值为1（管理员）
        self.radio_admin = tk.Radiobutton(self.frame, text='管理员', variable=self.user_type, value=1)
        self.radio_admin.grid(row=1, column=1, sticky="w")
        self.radio_user = tk.Radiobutton(self.frame, text='用户', variable=self.user_type, value=0)
        self.radio_user.grid(row=1, column=1, sticky="e")

        self.label_unit = tk.Label(self.frame, text="用户单位:")
        self.label_unit.grid(row=2, column=0, sticky="e")
        self.entry_unit = tk.Entry(self.frame)
        self.entry_unit.grid(row=2, column=1)

        self.label_user_name = tk.Label(self.frame, text="用户名:")
        self.label_user_name.grid(row=3, column=0, sticky="e")
        self.entry_user_name = tk.Entry(self.frame)
        self.entry_user_name.grid(row=3, column=1)

        self.label_pwd = tk.Label(self.frame, text="登录密码:")
        self.label_pwd.grid(row=4, column=0, sticky="e")
        self.entry_pwd = tk.Entry(self.frame)
        self.entry_pwd.grid(row=4, column=1)

        # self.label_sex = tk.Label(self.frame, text="用户性别:")
        # self.label_sex.grid(row=5, column=0, sticky="e")
        # self.entry_sex = tk.Entry(self.frame)
        # self.entry_sex.grid(row=5, column=1)

        self.label_sex = tk.Label(self.frame, text="用户性别:")
        self.label_sex.grid(row=5, column=0, sticky="e")
        self.sex = tk.StringVar(value='男')  # 设置默认值为'男'
        self.radio_male = tk.Radiobutton(self.frame, text='男', variable=self.sex, value='男')
        self.radio_male.grid(row=5, column=1, sticky="w")
        self.radio_female = tk.Radiobutton(self.frame, text='女', variable=self.sex, value='女')
        self.radio_female.grid(row=5, column=1, sticky="e")

        # 提交按钮
        self.button_submit = tk.Button(self.frame, text="确定", command=self.submit_insert, font=("Helvetica", 16))
        self.button_submit.grid(row=6, column=0, columnspan=2, pady=10)

        self.button_back = tk.Button(self.frame, text="返回", command=self.show_initial_interface,
                                     font=("Helvetica", 16))
        self.button_back.grid(row=7, column=0, columnspan=2, pady=10)

    def show_delete_user_field(self):
        # 清除当前框架中的所有内容
        for widget in self.frame.winfo_children():
            widget.destroy()

        # 用户ID标签和输入框
        self.label_user_id = tk.Label(self.frame, text="用户ID:")
        self.label_user_id.grid(row=0, column=0, sticky="e")
        self.entry_user_id = tk.Entry(self.frame)
        self.entry_user_id.grid(row=0, column=1)

        # 删除按钮
        self.button_submit = tk.Button(self.frame, text="确定", command=self.submit_delete, font=("Helvetica", 16))
        self.button_submit.grid(row=1, column=0, columnspan=2, pady=10)

        self.button_back = tk.Button(self.frame, text="返回", command=self.show_initial_interface,
                                     font=("Helvetica", 16))
        self.button_back.grid(row=2, column=0, columnspan=2, pady=10)

    def submit_insert(self):
        # 获取用户输入的信息
        user_id = self.entry_user_id.get()
        user_type = self.user_type.get()
        unit = self.entry_unit.get()
        user_name = self.entry_user_name.get()
        pwd = self.entry_pwd.get()
        sex = self.sex.get()

        # 实例化Insert_User类并添加用户
        InsertUser(self.cursor, user_id, user_type, unit, user_name, pwd, sex)

    def submit_delete(self):
        # 获取用户输入的ID
        user_id = self.entry_user_id.get()

        # 实例化Delete_User类并删除用户
        DeleteUser(self.cursor, user_id)

    def get_top_frame(self):
        return self.top_frame


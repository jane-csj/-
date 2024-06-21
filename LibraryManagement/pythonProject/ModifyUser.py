"""
@Author:     
@Time:      2024/5/3 21:20
@What:      修改用户信息
"""
from Control import *
from tkinter import Button, Label, StringVar, Entry
from tkinter.ttk import Combobox
from SqlOperate import *

light_blue = '#add8e6'


def set_frame(tk, frame: Frame):
    frame.grid(row=0, column=0, sticky='nsew')
    tk.grid_rowconfigure(0, weight=1)
    tk.grid_columnconfigure(0, weight=1)


class Modify(Frame):
    flag = False
    m_font = ('Arial', 20)
    id_var = None
    name_var = None
    unit_var = None
    sex_var = None
    pos = 1

    def __init__(self, root: Tk):
        super().__init__(root)
        self.sex_combo = None
        self.modify_btn = None
        set_frame(root, self)
        self['bg'] = light_blue
        wel_label = Label(self, text='修改用户信息', font=self.m_font, bg=light_blue)
        wel_label.pack(fill='x', pady=50)
        search_frame = Frame(self, bg=light_blue)
        Label(search_frame, text='请输入用户ID：', font=self.m_font, bg=light_blue).pack(side='left', padx=10)
        str_id = StringVar()
        en_id = Entry(search_frame, textvariable=str_id, font=self.m_font)
        en_id.pack(side='left', padx=20)
        self.mdict = None

        def get_str():
            try:
                self.mdict = SQL().search_reader_by_id(user_id=en_id.get())
            except Exception as e:
                messagebox.showerror('错误', str(e))
            if self.mdict is None:
                messagebox.showerror('错误', '用户不存在')
                return
            self.id_var.set(self.mdict['user_id'])
            self.name_var.set(self.mdict['user_name'])
            self.pos = self.sex_var.index(self.mdict['sex'])
            self.unit_var.set(self.mdict['unit'])
            self.sex_combo.current(self.pos)
            self.modify_btn.config(state='normal')

        search_btn = Button(search_frame, text='查询', command=lambda: get_str())
        search_btn.config(width=10)
        search_btn.pack(side='left')

        en_id.bind('<Return>', lambda event: search_btn.invoke())

        def delete_str(event):
            if self.id_var.get() == '':
                return
            self.id_var.set('')
            self.name_var.set('')
            self.unit_var.set('')
            self.sex_combo.current(0)
            self.modify_btn.config(state='disabled')

        en_id.bind('<Key>', lambda event: delete_str(event))

        search_frame.pack()
        modify_frame = Frame(self, bg=light_blue)
        modify_frame.pack(fill='both', expand=True)
        self.set_modify(modify_frame)

    def get_frame(self):
        return self

    def set_modify(self, root: Frame):
        frame = Frame(root, bg=light_blue)
        frame.place(relx=0.4, rely=0.4)
        # 工号
        id_label = Label(frame, text='工号/学号', font=self.m_font, bg=light_blue)
        id_label.grid(row=0, column=0, padx=20)
        self.id_var = StringVar()
        id_en = Entry(frame, textvariable=self.id_var, font=self.m_font)
        id_en.grid(row=0, column=1)
        id_en.config(state='disabled')

        # 姓名
        name_label = Label(frame, text='姓名', font=self.m_font, bg=light_blue)
        name_label.grid(row=1, column=0, padx=20)
        self.name_var = StringVar()
        name_en = Entry(frame, textvariable=self.name_var, font=self.m_font)
        name_en.grid(row=1, column=1)

        # 单位
        unit_label = Label(frame, text='单位', font=self.m_font, bg=light_blue)
        unit_label.grid(row=2, column=0, padx=20)
        self.unit_var = StringVar()
        unit_en = Entry(frame, textvariable=self.unit_var, font=self.m_font)
        unit_en.grid(row=2, column=1)

        # 性别
        sex_label = Label(frame, text='性别', font=self.m_font, bg=light_blue)
        sex_label.grid(row=3, column=0, padx=20)
        self.sex_var = ['', '男', '女']
        self.sex_combo = Combobox(frame, values=self.sex_var, font=self.m_font, state='readonly')
        self.sex_combo.grid(row=3, column=1, padx=40)

        # 修改按钮
        def modify():
            user_name = self.name_var.get()
            unit = self.unit_var.get()
            sex = self.sex_var[self.sex_combo.current()]
            try:
                SQL().modify_reader_info(user_id=self.id_var.get(), user_name=user_name, unit=unit, sex=sex)
                messagebox.showinfo('提示', '修改成功')
            except Exception as e:
                messagebox.showerror('错误', str(e))

        self.modify_btn = Button(frame, text='修改', command=lambda: modify(), font=self.m_font, bg=light_blue)
        self.modify_btn.grid(row=4, column=0, columnspan=2, pady=20, sticky='nsew')
        self.modify_btn.config(state='disabled')


if __name__ == '__main__':
    win = Tk()
    win.state('zoomed')
    Modify(win)
    win.mainloop()

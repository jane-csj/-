"""
@Author:     
@Time:      2024/4/28 15:30
@What:      
"""
import pyodbc
from tkinter import messagebox
from Tools import singleton

SERVER = 'localhost'
DATABASE = 'LibraryManage'
USERNAME = 'sa'
PASSWORD = '6464334cp'
connect_string = (f'DRIVER={{ODBC Driver 18 for SQL Server}}; SERVER={SERVER};DATABASE={DATABASE};'
                  f'UID={USERNAME};PWD={PASSWORD};TrustServerCertificate=yes')


# 单例模式


@singleton
class SQL:
    conn = None

    # 通过user_id 查询密码
    # return： str
    def check_id_pwd(self, user_id):
        sql_str = (f"select  pwd from Reader where user_id = '{user_id}' "
                   f"and user_type=1")
        cursor = self.conn.cursor()
        cursor = cursor.execute(sql_str)
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return None
        else:
            return str(row[0]).strip()

    def __init__(self):
        try:
            self.conn = pyodbc.connect(connect_string)
        except pyodbc.Error as e:
            messagebox.showinfo('错误', str(e))

    # 通过user_id 查询读者信息
    def search_reader_by_id(self, user_id: str):
        sql_str = f'''
        select * from Reader where user_id = '{user_id}'
        '''
        cursor = self.conn.cursor()
        cursor.execute(sql_str)
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return None
        mdict = {'user_id': row.user_id.strip(), 'unit': row.unit.strip(),
                 'user_name': row.user_name.strip(), 'sex': row.sex.strip(), 'user_type': row.user_type}
        return mdict

    # 修改读者信息
    def modify_reader_info(self, user_id: str, unit: str, user_name: str, sex: str):
        sql_str = f'''
        update Reader set unit='{unit}', user_name='{user_name}', sex='{sex}' where user_id='{user_id}'
        '''
        cursor = self.conn.cursor()
        cursor.execute(sql_str)
        self.conn.commit()
        cursor.close()

    def get_return_infos(self):
        sql_str = """
        select Reader.user_id, user_name, book_name, lend_time, return_time  from Reader
        left join LendInfo li on Reader.user_id = li.user_id right outer join Book on li.book_id = Book.book_id 
        where return_time is not null
        """
        cursor = self.conn.cursor()
        cursor.execute(sql_str)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def get_return_info_by_book_isbn(self, isbn):
        sql_str = f"""
        select Reader.user_id, user_name, book_name, lend_time, return_time  from Reader
        left join LendInfo li on Reader.user_id = li.user_id right outer join Book on li.book_id = Book.book_id
        where Book.ISBN = '{isbn}'
        """
        cursor = self.conn.cursor()
        cursor.execute(sql_str)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def query_user_info(self):
        # pass
        """查询指定用户名的用户信息"""
        cursor = self.conn.cursor()
        sql_str = """
        SELECT user_id, user_name, sex, unit, user_type from Reader
        """
        cursor.execute(sql_str)
        cursor.execute(sql_str)
        rows = cursor.fetchall()
        cursor.close()
        if len(rows) == 0:
            return None
        else:
            return rows

    def get_lend_info(self):
        # 连接数据库

        # 创建游标
        cursor = self.conn.cursor()
        data_array = []  # 存放借阅信息的数组
        # 执行 SQL 查询，获取借阅信息
        sql_str = """select distinct Reader.user_id, user_name, book_name , lend_time, return_time from Reader join 
        dbo.LendInfo LI on Reader.user_id = LI.user_id right join dbo.Book B on B.book_id = LI.book_id where lend_time 
        is not null"""
        cursor.execute(sql_str)
        rows = cursor.fetchall()
        # 将借阅信息存放到数组data_array中
        for row in rows:
            data_array.append(list(row))  # 将元组转换为列表并添加到数组中
        # 关闭游标和连接
        cursor.close()
        return data_array

    # 功能2：从数据库中获取Book信息和统计借阅次数
    def get_rank_book(self):
        # 连接数据库

        # 创建游标
        cursor = self.conn.cursor()
        cursor1 = self.conn.cursor()  # 主要用于获取借阅次数
        # 执行 SQL 查询，获取借阅次数
        cursor1.execute(
            'SELECT Book.book_name, COUNT(Book.book_id) AS borrowing_count '
            'FROM Book LEFT JOIN LendInfo ON Book.book_id = LendInfo.book_id '
            'WHERE LendInfo.lend_time IS NOT NULL '
            'GROUP BY Book.book_id, Book.book_name ORDER BY borrowing_count;')
        # 将借阅次数存放到数组count中
        count = {}
        book_array = []  # 存放书籍信息的数组
        for row in cursor1:
            book_name = row[0]  # 获取书名
            borrowing_count = row[1]  # 获取借阅次数
            count[book_name] = borrowing_count  # 使用书名作为键，借阅次数作为值，存放到字典中
        # 执行 SQL 查询，获取借阅信息
        cursor.execute('SELECT book_name, publish, subject, ISBN, image FROM Book')
        # 将借阅信息存放到数组book_array中
        for row in cursor:
            book_data = list(row)  # 将元组转换为列表
            name = book_data.__getitem__(0)  # 获取书名
            # 在列表末尾添加额外的元组——借阅次数
            borrowing_count = count.get(name, 0)  # 通过书名在字典中查找对应的借阅次数，如果找不到，默认为0
            extra_tuple = (borrowing_count)  # 要添加的额外元组——借阅次数
            book_data.append(extra_tuple)
            book_array.append(book_data)  # 将包含额外信息的列表添加到数组中
        cursor.close()
        cursor1.close()
        return book_array

    def get_conn(self):
        return self.conn

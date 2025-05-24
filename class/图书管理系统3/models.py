from database import db
from config import BOOK_STATUS_AVAILABLE, BOOK_STATUS_BORROWED
import datetime

class User:
    def __init__(self, username, password, role, name=None, email=None):
        self.username = username
        self.password = password
        self.role = role
        self.name = name
        self.email = email

    @staticmethod
    def get_by_username(username):
        """根据用户名获取用户"""
        db.connect()
        try:
            db.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user_data = db.cursor.fetchone()
            if user_data:
                return {
                    'id': user_data[0],
                    'username': user_data[1],
                    'password': user_data[2],
                    'role': user_data[3],
                    'name': user_data[4],
                    'email': user_data[5]
                }
            return None
        finally:
            db.disconnect()

    def save(self):
        """保存用户信息"""
        db.connect()
        try:
            db.cursor.execute('''
                INSERT INTO users (username, password, role, name, email)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.username, self.password, self.role, self.name, self.email))
            db.commit()
        finally:
            db.disconnect()

class Book:
    def __init__(self, isbn, title, author=None, publisher=None):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publisher = publisher
        self.status = BOOK_STATUS_AVAILABLE

    @staticmethod
    def get_by_isbn(isbn):
        """根据ISBN获取图书"""
        db.connect()
        try:
            db.cursor.execute('SELECT * FROM books WHERE isbn = ?', (isbn,))
            book_data = db.cursor.fetchone()
            if book_data:
                return {
                    'id': book_data[0],
                    'isbn': book_data[1],
                    'title': book_data[2],
                    'author': book_data[3],
                    'publisher': book_data[4],
                    'status': book_data[5]
                }
            return None
        finally:
            db.disconnect()

    def save(self):
        """保存图书信息"""
        db.connect()
        try:
            db.cursor.execute('''
                INSERT INTO books (isbn, title, author, publisher, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.isbn, self.title, self.author, self.publisher, self.status))
            db.commit()
        finally:
            db.disconnect()

class Borrowing:
    def __init__(self, book_id, user_id):
        self.book_id = book_id
        self.user_id = user_id
        self.status = 'borrowed'
        self.borrow_date = datetime.datetime.now()
        self.return_date = None

    def save(self):
        """保存借阅记录"""
        db.connect()
        try:
            # 更新图书状态
            db.cursor.execute('''
                UPDATE books SET status = ? WHERE id = ?
            ''', (BOOK_STATUS_BORROWED, self.book_id))

            # 添加借阅记录
            db.cursor.execute('''
                INSERT INTO borrowings (book_id, user_id, status)
                VALUES (?, ?, ?)
            ''', (self.book_id, self.user_id, self.status))
            db.commit()
        finally:
            db.disconnect()

    @staticmethod
    def return_book(book_id):
        """归还图书"""
        db.connect()
        try:
            # 更新图书状态
            db.cursor.execute('''
                UPDATE books SET status = ? WHERE id = ?
            ''', (BOOK_STATUS_AVAILABLE, book_id))

            # 更新借阅记录
            db.cursor.execute('''
                UPDATE borrowings 
                SET status = 'returned', return_date = CURRENT_TIMESTAMP
                WHERE book_id = ? AND status = 'borrowed'
            ''', (book_id,))
            db.commit()
        finally:
            db.disconnect() 
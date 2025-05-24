import os
import sys
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import uic
from models import Book
from utils import validate_isbn
from database import db

def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class AddBookWindow(QWidget):
    def __init__(self):
        super().__init__()
        print("[DEBUG] 初始化添加图书窗口")
        # 加载UI
        ui_path = resource_path("ui/书籍添加页面.ui")
        self.ui = uic.loadUi(ui_path, self)
        
        # 绑定按钮事件
        self.ui.pushButton.clicked.connect(self.return_main)  # 返回按钮
        self.ui.pushButton_2.clicked.connect(self.save_book)  # 保存按钮

    def return_main(self):
        """返回主窗口"""
        print("[DEBUG] 返回主窗口")
        main_window = self.parent()
        if main_window:
            print("[DEBUG] 显示主窗口")
            main_window.show()
            main_window.find_all_books_admin('')  # 刷新图书列表
        self.hide()
        print("[DEBUG] 隐藏添加图书窗口")
        
    def save_book(self):
        """保存图书信息"""
        print("[DEBUG] 尝试保存图书信息")
        isbn = self.ui.textEdit.toPlainText().strip()  # ISBN输入框
        title = self.ui.textEdit_2.toPlainText().strip()  # 书名输入框
        author = self.ui.textEdit_3.toPlainText().strip()  # 作者输入框
        publisher = self.ui.textEdit_4.toPlainText().strip()  # 出版社输入框
        
        if not all([isbn, title]):
            print("[DEBUG] ISBN或书名为空")
            QMessageBox.warning(self, "错误", "ISBN和书名不能为空！")
            return
            
        if not validate_isbn(isbn):
            print(f"[DEBUG] ISBN格式不正确: {isbn}")
            QMessageBox.warning(self, "错误", "ISBN格式不正确！")
            return
            
        # 检查ISBN是否已存在
        if Book.get_by_isbn(isbn):
            print(f"[DEBUG] ISBN已存在: {isbn}")
            QMessageBox.warning(self, "错误", "该ISBN已存在！")
            return
            
        try:
            book = Book(isbn=isbn, title=title, author=author, publisher=publisher)
            book.save()
            print(f"[DEBUG] 图书添加成功: {title}")
            QMessageBox.information(self, "成功", "添加成功！")
            self.parent().show()
            self.hide()
            # 刷新主窗口的图书列表
            self.parent().find_all_books_admin('')
        except Exception as e:
            print(f"[DEBUG] 图书添加失败: {str(e)}")
            QMessageBox.warning(self, "错误", f"添加失败：{str(e)}")

class ChangeBookWindow(QWidget):
    def __init__(self):
        super().__init__()
        print("[DEBUG] 初始化修改图书窗口")
        # 加载UI
        ui_path = resource_path("ui/书籍信息修改页面.ui")
        self.ui = uic.loadUi(ui_path, self)
        
        self.book_id = None  # 当前编辑的图书ID
        
        # 绑定按钮事件
        self.ui.pushButton.clicked.connect(self.return_main)  # 返回按钮
        self.ui.pushButton_2.clicked.connect(self.save_changes)  # 保存按钮

    def showEvent(self, event):
        """窗口显示时加载图书信息"""
        super().showEvent(event)
        if self.book_id:
            self.load_book_info()
            
    def load_book_info(self):
        """加载图书信息"""
        print("[DEBUG] 加载图书信息")
        db.connect()
        try:
            db.cursor.execute('SELECT * FROM books WHERE id = ?', (self.book_id,))
            book = db.cursor.fetchone()
            if book:
                print(f"[DEBUG] 当前图书: {book[2]}")
                self.ui.textEdit.setText(book[1])  # ISBN
                self.ui.textEdit_2.setText(book[2])  # 书名
                self.ui.textEdit_3.setText(book[3] or '')  # 作者
                self.ui.textEdit_4.setText(book[4] or '')  # 出版社
        finally:
            db.disconnect()
            
    def return_main(self):
        """返回主窗口"""
        print("[DEBUG] 返回主窗口")
        main_window = self.parent()
        if main_window:
            print("[DEBUG] 显示主窗口")
            main_window.show()
            main_window.find_all_books_admin('')  # 刷新图书列表
        self.hide()
        print("[DEBUG] 隐藏修改图书窗口")
        
    def save_changes(self):
        """保存修改"""
        if not self.book_id:
            return
            
        isbn = self.ui.textEdit.toPlainText().strip()
        title = self.ui.textEdit_2.toPlainText().strip()
        author = self.ui.textEdit_3.toPlainText().strip()
        publisher = self.ui.textEdit_4.toPlainText().strip()
        
        if not all([isbn, title]):
            QMessageBox.warning(self, "错误", "ISBN和书名不能为空！")
            return
            
        if not validate_isbn(isbn):
            QMessageBox.warning(self, "错误", "ISBN格式不正确！")
            return
            
        db.connect()
        try:
            # 检查ISBN是否已被其他图书使用
            db.cursor.execute('SELECT id FROM books WHERE isbn = ? AND id != ?', 
                            (isbn, self.book_id))
            if db.cursor.fetchone():
                QMessageBox.warning(self, "错误", "该ISBN已被其他图书使用！")
                return
                
            # 更新图书信息
            db.cursor.execute('''
                UPDATE books 
                SET isbn = ?, title = ?, author = ?, publisher = ?
                WHERE id = ?
            ''', (isbn, title, author, publisher, self.book_id))
            db.commit()
            
            QMessageBox.information(self, "成功", "修改成功！")
            self.parent().show()
            self.hide()
            # 刷新主窗口的图书列表
            self.parent().find_all_books_admin('')
        except Exception as e:
            QMessageBox.warning(self, "错误", f"修改失败：{str(e)}")
        finally:
            db.disconnect() 
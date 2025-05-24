import os
import sys
from PyQt5.QtWidgets import QWidget, QMessageBox, QTextEdit, QPushButton, QHBoxLayout
from PyQt5 import uic
from models import Book, Borrowing
from database import db

def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        print("[DEBUG] 初始化主窗口")
        # 加载UI
        ui_path = resource_path("ui/主界面.ui")
        self.ui = uic.loadUi(ui_path, self)
        
        # 存储当前用户信息
        self.current_user = None
        
        # 存储其他窗口的引用
        self.login_window = None
        self.change_info_window = None
        self.add_book_window = None
        self.change_book_window = None
        self.add_user_window = None
        self.change_user_window = None
        
        # 绑定按钮事件
        self.ui.pushButton.clicked.connect(self.logout)  # 退出登录
        self.ui.pushButton_2.clicked.connect(self.exit_application)  # 退出系统
        self.ui.pushButton_6.clicked.connect(self.show_personal_info)  # 个人信息
        self.ui.pushButton_3.clicked.connect(self.show_borrow_page)  # 图书借阅
        self.ui.pushButton_4.clicked.connect(self.show_book_management)  # 图书管理
        self.ui.pushButton_5.clicked.connect(self.show_user_management)  # 用户管理
        self.ui.pushButton_7.clicked.connect(self.open_change_info)  # 修改个人信息
        self.ui.pushButton_14.clicked.connect(self.open_add_book)  # 添加图书
        self.ui.pushButton_17.clicked.connect(self.open_add_user)  # 添加用户
        
        # 绑定搜索框事件
        self.ui.lineEdit_4.textChanged.connect(self.find_borrowed_books)  # 已借图书搜索
        self.ui.lineEdit_2.textChanged.connect(self.find_all_books)  # 所有图书搜索
        self.ui.lineEdit_5.textChanged.connect(self.find_all_books_admin)  # 管理员图书搜索
        self.ui.lineEdit_7.textChanged.connect(self.find_all_users)  # 用户搜索
        
    def init_user_info(self):
        """初始化用户信息显示"""
        print("[DEBUG] 初始化用户信息显示")
        if not self.current_user:
            print("[DEBUG] 当前用户信息为空")
            return
            
        print(f"[DEBUG] 当前用户: {self.current_user['username']}, 角色: {self.current_user['role']}")
        self.ui.textEdit_7.setText(self.current_user['username'])
        self.ui.textEdit_10.setText('*' * len(self.current_user['password']))
        self.ui.textEdit_8.setText(self.current_user.get('name', ''))
        self.ui.textEdit_11.setText(str(self.current_user['id']))
        self.ui.textEdit_9.setText(self.current_user['role'])
        self.ui.textEdit_12.setText('1' if self.current_user['role'] == 'admin' else '0')
        
    def show_personal_info(self):
        """显示个人信息页面"""
        print("[DEBUG] 切换到个人信息页面")
        self.ui.stackedWidget.setCurrentIndex(0)
        self.init_user_info()
        
    def show_borrow_page(self):
        """显示借阅页面"""
        print("[DEBUG] 切换到借阅页面")
        self.ui.stackedWidget.setCurrentIndex(1)
        self.find_borrowed_books(self.ui.lineEdit_4.text())
        self.find_all_books(self.ui.lineEdit_2.text())
        
    def show_book_management(self):
        """显示图书管理页面"""
        print("[DEBUG] 切换到图书管理页面")
        self.ui.stackedWidget.setCurrentIndex(2)
        self.find_all_books_admin(self.ui.lineEdit_5.text())
        
    def show_user_management(self):
        """显示用户管理页面"""
        print("[DEBUG] 切换到用户管理页面")
        self.ui.stackedWidget.setCurrentIndex(3)
        self.find_all_users(self.ui.lineEdit_7.text())
        
    def find_borrowed_books(self, search_text):
        """查找已借图书"""
        self.clear_layout(self.ui.verticalLayout_2)
        
        db.connect()
        try:
            # 查询当前用户借阅的图书
            db.cursor.execute('''
                SELECT b.*, br.id as borrow_id, br.borrow_date
                FROM books b
                JOIN borrowings br ON b.id = br.book_id
                WHERE br.user_id = ? AND br.status = 'borrowed'
                AND (b.title LIKE ? OR b.author LIKE ?)
            ''', (self.current_user['id'], f'%{search_text}%', f'%{search_text}%'))
            
            books = db.cursor.fetchall()
            
            for book in books:
                layout = QHBoxLayout()
                
                # 创建图书信息显示
                info = QTextEdit()
                info.setPlaceholderText("图书信息：")
                info.setText(f"书名：{book[2]}\n作者：{book[3]}\n出版社：{book[4]}\n借阅时间：{book[7]}")
                layout.addWidget(info)
                
                # 创建归还按钮
                return_btn = QPushButton("归还")
                return_btn.clicked.connect(lambda checked, bid=book[0]: self.return_book(bid))
                layout.addWidget(return_btn)
                
                self.ui.verticalLayout_2.addLayout(layout)
        finally:
            db.disconnect()
            
    def find_all_books(self, search_text):
        """查找所有可借图书"""
        self.clear_layout(self.ui.verticalLayout_3)
        
        db.connect()
        try:
            # 查询可借图书
            db.cursor.execute('''
                SELECT * FROM books
                WHERE status = 'available'
                AND (title LIKE ? OR author LIKE ?)
            ''', (f'%{search_text}%', f'%{search_text}%'))
            
            books = db.cursor.fetchall()
            
            for book in books:
                layout = QHBoxLayout()
                
                # 创建图书信息显示
                info = QTextEdit()
                info.setPlaceholderText("图书信息：")
                info.setText(f"书名：{book[2]}\n作者：{book[3]}\n出版社：{book[4]}")
                layout.addWidget(info)
                
                # 创建借阅按钮
                borrow_btn = QPushButton("借阅")
                borrow_btn.clicked.connect(lambda checked, bid=book[0]: self.borrow_book(bid))
                layout.addWidget(borrow_btn)
                
                self.ui.verticalLayout_3.addLayout(layout)
        finally:
            db.disconnect()
            
    def find_all_books_admin(self, search_text):
        """管理员查找所有图书"""
        self.clear_layout(self.ui.verticalLayout_4)
        
        db.connect()
        try:
            # 查询所有图书
            db.cursor.execute('''
                SELECT * FROM books
                WHERE title LIKE ? OR author LIKE ?
            ''', (f'%{search_text}%', f'%{search_text}%'))
            
            books = db.cursor.fetchall()
            
            for book in books:
                layout = QHBoxLayout()
                
                # 创建图书信息显示
                info = QTextEdit()
                info.setPlaceholderText("图书信息：")
                info.setText(f"书名：{book[2]}\n作者：{book[3]}\n出版社：{book[4]}\n状态：{book[5]}")
                layout.addWidget(info)
                
                # 创建修改按钮
                change_btn = QPushButton("修改信息")
                change_btn.clicked.connect(lambda checked, bid=book[0]: self.change_book(bid))
                layout.addWidget(change_btn)
                
                self.ui.verticalLayout_4.addLayout(layout)
        finally:
            db.disconnect()
            
    def find_all_users(self, search_text):
        """查找所有用户"""
        self.clear_layout(self.ui.verticalLayout_12)
        
        db.connect()
        try:
            # 查询用户
            db.cursor.execute('''
                SELECT * FROM users
                WHERE username LIKE ? OR name LIKE ?
            ''', (f'%{search_text}%', f'%{search_text}%'))
            
            users = db.cursor.fetchall()
            
            for user in users:
                layout = QHBoxLayout()
                
                # 创建用户信息显示
                info = QTextEdit()
                info.setPlaceholderText("用户信息：")
                info.setText(f"用户名：{user[1]}\n姓名：{user[4]}\n角色：{user[3]}")
                layout.addWidget(info)
                
                # 创建修改按钮
                change_btn = QPushButton("修改信息")
                change_btn.clicked.connect(lambda checked, uid=user[0]: self.change_user(uid))
                layout.addWidget(change_btn)
                
                self.ui.verticalLayout_12.addLayout(layout)
        finally:
            db.disconnect()
            
    def return_book(self, book_id):
        """归还图书"""
        try:
            Borrowing.return_book(book_id)
            QMessageBox.information(self, "成功", "归还成功！")
            self.find_borrowed_books(self.ui.lineEdit_4.text())
            self.find_all_books(self.ui.lineEdit_2.text())
        except Exception as e:
            QMessageBox.warning(self, "错误", f"归还失败：{str(e)}")
            
    def borrow_book(self, book_id):
        """借阅图书"""
        try:
            borrowing = Borrowing(book_id=book_id, user_id=self.current_user['id'])
            borrowing.save()
            QMessageBox.information(self, "成功", "借阅成功！")
            self.find_borrowed_books(self.ui.lineEdit_4.text())
            self.find_all_books(self.ui.lineEdit_2.text())
        except Exception as e:
            QMessageBox.warning(self, "错误", f"借阅失败：{str(e)}")
            
    def change_book(self, book_id):
        """修改图书信息"""
        self.change_book_window.book_id = book_id
        self.change_book_window.show()
        self.hide()
        
    def change_user(self, user_id):
        """修改用户信息"""
        self.change_user_window.user_id = user_id
        self.change_user_window.show()
        self.hide()
        
    def open_change_info(self):
        """打开修改个人信息窗口"""
        print("[DEBUG] 打开修改个人信息窗口")
        if not self.change_info_window:
            print("[DEBUG] 警告：修改信息窗口对象为空")
            return
            
        print(f"[DEBUG] 当前用户信息: {self.current_user}")
        self.change_info_window.show()
        self.hide()
        print("[DEBUG] 主窗口已隐藏")
        
    def open_add_book(self):
        """打开添加图书窗口"""
        self.add_book_window.show()
        self.hide()
        
    def open_add_user(self):
        """打开添加用户窗口"""
        self.add_user_window.show()
        self.hide()
        
    def logout(self):
        """退出登录"""
        self.current_user = None
        self.login_window.show()
        self.hide()
        
    def exit_application(self):
        """退出应用程序"""
        print("[DEBUG] 退出应用程序")
        reply = QMessageBox.question(self, '确认退出', 
                                   "确定要退出程序吗？",
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            print("[DEBUG] 用户确认退出")
            QApplication.quit()  # 这将关闭整个应用程序
        
    def closeEvent(self, event):
        """窗口关闭事件处理"""
        print("[DEBUG] 触发窗口关闭事件")
        reply = QMessageBox.question(self, '确认退出', 
                                   "确定要退出程序吗？",
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            print("[DEBUG] 用户确认退出")
            event.accept()
            QApplication.quit()
        else:
            print("[DEBUG] 用户取消退出")
            event.ignore()
        
    def clear_layout(self, layout):
        """清空布局"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout()) 
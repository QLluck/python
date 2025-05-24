import sys
import os
from PyQt5.QtWidgets import QApplication
from database import db
from ui.login_window import LoginWindow
from ui.register_window import RegisterWindow
from ui.main_window import MainWindow
from ui.change_info_window import ChangeInfoWindow
from ui.book_management import AddBookWindow, ChangeBookWindow
from ui.user_management import AddUserWindow, ChangeUserWindow

def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

if __name__ == "__main__":
    # 初始化数据库
    db.init_database()
    
    # 创建应用
    app = QApplication(sys.argv)
    
    # 创建窗口实例
    login_window = LoginWindow()
    main_window = MainWindow()
    register_window = RegisterWindow()
    change_info_window = ChangeInfoWindow()
    add_book_window = AddBookWindow()
    change_book_window = ChangeBookWindow()
    add_user_window = AddUserWindow()
    change_user_window = ChangeUserWindow()
    
    # 设置窗口关系
    register_window.setParent(login_window)
    main_window.setParent(login_window)
    change_info_window.setParent(main_window)
    add_book_window.setParent(main_window)
    change_book_window.setParent(main_window)
    add_user_window.setParent(main_window)
    change_user_window.setParent(main_window)
    
    # 设置窗口引用
    login_window.register_window = register_window
    login_window.main_window = main_window
    register_window.login_window = login_window
    main_window.login_window = login_window
    main_window.change_info_window = change_info_window
    main_window.add_book_window = add_book_window
    main_window.change_book_window = change_book_window
    main_window.add_user_window = add_user_window
    main_window.change_user_window = change_user_window
    
    # 显示登录窗口
    login_window.show()
    
    sys.exit(app.exec_()) 
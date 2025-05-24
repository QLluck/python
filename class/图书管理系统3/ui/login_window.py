import os
import sys
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import uic
from models import User
from utils import hash_password

def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        print("[DEBUG] 初始化登录窗口")
        # 加载UI
        ui_path = resource_path("ui/登录界面完美.ui")
        self.ui = uic.loadUi(ui_path, self)
        
        # 存储其他窗口的引用
        self.register_window = None
        self.main_window = None
        
        # 绑定按钮事件
        self.ui.pushButton.clicked.connect(self.login)  # 登录按钮
        self.ui.pushButton_2.clicked.connect(self.open_register)  # 注册按钮
        self.ui.pushButton_3.clicked.connect(self.hide)  # 退出按钮改为隐藏窗口
        
    def login(self):
        """登录处理"""
        print("[DEBUG] 尝试登录")
        username = self.ui.lineEdit_7.text().strip()
        password = self.ui.lineEdit_5.text().strip()
        
        if not username or not password:
            print("[DEBUG] 用户名或密码为空")
            self.show_error("用户名和密码不能为空")
            return
            
        # 获取用户信息
        user_data = User.get_by_username(username)
        if not user_data:
            print(f"[DEBUG] 用户不存在: {username}")
            self.show_error("用户不存在，请先注册")
            return
            
        # 验证密码
        if user_data['password'] != hash_password(password):
            print("[DEBUG] 密码错误")
            self.show_error("密码错误")
            return
            
        print(f"[DEBUG] 登录成功: {username}, 角色: {user_data['role']}")
        QMessageBox.information(self, "登录成功", "欢迎回来！")
        
        # 设置主窗口用户信息
        self.main_window.current_user = user_data
        self.main_window.init_user_info()
        
        # 根据用户角色设置界面
        if user_data['role'] == 'admin':
            self.main_window.ui.label.setText(f"管理员: {username}")
        else:
            self.main_window.ui.label.setText(f"用户: {username}")
            # 普通用户隐藏管理功能
            self.main_window.ui.pushButton_4.hide()  # 图书管理
            self.main_window.ui.pushButton_5.hide()  # 用户管理
            
        # 显示主窗口
        self.main_window.show()
        self.hide()
        
    def open_register(self):
        """打开注册窗口"""
        self.register_window.show()
        self.hide()
        
    def show_error(self, message):
        """显示错误信息"""
        self.ui.textBrowser_2.setHtml(f'''
            <html>
            <body>
                <style>
                    .error-text {{
                        color: #ff2121;
                        font-family: 'Arial', sans-serif;
                        text-align: center;
                        font-size: 10px;
                        line-height: 0.3;
                    }}
                </style>
                <p class="error-text">{message}</p>
            </body>
            </html>
        ''') 
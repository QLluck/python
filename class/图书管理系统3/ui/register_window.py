import os
import sys
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import uic
from models import User
from utils import hash_password
from config import ROLE_USER

def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        print("[DEBUG] 初始化注册窗口")
        # 加载UI
        ui_path = resource_path("ui/注册界面完美.ui")
        self.ui = uic.loadUi(ui_path, self)
        
        # 存储登录窗口的引用
        self.login_window = None
        
        # 绑定按钮事件
        self.ui.pushButton.clicked.connect(self.register)  # 注册按钮
        self.ui.pushButton_2.clicked.connect(self.open_login)  # 返回登录按钮
        self.ui.pushButton_3.clicked.connect(self.open_login)  # 退出按钮改为返回登录
        
        # 绑定输入框事件
        self.ui.lineEdit_5.textChanged.connect(self.check_password)  # 密码输入框
        self.ui.lineEdit_7.textChanged.connect(self.check_username)  # 用户名输入框
        
    def register(self):
        """注册处理"""
        username = self.ui.lineEdit_7.text().strip()
        password = self.ui.lineEdit_5.text().strip()
        
        if not username or not password:
            self.show_error("用户名和密码不能为空")
            return
            
        # 检查用户名是否已存在
        if User.get_by_username(username):
            self.show_error("用户名已存在")
            return
            
        # 检查密码强度
        if self.check_password(password) != 0:
            return
            
        # 创建新用户
        user = User(username=username, 
                   password=hash_password(password),
                   role=ROLE_USER)
        try:
            user.save()
            QMessageBox.information(self, "注册成功", "请返回登录！")
            self.open_login()
        except Exception as e:
            self.show_error(f"注册失败: {str(e)}")
            
    def check_password(self, password):
        """检查密码强度"""
        if not password:
            return 1
            
        has_digit = any(c.isdigit() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        errors = []
        if not has_digit:
            errors.append("密码中无数字")
        if not has_upper:
            errors.append("密码中无大写字母")
        if not has_lower:
            errors.append("密码中无小写字母")
        if not has_special:
            errors.append("密码中无特殊字符")
        if len(password) < 8:
            errors.append("密码长度小于8")
            
        if errors:
            error_html = "".join(f'<p class="custom-text">{error}</p>' for error in errors)
            self.show_message(error_html)
            return 1
        else:
            self.show_message('<p class="custom-text2">密码符合要求</p>')
            return 0
            
    def check_username(self, username):
        """检查用户名"""
        # 这里可以添加用户名的验证规则
        # 例如：检查特殊字符、长度限制等
        pass
        
    def open_login(self):
        """返回登录窗口"""
        self.login_window.show()
        self.hide()
        
    def show_error(self, message):
        """显示错误信息"""
        self.show_message(f'<p class="custom-text">{message}</p>')
        
    def show_message(self, html_message):
        """显示消息"""
        self.ui.textBrowser_2.setHtml(f'''
            <html>
            <body>
                <style>
                    .custom-text {{
                        color: #ff2121;
                        font-family: 'Arial', sans-serif;
                        text-align: center;
                        font-size: 10px;
                        line-height: 0.3;
                    }}
                    .custom-text2 {{
                        color: #00e500;
                        font-family: 'Arial', sans-serif;
                        text-align: center;
                        font-size: 10px;
                        line-height: 0.3;
                    }}
                </style>
                {html_message}
            </body>
            </html>
        ''') 
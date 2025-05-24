import os
import sys
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import uic
from models import User
from utils import hash_password, validate_email
from database import db

def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class ChangeInfoWindow(QWidget):
    def __init__(self):
        super().__init__()
        print("[DEBUG] 初始化修改个人信息窗口")
        # 加载UI
        ui_path = resource_path("ui/修改信息界面.ui")
        self.ui = uic.loadUi(ui_path, self)
        
        # 绑定按钮事件
        self.ui.pushButton.clicked.connect(self.return_main)  # 返回按钮
        self.ui.pushButton_2.clicked.connect(self.save_changes)  # 保存按钮
        
        # 绑定输入框事件
        self.ui.textEdit_4.textChanged.connect(self.check_password)  # 密码输入框
        self.ui.textEdit.textChanged.connect(self.check_username)  # 用户名输入框
        
    def showEvent(self, event):
        """窗口显示时加载用户信息"""
        super().showEvent(event)
        print("[DEBUG] 显示修改个人信息窗口")
        self.load_user_info()
        
    def load_user_info(self):
        """加载用户信息"""
        print("[DEBUG] 加载用户信息")
        main_window = self.parent()
        if not main_window:
            print("[DEBUG] 警告：无法获取主窗口对象")
            return
            
        if not hasattr(main_window, 'current_user') or not main_window.current_user:
            print("[DEBUG] 警告：主窗口没有当前用户信息")
            return
            
        user = main_window.current_user
        print(f"[DEBUG] 当前用户: {user['username']}")
        self.ui.textEdit.setText(user['username'])
        self.ui.textEdit_4.setText('')  # 密码留空
        self.ui.textEdit_2.setText(user.get('name', ''))
        self.ui.textEdit_5.setText(str(user['id']))
        self.ui.textEdit_3.setText(user['role'])
        self.ui.textEdit_6.setText('1' if user['role'] == 'admin' else '0')
        
    def check_password(self):
        """检查密码强度"""
        password = self.ui.textEdit_4.toPlainText().strip()
        if not password:
            return
            
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
        else:
            self.show_message('<p class="custom-text2">密码符合要求</p>')
            
    def check_username(self):
        """检查用户名"""
        username = self.ui.textEdit.toPlainText().strip()
        if not username:
            return
            
        main_window = self.parent()
        if not main_window or not main_window.current_user:
            return
            
        # 如果用户名没有改变，不需要检查
        if username == main_window.current_user['username']:
            return
            
        # 检查用户名是否已被使用
        if User.get_by_username(username):
            self.show_message('<p class="custom-text">该用户名已存在</p>')
        
    def return_main(self):
        """返回主窗口"""
        print("[DEBUG] 返回主窗口")
        main_window = self.parent()
        if main_window:
            print(f"[DEBUG] 主窗口对象: {main_window}")
            main_window.show()
            main_window.init_user_info()  # 刷新主窗口的用户信息显示
            print("[DEBUG] 主窗口已显示")
        else:
            print("[DEBUG] 警告：无法获取主窗口对象")
        self.hide()
        print("[DEBUG] 修改信息窗口已隐藏")
        
    def save_changes(self):
        """保存修改"""
        print("[DEBUG] 尝试保存修改")
        main_window = self.parent()
        if not main_window or not main_window.current_user:
            print("[DEBUG] 无法获取主窗口或用户信息")
            return
            
        user_id = main_window.current_user['id']
        username = self.ui.textEdit.toPlainText().strip()
        password = self.ui.textEdit_4.toPlainText().strip()
        name = self.ui.textEdit_2.toPlainText().strip()
        
        if not username:
            QMessageBox.warning(self, "错误", "用户名不能为空！")
            return
            
        # 如果用户名改变了，检查是否已被使用
        if username != main_window.current_user['username']:
            if User.get_by_username(username):
                QMessageBox.warning(self, "错误", "该用户名已被使用！")
                return
                
        # 如果提供了新密码，检查密码强度
        if password:
            has_digit = any(c.isdigit() for c in password)
            has_upper = any(c.isupper() for c in password)
            has_lower = any(c.islower() for c in password)
            has_special = any(not c.isalnum() for c in password)
            
            if not all([has_digit, has_upper, has_lower, has_special, len(password) >= 8]):
                QMessageBox.warning(self, "错误", "密码不符合要求！")
                return
                
        db.connect()
        try:
            if password:
                # 更新包括密码在内的所有信息
                db.cursor.execute('''
                    UPDATE users 
                    SET username = ?, password = ?, name = ?
                    WHERE id = ?
                ''', (username, hash_password(password), name, user_id))
            else:
                # 只更新用户名和姓名
                db.cursor.execute('''
                    UPDATE users 
                    SET username = ?, name = ?
                    WHERE id = ?
                ''', (username, name, user_id))
            db.commit()
            
            # 更新主窗口中的用户信息
            db.cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            user = db.cursor.fetchone()
            if user:
                main_window.current_user = {
                    'id': user[0],
                    'username': user[1],
                    'password': user[2],
                    'role': user[3],
                    'name': user[4],
                    'email': user[5]
                }
                main_window.init_user_info()
            
            QMessageBox.information(self, "成功", "修改成功！")
            self.return_main()
        except Exception as e:
            QMessageBox.warning(self, "错误", f"修改失败：{str(e)}")
        finally:
            db.disconnect()
            
    def show_message(self, html_message):
        """显示消息"""
        self.ui.textBrowser.setHtml(f'''
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
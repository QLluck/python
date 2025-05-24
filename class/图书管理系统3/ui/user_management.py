import os
import sys
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import uic
from models import User
from utils import hash_password, validate_email
from config import ROLE_USER, ROLE_ADMIN
from database import db

def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class AddUserWindow(QWidget):
    def __init__(self):
        super().__init__()
        print("[DEBUG] 初始化添加用户窗口")
        # 加载UI
        ui_path = resource_path("ui/添加用户界面.ui")
        self.ui = uic.loadUi(ui_path, self)
        
        # 绑定按钮事件
        self.ui.pushButton.clicked.connect(self.return_main)  # 返回按钮
        self.ui.pushButton_2.clicked.connect(self.save_user)  # 保存按钮

    def return_main(self):
        """返回主窗口"""
        print("[DEBUG] 返回主窗口")
        main_window = self.parent()
        if main_window:
            print("[DEBUG] 显示主窗口")
            main_window.show()
            main_window.find_all_users('')  # 刷新用户列表
        self.hide()
        print("[DEBUG] 隐藏添加用户窗口")
        
    def save_user(self):
        """保存用户信息"""
        print("[DEBUG] 尝试保存用户信息")
        username = self.ui.lineEdit.text().strip()
        password = self.ui.lineEdit_2.text().strip()
        
        if not all([username, password]):
            print("[DEBUG] 用户名或密码为空")
            QMessageBox.warning(self, "错误", "用户名和密码不能为空！")
            return
            
        # 检查用户名是否已存在
        if User.get_by_username(username):
            print(f"[DEBUG] 用户名已存在: {username}")
            QMessageBox.warning(self, "错误", "该用户名已存在！")
            return
            
        try:
            user = User(username=username, 
                       password=hash_password(password),
                       role=ROLE_USER)
            user.save()
            print(f"[DEBUG] 用户添加成功: {username}")
            QMessageBox.information(self, "成功", "添加成功！")
            self.parent().show()
            self.hide()
            # 刷新主窗口的用户列表
            self.parent().find_all_users('')
        except Exception as e:
            print(f"[DEBUG] 用户添加失败: {str(e)}")
            QMessageBox.warning(self, "错误", f"添加失败：{str(e)}")

class ChangeUserWindow(QWidget):
    def __init__(self):
        super().__init__()
        print("[DEBUG] 初始化修改用户窗口")
        # 加载UI
        ui_path = resource_path("ui/用户修改页面.ui")
        self.ui = uic.loadUi(ui_path, self)
        
        self.user_id = None  # 当前编辑的用户ID
        
        # 绑定按钮事件
        self.ui.pushButton.clicked.connect(self.return_main)  # 返回按钮
        self.ui.pushButton_2.clicked.connect(self.save_changes)  # 保存按钮

    def showEvent(self, event):
        """窗口显示时加载用户信息"""
        super().showEvent(event)
        if self.user_id:
            self.load_user_info()
            
    def load_user_info(self):
        """加载用户信息"""
        db.connect()
        try:
            db.cursor.execute('SELECT * FROM users WHERE id = ?', (self.user_id,))
            user = db.cursor.fetchone()
            if user:
                self.ui.lineEdit.setText(user[1])  # 用户名
                self.ui.lineEdit_2.setText('')  # 密码留空
                self.ui.lineEdit_3.setText(user[4] or '')  # 姓名
                self.ui.lineEdit_4.setText(user[5] or '')  # 邮箱
                # 设置角色选择
                self.ui.comboBox.setCurrentText('管理员' if user[3] == ROLE_ADMIN else '普通用户')
        finally:
            db.disconnect()
            
    def return_main(self):
        """返回主窗口"""
        print("[DEBUG] 返回主窗口")
        main_window = self.parent()
        if main_window:
            print("[DEBUG] 显示主窗口")
            main_window.show()
            main_window.find_all_users('')  # 刷新用户列表
        self.hide()
        print("[DEBUG] 隐藏修改用户窗口")
        
    def save_changes(self):
        """保存修改"""
        if not self.user_id:
            return
            
        username = self.ui.lineEdit.text().strip()
        password = self.ui.lineEdit_2.text().strip()
        name = self.ui.lineEdit_3.text().strip()
        email = self.ui.lineEdit_4.text().strip()
        role = ROLE_ADMIN if self.ui.comboBox.currentText() == '管理员' else ROLE_USER
        
        if not username:
            QMessageBox.warning(self, "错误", "用户名不能为空！")
            return
            
        if email and not validate_email(email):
            QMessageBox.warning(self, "错误", "邮箱格式不正确！")
            return
            
        db.connect()
        try:
            # 检查用户名是否已被其他用户使用
            db.cursor.execute('SELECT id FROM users WHERE username = ? AND id != ?', 
                            (username, self.user_id))
            if db.cursor.fetchone():
                QMessageBox.warning(self, "错误", "该用户名已被其他用户使用！")
                return
                
            # 更新用户信息
            if password:
                # 如果提供了新密码，则更新密码
                db.cursor.execute('''
                    UPDATE users 
                    SET username = ?, password = ?, role = ?, name = ?, email = ?
                    WHERE id = ?
                ''', (username, hash_password(password), role, name, email, self.user_id))
            else:
                # 如果没有提供新密码，则不更新密码
                db.cursor.execute('''
                    UPDATE users 
                    SET username = ?, role = ?, name = ?, email = ?
                    WHERE id = ?
                ''', (username, role, name, email, self.user_id))
            db.commit()
            
            QMessageBox.information(self, "成功", "修改成功！")
            self.parent().show()
            self.hide()
            # 刷新主窗口的用户列表
            self.parent().find_all_users('')
        except Exception as e:
            QMessageBox.warning(self, "错误", f"修改失败：{str(e)}")
        finally:
            db.disconnect() 
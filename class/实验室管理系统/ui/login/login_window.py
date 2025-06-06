from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt5 import uic
import sys
import os
import utils.path_helper 
import ui.login.register_window
from ui.ui_tools import UITools
from utils.icon_helper import set_app_icon
from utils.logger import info, debug, warning, error, exception
from utils import ValidationUtils as vu
from database import User
from utils import HashUtils as hu

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 加载UI文件
        uic.loadUi(utils.path_helper.get_ui_path('login/login_window.ui'), self)
        debug(utils.path_helper.get_ui_path('login/login_window.ui'))
        # 设置窗口图标
        set_app_icon(self)
        
        # 绑定按钮事件
        self.pushButton.clicked.connect(self.login)  # 登录按钮
        self.pushButton_2.clicked.connect(self.register)  # 注册按钮
        self.pushButton_3.clicked.connect(self.exit_system)  # 退出按钮
        
        # 设置错误提示样式
        self.textBrowser_2.setStyleSheet("""
            QTextBrowser {
                color: red;
                background-color: transparent;
                border: none;
            }
        """)
        
        # 居中显示窗口
        UITools.center_window(self)
        
        # 初始化用户对象
        self.current_user = None
        
        debug("登录窗口初始化完成")
        
    def login(self):
        """登录功能"""
        info(f"用户尝试登录")
        username = self.lineEdit_7.text().strip()  # 获取账号
        password = self.lineEdit_5.text().strip()  # 获取密码
        self.clear_error()
        
        # 验证输入不能为空
        if not username or not password:
            warning("用户名或密码为空")
            self.show_error("用户名和密码不能为空！")
            return
            
        try:
            # 验证用户名格式
            is_valid, error_msg = vu.validate_username(username)
            if not is_valid:
                warning(f"用户名格式错误: {error_msg}")
                self.show_error(error_msg)
                return
                
            # 验证密码格式
            is_valid, error_msg = vu.validate_password(password)
            if not is_valid:
                warning(f"密码格式错误: {error_msg}")
                self.show_error(error_msg)
                return
            #对密码进行哈希加密
            password = hu.hash_string(password)
            # 创建用户对象并尝试登录
            user = User()
            if user.login(username, password):
                self.current_user = user
                info(f"用户 {username} 登录成功")
                self.login_success()
            else:
                warning(f"用户 {username} 登录失败")
                self.show_error("用户名或密码错误！")
                
        except ValueError as e:
            warning(f"登录验证错误: {str(e)}")
            self.show_error("用户名或密码错误！")
        except Exception as e:
            error(f"登录过程发生错误: {str(e)}")
            exception("登录异常详细信息")
            QMessageBox.critical(self, "错误", "登录失败，请稍后重试！")
    
    def login_success(self):
        """登录成功后的处理"""
        info(f"准备打开{self.current_user.role}角色的主界面")
        try:
            from ui.menu.main_window import MainWindow
            # 传入登录窗口实例
            self.main_window = MainWindow(self.current_user.get_info(), self)
            self.main_window.show()
            self.hide()
            QMessageBox.information(self, "成功", "登录成功！")
        except Exception as e:
            error(f"打开主界面失败: {str(e)}")
            exception("打开主界面异常详细信息")
            QMessageBox.critical(self, "错误", "打开主界面失败，请稍后重试！")
        
    def show_error(self, message):
        """显示错误信息"""
        self.textBrowser_2.setText(f"<p style='color: red;'>{message}</p>")
        
    def clear_error(self):
        """清除错误信息"""
        self.textBrowser_2.clear()
        
    def register(self):
        """打开注册界面"""
        info("用户点击注册按钮，准备打开注册界面")
        self.register_window = ui.login.register_window.RegisterWindow()
        UITools.adjust_new_window_position(self, self.register_window)
        self.register_window.show()
        self.hide()
        debug("注册界面已打开")
        
    def exit_system(self):
        """退出系统"""
        info("用户退出系统")
        QApplication.quit()
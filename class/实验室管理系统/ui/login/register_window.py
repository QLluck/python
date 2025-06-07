from PyQt5 import uic
import sys
import os
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
import utils
from ui.ui_tools import UITools
from utils.icon_helper import set_app_icon
from utils.logger import info, debug, warning, error, exception
from utils import ValidationUtils as vu
from database.models.user import User
from datetime import datetime
from utils import db 
from utils import HashUtils as hu
class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 加载UI文件
        uic.loadUi(utils.path_helper.get_ui_path('login/register_window.ui'), self)
        
        # 设置窗口图标
        set_app_icon(self)
        
        # 绑定按钮事件
        self.pushButton.clicked.connect(self.do_register)      # 注册按钮
        self.pushButton_2.clicked.connect(self.back_to_login)  # 返回按钮
        self.pushButton_3.clicked.connect(self.exit_system)    # 退出按钮
        
        # 设置错误提示文本框样式
        self.textBrowser_2.setStyleSheet("""
            QTextBrowser {
                color: red;
                background-color: transparent;
                border: none;
            }
        """)
        
        # 居中显示窗口
        UITools.center_window(self)
        #
        debug("注册窗口初始化完成")        
    def validate_input(self):
        """验证输入"""
        info("验证注册账号输入")
        username = self.lineEdit_7.text().strip()
        password = self.lineEdit_5.text().strip()
        
        result = vu.validate_username(username)
        # 检查是否为空
        if not result[0]:
            self.show_error(result[1])
            warning(result[1])
            return False
        result = vu.validate_password(password)
        if not result[0]:
            self.show_error(result[1])
            warning(result[1])
            return False
        with db.get_connection() as conn:
            cursor=conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user=cursor.fetchone()
            if user:
                self.show_error("用户已存在")
                warning("用户尝试注册{username}用户已存在")
                return False

        
        return True
        
    def do_register(self):
        """执行注册"""
        info("执行注册")
        try:
            # 清除错误提示
            self.clear_error()
            
            # 获取输入
            username = self.lineEdit_7.text().strip()
            password = self.lineEdit_5.text().strip()
            
            # 验证输入
            if not self.validate_input(): 
                return
            
            # 这里暂时只显示成功消息，不进行实际的数据库操作
            user=User()
            user.username=username
            user.password=hu.hash_string(password)
            user.role="student"
            
            try:
                # TODO: 实际的数据库操作
                db.insert("users", user.get_info())
                
                pass
            except Exception as e:
                error(f"提交数据库信息失败: {str(e)}")
                exception("详细错误信息")
                QMessageBox.information(
                    self,
                    "错误",
                    f"账号 {username} 注册失败！\n请重试",
                    QMessageBox.Ok
                )
                return  # 如果出错就直接返回，不执行后面的成功消息

            # 只有在没有错误的情况下才显示成功消息
            QMessageBox.information(
                self,
                "注册成功",
                f"账号 {username} 注册成功！\n请返回登录。",
                QMessageBox.Ok
            )
            # 返回登录界面
            self.back_to_login()
                
        except Exception as e:
            error(f"登录过程发生错误: {str(e)}")
            exception("登录异常详细信息")
            QMessageBox.critical(self, "错误", "注册失败，请稍后重试！")
            
    def show_error(self, message):
        """显示错误信息"""
        self.textBrowser_2.setText(f"<p style='color: red;'>{message}</p>") #使用https格式
        
    def clear_error(self):
        """清除错误信息"""
        self.textBrowser_2.clear()
        
    def back_to_login(self):
        """返回登录界面"""
        info("返回登录界面")
        from ui.login.login_window import LoginWindow
        self.login_window = LoginWindow()
        # 根据当前窗口位置调整登录窗口位置
        UITools.adjust_new_window_position(self, self.login_window)
        self.login_window.show()
        self.close()
        debug("返回登录界面完成")
    def exit_system(self):
        """退出系统"""
        info("退出系统")
        QApplication.quit()

# 测试代码
if __name__ == "__main__":
    app = QApplication(sys.argv)
    register_window = RegisterWindow()
    register_window.show()
    sys.exit(app.exec_())
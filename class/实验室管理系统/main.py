#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
实验室管理系统主入口文件
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon#设置图标
from ui.login.login_window import LoginWindow
from utils.icon_helper import get_icon_path

def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序图标
    app.setWindowIcon(QIcon(get_icon_path('app_icon.svg'))) #导入图标路径
    
    # 显示登录窗口
    login_window = LoginWindow()
    login_window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 
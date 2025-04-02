import os, sys
from library_management_system.ui import show_welcome, show_error
from library_management_system.auth import register, login

def main():
    # 显示欢迎界面并获取用户选择
    flag = show_welcome()
    
    # 根据用户选择执行相应功能
    if flag == "1":
        # 注册
        register()
    elif flag == "2":
        # 登录
        login()
    else:
        # 用户既不选择登录也不选择注册
        show_error("请输入数字1或者2！")

if __name__ == "__main__":
    main()

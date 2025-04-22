from .registration import zhuce
from .login import denlu
from .user_menu import userMenu
from .admin_menu import adminMenu

# 初始化数据
vip_info = [{'name': '张三', 'psw': ''},
            {'name': '李四', 'psw': 'ls444444'},
            {'name': '王五', 'psw': 'ww555555'},
            {'name': '周六', 'psw': 'zl666666'},
            {'name': '袁鑫晨', 'psw': '2415929709'}]
data = [{'name': '张三', 'id': 'zs333333', '性别': '男'},
        {'name': '李四', 'id': 'ls444444', '性别': '男'},
        {'name': '王五', 'id': 'ww555555', '性别': '男'},
        {'name': '周六', 'id': 'zl666666', '性别': '男'},
        {'name': '袁鑫晨', 'id': '2415929709', '性别': '男'}]
# 用户名列表
vip_name = [vip_info[i]["name"] for i in range(len(vip_info))]

# 建立敏感词库
sensitive_character = ["傻", "屁", "草", "操", "垃圾", "z", "蠢", "笨", "呆"]
# 管理员
adminList = ["张三", "李四"]

def main():
    while True:
        print("欢迎使用本系统！")
        print("1. 注册")
        print("2. 登录")
        print("3. 退出系统")
        choice = input("请输入你的选择: ")
        if choice == '1':
            zhuce(vip_info, vip_name, data, sensitive_character)
        elif choice == '2':
            user = denlu(vip_info, vip_name, data, sensitive_character)
            if user:
                if user in adminList:
                    adminMenu(user, vip_info, vip_name, data, sensitive_character)
                else:
                    userMenu(user, vip_info, vip_name, data)
        elif choice == '3':
            print("已退出系统。")
            break
        else:
            print("无效的选择，请重新输入。")

if __name__ == "__main__":
    main()
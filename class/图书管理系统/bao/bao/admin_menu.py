from .registration import zhuce
from . import login

def userAdd(vip_info, vip_name, data):
    zhuce(vip_info, vip_name, data, [])  # 调用注册函数

def userChange(vip_info, vip_name, data):
    name = input("请输入要修改信息的用户名: ")
    if name not in vip_name:
        print("该用户名未注册，无法修改信息。")
        return
    for i in range(len(vip_info)):
        if vip_info[i]['name'] == name:
            print("请输入新密码，输入过程中密码将以 * 显示: ")
            new_psw = login.jiami()
            vip_info[i]['psw'] = new_psw
    for i in range(len(data)):
        if data[i]['name'] == name:
            new_id = input("请输入新的用户ID: ")
            new_gender = input("请输入新的用户性别: ")
            data[i]['id'] = new_id
            data[i]['性别'] = new_gender
    print("用户信息修改成功！")

def userDelete(vip_info, vip_name, data):
    name = input("请输入要删除的用户名: ")
    if name not in vip_name:
        print("该用户名未注册，无法删除。")
        return
    for vip in vip_info:
        if vip['name'] == name:
            vip_info.remove(vip)
            vip_name.remove(name)
    for d in data:
        if d['name'] == name:
            data.remove(d)
    print("用户删除成功！")

def userPrint(vip_info, vip_name, data):
    print("用户信息如下：")
    for i in range(len(vip_info)):
        print(f"用户名: {vip_info[i]['name']}, 密码: {vip_info[i]['psw']}, ID: {data[i]['id']}, 性别: {data[i]['性别']}")

def adminMenu(user, vip_info, vip_name, data, sensitive_character):
    while True:
        print(f"欢迎，管理员 {user}！")
        print("1. 添加用户")
        print("2. 修改用户信息")
        print("3. 删除用户")
        print("4. 查看用户信息")
        print("5. 退出管理界面")
        choice = input("请输入你的选择: ")
        if choice == '1':
            userAdd(vip_info, vip_name, data)
        elif choice == '2':
            userChange(vip_info, vip_name, data)
        elif choice == '3':
            userDelete(vip_info, vip_name, data)
        elif choice == '4':
            userPrint(vip_info, vip_name, data)
        elif choice == '5':
            print("已退出管理界面。")
            break
        else:
            print("无效的选择，请重新输入。")
import msvcrt, os, sys

# 密码加密显示
def jiami():
    password = ""
    while True:
        char = msvcrt.getch()
        if char == b'\r':  # 回车表示输入结束
            print()
            break
        elif char == b'\x08':  # 退格键
            if password:
                password = password[:-1]
                print('\b \b', end='', flush=True)
        else:
            password += char.decode()
            print('*', end='', flush=True)
    return password

def zhuce():
    name = input("请输入要注册的用户名: ")
    if name in vip_name:
        print("该用户名已存在，请重新选择。")
        return
    # 检查敏感词
    for word in sensitive_character:
        if word in name:
            print("用户名包含敏感词，请重新输入。")
            return
    print("请输入密码，输入过程中密码将以 * 显示: ")
    psw = jiami()
    new_vip = {'name': name, 'psw': psw}
    vip_info.append(new_vip)
    vip_name.append(name)
    id = input("请输入用户ID: ")
    gender = input("请输入用户性别: ")
    new_data = {'name': name, 'id': id, '性别': gender}
    data.append(new_data)
    print("注册成功！")

def denlu():
    name = input("请输入用户名: ")
    if name not in vip_name:
        print("该用户名未注册，请先注册。")
        return
    print("请输入密码，输入过程中密码将以 * 显示: ")
    psw = jiami()
    for vip in vip_info:
        if vip['name'] == name and vip['psw'] == psw:
            print("登录成功！")
            return name
    print("密码错误，请重新输入。")
    return None

def userMenu():
    while True:
        print(f"欢迎，{user}！")
        print("1. 退出登录")
        choice = input("请输入你的选择: ")
        if choice == '1':
            print("已退出登录。")
            break
        else:
            print("无效的选择，请重新输入。")

def adminMenu():
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

def userAdd():
    zhuce(vip_info, vip_name, data, [])  # 调用注册函数

def userChange(vip_info, vip_name, data):
    name = input("请输入要修改信息的用户名: ")
    if name not in vip_name:
        print("该用户名未注册，无法修改信息。")
        return
    for i in range(len(vip_info)):
        if vip_info[i]['name'] == name:
            print("请输入新密码，输入过程中密码将以 * 显示: ")
            new_psw = jiami()
            vip_info[i]['psw'] = new_psw
    for i in range(len(data)):
        if data[i]['name'] == name:
            new_id = input("请输入新的用户ID: ")
            new_gender = input("请输入新的用户性别: ")
            data[i]['id'] = new_id
            data[i]['性别'] = new_gender
    print("用户信息修改成功！")

def userDelete():
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

def userPrint():
    print("用户信息如下：")
    for i in range(len(vip_info)):
        print(f"用户名: {vip_info[i]['name']}, 密码: {vip_info[i]['psw']}, ID: {data[i]['id']}, 性别: {data[i]['性别']}")

# ---------------【系统初始化】---------------
# vip_info  系统内已注册用户信息表
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

# ---------------【欢迎界面】---------------
main()
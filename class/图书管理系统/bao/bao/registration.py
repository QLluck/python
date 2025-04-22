import msvcrt

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

def zhuce(vip_info, vip_name, data, sensitive_character):
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
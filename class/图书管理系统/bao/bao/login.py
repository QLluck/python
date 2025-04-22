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

def denlu(vip_info, vip_name, data, sensitive_character):
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
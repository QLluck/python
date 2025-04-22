def userMenu(user, vip_info, vip_name, data):
    while True:
        print(f"欢迎，{user}！")
        print("1. 退出登录")
        choice = input("请输入你的选择: ")
        if choice == '1':
            print("已退出登录。")
            break
        else:
            print("无效的选择，请重新输入。")
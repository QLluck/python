  welcome = ["===========================",
               "欢迎使用图书馆借阅管理系统",
               "开始进行用户注册",
               "==========================="]
    for i in welcome:
        print("%s" % i.center(18, "　"))


    reg_name = input("请输入注册用户名：\n")  # 接收"新注册的用户名"。
    for i in sensitive_character:
        while True:
            if i in reg_name:
                reg_name = reg_name.replace(i, '*')
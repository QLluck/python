import msvcrt, os, sys
'''
msvcrt.getche() 用于读取一个键盘按键，
并且以byte型返回，但是不会在控制台（一般是命令行）回显。
'''

# 密码加密显示
def jiami():
    print('请输入注册密码: ')
    li = []
    while 1:
        ch = msvcrt.getch()
        print(ch)
        if ch == b'\r':     # 回车
            # return b''.join(li).decode()  # 把list转换为字符串返回
            break
        elif ch == b'\x08':     # 退格
            if li:
                li.pop()
                msvcrt.putch(b'\b')
                msvcrt.putch(b' ')
                msvcrt.putch(b'\b')
        # Esc
        elif ch == b'\x1b':
            break
        else:
            li.append(ch)
            msvcrt.putch(b'*')
            print(li)
    return b''.join(li).decode()


#---------------【系统初始化】---------------
# vip_info  系统内已注册用户信息表
vip_info = [{'name': '张三', 'psw': 'zs333333'},
            {'name': '李四', 'psw': 'ls444444'},
            {'name': '王五', 'psw': 'ww555555'},
            {'name': '周六', 'psw': 'zl666666'}]

# 用户名列表
vip_name = [vip_info[i]["name"] for i in range(len(vip_info))]
# print(vip_name)  # ['张三', '李四', '王五', '周六']


# 建立敏感词库
sensitive_character = ["傻", "屁", "草", "操", "垃圾", "z"]


#---------------【欢迎界面】---------------
welcome = ["===========================",
           "欢迎使用图书馆借阅管理系统",
           "1 注册",
           "2 登录",
           "==========================="]
for i in welcome:
    print("%s" % i.center(18, "　"))

flag = input("请输入（1 or 2）选择系统功能:")


#---------------【注册】---------------
if flag == "1":
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
                print("用户名包含非法字{}，请重新输入。".format(reg_name))
                # 让用户重新输用户名。
                reg_name = input("请输入注册用户名：\n")
            else:
                break

    # 2、用户名是否已注册，如果已注册，让用户重新填写用户名
    if reg_name in vip_name:
        print('该用户名已被注册！')  # 如果已经存在，提示用于无法注册。

    else:
        # 3、如果用户名合法且不存在，则进行更进一步的注册操作，输入密码判断密码是否合法。
        while True:
            reg_psw = input("请输入注册密码：\n")
            #reg_psw = jiami()
            print(reg_psw)
            # 4、判断密码长度
            if len(reg_psw) < 6:
                print('密码太简单!密码长度应为为6-18位!，请重新输入：')
                continue

            # 5、判断密码是否为密码+数字混合型
            # .isalpha()方法检测字符串是否只由字母组成。.isdigit() 方法检测字符串是否只由数字组成。
            elif reg_psw.isalpha() or reg_psw.isdigit():
                print("请不要使用纯字母或纯数字密码，应该为数字字母混合密码，请重新输入：")
                continue

            else:
                # 定义一个字典，用于接收新注册用户的“用户名-密码”键值对表。
                person_info = dict.fromkeys(["name", "psw"])
                # 将用“户名-密码”键值对存入字典。
                person_info['name'] = reg_name
                person_info['psw'] = reg_psw
                # 将新注册用户信息更新到vip_info表内。
                vip_info += [person_info]
                print("恭喜，注册成功。")

                #---------------【更新vip数据库】---------------
                # 将新注册用户信息写入info文件。涉及知识点列表元素的添加。
                vip_name = [vip_info[i]["name"] for i in range(len(vip_info))]
                # print("更新后的用户信息表：", vip_info)


                # ---------------【注册完成后，让新用户登录系统】---------------
                welcome = ["===========================",
                           "欢迎使用图书馆借阅管理系统",
                           "开始进行用户登录",
                           "==========================="]
                for i in welcome:
                    print("%s" % i.center(18, "　"))


                # 创建一个新的空用户名字典用于存储当前登录用户信息
                log_vip = dict.fromkeys(["name", "psw"])

                log_conut1 = 3
                while log_conut1:
                    log_name = input("请输入用户名：\n")
                    # 如果用户名不存在，则登录失败。
                    if log_name not in vip_name:
                        log_conut1 -= 1
                        # 判断用户是否存在，如果不存在提示“用户名不存在，请先完成注册！”。
                        print("用户名不存在，您还要{}次试错机会。".format(log_conut1))
                        continue

                    else:
                        # 如果用户名存在，则继续往下判断。
                        # 则获取该用户名的索引，因为后面需要通过索引得到密码数据。
                        conut_log2 = 3
                        while conut_log2:
                            conut_log2 -= 1

                            cur_index = vip_name.index(log_name)
                            log_psw = input("请输入登录密码：\n")
                            log_vip["name"] = log_name
                            log_vip["psw"] = log_psw

                            # 判断密码是否正确，如果正确登录成功。
                            if log_psw == vip_info[cur_index]['psw']:
                                print('登录成功!跳转到《图书馆借阅管理系统》使用页面...')
                                break

                            # 如果密码不正确，提示密码错误，并尝试重新输入。
                            else:
                                print("密码输入不正确。您还有{}次试错机会。".format(conut_log2))
                                continue
                    break
                break


#---------------【登录】---------------
elif flag == "2":
    welcome = ["===========================",
               "欢迎使用图书馆借阅管理系统",
               "开始进行用户登录",
               "==========================="]
    for i in welcome:
        print("%s" % i.center(18, "　"))

    # 创建一个新的空用户名字典用于存储当前登录用户信息
    log_vip = dict.fromkeys(["name", "psw"])


    log_conut1 = 3
    while log_conut1:
        log_name = input("请输入用户名：\n")
        # 如果用户名不存在，则登录失败。
        if log_name not in vip_name:
            log_conut1 -= 1
            # 判断用户是否存在，如果不存在提示“用户名不存在，请先完成注册！”。
            print("用户名不存在，您还要{}次试错机会。".format(log_conut1))
            continue

        else:
            # 如果用户名存在，则继续往下判断。
            #则获取该用户名的索引，因为后面需要通过索引得到密码数据。
            conut_log2 = 3
            while conut_log2:
                conut_log2 -= 1

                cur_index = vip_name.index(log_name)
                log_psw = input("请输入登录密码：\n")
                log_vip["name"] = log_name
                log_vip["psw"] = log_psw

                # 判断密码是否正确，如果正确登录成功。
                if log_psw == vip_info[cur_index]['psw']:
                    print('登录成功!跳转到《图书馆借阅管理系统》使用页面...')
                    break

                # 如果密码不正确，提示密码错误，并尝试重新输入。
                else:
                    print("密码输入不正确。您还有{}次试错机会。".format(conut_log2))
                    continue
        break

#---------------【用户既不选择登录也不选择注册】---------------
else:
    print("请输入数字1或者2！")




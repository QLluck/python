# 显示欢迎界面
def show_welcome():
    welcome = ["===========================",
               "欢迎使用图书馆借阅管理系统",
               "1 注册",
               "2 登录",
               "==========================="]
    for i in welcome:
        print("%s" % i.center(18, "　"))
    return input("请输入（1 or 2）选择系统功能:")

# 显示注册界面
def show_register_ui():
    welcome = ["===========================",
               "欢迎使用图书馆借阅管理系统",
               "开始进行用户注册",
               "==========================="]
    for i in welcome:
        print("%s" % i.center(18, "　"))

# 显示登录界面
def show_login_ui():
    welcome = ["===========================",
               "欢迎使用图书馆借阅管理系统",
               "开始进行用户登录",
               "==========================="]
    for i in welcome:
        print("%s" % i.center(18, "　"))

# 显示登录成功信息
def show_login_success():
    print('登录成功!跳转到《图书馆借阅管理系统》使用页面...')

# 显示错误信息
def show_error(message):
    print(message)

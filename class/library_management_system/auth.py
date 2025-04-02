from library_management_system.data import get_vip_names, add_user, verify_user, check_sensitive_words
from library_management_system.ui import show_register_ui, show_login_ui, show_login_success, show_error
from library_management_system.utils import jiami

# 注册功能
def register():
    show_register_ui()
    
    # 获取用户名并检查合法性
    reg_name = input("请输入注册用户名：\n")
    is_valid, reg_name = check_sensitive_words(reg_name)
    while not is_valid:
        show_error("用户名包含非法字{}，请重新输入。".format(reg_name))
        reg_name = input("请输入注册用户名：\n")
        is_valid, reg_name = check_sensitive_words(reg_name)
    
    # 检查用户名是否已注册
    vip_names = get_vip_names()
    if reg_name in vip_names:
        show_error('该用户名已被注册！')
        return False
    
    # 密码注册
    while True:
        # 可以使用加密输入或普通输入
        # reg_psw = jiami()
        reg_psw = input("请输入注册密码：\n")
        print(reg_psw)
        
        # 判断密码长度
        if len(reg_psw) < 6:
            show_error('密码太简单!密码长度应为为6-18位!，请重新输入：')
            continue
        
        # 判断密码是否为密码+数字混合型
        elif reg_psw.isalpha() or reg_psw.isdigit():
            show_error("请不要使用纯字母或纯数字密码，应该为数字字母混合密码，请重新输入：")
            continue
        
        else:
            # 添加用户
            add_user(reg_name, reg_psw)
            show_error("恭喜，注册成功。")
            
            # 注册成功后自动登录
            return login()

# 登录功能
def login():
    show_login_ui()
    
    # 创建一个新的空用户名字典用于存储当前登录用户信息
    log_vip = dict.fromkeys(["name", "psw"])
    
    # 用户名验证，最多尝试3次
    log_count1 = 3
    while log_count1:
        log_name = input("请输入用户名：\n")
        vip_names = get_vip_names()
        
        # 如果用户名不存在
        if log_name not in vip_names:
            log_count1 -= 1
            show_error("用户名不存在，您还要{}次试错机会。".format(log_count1))
            continue
        
        # 如果用户名存在，验证密码，最多尝试3次
        else:
            count_log2 = 3
            while count_log2:
                count_log2 -= 1
                
                log_psw = input("请输入登录密码：\n")
                log_vip["name"] = log_name
                log_vip["psw"] = log_psw
                
                # 验证密码
                success, message = verify_user(log_name, log_psw)
                if success:
                    show_login_success()
                    return True, log_vip
                else:
                    show_error("密码输入不正确。您还有{}次试错机会。".format(count_log2))
                    continue
        
        # 如果用户名存在但密码尝试次数用完，退出循环
        break
    
    return False, None

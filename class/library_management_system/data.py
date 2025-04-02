# 系统内已注册用户信息表
vip_info = [{'name': '张三', 'psw': 'zs333333'},
            {'name': '李四', 'psw': 'ls444444'},
            {'name': '王五', 'psw': 'ww555555'},
            {'name': '周六', 'psw': 'zl666666'}]

# 用户名列表
def get_vip_names():
    return [vip_info[i]["name"] for i in range(len(vip_info))]

# 建立敏感词库
sensitive_character = ["傻", "屁", "草", "操", "垃圾", "z"]

# 添加新用户到系统
def add_user(username, password):
    person_info = {'name': username, 'psw': password}
    vip_info.append(person_info)
    return True

# 验证用户登录
def verify_user(username, password):
    vip_names = get_vip_names()
    if username not in vip_names:
        return False, "用户名不存在"
    
    cur_index = vip_names.index(username)
    if password == vip_info[cur_index]['psw']:
        return True, "登录成功"
    else:
        return False, "密码不正确"

# 检查用户名是否包含敏感词
def check_sensitive_words(username):
    original = username
    for i in sensitive_character:
        if i in username:
            username = username.replace(i, '*')
    
    if original != username:
        return False, username
    return True, username

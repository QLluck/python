import getpass, os, sys

def jiami():
    print('请输入注册密码: ')
    # 使用getpass模块，这是跨平台的，在macOS上也能工作
    password = getpass.getpass(prompt='')
    return password
s = jiami();
print(f"输入的密码是{s}");

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
s=jiami();
print(f"{s}")
import msvcrt, os, sys

def jiami():
    print('请输入注册密码: ')
    li = []
    while 1:
        ch = msvcrt.getch()#接受键盘输入数据 不显示在终端里
       
        if ch == b'\r':     #如果输入为回车 就退出输入
           
            break
        elif ch == b'\x08':      #  如果输入等于退格键
            if li:
                li.pop()#删除pop
                msvcrt.putch(b'\b')#光标往左边移动一格
                msvcrt.putch(b' ')#覆盖当前位置的字符
                msvcrt.putch(b'\b')#光标往左边移动一格
        # Esc1
        elif ch == b'\x1b': # 如果输入字符等于esc 就结束
            break
        else:
            li.append(ch)
            msvcrt.putch(b'*')
            #print(li)
    return b''.join(li).decode() # return b''.join(li).decode()  # 把list转换为字符串返回
s =  jiami();
print()
print(f"您输入的密码是{s}")
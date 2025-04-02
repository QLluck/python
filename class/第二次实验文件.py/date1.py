import datetime
def f(n:str,m:str):
        m= datetime.datetime.strptime(m, "%Y-%m-%d %H:%M:%S")
        n=datetime.datetime.strptime(n, "%Y-%m-%d %H:%M:%S")
      
        td=(n-m).seconds;
        dd=(n-m).days;
        # print(f"差值为{(n-m).days}天{(n-m).seconds}秒")
        if dd<0:
            print(f"{m}>{n}:未来时间")
        elif dd/365>=1:
            print(f"{m}>{n}:{m.year}年{m.month}月")
        elif dd/30 >=1:
            print(f"{m}>{n}:{m.year}年{m.month}月{m.day}日")
        elif dd>=1:
            print(f"{n}>{m}:{dd}天前")
        elif td/3600>=1:
            print(f"{n}>{m}:{ td//3600 }小时前")
        elif td/60>=1:
            print(f"{n}>{m}:{ td//60 }分钟前")
        elif td>=0:
            print(f"{n}<{m}:{td}秒前")
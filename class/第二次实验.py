def class_1():
    x = int(input())
    def f(x):
        if x<1 :
            return x
        elif 1<=x and x<10 :
            return 2*x-1
        elif 10<=x :
            return 3*x-11
    print(f(x))
    print("24软工智能一班袁鑫晨 2415929709 6组6号")

def class_2():
    
    l1 = eval(input())
    l2=eval(input())
    def f(l1:list,l2:list):

        l1.extend(l2)#将l2添加到l1后面
        l1.sort()#对l1排序
        return l1 ;#返回新列表
    print(f(l1,l2))
    print("24软工智能一班袁鑫晨 2415929709 6组6号")

def class_3():
    s = input()
    def f(s:str):
        #先转小写
        s=s.lower();
        #print(s)

        #提取s中所有数字和字母字符 加入ans
        ans =""
        for i in s :#将字符转成ascll码值进行比较
            #如果字符是数字或字母 则加入字符串ans
            if ord('0')<=ord(i) and ord(i)<=ord('9'): 
                ans = ans+ i ;
            elif ord('a')<= ord(i) and ord(i)<=ord('z') :
                ans= ans+ i ;
        if ans==ans[::-1]:#用切片反转操作判断是否是回文字符串
            return True
        else :
            return False
    
    print(f(s));
    print("24软工智能一班袁鑫晨 2415929709 6组6号")
def class_4():
    lis=  list(map(int,input("输入学生成绩").split(','))) #将字符串分割并将其转换成字典
   # print(lis)
    def f(args):
        ma = max(args)#求最大值
        mi = min(args)#求最小值
      #  print(args)
        
        arrag =round( sum(args)/len(args),1);#求平均值并保留一位小数

        num = 0 ;
        for i in args:#求不及格人数num
            if i<60 :
                num+=1;
        return (arrag,ma,mi,num)

    print(f(lis));
    print("24软工智能一班袁鑫晨 2415929709 6组6号")

    
    
def class_5():
    import math#导入math包
    a,b =map(int,input("请输入两个数").split()) 
    def is_prime(x):#判断是否为素数的函数  思路是从2到x-1遍历i 如果遇到能整除x的数就不是素数 反之是
        for i in range(2,x):
            if(x%i==0):
                return False


        return True
    sum = 0 ;
    for i in range(a,b+1):#遍历a到b 如果是素数就加其平方
        if is_prime(i):
            sum += math.pow(i,2);
    print(int(sum));#输出是小数,转成整数
    print("24软工智能一班袁鑫晨 2415929709 6组6号")

def class_6():
    lis =[ eval(i) for i in  input("输入参数").split()];
    print(lis)
    def is_int(s): #自己写的判断是否为整数和字母
        for i in s:
            if ord('0')<=ord(i) and ord(i)<=ord('9'):
                continue
            else :
                return False
        return True
    def my_sum(*args):
        sum = 0 ;
        print(*args)
        

        for i in list(*args) :
            if is_int(i):
                sum += int(i) ;
        return sum
    print( my_sum(lis))
    print("24软工智能一班袁鑫晨 2415929709 6组6号")
class_6()










def class_7() :
      def a(m,n):
          if m==0:
              return n+1
          elif m>0 and n==0 :
              return a(m-1,1)
          elif m>0 and n>0:
              return a(m-1,a(m,n-1))
      m,n=map(int,input("输入两个不大于4和3的整数").split());
      print(a(m,n))
      print("24软工智能一班袁鑫晨 2415929709 6组6号");

def class_8():
    persons = [{'name': 'Dong', 'age': 37},

               {'name': 'Zhang', 'age': 40},

               {'name': 'Li', 'age': 50},

               {'name': 'Dong', 'age': 43}]
    def f(lis):

        lis =sorted(persons, key=lambda x:(x["name"],-x["age"]))
        return lis

    persons=f(persons)
    print(persons)
    print("24软工智能一班袁鑫晨 2415929709 6组6号")


import datetime
def f(n,m):
        td=(n-m).seconds;
        if td/3600/24 /365>=1:
            print(f"{n}>{m}:{m}")
            return
        elif td/3600 /24 >=1:
            print(f"{n}>{m}:{td}天前")
        elif td/3600>=1:
            print(f"{n}>{m}:{td}小时前")
        elif td>=0:
            print(f"{n}>{m}:{td}秒前")
        elif td<0:
            print(f"{n}<{m}:未来时间")

def class_9():
    import datetime
    import data1
    ji = input("输入基准时间")
    ji = datetime.datetime.strptime(ji, "%Y-%m-%d %H:%M:%S")
    ce =  input("输入测试时间")
    ce = datetime.datetime.strptime(ce, "%Y-%m-%d %H:%M:%S")
    data1.f(ce,ji)
    print(ji);


def class_10():
    import numpy as np
    a1 = eval(input("输入a1"))

    b1 = eval(input("输入b1"))
    a1=np.array(a1);
    b1=np.array(b1)
    a2 = eval(input("输入a2"))
    b2 = eval(input("输入b2"))
    a2 = np.array(a2);
    b2 = np.array(b2)
    def  f(a1,a2):
        return a1.dot(a2)

    print(f(a1,b1));
    print(f(a2,b2))

def class_11():
    s=input();
    ans=[]
    def f(s):
        return s==s[::-1]
    for i in range(1,len(s)+1):
        for j in range(len(s)-i+1):
            if f(s[j:j+i]):
                ans.append(s[j:j+i]);
    print(ans);





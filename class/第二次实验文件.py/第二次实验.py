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
    lis =[ eval(i) for i in  input("输入参数").split()];#用eval()把字符串转换成表达式
    
   
    def my_sum(*args):
        sum = 0 ;
        print(*args)
        

        for i in list(*args) :
            if str(type(i))=="<class 'int'>":
                sum += int(i) ;
        return sum
    print( my_sum(lis))
    print("24软工智能一班袁鑫晨 2415929709 6组6号")











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
    persons = eval(input())
    def f(lis):

        lis =sorted(persons, key=lambda x:(x["name"],-x["age"]))
        return lis

    persons=f(persons)
    print(persons)
    print("24软工智能一班袁鑫晨 2415929709 6组6号")



def class_9():
    import datetime
    import date1
    # ji = input("输入基准时间")
    # ce =  input("输入测试时间")
    ce="2020-02-29 09:30:30"
    ji ="2018-03-01 09:00:00"
    date1.f(ce,ji)
    ce="2020-02-29 09:30:30"
    ji ="2020-01-01 09:00:00"
    date1.f(ce,ji)
    ce="2020-02-29 09:30:30"
    ji ="2020-02-01 09:00:00"
    date1.f(ce,ji)
    ce="2020-02-29 09:30:30"
    ji ="2020-02-29 08:00:00"
    date1.f(ce,ji)
    ce="2020-02-29 09:30:30"
    ji ="2020-02-29 09:29:20"
    date1.f(ce,ji)
    ce="2020-02-29 09:30:30"
    ji ="2020-02-29 09:29:50"
    date1.f(ce,ji)
    ce="2020-02-29 09:30:30"
    ji ="2020-02-29 09:30:40"
    date1.f(ce,ji)
    print("24软工智能一班袁鑫晨 2415929709 6组6号")
    
    

   


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
    print("24软工智能一班袁鑫晨 2415929709 6组6号")


def class_11():
    import copy
    s=input();
    ans=[]#用来存储答案列表
    ans1=[]#用来存储一个可能分割字符串的列表
    def dfs(i:int,s:str):#i为当前索引值,s为字符串
        
        if(i>=len(s)):#如果索引大于字符串长度len(s)就结束 说明已经找到一个答案ans1 将ans1添加进列表ans
                ans.append(copy.deepcopy(ans1));
                print(f"其中一个可能为{ans1}")
                return;
        for j in range(1,len(s)):#j 为分割字符串的长度
            if(i+j>len(s)):#如果 当前索引 + 字符串长度  大于len(s)则 返回 
                return;
            if(s[i:j+i]==s[i:j+i][::-1]):#判断 当前切片是否为回文字符串
                ans1.append(s[i:i+j])
            else :#如果不是 切片长度加1
                continue;
            
            dfs(i+j,s)#如果当前切片是回文字符串 则索引前进到i+j 也就是切片长度的下一位 继续查找回文字符串
            ans1.pop()#回溯  找完一种可能之后 删除当前的切片  继续寻找下一个合适切片
    
        
    dfs(0,s);
    print(f"总答案为{ans}");
    print("24软工智能一班袁鑫晨 2415929709 6组6号")








def class1():
    def isPri(x ):
        if(x==1 or x==0):
            return 0
        for i in range(2,x):
            if x%i==0:
                return 0
        return 1
    with open("data.txt",'w') as f :
        for i in range(1,100):
            prime=[]
            for j in range( (i-1)*100,100*i  ):
                if(isPri(j)):
                    prime.append(j)
            for j in range(len(prime)):
                if(j!=len(prime)-1):
                    f.write(str(prime[j])+",")
                else :
                    f.write(str(prime[j]))


            f.write('\n')
    print("24软工智能一班 袁鑫晨 2415929709 六组六号")

def class2():
    import random,csv
    first_name=["张","李","王","刘","杨","陈","黄","赵","吴","周","徐"]
    last_name_nan=["奕辰","宇轩","浩宇","亦辰","宇辰","子墨","宇航","浩然","梓豪","亦宸"]
    last_name_nv = ["一诺","依诺","欣怡","梓涵","语桐","欣妍","可欣","语汐","雨桐","梦瑶"]
    xingBie=["男","女"]
    #先生成50个人的随机信息
    class Student:
        def __init__(self,name=0,gender=0,age=0,grade=0):
            self.name=name
            self.gender=gender
            self.age=age
            self.grade =grade
        def __str__(self):
            return f"{self.name},{self.gender},{self.age},{self.grade}"

    stu=[]
    stu_bad=[]
    for i in range(50):
        temp=Student()
        temp.gender = xingBie[random.randint(0,1)]
        if(temp.gender=="男"):
            temp.name=first_name[random.randint(0,len(first_name)-1)] + last_name_nan[ random.randint(0,len(last_name_nan)-1)]
        else :
            temp.name = first_name[random.randint(0, len(first_name) - 1)] + last_name_nv[ random.randint(0, len(last_name_nv) - 1)]
        temp.age=random.randint(18,24)
        temp.grade=random.randint(0,100)
        if(temp.grade<60) :
            stu_bad.append(temp)
        stu.append(temp)
    #写入csv文件
    with open("info.csv",'w',newline='') as csvw:
        write = csv.writer(csvw)
        write.writerow(["姓名","性别","年龄","成绩"])
        for i in range(len(stu)):
            write.writerow(str(stu[i]).split(','))
            print(str(stu[i]).split(','))

        for i in range(len(stu_bad)) :
            name = stu_bad[i].name +".bat";
            with open(name,"wb+") as f :
                data = str(stu_bad[i]).encode('utf-8')
                f.write(data)
                f.write(b'\n')
    print("24软工智能一班 袁鑫晨 2415929709 六组六号")
                
            



def class3():
    import os
    path=r'C:\Windows\System32'
    print(os.walk(path))
    for root ,dirs,files in os.walk(path):
        if not dirs and not files :
            print(f"空文件夹{root}")

def class4():
    class Error(Exception):
        def __init__(self,data):
            Exception.__init__(self,data);
            self.data=data;
        def __str__(self):
            return f"{self.data}:当前成绩无效:"
    def pan(data):
        for i in range(len(data)):
            if '0'<=data[i] and data[i]<='9':
                continue;
            else :
                raise Error(data)
        data = int(data)
        if 0<= data and data<=100:
            return data ;
        else :
            raise Error(data);
    name=input("输入姓名")
    grade =input("输入分数")
    try:
        grade = pan(grade);
    except Error as e :
        print(e);
    else :
        print(f"name:{name} grade:{grade}")
    print("24软工智能一班 袁鑫晨 2415929709 六组六号")
def class5():
    class IllegalArgumentException(Exception):
        def __init__(self,data):
            Exception.__init__(self,data);
            self.data=data;
        def __str__(self):
            return f"{self.data[0]},{self.data[1]},{self.data[2]}不能构成三角形"
    class IllegalArgLenException(Exception):

            def __init__(self, data):
                Exception.__init__(self, data);
                self.data = data;

            def __str__(self):
                return f"参数个数不正确"
    def my_input():
        data = input("请输入三条边").split();
        if len(data)!=3:
            raise IllegalArgLenException(data);
        try:
            for i in range(len(data)):
                data[i]=float(data[i])
        except:
            print("参数类型不正确")
        sorted(data);
        if data[0] + data[1] <= data[2]:
            raise IllegalArgumentException(data)
        return data;
    data=[]
    try :
        data=my_input();
    except (IllegalArgumentException,IllegalArgLenException,TypeError) as e :
        print(e);
    else :


        print(f"该三角形的周长为{sum(data)}")
    finally:
        print("程序运行结束")
    print("24软工智能一班 袁鑫晨 2415929709 六组六号")

def class6():
    a,b=map(int,input().split(','))
    ans = a-100;
    try:
        assert abs(ans-b) <=5,"体重不达标"
    except AssertionError as e :
        print(e);
    else :
        print("体重在正常范围")
    print("24软工智能一班 袁鑫晨 2415929709 六组六号")
class6()


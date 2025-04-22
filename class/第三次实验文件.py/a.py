def class1():
    class Employee:
        id =1001;
        def __init__(self,name):


            self.name =name ;
            self.employee_id =Employee.id ;
            Employee.id+=1;

        def display_info(self):
            print(f"姓名{self.name} 工号{self.employee_id}")
    print(Employee.id)
    per = Employee("张三");
    print(per.id)
    per2=Employee("李四");
    per.display_info()
    per2.display_info();
    print("24软工智能一班袁鑫晨 2415929709 6组6号")
def class2():
    import math
    class Triangle:
        def __init__(self,a,b,c):
            list=[a,b,c];
            list.sort();
            a=list[0];
            b=list[1];
            c=list[2];
            #判断周长是否符合三角形
            if a+b<=c:
                print(f"错误{a,b,c}无法构成一个三角形")
                return ;
            self.a = a ;
            self.b =b;
            self.c=c;

        def perimEter(self):
            return self.a+self.b+self.c
        def area(self):
            s = self.perimEter()/2
            res = math.sqrt(s*(s-self.a)*(s-self.b)*(s-self.c))
            res = round(res,2)
            return  res

    t1 = Triangle(1,1,1);
    print(t1.area())
    t2=Triangle(1,2,1)
    print("24软工智能一班袁鑫晨 2415929709 6组6号")
def class3():
    class BankAccount:
        def __init__(self):
            self.__balance =0 ;
        def   deposit(self,amount):
            if(amount<0):
                print(f"出错,无法存入{amount}")
                return;
            self.__balance += amount ;
            print(f"成功存款{amount}元")
        def withdraw(self,num):
            if(self.__balance<num):
                print(f"余额不足")
                return
            self.__balance-=num ;
            print(f"取款成功,当前还剩{self.__balance}元")
        @property
        def amount(cls):
                return cls.__balance ;
    per =  BankAccount();
    per.deposit(100)
    per.deposit(-100)
    per.withdraw(50)
    per.withdraw(100)
    print(per.amount)
    print("24软工智能一班袁鑫晨 2415929709 6组6号")
def class4():
    class Complex:
        def __init__(self,i,j):
            self.r = i ;
            self.v = j ;
        def __add__(self,b):
            r = self.r + b.r ;
            v = self.v +b.v ;
            return Complex(r,v)
        def __sub__(self,b):
            r = self.r - b.r;
            v = self.v - b.v;
            return Complex(r,v)
        def __mul__(self,b):
            r = self.r * b;
            v = self.v * b;
            return Complex(r,v);

        def __str__(self):
            return f"{self.r}+{self.v}i"
    c1 = Complex(1,2);
    c2 = Complex(3,4);
    print(c1)
    print(c2)
    print(c1+c2)
    print(c1*2)
    print(c1-c2)
    print("24软工智能一班袁鑫晨 2415929709 6组6号")
def class5():
    class Animal:
        def speak(self):
            pass
    class Dog(Animal):
        def speak(self):
            return "汪汪汪"
    class  Cat(Animal):
        def speak(self):
            return "喵喵喵"
    d = Dog()
    c=Cat();
    print(d.speak())
    print(c.speak())
    print("24软工智能一班袁鑫晨 2415929709 6组6号")
def class6():
    class Time:
        def __init__(self,h,f):
            self.h =h;
            self.f=f;
        def __add__(self,b):
            #先全转成分钟
            all = self.allF() + b.allF()
            return Time(all//60 ,all%60)
        def allF(self):
            return self.h*60 + self.f ;
        def __str__(self):
            return f"{self.h}小时{self.f}分钟"
    t1 = Time(1,2);
    t2=Time(5,59);
    print(t1);
    print(t2);
    print(f"{t1}+{t2}={t1+t2}");
    print("24软工智能一班袁鑫晨 2415929709 6组6号")
def class7():
    class Book:
        def __init__(self,title,author):
            self.title = title
            self.author = author
        def __str__(self):
            return f"书名为{self.title} 作者为{self.author}"

    class Library:
        def __init__(self):
            self.books=[]
        def add_book(self,b):
            self.books.append(b);
        def list_books(self):
            for i in self.books :
                print(i);
    l = Library()
    l.add_book(Book("三国演义","罗贯中"))
    l.add_book(Book("三体","刘慈欣"))
    l.list_books()
    print("24软工智能一班袁鑫晨 2415929709 6组6号")
def class8():
    class car:
        def __init__(self,speed,type:str):
            self.speed=speed ;
            self.type =type ;
        @staticmethod
        def increased_energy(cls):
            cls.increased_energy(cls);

        def __str__(self):
            return f"{self.type}类型 速度{self.speed}的车"
    class you_car(car):#油车
        @staticmethod
        def increased_energy(cls):
            print(f"给{cls.type}加油")
        pass
    class new_car(car):#电动车
        @staticmethod
        def increased_energy(cls):
            print(f"给{cls.type}充电")
        pass
    you= you_car(100,"油车")
    new= new_car(100,"电车")
    car.increased_energy(you)
    car.increased_energy(new)
    print("软工智能1班 袁鑫晨 2415929709 六组六号")
def class9():
    class Person:
        def __init__(self,name,age):
            self.name =name
            self.age = age
    class Student(Person):
        def __init__(self,name,age,id):
            super().__init__(name,age);
            self.id =id ;
        def display_info(self):
            print(f"学生{self.name}年龄{self.age} 学号{self.id}")

    class Teacher(Person):
        def __init__(self,name,age,id):
            super().__init__(name,age);
            self.id =id ;

        def display_info(self):
            print(f"教师{self.name} 年龄{self.age} 工号{self.id}")
    t = Teacher("张三",30,1123123);
    s=Student("李四",18,1000000);
    t.display_info()
    s.display_info()
    print("软工智能1班 袁鑫晨 2415929709 六组六号")
def class10():
    class Temperature:
        def __init__(self,c,f):
            self.c = c ;
            self.f=f;#默认符号位摄氏度

        @staticmethod
        def celsius_to_kelvin(c):
            t1 = Temperature.from_string(c)

            return Temperature(t1.c + 273.15,'K')  ;
        @staticmethod
        def from_string(temp_str):

            if (temp_str[len(temp_str) - 1] == 'C'):
                return Temperature(float(temp_str[:len(temp_str) - 1]), "C");
            elif temp_str[len(temp_str) - 1] == 'K': 

                return Temperature(float(temp_str[:len(temp_str) - 1]), "K");
        def __str__(self):
            return f"{self.c}{self.f}"


    
    print(Temperature.celsius_to_kelvin("1000.55K"))
    t1=Temperature.celsius_to_kelvin("10.1C");
    t2 = Temperature.celsius_to_kelvin("10.1K")
    t3= Temperature.from_string("123.1K")
    t4=Temperature.from_string("-123.1K")
    print(t1)
    print(t2)
    print(t3)
    print(t4)
    print("24软工智能一班袁鑫晨 2415929709 6组6号")
class10()



    




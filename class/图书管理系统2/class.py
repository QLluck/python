class User:
    allId=1
    def __init__(self,username,code,name="未知"):
        self.username=username
        self.code=code
        self.name=name
        self.id=User.allId
        User.allId+=1
        self.borrowList:list[Book]=[]
        
        
    def printMenu():
        welcome = ["===========================",
                    "1. 注册",
                    "2. 登录",
                    "3. 图书借阅界面",
                    "4. 退出登录",
                    "5. 退出系统",
                    "6. 注销账号"
                    "==========================="]
        for i in welcome:
            print("%s" % i.center(18, "　"))
    def change(self,username=0,code=0,name=0):#修改信息
        if(username):
            self.username=username
        if(code):
            self.code=code
        if(name):
            self.name=name
    def borrowBook(self):
        book:Book=library.findBook()
        if(book):
            print("借阅成功")
            book.borrowUser=self 
            book.borrow=1
            self.borrowList.append(book)
        else:
            print("借阅失败")
    def borrowPrint(self):
        print("您借阅的书籍有:")
        for i in range(len(self.borrowList)) :
            print(f"{i}.{self}")
    def borrowReturn(self):
        self.borrowPrint()
        while(1):
            num=input("请输入你要归还的编号:")
            #判断输入是否全文数字
            flag=0;
            for i in range(len(num)):
                if '0'<=num and num<='9':
                    continue;
                else :
                    flag=1;
                    break;
            num=int(num)
            if(num<0 and len(self.borrowList)-1<num):
                flag=1
            if(flag):
                print("输入不合法,请重新输入")
                continue;
        self.borrowList[num].borrow=0;
        self.borrowList[num].borrowUser=0
        self.borrowList.pop(num)
        print("归还成功")
        
    def deleteUser(self):
        print("警告:一旦注销,个人信息全部消失")
        num=input("输入YES确认");
        if(num=='YES'):
            num=input("再次输入YES确认,注意:确认后用户数据全部消失");
            if(num=="YES"):
                
                   
         
            
        
        

    
    def __str__(self):
        return f"用户名:{self.username} id号:{self.id} 真实姓名:{self.name}"
class Book:
    def __init__(self,name,author):
        self.name=name
        self.author=author
        self.borrow =0
        self.borrowUser :User= 0 #后面直接指向学生
    def __str__(self):
        return f"书名:{self.name} 作者名:{self.author}"   

        
        
        
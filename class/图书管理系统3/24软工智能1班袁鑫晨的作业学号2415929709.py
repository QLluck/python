import msvcrt, os, sys
class User:
    allId=1
    def __init__(self,username,code,name="未知"):#初始化user
        self.username=username
        self.code=code
        self.name=name
        self.id=User.allId
        User.allId+=1
        self.borrowList:list[Book]=[]
        self.permission=0
        
        
    def printMenu(self):#打印普通用户菜单
        welcome = ["===========================",
                    "1. 注册",
                    "2. 登录",
                    "3. 图书借阅界面",
                    "4. 退出登录",
                    "5. 退出系统",
                    "6. 注销账号",
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
        id=Data.findBook()#查询书籍
        if(id!=-1):
            print("借阅成功")
            Data.bookList[id].borrowuser=self 
            Data.bookList[id].borrow=1
            self.borrowList.append(Data.bookList[id])
        else:
            print("借阅失败")
    def borrowPrint(self):
        print("您借阅的书籍有:")
        for i in range(len(self.borrowList)) :
            print(f"{i}.{self.borrowList[i]}")
    def borrowReturn(self):
        self.borrowPrint()
        num=Data.dataInputInt(0,len(self.borrowList)-1)
        self.borrowList[num].borrow=0;
        self.borrowList[num].borrowUser=0
        self.borrowList.pop(num)
        print("归还成功")
        
    def deleteSelfUser(self):
        print("警告:一旦注销,信息全部消失")
        num=input("输入YES确认");
        if(num=='YES'):
            num=input("再次输入YES确认,注意:确认后数据全部消失");
            if(num=="YES"):
                
                id = Data.findUserId(self)
                Data.userList.pop(id)
                print("删除成功")
                return 1
            else :
                print("取消成功")
                return 0
                
                    
        else  :
            print("取消成功")
            return 0
    def menu(self):
        while(1):
            self.printMenu()
            a = Data.dataInputInt(1,6)
            if (a==1):
                Data.userAdd()
            elif(a==2):
               p=  Data.register()
               if(p==-1):
                   print("登入失败")
                   continue
               print("登录成功")
               return p 
            elif a==3:
                self.bookMenu()
            elif a==4:
                print("退出登录成功")
                return 1
            elif a==5 :
                print("退出系统")
                return 2 
            elif a==6:
                if(self.deleteSelfUser()):
                     return 1
    def bookMenu(self):
        while(1):
            welcome = ["===========================",
                "1. 借阅",
                "2. 归还",
                "3. 查看借阅书籍",
                "4. 退出",
                "==========================="]
            for i in welcome:
                print("%s" % i.center(18, "　"))
            
            a=Data.dataInputInt(1,4)
            if(a==1):
                self.borrowBook()
            elif (a==2):
                self.borrowReturn()
            elif (a==3):
                self.borrowPrint()
            elif(a==4):
                return 
   
                
                   
         
            
        
        

    
    def __str__(self):
        return f"用户名:{self.username} id号:{self.id} 真实姓名:{self.name}"
class Admin(User):
    def __init__(self,username,code,name="未知"):
        super().__init__(username,code)
        self.permission=1#权限表示
    def printMenu(self):
        welcome = ["===========================",
                "1. 注册",
                "2. 登录",
                "3. 图书借阅界面",
                "4. 退出登录",
                "5. 退出系统",
                "6. 注销账号",
                "7. 增加用户",
                "8. 删除用户",
                "9. 修改用户",
                "10.查询用户",
                "==========================="]
        for i in welcome:
            print("%s" % i.center(18, "　"))
    def findUser(self):
        id = Data.findUser()
        print("查询成功")
        print(Data.userList[id])
        return id      
    def findBook(self):
        id = Data.findBook()
        print("查询成功")
        print(Data.bookList[id])
        return id   
    def changeBook(self):
        print("选择要修改的书籍")
        id = Data.findBook()
        welcome = ["===========================",
        "1. 修改书名",
        "2. 修改作者名",
        "==========================="]
        for i in welcome:
            print("%s" % i.center(18, "　"))
        num = Data.dataInputInt(1,2)
        if(num==1):
            print("请输入书名")
            name = Data.dataInputStr()
            Data.bookList[id].change(name=name)
            print("修改成功")
        elif(num==2):
            print("请输入作者名")
            author = Data.dataInputStr()
            Data.bookList[id].change(author=author)
            print("修改成功")
    def changeUser(self):
        print("选择要修改的用户")
        id = Data.findUser()
        welcome = ["===========================",
        "1. 修改用户名",
        "2. 修改姓名",
        "==========================="]
        for i in welcome:
            print("%s" % i.center(18, "　"))
        num = Data.dataInputInt(1,2)
        if(num==1):
            print("请输入用户名")
            username = Data.dataInputStr()
            Data.userList[id].change(username=username)
            print("修改成功")
        elif(num==2):
            print("请输入姓名")
            name = Data.dataInputStr()
            Data.userList[id].change(name=name)
            print("修改成功")
    def deleteUser(self):
        id =Data.findUser()
        if(id==-1):
            print("删除失败")
            return ;
        Data.userList.pop(id);
        print("删除成功")
    def deleteBook(self):
        id =Data.findBook()
        if(id==-1):
            print("删除失败")
            return ;
        Data.bookList.pop(id);
        print("删除成功")
    def menu(self):
        while(1):
            self.printMenu()
            a = Data.dataInputInt(1,10)
            if (a==1):
                Data.userAdd()
            elif(a==2):
               p=  Data.register()
               if(p==-1):
                   print("登入失败")
                   continue
               print("登录成功")
               return p 
            elif a==3:
                self.bookMenu()
            elif a==4:
                print("退出登录成功")
                return 1
            elif a==5 :
                print("退出系统")
                return 2 
            elif a==6:
                if(self.deleteSelfUser()):
                    return 1
            elif a==7:
                Data.userAdd()
            elif a==8:
                self.deleteUser()
            elif a==9:
                self.changeUser()
            elif a==10:
                self.findUser()
    
    def bookMenu(self):
        while(1):
            welcome = ["===========================",
                "1. 借阅",
                "2. 归还",
                "3. 查看借阅书籍",
                "4. 退出",
                "5. 添加书籍",
                "6. 删除书籍",
                "7. 修改书籍",
                "8. 查询书籍",
                "==========================="]
            for i in welcome:
                print("%s" % i.center(18, "　"))
            
            a=Data.dataInputInt(1,8)
            if(a==1):
                self.borrowBook()
            elif (a==2):
                self.borrowReturn()
            elif (a==3):
                self.borrowPrint()
            elif(a==4):
                return  
            elif a==5:
                Data.bookAdd()
            elif a==6:
                self.deleteBook()
            elif a==7:
                self.changeBook()
            elif a==8:
                self.findBook()
            
            
            
            
    
class Book:
    def __init__(self,name,author):
        self.name=name
        self.author=author
        self.borrow =0
        self.borrowUser :User= 0 #后面直接指向学生
    def __str__(self):
        return f"书名:{self.name} 作者名:{self.author}"   
    def change(self,name=0,author=0):#修改信息
        if(name):
            self.name=name
        if(author):
            self.author=author
        

class Data:
    userList=[]
    bookList=[]
    sensitive_character = ["傻", "屁", "草", "操", "垃圾", "z", "蠢", "笨", "呆"]
    @staticmethod
    def findBook():
        welcome = ["===========================",
                "1. 名字查询",
                "2. 作者查询",
                "3. 查询全部",
                "==========================="]
        for i in welcome:
            print("%s" % i.center(18, "　"))
        a=Data.dataInputInt(1,3)
        p=0
        if(a==1):
            name=Data.dataInputStr();
            find=[]
            for i in Data.bookList :
                if name in i.name :
                    find.append(i)
            if(len(find)==0):
                print("未找到相关书籍")
                return -1 
            print(f"找到{len(find)}条查询结果")
            for i in range(len(find)):
                print(f"{i}.{find[i]}")
            print("输入要选择的书籍")
            num = Data.dataInputInt(0,len(find)-1)
            return num 
        elif (a==2):
            name=Data.dataInputStr();
            find=[]
            for i in Data.bookList :
                if name in i.author :
                    find.append(i)
            if(len(find)==0):
                print("未找到相关书籍")
                return -1 
            print(f"找到{len(find)}条查询结果")
            for i in range(len(find)):
                print(f"{i}.{find[i]}")
            print("输入要选择的书籍")
            num = Data.dataInputInt(0,len(find)-1)
            return num
        elif (a==3):
            Data.showAllBook()
            print("输入要选择的书籍")
            num = Data.dataInputInt(0,len(Data.bookList)-1)
            return num
            
        return -1
            
    @staticmethod
    def findUser():
        welcome = ["===========================",
                "1. 名字查询",
                "2. 用户名查询",
                "3. 查询所有",
                "==========================="]
        for i in welcome:
            print("%s" % i.center(18, "　"))
        a=Data.dataInputInt(1,3)
        p=0
        if(a==1):
            name=Data.dataInputStr();
            find=[]
            for i in Data.userList :
                if name in i.name :
                    find.append(i)
            if(len(find)==0):
                print("未找到相关用户")
                return -1
            print(f"找到{len(find)}条查询结果")
            for i in range(len(find)):
                print(f"{i}.{find[i]}")
            print("输入要选择的用户")
            num = Data.dataInputInt(0,len(find)-1)
            return num
        elif (a==2):
            name=Data.dataInputStr();
            find=[]
            for i in Data.userList :
                if name in i.username :
                    find.append(i)
            if(len(find)==0):
                print("未找到相关用户")
                return -1 
            print(f"找到{len(find)}条查询结果")
            for i in range(len(find)):
                print(f"{i}.{find[i]}")
            print("输入要选择的用户")
            num = Data.dataInputInt(0,len(find)-1)
            return num
        elif (a==3):
            Data.showAllUser()
            print("输入要选择的用户")
            num = Data.dataInputInt(0,len(Data.userList)-1)
            return num
            
            
            
            
                    
            
            
            
    @staticmethod
    def dataInputInt(l,r):
        num=0
        while(1):
            num=input("请输入编号:")
            #判断输入是否全文数字
            flag=0;
            for i in range(len(num)):
                if '0'<=num and num<='9':
                    continue;
                else :
                    flag=1;
                    break;
            num=int(num)
            if(num<l or r<num):
                flag=1
            if(flag):
                print("输入不合法,请重新输入")
                continue;
            
            return num
    @staticmethod
    def dataInputStr():
        str=0
        while(1):
            str=input("请输入:")
            #判断输入是否有敏感词
            flag=0;
            for i in Data.sensitive_character :
                if i in str:
                    flag=1;
                    str.replace(i,'*')
            if(flag):
                print(f"输入的 {str} 内含有敏感字符")
                print("输入不合法,请重新输入")
                continue;
            return str
    @staticmethod
    def findUserId(user):
        for i in  range(len(Data.userList)):
            if Data.userList[i].id == user.id:
                return i
        return -1 #未找到用户
    @staticmethod
    def findBookId(book):
        for i in  range(len(Data.bookList)):
            if Data.bookList[i].name == book.name and  Data.bookList[i].author == book.author :
                return i
        return -1 #未找到书籍
    @staticmethod
    def usernameCheck(str):#用户名重名检测 + 注册时候用户名查询
        for i in range(len(Data.userList)):
            if Data.userList[i].username == str:
                return i
        return -1
    @staticmethod
    def booknameCheck(str):#书名重名检测
        for i in range(len(Data.bookList)):
            if Data.bookList[i].name==str:
                return i
        return -1 
    @staticmethod
    def userAdd():
        while(1):
            print("输入用户名")
            username = Data.dataInputStr()
            if(Data.usernameCheck(username)!=-1):
                print("用户名重复,请重新输入")
                continue;
            else :
                break;
        while(1):
            print("请输入密码")
            password = Data.jiami()
            flag=0
            #密码检测 
            numint=0#数字
            num_word_up=0#大写字母
            num_word_low=0#小写字母
            num_other=0#其他字符
            for i in password:
                if '0'<=i and i <='9':
                    numint+=1;
                elif 'a'<=i and i<='z':
                    num_word_low+=1
                elif 'A'<=i and i<='Z':
                    num_word_up+=1
                else :
                    num_other+=1
            if numint==0:
                flag=1
                print("密码中无数字")
            if num_word_up==0:
                flag=1
                print("密码中无大写字母")
            if num_word_low==0:
                flag=1
                print("密码中无小写字母")
            if num_other==0:
                flag=1
                print("密码中无其他字符")
            if len(password)<8:
                flag=1
                print("密码长度小于8!")
            if (flag==1):
                print("请重新输入密码")
                continue;
            break;
        usertemp = User(username,password)
        Data.userList.append(usertemp)
        print("添加成功");
    @staticmethod
    def bookAdd():
        while(1):
            print("请输入书名")
            name =Data.dataInputStr()
            if(Data.booknameCheck(name)!=-1):
                print("书名重复,请重新输入")
                continue;
            else :
                break;
        print("请输入作者名")
        author = Data.dataInputStr()
        booktemp = Book(name,author)
        Data.bookList.append(booktemp)
        print("添加成功")
        
            
                
            
            
    @staticmethod
    def jiami():
        password = ""
        while True:
            char = msvcrt.getch()
            if char == b'\r':  # 回车表示输入结束
                print()
                break
            elif char == b'\x08':  # 退格键
                if password:
                    password = password[:-1]
                    print('\b \b', end='', flush=True)
            else:
                password += char.decode()
                print('*', end='', flush=True)
        return password
    @staticmethod
    def showAllBook():
        for i in range(len(Data.bookList)):
            print(f"{i}.{Data.bookList[i]}")
    @staticmethod
    def showAllUser():
        for i in range(len(Data.userList)):
            print(f"{i}.{Data.userList[i]}")
    @staticmethod
    def register():

            
        print("请输入用户名")
        username = Data.dataInputStr()
        flag = Data.usernameCheck(username)
        if(flag==-1):
            print("未查到该用户,请注册")
            return -1
        chance = 3 ;
        while(chance):
            print("请输入密码")
            password=Data.jiami()
            if password == Data.userList[flag].code :
                return Data.userList[flag]
            print(f"密码错误 还剩{chance}次机会")
            chance-=1
        return -1 
            
            
def init():
    p1 = User("张三","12345")
    p2 = User("1","1")
    Data.userList.append(p1)
    Data.userList.append(p2)
    b1= Book("三体","刘慈欣")
    b2=Book("三国演绎","罗贯中")
    Data.bookList.append(b1)
    Data.bookList.append(b2)
    a1 = Admin("0","0")
    Data.userList.append(a1)
def main():
    while(1):
        welcome = ["===========================",
        "1. 登录",
        "2. 注册",
        "3. 离开系统",
        "==========================="]
        for i in welcome:
            print("%s" % i.center(18, "　"))
        a = Data.dataInputInt(1,3)
        if(a==1):
            p= Data.register()
            if(p!=-1):
                while(1):
                    print("登录成功")
                    p= p.menu()
               
                    if(p==2):
                        return 
                    elif p==1:
                        break;

                    
            else :
                print("登录失败")
        elif (a==2):
            Data.userAdd()
            print("注册成功,请登录")
            continue;
            
        elif a==3:
            return     
init()
main()   
            
    
        
        
        
        
        
        
            
        
        
        
    
    

        
        
        
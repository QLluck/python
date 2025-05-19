import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget,QMessageBox, QTextEdit, QPushButton,  QHBoxLayout,QPushButton
from PyQt5 import uic
import menu
def resource_path(relative_path):
    """获取资源文件的绝对路径，适应打包后的环境"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
class loginForm(QWidget):
    def __init__(self):
        super().__init__()
        ui_path = resource_path("图书管理系统3/登录界面完美.ui")
        self.ui=uic.loadUi(ui_path,self)
        #信号联系
        self.ui.pushButton_2.clicked.connect(self.open_registerForm)
        self.ui.pushButton_3.clicked.connect(self.app_exit)
        self.ui.pushButton.clicked.connect(self.login)
        #QApplication.instance().aboutToQuit.connect(self.on_application_exit)
    def open_registerForm(self):
        
        register.show()
        self.hide()
    def app_exit(slef):
        QApplication.exit()
    def login(self):
            
    
            
        
        username = self.ui.lineEdit_7.text()
        flag = menu.Data.usernameCheck(username)
        if(flag==-1):
            self.print_textBrowser_2("<p class=\"custom-text\">未查到当前用户,请注册</p>")
            #self.print_textBrowser_2("<p class=\"custom-text\">密码错误</p>")
            
            return -1
      
        password = self.ui.lineEdit_5.text()
       # print(menu.Data.userList[flag].code)
       # print(self.ui.lineEdit_5.text())
       
        
        if password == menu.Data.userList[flag].code :
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("登录成功")
                msg_box.setText("登录成功!")

                # 显示消息框
                msg_box.exec_()
                
                mainW.show()
                self.hide()
                menu.p=menu.Data.userList[flag]
                if(menu.p.permission==0):
                    mainW.ui.label.setText(f"用户:{menu.p.username}")
                    mainW.ui.pushButton_4.hide()
                    mainW.ui.pushButton_5.hide()
                elif menu.p.permission==1 :
                    mainW.ui.label.setText(f"管理员:{menu.p.username}")
                self.init_proData()#初始化主界面
        else:
            self.print_textBrowser_2("<p class=\"custom-text\">密码错误</p>")
            
    def init_proData(self):
        mainW.ui.textEdit_7.setText(menu.p.username)
        mainW.ui.textEdit_10.setText( len(menu.p.code )* '*')
        mainW.ui.textEdit_8.setText(menu.p.name)
        mainW.ui.textEdit_11.setText(str(menu.p.id))
        mainW.ui.textEdit_9.setText(menu.p.status)
        mainW.ui.textEdit_12.setText( str(menu.p.permission) )
        
           
        
        
        
       
    def print_textBrowser_2(self,text):
        html_content = f"""
<html>
<body>
        <style>
                .custom-text {{
                    color: #ff2121; /* 设置字体颜色为 #ff2121 */
                    font-family: 'Arial', sans-serif;
                    text-align: center;
                    font-size: 10px; /* 字体大小 */
                    line-height: 0.3; /* 行间距 */
                    
                }}
                    .custom-text2 {{
                    color: #00e500; /* 设置字体颜色为 #ff2121 */
                    font-family: 'Arial', sans-serif;
                    text-align: center;
                    font-size: 10px; /* 字体大小 */
                    line-height: 0.3; /* 行间距 */
                }}
            </style>
            
            {text}
</body>
</html>
"""     
        self.ui.textBrowser_2.setHtml(html_content)
    

   
        
        
class registerForm(QWidget):#注册按钮函数
    def __init__(self):
        super().__init__()
        ui_path = resource_path("图书管理系统3/注册界面完美.ui")
        self.ui=uic.loadUi(ui_path,self)
        
        self.ui.pushButton_2.clicked.connect(self.open_loginForm)
        self.ui.pushButton_3.clicked.connect(self.app_exit)
        self.ui.lineEdit_5.textChanged.connect(self.checkPassward)
        self.ui.lineEdit_7.textChanged.connect(self.checkUserId)
        self.ui.pushButton.clicked.connect(self.register)
    def open_loginForm(self):#登录按钮函数
        
        login.show();
        self.hide()
    def app_exit(slef):
        QApplication.exit()
    def checkPassward(self,text):
            password = text
            flag=0
            #密码检测 
            numint=0#数字
            num_word_up=0#大写字母
            num_word_low=0#小写字母
            num_other=0#其他字符
            num_int_html=""
            num_word_up_html=""
            num_word_low_html=""
            num_other_html=""
            num_len_html=""
            right_html=""
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
                num_int_html= "<p class=\"custom-text\">密码中无数字</p>"
            if num_word_up==0:
                flag=1
                num_word_up_html= "<p class=\"custom-text\">密码中无大写字母</p>"
            if num_word_low==0:
                flag=1
                num_word_low_html= "<p class=\"custom-text\">密码中无小写字母</p>"
            if num_other==0:
                flag=1
                num_other_html= "<p class=\"custom-text\">密码中无小其他字符</p>"
            if len(password)<8:
                flag=1
                num_len_html= "<p class=\"custom-text\">密码长度小于8</p>"
            if (flag==0):
                right_html="<p class=\"custom-text2\">密码符合要求</p>"
            html_content =  num_int_html +num_word_up_html+ num_word_low_html+num_other_html + num_len_html+right_html
            self.print_textBrowser_2(html_content)
            return flag
    def checkUserId(self,text):
        str=text
            #判断输入是否有敏感词
       # print(str)
        flag=0;
        for i in menu.Data.sensitive_character :
            if i in str:
                flag=1;
                str=str.replace(i,'*'*len(i))
               # print(str)
        right=""
        if(flag):
            self.ui.lineEdit_7.setText(str)
            right="<p class=\"custom-text\">输入中有敏感词请重新输入</p>"
        self.print_textBrowser_2(right)
    def register(self):#注册
        username =self.ui.lineEdit_7.text()
        password = self.ui.lineEdit_5.text()
        if(menu.Data.usernameCheck(username)!=-1):
            self.print_textBrowser_2("<p class=\"custom-text\">该用户名已存在</p>")
            return ;
        flag = self.checkPassward(password)
        if(flag==0):
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("注册成功")
            msg_box.setText("注册成功!")

            # 显示消息框
            msg_box.exec_()
           
            
            login.show()
            self.hide()
            self.loginForm.print_textBrowser_2("<p class=\"custom-text2\">注册成功,请登录</p>")
            usertemp = menu.User(username,password)
            menu.Data.userList.append(usertemp)
        
    def print_textBrowser_2(self,text):
        html_content = f"""
<html>
    <body>
          <style>
                    .custom-text {{
                        color: #ff2121; /* 设置字体颜色为 #ff2121 */
                        font-family: 'Arial', sans-serif;
                        text-align: center;
                        font-size: 10px; /* 字体大小 */
                        line-height: 0.3; /* 行间距 */
                        
                    }}
                     .custom-text2 {{
                        color: #00e500; /* 设置字体颜色为 #ff2121 */
                        font-family: 'Arial', sans-serif;
                        text-align: center;
                        font-size: 10px; /* 字体大小 */
                        line-height: 0.3; /* 行间距 */
                    }}
                </style>
             
                {text}
    </body>
</html>
"""     
        self.ui.textBrowser_2.setHtml(html_content)
        
class mainWindow(QWidget):
    def __init__(self):
        super().__init__()
        ui_path = resource_path("图书管理系统3/主界面.ui")
        self.ui=uic.loadUi(ui_path,self)
        self.ui.pushButton.clicked.connect(self.login);
        self.ui.pushButton_7.clicked.connect(self.open_changeProDataForm);
        self.ui.pushButton_2.clicked.connect(self.app_exit);    
        self.ui.pushButton_6.clicked.connect(lambda: (self.ui.stackedWidget.setCurrentIndex(0),self.init_proData()) );
        self.ui.pushButton_3.clicked.connect(lambda: (self.ui.stackedWidget.setCurrentIndex(1),self.findProBook(self.lineEdit_4.text()),self.findallBook(self.lineEdit_2.text()) ) );
        self.ui.pushButton_4.clicked.connect(lambda: (self.ui.stackedWidget.setCurrentIndex(2) ,self.findallBook2(self.lineEdit_5.text()) )  );
        self.ui.pushButton_5.clicked.connect(lambda:( self.ui.stackedWidget.setCurrentIndex(3),self.findallUser(self.lineEdit_7.text()) ) );
        self.ui.pushButton_14.clicked.connect(self.addBook);
        self.ui.pushButton_17.clicked.connect(self.addUser);
        

        self.ui.lineEdit_4.textChanged.connect(self.findProBook)
        self.ui.lineEdit_2.textChanged.connect(self.findallBook)
        self.ui.lineEdit_5.textChanged.connect(self.findallBook2)
    def addBook(self):
        ab.show()
        self.hide()
    def addUser(self):
        au.show()
        self.hide()
    def findProBook(self, text):
        #print(text)
        # 调用 clear_layout 函数清空 verticalLayout_2
        self.clear_layout(self.ui.verticalLayout_2)

        self.find = []
        it =0 
        for i in menu.p.borrowList:
            if text:
                if text in i.name:
                    self.find.append([i,it])
                    #print(f"{text}{i.name}")
            elif not text:
                self.find.append([i,it])
            it +=1
        #print(find)
        
        for i in self.find:
            # 创建水平布局
            layout = QHBoxLayout()

            # 创建 QTextEdit 控件并添加到布局
            text_edit = QTextEdit()
            text_edit.setPlaceholderText("书名：")
            text_edit.setText(i[0].name)
            layout.addWidget(text_edit)

            # 创建按钮并添加到布局
  

            return_button = QPushButton("归还")
            layout.addWidget(return_button)
            return_button.clicked.connect(lambda checked, num= i[1] : self.return_book(num))

            # 将布局添加到 verticalLayout_2
            self.ui.verticalLayout_2.addLayout(layout)
    def findallBook(self, text):
        #print(text)
        # 调用 clear_layout 函数清空 verticalLayout_2
        self.clear_layout(self.ui.verticalLayout_10)

        self.find = []
        it =0 
        for i in menu.Data.bookList:
            if text:
                if text in i.name:
                    self.find.append([i,it])
                    #print(f"{text}{i.name}")
            elif not text:
                self.find.append([i,it])
            it +=1
        #print(find)
        
        for i in self.find:
            # 创建水平布局
            layout = QHBoxLayout()

            # 创建 QTextEdit 控件并添加到布局
            text_edit = QTextEdit()
            text_edit.setPlaceholderText("书名：")
            text_edit.setText(i[0].name)
            layout.addWidget(text_edit)

            # 创建按钮并添加到布局
  

            return_button = QPushButton("借阅")
            layout.addWidget(return_button)
            return_button.clicked.connect(lambda checked, num= i[1] : self.borrow_book(num))

            # 将布局添加到 verticalLayout_2
            self.ui.verticalLayout_10.addLayout(layout)
            
    def findallBook2(self, text):
        #print(text)
        # 调用 clear_layout 函数清空 verticalLayout_2
        self.clear_layout(self.ui.verticalLayout_11)

        self.find = []
        it =0 
        for i in menu.Data.bookList:
            if text:
                if text in i.name:
                    self.find.append([i,it])
                    #print(f"{text}{i.name}")
            elif not text:
                self.find.append([i,it])
            it +=1
        #print(find)
        
        for i in self.find:
            # 创建水平布局
            layout = QHBoxLayout()

            # 创建 QTextEdit 控件并添加到布局
            text_edit = QTextEdit()
            text_edit.setPlaceholderText("书名：")
            text_edit.setText(i[0].name)
            layout.addWidget(text_edit)

            # 创建按钮并添加到布局
  

            return_button = QPushButton("修改信息")
            layout.addWidget(return_button)
            return_button.clicked.connect(lambda checked, num= i[1] : self.change_book(num))

            # 将布局添加到 verticalLayout_2
            self.ui.verticalLayout_11.addLayout(layout)
    def findallUser(self, text):
        #print(text)
        # 调用 clear_layout 函数清空 verticalLayout_2
        self.clear_layout(self.ui.verticalLayout_12)

        self.find = []
        it =0 
        for i in menu.Data.userList:
            if text:
                if text in i.username:
                    self.find.append([i,it])
                    #print(f"{text}{i.name}")
            elif not text:
                self.find.append([i,it])
            it +=1
        #print(find)
        
        for i in self.find:
            # 创建水平布局
            layout = QHBoxLayout()

            # 创建 QTextEdit 控件并添加到布局
            text_edit = QTextEdit()
            text_edit.setPlaceholderText("用户：")
            text_edit.setText(i[0].username)
            layout.addWidget(text_edit)

            # 创建按钮并添加到布局
  

            return_button = QPushButton("修改信息")
            layout.addWidget(return_button)
            return_button.clicked.connect(lambda checked, num= i[1] : self.change_user(num))

            # 将布局添加到 verticalLayout_2
            self.ui.verticalLayout_12.addLayout(layout)
            
    def return_book(self,num):
        book=self.find[num];
        menu.p.borrowList[num].borrow=0;
        menu.p.borrowList[num].borrowUser=0
        menu.p.borrowList.pop(num)
        self.findProBook('')
    def borrow_book(self,num):
        menu.Data.bookList[num].borrowuser=menu.p
        menu.Data.bookList[num].borrow=1
        menu.p.borrowList.append(menu.Data.bookList[num])
        self.findProBook('')
    def change_book(self,num):
        cb.id=num;
        cb.show()
        self.hide()
    def change_user(self,num):
        cu.id=num
        cu.show()
        self.hide()
        
        
        
    def clear_layout(self, layout):

        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout()) 
    def app_exit(slef):
        QApplication.exit()
    def login(self):
        
        login.show()
        self.hide()
    def init_proData(self):
        self.ui.textEdit_7.setText(menu.p.username)
        self.ui.textEdit_10.setText(len(menu.p.code)*'*' )
        self.ui.textEdit_8.setText(menu.p.name)
        self.ui.textEdit_11.setText(str(menu.p.id))
        self.ui.textEdit_9.setText(menu.p.status)
        self.ui.textEdit_12.setText( str(menu.p.permission) )
    def open_changeProDataForm(self):
       
        change.show()
        self.hide()
        self.init_changeProDataForm();
    def init_changeProDataForm(self):
       change.textEdit.setText(menu.p.username)
       change.textEdit_4.setText(menu.p.code)
       change.textEdit_2.setText(menu.p.name)
       change.textEdit_5.setText(str(menu.p.id))
       change.textEdit_3.setText(menu.p.status)
       change.textEdit_6.setText( str(menu.p.permission) )
        
        
        
class changeProDataForm(QWidget):
    def __init__(self):
        super().__init__()
        
        ui_path = resource_path("图书管理系统3/修改信息界面.ui")
        self.ui=uic.loadUi(ui_path,self)
        #信号联系
        self.ui.pushButton.clicked.connect(self.return_mainWindow)
        self.ui.pushButton_2.clicked.connect(self.changeData)
        self.ui.textEdit_4.textChanged.connect(self.checkPassward)
        self.ui.textEdit.textChanged.connect(self.checkUserId)
        self.ui.textEdit_2.textChanged.connect(self.checkName)
        self.ui.pushButton.clicked.connect(self.changeData)
        
    def return_mainWindow(self):
       
        mainW.show()
        self.hide()
    def changeData(self):
        username =self.ui.textEdit.toPlainText()
        password = self.ui.textEdit_4.toPlainText()
        name= self.ui.textEdit_2.toPlainText()
        print([password])
        if menu.p.username != ''.join(username) :
            if(menu.Data.usernameCheck(username)!=-1):
                self.print_textBrowser("<p class=\"custom-text\">该用户名已存在</p>")
         
                return ;
        if menu.p.code!=''.join(password):
            flag = self.checkPassward()
            if flag!=0:
                return;
        menu.p.username =username
        menu.p.code = password
        menu.p.name=name
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("修改成功")
        msg_box.setText("修改成功!")

        # 显示消息框
        msg_box.exec_()
        mainW.init_proData()
        mainW.show()
        self.hide()
           # self.loginForm.print_textBrowser_2("<p class=\"custom-text2\">注册成功,请登录</p>")     
    
    def checkPassward(self):
        password = self.ui.textEdit_4.toPlainText()
        flag=0
        #密码检测 
        numint=0#数字
        num_word_up=0#大写字母
        num_word_low=0#小写字母
        num_other=0#其他字符
        num_int_html=""
        num_word_up_html=""
        num_word_low_html=""
        num_other_html=""
        num_len_html=""
        right_html=""
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
            num_int_html= "<p class=\"custom-text\">密码中无数字</p>"
        if num_word_up==0:
            flag=1
            num_word_up_html= "<p class=\"custom-text\">密码中无大写字母</p>"
        if num_word_low==0:
            flag=1
            num_word_low_html= "<p class=\"custom-text\">密码中无小写字母</p>"
        if num_other==0:
            flag=1
            num_other_html= "<p class=\"custom-text\">密码中无小其他字符</p>"
        if len(password)<8:
            flag=1
            num_len_html= "<p class=\"custom-text\">密码长度小于8</p>"
        if (flag==0):
            right_html="<p class=\"custom-text2\">密码符合要求</p>"
        html_content =  num_int_html +num_word_up_html+ num_word_low_html+num_other_html + num_len_html+right_html
        self.print_textBrowser(html_content)
        return flag
    def checkUserId(self):
        str=self.ui.textEdit.toPlainText();
        #判断输入是否有敏感词
    # print(str)
        flag=0;
        for i in menu.Data.sensitive_character :
            if i in str:
                flag=1;
                str=str.replace(i,'*'*len(i))
                # print(str)
        right=""
        if(flag):
            self.ui.textEdit.setText(str)
            right="<p class=\"custom-text\">输入中有敏感词请重新输入</p>"
        self.print_textBrowser(right)
    def checkName(self):
        str=self.ui.textEdit_2.toPlainText()
        #判断输入是否有敏感词
    # print(str)
        flag=0;
        for i in menu.Data.sensitive_character :
            if i in str:
                flag=1;
                str=str.replace(i,'*'*len(i))
                # print(str)
        right=""
        if(flag):
            self.ui.textEdit_2.setText(str)
            right="<p class=\"custom-text\">输入中有敏感词请重新输入</p>"
        self.print_textBrowser(right)
    def print_textBrowser(self,text):
            html_content = f"""
<html>
    <body>
          <style>
                    .custom-text {{
                        color: #ff2121; /* 设置字体颜色为 #ff2121 */
                        font-family: 'Arial', sans-serif;
                        text-align: center;
                        font-size: 10px; /* 字体大小 */
                        line-height: 0.3; /* 行间距 */
                        
                    }}
                     .custom-text2 {{
                        color: #00e500; /* 设置字体颜色为 #ff2121 */
                        font-family: 'Arial', sans-serif;
                        text-align: center;
                        font-size: 10px; /* 字体大小 */
                        line-height: 0.3; /* 行间距 */
                    }}
                </style>
             
                {text}
    </body>
</html>
"""     
            self.ui.textBrowser.setHtml(html_content)      
class changeBook(QWidget):
    def __init__(self):
        super().__init__()
        ui_path = resource_path("图书管理系统3/书籍信息修改页面.ui")
        self.ui=uic.loadUi(ui_path,self)
        self.ui.pushButton.clicked.connect(self.return_main)
        self.ui.pushButton_2.clicked.connect(self.save)
        self.id=-1
    def return_main(self):
        mainW.show()
        self.hide()
    def save(self):
        menu.Data.bookList[self.id].name=self.ui.lineEdit.text()
        menu.Data.bookList[self.id].author=self.ui.lineEdit_2.text()
        mainW.findallBook2('')
        mainW.show()
        self.hide()
class addBook(QWidget):
    def __init__(self):
        super().__init__()
        ui_path = resource_path("图书管理系统3/书籍添加页面.ui")
        self.ui=uic.loadUi(ui_path,self)
        self.ui.pushButton.clicked.connect(self.return_main)
        self.ui.pushButton_2.clicked.connect(self.save)
        self.id=-1
    def return_main(self):
        mainW.show()
        self.hide()
    def save(self):
        temp=menu.Book(self.ui.lineEdit.text(),self.ui.lineEdit_2.text())
        menu.Data.bookList.append(temp)
        mainW.findallBook2('')
        mainW.show()
        self.hide()

def save_data():
    menu.save_users_to_csv( __file__.replace("界面联系.py","users.csv"))
    menu.save_books_to_csv( __file__.replace("界面联系.py","books.csv") )
class addUser(QWidget):
    def __init__(self):
        super().__init__()
        ui_path = resource_path("图书管理系统3/添加用户界面.ui")
        self.ui=uic.loadUi(ui_path,self)
        self.ui.pushButton.clicked.connect(self.return_main)
        self.ui.pushButton_2.clicked.connect(self.save)
        self.id=-1
    def return_main(self):
        mainW.show()
        self.hide()
    def save(self):
        temp=menu.User(self.ui.lineEdit.text(),self.ui.lineEdit_2.text())
        menu.Data.userList.append(temp)
        mainW.findallUser('')
        mainW.show()
        self.hide()
class changeUser(QWidget):
    def __init__(self):
        super().__init__()
        ui_path = resource_path("图书管理系统3/用户修改页面.ui")
        self.ui=uic.loadUi(ui_path,self)
        self.ui.pushButton.clicked.connect(self.return_main)
        self.ui.pushButton_2.clicked.connect(self.save)
        self.id=-1
    def return_main(self):
        mainW.show()
        self.hide()
    def save(self):
        menu.Data.userList[self.id].name=self.ui.lineEdit.text()
        menu.Data.userList[self.id].author=self.ui.lineEdit_2.text()
        #menu.Data.UserList.append(temp)
        mainW.findallUser('')
        mainW.show()
        self.hide()

 # 递归清空子布局
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(save_data)
    login=loginForm();
    register=registerForm()
    mainW=mainWindow()
    change=changeProDataForm()
    cb=changeBook()
    ab=addBook()
    au=addUser()
    cu=changeUser()
    login.show()
    # w1 = changeProDataForm()
    # w1.show()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic
import menu
class loginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.ui=uic.loadUi(__file__.replace("界面联系.py","登录界面完美.ui"),self)
        #信号联系
        self.ui.pushButton_2.clicked.connect(self.open_registerForm)
        self.ui.pushButton_3.clicked.connect(self.app_exit)
        self.ui.pushButton.clicked.connect(self.login)
        #QApplication.instance().aboutToQuit.connect(self.on_application_exit)
    def open_registerForm(self):
        self.registerForm=registerForm()
        self.registerForm.show()
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
            
                self.mainWindow = mainWindow()
                self.mainWindow.show()
                self.hide()
                menu.p=menu.Data.userList[flag]
                if(menu.p.permission==0):
                    self.mainWindow.ui.label.setText(f"用户:{menu.p.username}")
                    self.mainWindow.ui.pushButton_4.hide()
                    self.mainWindow.ui.pushButton_5.hide()
                elif menu.p.permission==1 :
                    self.mainWindow.ui.label.setText(f"管理员:{menu.p.username}")
                self.init_proData()#初始化主界面
        else:
            self.print_textBrowser_2("<p class=\"custom-text\">密码错误</p>")
            
    def init_proData(self):
        self.mainWindow.ui.textEdit_7.setText(menu.p.username)
        self.mainWindow.ui.textEdit_10.setText(len(menu.p.code )* '*')
        self.mainWindow.ui.textEdit_8.setText(menu.p.name)
        self.mainWindow.ui.textEdit_11.setText(str(menu.p.id))
        self.mainWindow.ui.textEdit_9.setText(menu.p.status)
        self.mainWindow.ui.textEdit_12.setText( str(menu.p.permission) )
        
           
        
        
        
       
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
        self.ui=uic.loadUi(__file__.replace("界面联系.py","注册界面完美.ui"),self)
        
        self.ui.pushButton_2.clicked.connect(self.open_loginForm)
        self.ui.pushButton_3.clicked.connect(self.app_exit)
        self.ui.lineEdit_5.textChanged.connect(self.checkPassward)
        self.ui.lineEdit_7.textChanged.connect(self.checkUserId)
        self.ui.pushButton.clicked.connect(self.register)
    def open_loginForm(self):#登录按钮函数
        self.loginForm=loginForm()
        self.loginForm.show();
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
            self.loginForm=loginForm()
            
            self.loginForm.show()
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
        self.ui=uic.loadUi(__file__.replace("界面联系.py","主界面.ui"),self)
        self.ui.pushButton.clicked.connect(self.login);
        self.ui.pushButton_2.clicked.connect(self.app_exit);
        self.ui.pushButton_6.clicked.connect(lambda: (self.ui.stackedWidget.setCurrentIndex(0),self.init_proData()) );
        self.ui.pushButton_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1));
        self.ui.pushButton_4.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2));
        self.ui.pushButton_5.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3));

        
    def app_exit(slef):
        QApplication.exit()
    def login(self):
        self.loginWindow=loginForm()
        self.loginWindow.show()
        self.hide()
    def init_proData(self):
        self.ui.textEdit_7.setText(menu.p.username)
        self.ui.textEdit_10.setText(len(menu.p.code )* '*')
        self.ui.textEdit_8.setText(menu.p.name)
        self.ui.textEdit_11.setText(str(menu.p.id))
        self.ui.textEdit_9.setText(menu.p.status)
        self.ui.textEdit_12.setText( str(menu.p.permission) )

def save_data():
    print("正常退出")

    
if __name__=="__main__":
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(save_data)
    login=loginForm();
    login.show()
    sys.exit(app.exec_())
    
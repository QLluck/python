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
        
    def open_registerForm(self):
        self.registerForm=registerForm()
        self.registerForm.show()
        self.hide()
    def app_exit(slef):
        QApplication.exit()

   
        
        
class registerForm(QWidget):#注册按钮函数
    def __init__(self):
        super().__init__()
        self.ui=uic.loadUi(__file__.replace("界面联系.py","注册界面完美.ui"),self)
        
        self.ui.pushButton_2.clicked.connect(self.open_loginForm)
        self.ui.pushButton_3.clicked.connect(self.app_exit)
        self.ui.lineEdit_5.textChanged.connect(self.checkPassward)
        self.ui.lineEdit_7.textChanged.connect(self.checkUserId)
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
                num_word_low_html= "<p class=\"custom-text\">密码长度小于8</p>"
            if (flag==0):
                right_html="<p class=\"custom-text2\">密码符合要求</p>"
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
           {  num_int_html}
            {num_word_up_html}
           { num_word_low_html}
            {num_other_html}
            {num_len_html}
            {right_html}
                
    </body>
</html>
"""
            self.ui.textBrowser_2.setHtml(html_content)
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
             
                {right}
    </body>
</html>
"""     
        self.ui.textBrowser_2.setHtml(html_content)
        
        
if __name__=="__main__":
    app = QApplication(sys.argv)
    login=loginForm();
    login.show()
    sys.exit(app.exec_())
    
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic
class loginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.ui=uic.loadUi(__file__.replace("界面联系.py","登录界面完美.ui"),self)
        #信号联系
        self.ui.pushButton_2.clicked.connect(self.open_registerForm)
    def open_registerForm(self):
        self.registerForm=registerForm()
        self.registerForm.show()
        self.hide()
class registerForm(QWidget):
    def __init__(self):
        super().__init__()
        self.ui=uic.loadUi(__file__.replace("界面联系.py","注册界面完美.ui"),self)
        self.ui.pushButton_2.clicked.connect(self.open_loginForm)
    def open_loginForm(self):
        self.loginForm=loginForm()
        self.loginForm.show();
        self.hide()
        
if __name__=="__main__":
    app = QApplication(sys.argv)
    login=loginForm();
    login.show()
    sys.exit(app.exec_())
    
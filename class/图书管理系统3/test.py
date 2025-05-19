import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic
import menu
class mainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui=uic.loadUi(__file__.replace("界面联系.py","登录界面完美.ui"),self)
        #信号联系
        self.ui.pushButton_2.clicked.connect(self.open_registerForm)
        self.ui.pushButton_3.clicked.connect(self.app_exit)
        
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    login=mainWindow();
    login.show()
    sys.exit(app.exec_())
    
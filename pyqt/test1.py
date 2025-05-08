from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QLabel,QLineEdit,QDesktopWidget
import sys 
#创建程序
app = QApplication(sys.argv)
#w为一个小控件
w = QWidget()
#label
# label = QLabel("不知道:")
# label.setParent(w);
label=QLabel("密码:",w);
#设置长和宽 两队坐标 (1) ,(2) 1是
label.setGeometry(30,30,30,30); #左上角，和
#按钮类
btn = QPushButton("注册",w)
btn.setGeometry(80,80,300,30)

#输入框
edit=QLineEdit("输入账号:",w);
edit.setGeometry(80,30,1000,30);
#设置窗口标题
w.setWindowTitle("窗口");
#窗口大小 

len=500;
high =500;
w.resize(len,high)

#获取屏幕组件
center_pointer=QDesktopWidget().availableGeometry().center()
x=center_pointer.x();
y=center_pointer.y();
w.move(x-len/2,y-high/2);
#展示窗口

w.show()

#死循环 监听
app.exec_()

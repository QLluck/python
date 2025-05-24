import sys
import os
from PyQt5.QtWidgets import QApplication
from ui.login import LoginWindow
from database.init_db import init_database
from config import DB_CONFIG

def main():
    # 只在数据库文件不存在时初始化数据库
    db_path = DB_CONFIG['database']
    if not os.path.exists(db_path):
        print(f"数据库文件不存在，正在初始化：{db_path}")
        init_database()
    
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 创建并显示登录窗口
    login_window = LoginWindow()
    login_window.show()
    
    # 运行应用程序
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 
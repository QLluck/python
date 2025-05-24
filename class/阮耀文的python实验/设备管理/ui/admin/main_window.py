from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QStackedWidget, QLabel)
from PyQt5.QtCore import Qt
from .device_management import DeviceManagementWidget
from .user_management import UserManagementWidget
from .borrow_management import BorrowManagementWidget
from .profile_management import ProfileManagementWidget

class AdminMainWindow(QMainWindow):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('设备管理系统 - 管理员')
        self.setMinimumSize(1200, 800)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QHBoxLayout(central_widget)

        # 左侧菜单
        menu_widget = QWidget()
        menu_layout = QVBoxLayout(menu_widget)
        menu_layout.setSpacing(10)
        menu_layout.setContentsMargins(10, 20, 10, 20)

        # 用户信息
        user_info = QLabel(f"管理员：{self.user_data['username']}")
        user_info.setStyleSheet("font-size: 14px; font-weight: bold;")
        menu_layout.addWidget(user_info)
        menu_layout.addSpacing(20)

        # 菜单按钮
        self.device_btn = QPushButton('设备管理')
        self.user_btn = QPushButton('学生账号管理')
        self.borrow_btn = QPushButton('借用管理')
        self.profile_btn = QPushButton('个人信息')

        # 设置按钮样式
        for btn in [self.device_btn, self.user_btn, self.borrow_btn, self.profile_btn]:
            btn.setFixedHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding-left: 20px;
                    border: none;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)
            menu_layout.addWidget(btn)

        menu_layout.addStretch()
        menu_widget.setFixedWidth(200)
        main_layout.addWidget(menu_widget)

        # 右侧内容区域
        self.content_stack = QStackedWidget()
        
        # 添加各个功能页面
        self.device_widget = DeviceManagementWidget()
        self.user_widget = UserManagementWidget()
        self.borrow_widget = BorrowManagementWidget()
        self.profile_widget = ProfileManagementWidget(self.user_data)

        self.content_stack.addWidget(self.device_widget)
        self.content_stack.addWidget(self.user_widget)
        self.content_stack.addWidget(self.borrow_widget)
        self.content_stack.addWidget(self.profile_widget)

        main_layout.addWidget(self.content_stack)

        # 连接信号
        self.device_btn.clicked.connect(lambda: self.switch_page(0))
        self.user_btn.clicked.connect(lambda: self.switch_page(1))
        self.borrow_btn.clicked.connect(lambda: self.switch_page(2))
        self.profile_btn.clicked.connect(lambda: self.switch_page(3))

        # 默认显示设备管理页面
        self.switch_page(0)

    def switch_page(self, index):
        self.content_stack.setCurrentIndex(index)
        # 更新按钮样式
        buttons = [self.device_btn, self.user_btn, self.borrow_btn, self.profile_btn]
        for i, btn in enumerate(buttons):
            if i == index:
                btn.setStyleSheet("""
                    QPushButton {
                        text-align: left;
                        padding-left: 20px;
                        border: none;
                        border-radius: 5px;
                        background-color: #e0e0e0;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        text-align: left;
                        padding-left: 20px;
                        border: none;
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: #e0e0e0;
                    }
                """) 
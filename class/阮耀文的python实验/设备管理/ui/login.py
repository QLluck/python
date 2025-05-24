from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt
from database.db_utils import DatabaseConnection
from utils.validators import Validators
from .admin.main_window import AdminMainWindow
from .student.main_window import StudentMainWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.login_attempts = 0
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('设备管理系统 - 登录')
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()
        layout.setSpacing(20)

        # 角色选择
        role_layout = QHBoxLayout()
        role_label = QLabel('角色:')
        self.role_combo = QComboBox()
        self.role_combo.addItems(['学生', '管理员'])
        role_layout.addWidget(role_label)
        role_layout.addWidget(self.role_combo)
        layout.addLayout(role_layout)

        # 用户名
        username_layout = QHBoxLayout()
        username_label = QLabel('用户名:')
        self.username_input = QLineEdit()
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)

        # 密码
        password_layout = QHBoxLayout()
        password_label = QLabel('密码:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)

        # 登录按钮
        self.login_button = QPushButton('登录')
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        role = 'admin' if self.role_combo.currentText() == '管理员' else 'student'

        print(f"尝试登录：用户名={username}, 角色={role}")

        if not username or not password:
            QMessageBox.warning(self, '错误', '请输入用户名和密码')
            return

        db = DatabaseConnection()
        query = "SELECT * FROM users WHERE username = ? AND role = ?"
        print(f"执行查询：{query}")
        print(f"参数：{(username, role)}")
        result = db.execute_query(query, (username, role))
        print(f"查询结果：{result}")

        if not result:
            self.login_attempts += 1
            if self.login_attempts >= 3:
                QMessageBox.critical(self, '错误', '登录失败次数过多，程序将关闭')
                self.close()
            else:
                QMessageBox.warning(self, '错误', f'用户名或密码错误，还剩{3-self.login_attempts}次机会')
            return

        user = result[0]
        stored_password = user['password']
        print(f"数据库中的密码类型：{type(stored_password)}")
        # 如果存储的密码已经是bytes类型，就不需要encode
        if isinstance(stored_password, str):
            print("密码是字符串类型，转换为bytes")
            stored_password = stored_password.encode('utf-8')
            
        print("验证密码...")
        if not Validators.verify_password(password, stored_password):
            print("密码验证失败")
            self.login_attempts += 1
            if self.login_attempts >= 3:
                QMessageBox.critical(self, '错误', '登录失败次数过多，程序将关闭')
                self.close()
            else:
                QMessageBox.warning(self, '错误', f'用户名或密码错误，还剩{3-self.login_attempts}次机会')
            return

        print("密码验证成功")
        QMessageBox.information(self, '成功', '登录成功')
        
        # 根据角色打开相应的主界面
        if role == 'admin':
            print("打开管理员主界面")
            self.admin_window = AdminMainWindow(user)
            self.admin_window.show()
        else:
            print("打开学生主界面")
            self.student_window = StudentMainWindow(user)
            self.student_window.show()
        
        self.close() 
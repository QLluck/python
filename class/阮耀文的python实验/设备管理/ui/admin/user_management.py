from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QMessageBox,
                             QDialog, QLabel, QLineEdit, QComboBox)
from PyQt5.QtCore import Qt
from database.db_utils import DatabaseConnection
from utils.validators import Validators

class UserDialog(QDialog):
    def __init__(self, parent=None, user_data=None):
        super().__init__(parent)
        self.user_data = user_data
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('学生账号信息')
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        # 用户名（学号）
        username_layout = QHBoxLayout()
        username_label = QLabel('学号:')
        self.username_input = QLineEdit()
        if self.user_data:
            self.username_input.setText(self.user_data['username'])
            self.username_input.setReadOnly(True)
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

        # 手机号
        phone_layout = QHBoxLayout()
        phone_label = QLabel('手机号:')
        self.phone_input = QLineEdit()
        if self.user_data:
            self.phone_input.setText(self.user_data['phone'])
        phone_layout.addWidget(phone_label)
        phone_layout.addWidget(self.phone_input)
        layout.addLayout(phone_layout)

        # 按钮
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton('保存')
        self.cancel_btn = QPushButton('取消')
        self.save_btn.clicked.connect(self.validate_and_accept)
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def validate_and_accept(self):
        # 验证用户名
        if not self.username_input.text().strip():
            QMessageBox.warning(self, '错误', '请输入学号')
            return

        # 验证密码
        if not self.user_data:  # 新用户必须输入密码
            if not self.password_input.text():
                QMessageBox.warning(self, '错误', '请输入密码')
                return
            is_valid, message = Validators.validate_password(self.password_input.text())
            if not is_valid:
                QMessageBox.warning(self, '错误', message)
                return
        elif self.password_input.text():  # 修改密码时验证新密码
            is_valid, message = Validators.validate_password(self.password_input.text())
            if not is_valid:
                QMessageBox.warning(self, '错误', message)
                return

        # 验证手机号
        is_valid, message = Validators.validate_phone(self.phone_input.text())
        if not is_valid:
            QMessageBox.warning(self, '错误', message)
            return

        self.accept()

    def get_user_data(self):
        data = {
            'username': self.username_input.text().strip(),
            'phone': self.phone_input.text().strip()
        }
        if not self.user_data or self.password_input.text():  # 新用户或修改密码
            password = self.password_input.text()
            hashed = Validators.hash_password(password)
            data['password'] = hashed
        return data

class UserManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_users()

    def init_ui(self):
        layout = QVBoxLayout()

        # 工具栏
        toolbar = QHBoxLayout()
        self.add_btn = QPushButton('添加学生')
        self.edit_btn = QPushButton('编辑学生')
        self.delete_btn = QPushButton('删除学生')
        self.refresh_btn = QPushButton('刷新')

        for btn in [self.add_btn, self.edit_btn, self.delete_btn, self.refresh_btn]:
            toolbar.addWidget(btn)

        toolbar.addStretch()
        layout.addLayout(toolbar)

        # 用户列表
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(4)
        self.user_table.setHorizontalHeaderLabels(['ID', '学号', '手机号', '创建时间'])
        self.user_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.user_table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.user_table)

        # 连接信号
        self.add_btn.clicked.connect(self.add_user)
        self.edit_btn.clicked.connect(self.edit_user)
        self.delete_btn.clicked.connect(self.delete_user)
        self.refresh_btn.clicked.connect(self.load_users)

        self.setLayout(layout)

    def load_users(self):
        db = DatabaseConnection()
        users = db.execute_query("SELECT * FROM users WHERE role = 'student' ORDER BY id")
        
        self.user_table.setRowCount(len(users))
        for i, user in enumerate(users):
            self.user_table.setItem(i, 0, QTableWidgetItem(str(user['id'])))
            self.user_table.setItem(i, 1, QTableWidgetItem(user['username']))
            self.user_table.setItem(i, 2, QTableWidgetItem(user['phone']))
            self.user_table.setItem(i, 3, QTableWidgetItem(str(user['created_at'])))

    def add_user(self):
        dialog = UserDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            user_data = dialog.get_user_data()
            db = DatabaseConnection()
            
            # 检查用户名是否已存在
            existing_user = db.execute_query(
                "SELECT id FROM users WHERE username = %s",
                (user_data['username'],)
            )
            if existing_user:
                QMessageBox.warning(self, '错误', '该学号已被注册')
                return
                
            query = """
                INSERT INTO users (role, username, password, phone)
                VALUES ('student', %s, %s, %s)
            """
            try:
                db.execute_query(query, (
                    user_data['username'],
                    user_data['password'],
                    user_data['phone']
                ))
                self.load_users()
                QMessageBox.information(self, '成功', '学生账号添加成功')
            except Exception as e:
                QMessageBox.critical(self, '错误', f'学生账号添加失败：{str(e)}')

    def edit_user(self):
        current_row = self.user_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, '警告', '请先选择要编辑的学生')
            return

        user_id = int(self.user_table.item(current_row, 0).text())
        db = DatabaseConnection()
        user = db.execute_query("SELECT * FROM users WHERE id = %s", (user_id,))[0]

        dialog = UserDialog(self, user)
        if dialog.exec_() == QDialog.Accepted:
            user_data = dialog.get_user_data()
            if 'password' in user_data:  # 如果修改了密码
                query = """
                    UPDATE users
                    SET password = %s, phone = %s
                    WHERE id = %s
                """
                params = (user_data['password'], user_data['phone'], user_id)
            else:  # 只修改手机号
                query = """
                    UPDATE users
                    SET phone = %s
                    WHERE id = %s
                """
                params = (user_data['phone'], user_id)

            try:
                db.execute_query(query, params)
                self.load_users()
                QMessageBox.information(self, '成功', '学生信息更新成功')
            except Exception as e:
                QMessageBox.critical(self, '错误', f'学生信息更新失败：{str(e)}')

    def delete_user(self):
        current_row = self.user_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, '警告', '请先选择要删除的学生')
            return

        user_id = int(self.user_table.item(current_row, 0).text())
        reply = QMessageBox.question(
            self, '确认', '确定要删除这个学生账号吗？',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            db = DatabaseConnection()
            try:
                # 检查是否有未完成的借用记录
                records = db.execute_query(
                    "SELECT id FROM borrow_records WHERE user_id = %s AND status != '已归还'",
                    (user_id,)
                )
                if records:
                    QMessageBox.warning(self, '警告', '该学生还有未归还的设备，无法删除账号')
                    return
                    
                db.execute_query("DELETE FROM users WHERE id = %s", (user_id,))
                self.load_users()
                QMessageBox.information(self, '成功', '学生账号删除成功')
            except Exception as e:
                QMessageBox.critical(self, '错误', f'学生账号删除失败：{str(e)}') 
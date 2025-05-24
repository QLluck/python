from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QLineEdit, QMessageBox)
from PyQt5.QtCore import Qt
from database.db_utils import DatabaseConnection
from utils.validators import Validators

class ProfileManagementWidget(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # 标题
        title = QLabel('个人信息管理')
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # 用户名（只读）
        username_layout = QHBoxLayout()
        username_label = QLabel('用户名:')
        self.username_input = QLineEdit(self.user_data['username'])
        self.username_input.setReadOnly(True)
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)

        # 手机号
        phone_layout = QHBoxLayout()
        phone_label = QLabel('手机号:')
        self.phone_input = QLineEdit(self.user_data['phone'])
        phone_layout.addWidget(phone_label)
        phone_layout.addWidget(self.phone_input)
        layout.addLayout(phone_layout)

        # 修改密码
        password_title = QLabel('修改密码')
        password_title.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 20px;")
        layout.addWidget(password_title)

        # 原密码
        old_password_layout = QHBoxLayout()
        old_password_label = QLabel('原密码:')
        self.old_password_input = QLineEdit()
        self.old_password_input.setEchoMode(QLineEdit.Password)
        old_password_layout.addWidget(old_password_label)
        old_password_layout.addWidget(self.old_password_input)
        layout.addLayout(old_password_layout)

        # 新密码
        new_password_layout = QHBoxLayout()
        new_password_label = QLabel('新密码:')
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        new_password_layout.addWidget(new_password_label)
        new_password_layout.addWidget(self.new_password_input)
        layout.addLayout(new_password_layout)

        # 确认新密码
        confirm_password_layout = QHBoxLayout()
        confirm_password_label = QLabel('确认新密码:')
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        confirm_password_layout.addWidget(confirm_password_label)
        confirm_password_layout.addWidget(self.confirm_password_input)
        layout.addLayout(confirm_password_layout)

        # 按钮
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton('保存修改')
        self.save_btn.clicked.connect(self.save_changes)
        button_layout.addWidget(self.save_btn)
        layout.addLayout(button_layout)

        layout.addStretch()
        self.setLayout(layout)

    def save_changes(self):
        # 验证手机号
        is_valid, message = Validators.validate_phone(self.phone_input.text())
        if not is_valid:
            QMessageBox.warning(self, '错误', message)
            return

        # 如果要修改密码
        if self.old_password_input.text() or self.new_password_input.text() or self.confirm_password_input.text():
            # 验证原密码
            db = DatabaseConnection()
            user = db.execute_query("SELECT password FROM users WHERE id = %s", (self.user_data['id'],))[0]
            if not Validators.verify_password(self.old_password_input.text(), user['password'].encode('utf-8')):
                QMessageBox.warning(self, '错误', '原密码错误')
                return

            # 验证新密码
            if self.new_password_input.text() != self.confirm_password_input.text():
                QMessageBox.warning(self, '错误', '两次输入的新密码不一致')
                return

            is_valid, message = Validators.validate_password(self.new_password_input.text())
            if not is_valid:
                QMessageBox.warning(self, '错误', message)
                return

            # 更新密码和手机号
            try:
                db.execute_query("""
                    UPDATE users
                    SET password = %s, phone = %s
                    WHERE id = %s
                """, (
                    Validators.hash_password(self.new_password_input.text()),
                    self.phone_input.text(),
                    self.user_data['id']
                ))
                QMessageBox.information(self, '成功', '个人信息更新成功')
                # 清空密码输入框
                self.old_password_input.clear()
                self.new_password_input.clear()
                self.confirm_password_input.clear()
            except Exception as e:
                QMessageBox.critical(self, '错误', f'更新失败：{str(e)}')
        else:
            # 只更新手机号
            try:
                db = DatabaseConnection()
                db.execute_query("""
                    UPDATE users
                    SET phone = %s
                    WHERE id = %s
                """, (self.phone_input.text(), self.user_data['id']))
                QMessageBox.information(self, '成功', '手机号更新成功')
            except Exception as e:
                QMessageBox.critical(self, '错误', f'更新失败：{str(e)}') 
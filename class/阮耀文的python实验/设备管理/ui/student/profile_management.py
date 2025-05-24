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
        self.load_user_data()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # 标题
        title = QLabel('个人信息管理')
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # 学号（只读）
        student_id_layout = QHBoxLayout()
        student_id_label = QLabel('学号:')
        self.student_id_input = QLineEdit()
        self.student_id_input.setReadOnly(True)
        student_id_layout.addWidget(student_id_label)
        student_id_layout.addWidget(self.student_id_input)
        layout.addLayout(student_id_layout)

        # 手机号
        phone_layout = QHBoxLayout()
        phone_label = QLabel('手机号:')
        self.phone_input = QLineEdit()
        phone_layout.addWidget(phone_label)
        phone_layout.addWidget(self.phone_input)
        layout.addLayout(phone_layout)

        # 修改密码部分
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
        confirm_password_label = QLabel('确认密码:')
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        confirm_password_layout.addWidget(confirm_password_label)
        confirm_password_layout.addWidget(self.confirm_password_input)
        layout.addLayout(confirm_password_layout)

        # 保存按钮
        self.save_btn = QPushButton('保存修改')
        self.save_btn.clicked.connect(self.save_changes)
        layout.addWidget(self.save_btn)

        layout.addStretch()
        self.setLayout(layout)

    def load_user_data(self):
        self.student_id_input.setText(self.user_data['username'])
        self.phone_input.setText(self.user_data.get('phone', ''))

    def save_changes(self):
        # 验证手机号
        phone = self.phone_input.text().strip()
        if phone and not Validators.validate_phone(phone):
            QMessageBox.warning(self, '警告', '请输入有效的手机号码')
            return

        # 检查是否要修改密码
        old_password = self.old_password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        try:
            db = DatabaseConnection()
            updates = []
            params = []

            # 如果输入了原密码，则验证并更新密码
            if old_password:
                # 验证原密码
                result = db.execute_query("""
                    SELECT password FROM users
                    WHERE id = %s AND password = %s
                """, (self.user_data['id'], old_password))
                
                if not result:
                    QMessageBox.warning(self, '警告', '原密码错误')
                    return

                # 验证新密码
                if not new_password or not confirm_password:
                    QMessageBox.warning(self, '警告', '请输入新密码和确认密码')
                    return

                if new_password != confirm_password:
                    QMessageBox.warning(self, '警告', '两次输入的新密码不一致')
                    return

                if not Validators.validate_password(new_password):
                    QMessageBox.warning(self, '警告', '新密码必须包含字母和数字，长度至少为6位')
                    return

                updates.append("password = %s")
                params.append(new_password)

            # 更新手机号
            if phone:
                updates.append("phone = %s")
                params.append(phone)

            if updates:
                # 添加用户ID到参数列表
                params.append(self.user_data['id'])
                
                # 执行更新
                query = f"""
                    UPDATE users
                    SET {', '.join(updates)}
                    WHERE id = %s
                """
                db.execute_query(query, tuple(params))
                
                QMessageBox.information(self, '成功', '个人信息已更新')
                
                # 清空密码输入框
                self.old_password_input.clear()
                self.new_password_input.clear()
                self.confirm_password_input.clear()
            else:
                QMessageBox.information(self, '提示', '没有需要更新的信息')

        except Exception as e:
            QMessageBox.critical(self, '错误', f'更新失败：{str(e)}') 
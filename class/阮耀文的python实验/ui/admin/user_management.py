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
            "SELECT id FROM users WHERE username = ?",
            (user_data['username'],)
        )
        if existing_user:
            QMessageBox.warning(self, '错误', '该学号已被注册')
            return
            
        query = """
            INSERT INTO users (role, username, password, phone)
            VALUES ('student', ?, ?, ?)
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
    user = db.execute_query("SELECT * FROM users WHERE id = ?", (user_id,))[0]

    dialog = UserDialog(self, user)
    if dialog.exec_() == QDialog.Accepted:
        user_data = dialog.get_user_data()
        if 'password' in user_data:  # 如果修改了密码
            query = """
                UPDATE users
                SET password = ?, phone = ?
                WHERE id = ?
            """
            params = (user_data['password'], user_data['phone'], user_id)
        else:  # 只修改手机号
            query = """
                UPDATE users
                SET phone = ?
                WHERE id = ?
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
                "SELECT id FROM borrow_records WHERE user_id = ? AND status != '已归还'",
                (user_id,)
            )
            if records:
                QMessageBox.warning(self, '警告', '该学生还有未归还的设备，无法删除账号')
                return
                
            db.execute_query("DELETE FROM users WHERE id = ?", (user_id,))
            self.load_users()
            QMessageBox.information(self, '成功', '学生账号删除成功')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'学生账号删除失败：{str(e)}') 
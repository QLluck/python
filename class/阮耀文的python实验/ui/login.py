        if not username or not password:
            QMessageBox.warning(self, '错误', '请输入用户名和密码')
            return

        db = DatabaseConnection()
        query = "SELECT * FROM users WHERE username = ? AND role = ?"
        result = db.execute_query(query, (username, role))

        if not result:
            self.login_attempts += 1
            if self.login_attempts >= 3:
                QMessageBox.critical(self, '错误', '登录失败次数过多，程序将关闭')
                self.close()
            else:
                QMessageBox.warning(self, '错误', f'用户名或密码错误，还剩{3-self.login_attempts}次机会')
            return 
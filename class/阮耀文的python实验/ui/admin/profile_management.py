# 验证原密码
db = DatabaseConnection()
user = db.execute_query("SELECT password FROM users WHERE id = ?", (self.user_data['id'],))[0]

# 如果存储的密码已经是bytes类型，就不需要encode
stored_password = user['password']
if isinstance(stored_password, str):
    stored_password = stored_password.encode('utf-8')

if not Validators.verify_password(old_password, stored_password):
    QMessageBox.warning(self, '错误', '原密码不正确')
    return

# 如果修改了密码
if new_password:
    # 验证新密码
    is_valid, message = Validators.validate_password(new_password)
    if not is_valid:
        QMessageBox.warning(self, '错误', message)
        return
    
    # 哈希新密码
    hashed_password = Validators.hash_password(new_password)
    try:
        db.execute_query("""
            UPDATE users
            SET password = ?
            WHERE id = ?
        """, (hashed_password, self.user_data['id']))
        QMessageBox.information(self, '成功', '密码修改成功')
    except Exception as e:
        QMessageBox.critical(self, '错误', f'密码修改失败：{str(e)}')

# 如果修改了手机号
if phone != self.user_data.get('phone', ''):
    # 验证手机号
    is_valid, message = Validators.validate_phone(phone)
    if not is_valid:
        QMessageBox.warning(self, '错误', message)
        return
    
    try:
        db.execute_query("""
            UPDATE users
            SET phone = ?
            WHERE id = ?
        """, (phone, self.user_data['id']))
        self.user_data['phone'] = phone
        QMessageBox.information(self, '成功', '手机号修改成功')
    except Exception as e:
        QMessageBox.critical(self, '错误', f'手机号修改失败：{str(e)}') 
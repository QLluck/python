# 检查是否已有未完成的借用
db = DatabaseConnection()
existing_borrow = db.execute_query("""
    SELECT * FROM borrow_records
    WHERE user_id = ? AND status IN ('申请中', '借用中')
""", (self.user_data['id'],))

if existing_borrow:
    QMessageBox.warning(self, '警告', '您已有未完成的借用申请或正在借用的设备')
    return

dialog = BorrowDialog(self, device)
if dialog.exec_() == QDialog.Accepted:
    borrow_data = dialog.get_borrow_data()
    try:
        db.execute_query("""
            INSERT INTO borrow_records (user_id, device_id, borrow_date, status)
            VALUES (?, ?, ?, '申请中')
        """, (
            self.user_data['id'],
            device['id'],
            borrow_data['borrow_date']
        ))
        self.load_devices()
        QMessageBox.information(self, '成功', '借用申请已提交，请等待管理员审核')
    except Exception as e:
        QMessageBox.critical(self, '错误', f'申请提交失败：{str(e)}') 
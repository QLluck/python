def load_records(self):
    db = DatabaseConnection()
    
    # 加载申请中的记录
    pending_records = db.execute_query("""
        SELECT br.*, d.name as device_name
        FROM borrow_records br
        JOIN devices d ON br.device_id = d.id
        WHERE br.user_id = ? AND br.status = '申请中'
        ORDER BY br.borrow_date DESC
    """, (self.user_data['id'],))
    self.load_table_data(self.pending_table, pending_records, '申请中')

    # 加载借用中的记录
    borrowing_records = db.execute_query("""
        SELECT br.*, d.name as device_name
        FROM borrow_records br
        JOIN devices d ON br.device_id = d.id
        WHERE br.user_id = ? AND br.status = '借用中'
        ORDER BY br.borrow_date DESC
    """, (self.user_data['id'],))
    self.load_table_data(self.borrowing_table, borrowing_records, '借用中')

    # 加载已归还的记录
    returned_records = db.execute_query("""
        SELECT br.*, d.name as device_name
        FROM borrow_records br
        JOIN devices d ON br.device_id = d.id
        WHERE br.user_id = ? AND br.status = '已归还'
        ORDER BY br.return_date DESC
    """, (self.user_data['id'],))
    self.load_table_data(self.returned_table, returned_records, '已归还')

def handle_cancel(self, record):
    reply = QMessageBox.question(self, '确认', '确定要取消该借用申请吗？',
                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if reply == QMessageBox.Yes:
        try:
            db = DatabaseConnection()
            db.execute_query("""
                DELETE FROM borrow_records
                WHERE id = ? AND user_id = ? AND status = '申请中'
            """, (record['id'], self.user_data['id']))
            self.load_records()
            QMessageBox.information(self, '成功', '借用申请已取消')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'取消申请失败：{str(e)}')

def handle_return(self, record):
    reply = QMessageBox.question(self, '确认', '确定要申请归还该设备吗？',
                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if reply == QMessageBox.Yes:
        try:
            db = DatabaseConnection()
            db.execute_query("""
                UPDATE borrow_records
                SET status = '待归还'
                WHERE id = ? AND user_id = ? AND status = '借用中'
            """, (record['id'], self.user_data['id']))
            self.load_records()
            QMessageBox.information(self, '成功', '归还申请已提交，请等待管理员确认')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'提交归还申请失败：{str(e)}') 
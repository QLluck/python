def load_records(self):
    db = DatabaseConnection()
    
    # 加载待审核记录
    pending_records = db.execute_query("""
        SELECT br.*, u.username as student_name, d.name as device_name
        FROM borrow_records br
        JOIN users u ON br.user_id = u.id
        JOIN devices d ON br.device_id = d.id
        WHERE br.status = '申请中'
        ORDER BY br.created_at DESC
    """)
    self.load_table_data(self.pending_table, pending_records, True)

    # 加载借用中记录
    borrowing_records = db.execute_query("""
        SELECT br.*, u.username as student_name, d.name as device_name
        FROM borrow_records br
        JOIN users u ON br.user_id = u.id
        JOIN devices d ON br.device_id = d.id
        WHERE br.status = '借用中'
        ORDER BY br.created_at DESC
    """)
    self.load_table_data(self.borrowing_table, borrowing_records, False)

    # 加载已归还记录
    returned_records = db.execute_query("""
        SELECT br.*, u.username as student_name, d.name as device_name
        FROM borrow_records br
        JOIN users u ON br.user_id = u.id
        JOIN devices d ON br.device_id = d.id
        WHERE br.status = '已归还'
        ORDER BY br.created_at DESC
    """)
    self.load_table_data(self.returned_table, returned_records, False)

def handle_action(self, record):
    db = DatabaseConnection()
    if record['status'] == '申请中':
        # 审核通过
        try:
            # 更新借用记录状态
            db.execute_query("""
                UPDATE borrow_records
                SET status = '借用中'
                WHERE id = ?
            """, (record['id'],))

            # 更新设备可借数量
            db.execute_query("""
                UPDATE devices
                SET available_qty = available_qty - 1
                WHERE id = ?
            """, (record['device_id'],))

            self.load_records()
            QMessageBox.information(self, '成功', '已通过借用申请')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'操作失败：{str(e)}')
    elif record['status'] == '借用中':
        # 确认归还
        try:
            # 更新借用记录状态
            db.execute_query("""
                UPDATE borrow_records
                SET status = '已归还', return_date = CURRENT_DATE
                WHERE id = ?
            """, (record['id'],))

            # 更新设备可借数量
            db.execute_query("""
                UPDATE devices
                SET available_qty = available_qty + 1
                WHERE id = ?
            """, (record['device_id'],))

            self.load_records()
            QMessageBox.information(self, '成功', '已确认设备归还')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'操作失败：{str(e)}') 
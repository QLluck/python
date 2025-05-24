from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QMessageBox,
                             QTabWidget, QLabel)
from PyQt5.QtCore import Qt
from database.db_utils import DatabaseConnection

class BorrowManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_records()

    def init_ui(self):
        layout = QVBoxLayout()

        # 创建标签页
        self.tab_widget = QTabWidget()
        
        # 待审核标签页
        self.pending_tab = QWidget()
        pending_layout = QVBoxLayout()
        self.pending_table = QTableWidget()
        self.pending_table.setColumnCount(6)
        self.pending_table.setHorizontalHeaderLabels(['ID', '学生', '设备', '借用时间', '状态', '操作'])
        pending_layout.addWidget(self.pending_table)
        self.pending_tab.setLayout(pending_layout)

        # 借用中标签页
        self.borrowing_tab = QWidget()
        borrowing_layout = QVBoxLayout()
        self.borrowing_table = QTableWidget()
        self.borrowing_table.setColumnCount(6)
        self.borrowing_table.setHorizontalHeaderLabels(['ID', '学生', '设备', '借用时间', '状态', '操作'])
        borrowing_layout.addWidget(self.borrowing_table)
        self.borrowing_tab.setLayout(borrowing_layout)

        # 已归还标签页
        self.returned_tab = QWidget()
        returned_layout = QVBoxLayout()
        self.returned_table = QTableWidget()
        self.returned_table.setColumnCount(7)
        self.returned_table.setHorizontalHeaderLabels(['ID', '学生', '设备', '借用时间', '归还时间', '状态', '操作'])
        returned_layout.addWidget(self.returned_table)
        self.returned_tab.setLayout(returned_layout)

        # 添加标签页
        self.tab_widget.addTab(self.pending_tab, "待审核")
        self.tab_widget.addTab(self.borrowing_tab, "借用中")
        self.tab_widget.addTab(self.returned_tab, "已归还")

        layout.addWidget(self.tab_widget)

        # 刷新按钮
        self.refresh_btn = QPushButton('刷新')
        self.refresh_btn.clicked.connect(self.load_records)
        layout.addWidget(self.refresh_btn)

        self.setLayout(layout)

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

    def load_table_data(self, table, records, is_pending):
        table.setRowCount(len(records))
        for i, record in enumerate(records):
            table.setItem(i, 0, QTableWidgetItem(str(record['id'])))
            table.setItem(i, 1, QTableWidgetItem(record['student_name']))
            table.setItem(i, 2, QTableWidgetItem(record['device_name']))
            table.setItem(i, 3, QTableWidgetItem(str(record['borrow_date'])))
            if not is_pending:
                table.setItem(i, 4, QTableWidgetItem(str(record['return_date'])))
            table.setItem(i, 4 if is_pending else 5, QTableWidgetItem(record['status']))

            # 添加操作按钮
            action_btn = QPushButton('审核通过' if is_pending else '确认归还')
            action_btn.clicked.connect(lambda checked, r=record: self.handle_action(r))
            table.setCellWidget(i, 5 if is_pending else 6, action_btn)

    def handle_action(self, record):
        db = DatabaseConnection()
        if record['status'] == '申请中':
            # 审核通过
            try:
                # 更新借用记录状态
                db.execute_query("""
                    UPDATE borrow_records
                    SET status = '借用中'
                    WHERE id = %s
                """, (record['id'],))

                # 更新设备可借数量
                db.execute_query("""
                    UPDATE devices
                    SET available_qty = available_qty - 1
                    WHERE id = %s
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
                    SET status = '已归还', return_date = CURDATE()
                    WHERE id = %s
                """, (record['id'],))

                # 更新设备可借数量
                db.execute_query("""
                    UPDATE devices
                    SET available_qty = available_qty + 1
                    WHERE id = %s
                """, (record['device_id'],))

                self.load_records()
                QMessageBox.information(self, '成功', '已确认设备归还')
            except Exception as e:
                QMessageBox.critical(self, '错误', f'操作失败：{str(e)}') 
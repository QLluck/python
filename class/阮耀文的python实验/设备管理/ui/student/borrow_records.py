from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QMessageBox,
                             QTabWidget)
from PyQt5.QtCore import Qt
from database.db_utils import DatabaseConnection

class BorrowRecordsWidget(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.init_ui()
        self.load_records()

    def init_ui(self):
        layout = QVBoxLayout()

        # 工具栏
        toolbar = QHBoxLayout()
        self.refresh_btn = QPushButton('刷新')
        self.refresh_btn.clicked.connect(self.load_records)
        toolbar.addWidget(self.refresh_btn)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        # 创建标签页
        self.tab_widget = QTabWidget()
        
        # 创建三个标签页
        self.pending_table = QTableWidget()
        self.borrowing_table = QTableWidget()
        self.returned_table = QTableWidget()

        # 设置表格
        for table in [self.pending_table, self.borrowing_table, self.returned_table]:
            table.setColumnCount(6)
            table.setHorizontalHeaderLabels(['ID', '设备名称', '借用日期', '归还日期', '状态', '操作'])
            table.setSelectionBehavior(QTableWidget.SelectRows)
            table.setSelectionMode(QTableWidget.SingleSelection)

        # 添加标签页
        self.tab_widget.addTab(self.pending_table, '申请中')
        self.tab_widget.addTab(self.borrowing_table, '借用中')
        self.tab_widget.addTab(self.returned_table, '已归还')

        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

    def load_records(self):
        db = DatabaseConnection()
        
        # 加载申请中的记录
        pending_records = db.execute_query("""
            SELECT br.*, d.name as device_name
            FROM borrow_records br
            JOIN devices d ON br.device_id = d.id
            WHERE br.user_id = %s AND br.status = '申请中'
            ORDER BY br.borrow_date DESC
        """, (self.user_data['id'],))
        self.load_table_data(self.pending_table, pending_records, '申请中')

        # 加载借用中的记录
        borrowing_records = db.execute_query("""
            SELECT br.*, d.name as device_name
            FROM borrow_records br
            JOIN devices d ON br.device_id = d.id
            WHERE br.user_id = %s AND br.status = '借用中'
            ORDER BY br.borrow_date DESC
        """, (self.user_data['id'],))
        self.load_table_data(self.borrowing_table, borrowing_records, '借用中')

        # 加载已归还的记录
        returned_records = db.execute_query("""
            SELECT br.*, d.name as device_name
            FROM borrow_records br
            JOIN devices d ON br.device_id = d.id
            WHERE br.user_id = %s AND br.status = '已归还'
            ORDER BY br.return_date DESC
        """, (self.user_data['id'],))
        self.load_table_data(self.returned_table, returned_records, '已归还')

    def load_table_data(self, table, records, status):
        table.setRowCount(len(records))
        for i, record in enumerate(records):
            table.setItem(i, 0, QTableWidgetItem(str(record['id'])))
            table.setItem(i, 1, QTableWidgetItem(record['device_name']))
            table.setItem(i, 2, QTableWidgetItem(str(record['borrow_date'])))
            table.setItem(i, 3, QTableWidgetItem(str(record['return_date'] or '')))
            table.setItem(i, 4, QTableWidgetItem(record['status']))

            # 添加操作按钮
            if status == '申请中':
                cancel_btn = QPushButton('取消申请')
                cancel_btn.clicked.connect(lambda checked, r=record: self.handle_cancel(r))
                table.setCellWidget(i, 5, cancel_btn)
            elif status == '借用中':
                return_btn = QPushButton('申请归还')
                return_btn.clicked.connect(lambda checked, r=record: self.handle_return(r))
                table.setCellWidget(i, 5, return_btn)
            else:
                table.setItem(i, 5, QTableWidgetItem(''))

    def handle_cancel(self, record):
        reply = QMessageBox.question(self, '确认', '确定要取消该借用申请吗？',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                db = DatabaseConnection()
                db.execute_query("""
                    DELETE FROM borrow_records
                    WHERE id = %s AND user_id = %s AND status = '申请中'
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
                    WHERE id = %s AND user_id = %s AND status = '借用中'
                """, (record['id'], self.user_data['id']))
                self.load_records()
                QMessageBox.information(self, '成功', '归还申请已提交，请等待管理员确认')
            except Exception as e:
                QMessageBox.critical(self, '错误', f'提交归还申请失败：{str(e)}') 
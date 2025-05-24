from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QMessageBox,
                             QDialog, QLabel, QDateEdit)
from PyQt5.QtCore import Qt, QDate
from database.db_utils import DatabaseConnection

class BorrowDialog(QDialog):
    def __init__(self, parent=None, device_data=None):
        super().__init__(parent)
        self.device_data = device_data
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('借用申请')
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()

        # 设备信息
        device_info = QLabel(f"设备：{self.device_data['name']}")
        device_info.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(device_info)

        # 借用日期
        date_layout = QHBoxLayout()
        date_label = QLabel('借用日期:')
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_input)
        layout.addLayout(date_layout)

        # 按钮
        button_layout = QHBoxLayout()
        self.submit_btn = QPushButton('提交申请')
        self.cancel_btn = QPushButton('取消')
        self.submit_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.submit_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_borrow_data(self):
        return {
            'borrow_date': self.date_input.date().toPyDate()
        }

class DeviceListWidget(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.init_ui()
        self.load_devices()

    def init_ui(self):
        layout = QVBoxLayout()

        # 工具栏
        toolbar = QHBoxLayout()
        self.refresh_btn = QPushButton('刷新')
        self.refresh_btn.clicked.connect(self.load_devices)
        toolbar.addWidget(self.refresh_btn)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        # 设备列表
        self.device_table = QTableWidget()
        self.device_table.setColumnCount(6)
        self.device_table.setHorizontalHeaderLabels(['ID', '设备名称', '总数', '可借数量', '状态', '操作'])
        self.device_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.device_table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.device_table)

        self.setLayout(layout)

    def load_devices(self):
        db = DatabaseConnection()
        devices = db.execute_query("SELECT * FROM devices ORDER BY id")
        
        self.device_table.setRowCount(len(devices))
        for i, device in enumerate(devices):
            self.device_table.setItem(i, 0, QTableWidgetItem(str(device['id'])))
            self.device_table.setItem(i, 1, QTableWidgetItem(device['name']))
            self.device_table.setItem(i, 2, QTableWidgetItem(str(device['total_qty'])))
            self.device_table.setItem(i, 3, QTableWidgetItem(str(device['available_qty'])))
            self.device_table.setItem(i, 4, QTableWidgetItem(device['status']))

            # 添加借用按钮
            borrow_btn = QPushButton('申请借用')
            borrow_btn.setEnabled(device['available_qty'] > 0 and device['status'] == '可用')
            borrow_btn.clicked.connect(lambda checked, d=device: self.handle_borrow(d))
            self.device_table.setCellWidget(i, 5, borrow_btn)

    def handle_borrow(self, device):
        # 检查是否已有未完成的借用
        db = DatabaseConnection()
        existing_borrow = db.execute_query("""
            SELECT * FROM borrow_records
            WHERE user_id = %s AND status IN ('申请中', '借用中')
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
                    VALUES (%s, %s, %s, '申请中')
                """, (
                    self.user_data['id'],
                    device['id'],
                    borrow_data['borrow_date']
                ))
                self.load_devices()
                QMessageBox.information(self, '成功', '借用申请已提交，请等待管理员审核')
            except Exception as e:
                QMessageBox.critical(self, '错误', f'申请提交失败：{str(e)}') 
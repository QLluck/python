from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QMessageBox,
                             QDialog, QLabel, QLineEdit, QSpinBox, QComboBox)
from PyQt5.QtCore import Qt
from database.db_utils import DatabaseConnection

class DeviceDialog(QDialog):
    def __init__(self, parent=None, device_data=None):
        super().__init__(parent)
        self.device_data = device_data
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('设备信息')
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        # 设备名称
        name_layout = QHBoxLayout()
        name_label = QLabel('设备名称:')
        self.name_input = QLineEdit()
        if self.device_data:
            self.name_input.setText(self.device_data['name'])
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # 总数
        total_layout = QHBoxLayout()
        total_label = QLabel('总数:')
        self.total_input = QSpinBox()
        self.total_input.setMinimum(0)
        self.total_input.setMaximum(9999)
        if self.device_data:
            self.total_input.setValue(self.device_data['total_qty'])
        total_layout.addWidget(total_label)
        total_layout.addWidget(self.total_input)
        layout.addLayout(total_layout)

        # 可借数量
        available_layout = QHBoxLayout()
        available_label = QLabel('可借数量:')
        self.available_input = QSpinBox()
        self.available_input.setMinimum(0)
        self.available_input.setMaximum(9999)
        if self.device_data:
            self.available_input.setValue(self.device_data['available_qty'])
        available_layout.addWidget(available_label)
        available_layout.addWidget(self.available_input)
        layout.addLayout(available_layout)

        # 状态
        status_layout = QHBoxLayout()
        status_label = QLabel('状态:')
        self.status_input = QComboBox()
        self.status_input.addItems(['可用', '维修中'])
        if self.device_data:
            self.status_input.setCurrentText(self.device_data['status'])
        status_layout.addWidget(status_label)
        status_layout.addWidget(self.status_input)
        layout.addLayout(status_layout)

        # 按钮
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton('保存')
        self.cancel_btn = QPushButton('取消')
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_device_data(self):
        return {
            'name': self.name_input.text(),
            'total_qty': self.total_input.value(),
            'available_qty': self.available_input.value(),
            'status': self.status_input.currentText()
        }

class DeviceManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_devices()

    def init_ui(self):
        layout = QVBoxLayout()

        # 工具栏
        toolbar = QHBoxLayout()
        self.add_btn = QPushButton('添加设备')
        self.edit_btn = QPushButton('编辑设备')
        self.delete_btn = QPushButton('删除设备')
        self.refresh_btn = QPushButton('刷新')

        for btn in [self.add_btn, self.edit_btn, self.delete_btn, self.refresh_btn]:
            toolbar.addWidget(btn)

        toolbar.addStretch()
        layout.addLayout(toolbar)

        # 设备列表
        self.device_table = QTableWidget()
        self.device_table.setColumnCount(5)
        self.device_table.setHorizontalHeaderLabels(['ID', '设备名称', '总数', '可借数量', '状态'])
        self.device_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.device_table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.device_table)

        # 连接信号
        self.add_btn.clicked.connect(self.add_device)
        self.edit_btn.clicked.connect(self.edit_device)
        self.delete_btn.clicked.connect(self.delete_device)
        self.refresh_btn.clicked.connect(self.load_devices)

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

    def add_device(self):
        dialog = DeviceDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            device_data = dialog.get_device_data()
            db = DatabaseConnection()
            query = """
                INSERT INTO devices (name, total_qty, available_qty, status)
                VALUES (%s, %s, %s, %s)
            """
            try:
                db.execute_query(query, (
                    device_data['name'],
                    device_data['total_qty'],
                    device_data['available_qty'],
                    device_data['status']
                ))
                self.load_devices()
                QMessageBox.information(self, '成功', '设备添加成功')
            except Exception as e:
                QMessageBox.critical(self, '错误', f'设备添加失败：{str(e)}')

    def edit_device(self):
        current_row = self.device_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, '警告', '请先选择要编辑的设备')
            return

        device_id = int(self.device_table.item(current_row, 0).text())
        db = DatabaseConnection()
        device = db.execute_query("SELECT * FROM devices WHERE id = %s", (device_id,))[0]

        dialog = DeviceDialog(self, device)
        if dialog.exec_() == QDialog.Accepted:
            device_data = dialog.get_device_data()
            query = """
                UPDATE devices
                SET name = %s, total_qty = %s, available_qty = %s, status = %s
                WHERE id = %s
            """
            try:
                db.execute_query(query, (
                    device_data['name'],
                    device_data['total_qty'],
                    device_data['available_qty'],
                    device_data['status'],
                    device_id
                ))
                self.load_devices()
                QMessageBox.information(self, '成功', '设备更新成功')
            except Exception as e:
                QMessageBox.critical(self, '错误', f'设备更新失败：{str(e)}')

    def delete_device(self):
        current_row = self.device_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, '警告', '请先选择要删除的设备')
            return

        device_id = int(self.device_table.item(current_row, 0).text())
        reply = QMessageBox.question(
            self, '确认', '确定要删除这个设备吗？',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            db = DatabaseConnection()
            try:
                db.execute_query("DELETE FROM devices WHERE id = %s", (device_id,))
                self.load_devices()
                QMessageBox.information(self, '成功', '设备删除成功')
            except Exception as e:
                QMessageBox.critical(self, '错误', f'设备删除失败：{str(e)}') 
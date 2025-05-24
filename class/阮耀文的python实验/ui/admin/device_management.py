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
            VALUES (?, ?, ?, ?)
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
    device = db.execute_query("SELECT * FROM devices WHERE id = ?", (device_id,))[0]

    dialog = DeviceDialog(self, device)
    if dialog.exec_() == QDialog.Accepted:
        device_data = dialog.get_device_data()
        query = """
            UPDATE devices
            SET name = ?, total_qty = ?, available_qty = ?, status = ?
            WHERE id = ?
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
            QMessageBox.information(self, '成功', '设备信息更新成功')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'设备信息更新失败：{str(e)}')

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
            db.execute_query("DELETE FROM devices WHERE id = ?", (device_id,))
            self.load_devices()
            QMessageBox.information(self, '成功', '设备删除成功')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'设备删除失败：{str(e)}') 
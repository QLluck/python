#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
用户信息编辑窗口实现
"""

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from utils import db, info, error, exception, get_ui_path, set_app_icon, HashUtils
from typing import Optional, Dict, Any

class UserInformationWindow(QtWidgets.QWidget):
    """用户信息编辑窗口类"""
    
    def __init__(self, user_info: Dict[str, Any], parent=None, edit_user_id: Optional[int] = None):
        """初始化用户信息编辑窗口
        
        Args:
            user_info: 当前登录用户信息字典
            parent: 父窗口实例
            edit_user_id: 要编辑的用户ID，如果为None则表示添加新用户
        """
        super().__init__()
        self.user_info = user_info
        self.edit_user_id = edit_user_id
        self.parent = parent
        
        # 加载UI
        ui_path = get_ui_path("menu/user_information.ui")
        uic.loadUi(ui_path, self)
        set_app_icon(self)
        
        # 设置窗口标题
        self.setWindowTitle("编辑用户信息" if edit_user_id else "添加用户")
        self.title_label.setText("编辑用户信息" if edit_user_id else "添加用户")
        
        # 设置按钮样式
        self.pushButton.setStyleSheet("""
            QPushButton {
                background-color: #f5f5f5;
                border: none;
                border-radius: 4px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #eeeeee;
            }
        """)
        self.pushButton_2.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        
        # 连接信号
        self.pushButton.clicked.connect(self.close)  # 返回按钮
        self.pushButton_2.clicked.connect(self.save)  # 保存按钮
        
        # 根据角色设置权限
        self.setup_permissions()
        
        # 如果是编辑模式，加载用户信息
        if edit_user_id:
            self.load_user_info()
            
        info(f"用户:{user_info['username']} 打开{'编辑' if edit_user_id else '添加'}用户窗口")
        
    def setup_permissions(self):
        """根据用户角色设置界面权限"""
        # 如果不是管理员，禁用权限选择
        if self.user_info['role'] != 'admin':
            self.comboBox.setEnabled(False)
            # 如果是编辑自己的信息，禁用用户名输入
            if self.edit_user_id == self.user_info['id']:
                self.lineEdit_2.setEnabled(False)  # 用户名
                
        # 设置权限选择框的值
        self.comboBox.setCurrentText('请选择权限')
        
    def load_user_info(self):
        """加载用户信息"""
        try:
            with db.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT username, real_name, role, student_id 
                    FROM users 
                    WHERE id = ?
                """, (self.edit_user_id,))
                result = cursor.fetchone()
                
                if result:
                    username, real_name, role, student_id = result
                    # 设置用户信息
                    self.lineEdit_2.setText(username)  # 用户名
                    self.lineEdit.setText(real_name if real_name else '')   # 真实姓名
                    self.comboBox.setCurrentText({    # 权限
                        'student': '学生',
                        'teacher': '教师',
                        'admin': '管理员'
                    }.get(role, '请选择权限'))
                    self.lineEdit_5.setText(student_id if student_id else '')  # 学号
                    
                    # 如果是编辑个人信息，密码框显示占位符
                    if self.edit_user_id == self.user_info['id']:
                        self.lineEdit_3.setPlaceholderText("不修改请留空")
                else:
                    error("未找到用户信息")
                    QMessageBox.warning(self, "错误", "未找到用户信息")
                    self.close()
                    
        except Exception as e:
            error(f"加载用户信息失败: {str(e)}")
            exception(f"加载用户信息失败: {str(e)}")
            QMessageBox.warning(self, "错误", "加载用户信息失败")
            self.close()
            
    def save(self):
        """保存用户信息"""
        try:
            # 获取输入值
            username = self.lineEdit_2.text().strip()
            password = self.lineEdit_3.text()
            real_name = self.lineEdit.text().strip()
            role = {
                '学生': 'student',
                '教师': 'teacher',
                '管理员': 'admin'
            }.get(self.comboBox.currentText())
            student_id = self.lineEdit_5.text().strip()
            
            # 验证输入
            if not username:
                QMessageBox.warning(self, "错误", "请输入用户名")
                return
                
            if not self.edit_user_id and not password:
                QMessageBox.warning(self, "错误", "请输入密码")
                return
                
            if not real_name:
                QMessageBox.warning(self, "错误", "请输入真实姓名")
                return
                
            if not role:
                QMessageBox.warning(self, "错误", "请选择用户权限")
                return
                
       
                
            # 如果不是学生，清空学号
            if role != 'student':
                student_id = None
                
            # 如果是编辑模式且没有输入新密码，保持原密码不变
            if self.edit_user_id and not password:
                with db.get_connection() as conn:
                    # 如果是教师转学生，需要处理其学生的teacher_id
                    if role == 'student':
                        cursor = conn.execute("SELECT role FROM users WHERE id = ?", (self.edit_user_id,))
                        current_role = cursor.fetchone()[0]
                        if current_role == 'teacher':
                            # 将该教师的所有学生的teacher_id设置为NULL
                            cursor.execute("UPDATE users SET teacher_id = NULL WHERE teacher_id = ?", (self.edit_user_id,))
                        
                        # 设置学生的teacher_id
                        cursor.execute("UPDATE users SET teacher_id = ? WHERE id = ?", (self.user_info['id'], self.edit_user_id))
                    
                    cursor = conn.execute("""
                        UPDATE users 
                        SET username = ?, real_name = ?, role = ?, student_id = ?
                        WHERE id = ?
                    """, (username, real_name, role, student_id, self.edit_user_id))
                    conn.commit()
            else:
                # 如果是新用户或修改了密码，需要加密密码
                password_hash = HashUtils.hash_string(password)
                
                if self.edit_user_id:
                    # 更新用户
                    with db.get_connection() as conn:
                        # 如果是教师转学生，需要处理其学生的teacher_id
                        if role == 'student':
                            cursor = conn.execute("SELECT role FROM users WHERE id = ?", (self.edit_user_id,))
                            current_role = cursor.fetchone()[0]
                            if current_role == 'teacher':
                                # 将该教师的所有学生的teacher_id设置为NULL
                                cursor.execute("UPDATE users SET teacher_id = NULL WHERE teacher_id = ?", (self.edit_user_id,))
                            
                            # 设置学生的teacher_id
                            cursor.execute("UPDATE users SET teacher_id = ? WHERE id = ?", (self.user_info['id'], self.edit_user_id))
                        
                        cursor = conn.execute("""
                            UPDATE users 
                            SET username = ?, password = ?, real_name = ?, role = ?, student_id = ?
                            WHERE id = ?
                        """, (username, password_hash, real_name, role, student_id, self.edit_user_id))
                        conn.commit()
                else:
                    # 添加新用户
                    with db.get_connection() as conn:
                        # 如果是学生，设置teacher_id
                        teacher_id = self.user_info['id'] if role == 'student' else None
                        
                        cursor = conn.execute("""
                            INSERT INTO users (username, password, role, real_name, student_id, teacher_id)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (username, password_hash, role, real_name, student_id, teacher_id))
                        conn.commit()
            
            QMessageBox.information(self, "成功", "保存成功")
            
            # 如果父窗口存在，刷新其用户列表
            if self.parent and hasattr(self.parent, 'load_users'):
                self.parent.load_users()
                
            # 关闭窗口
            self.close()
            
        except Exception as e:
            error(f"保存用户信息失败: {str(e)}")
            exception(f"保存用户信息失败: {str(e)}")
            QMessageBox.warning(self, "错误", "保存用户信息失败") 
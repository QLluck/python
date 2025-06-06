#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
创建/编辑实验窗口实现
"""

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from utils import db, info, error, exception, get_ui_path, set_app_icon, debug

class CreateExperimentWindow(QtWidgets.QWidget):
    """创建/编辑实验窗口类"""
    
    def __init__(self, user_info, parent=None, experiment_id=None):
        """初始化创建/编辑实验窗口
        
        Args:
            user_info: 用户信息字典
            parent: 父窗口实例
            experiment_id: 实验ID，如果是编辑模式则不为None
        """
        super().__init__()
        self.user_info = user_info
        self.parent = parent
        self.experiment_id = experiment_id
        self.is_edit = experiment_id is not None
        
        # 加载UI
        ui_path = get_ui_path("menu/create_experiment.ui")
        uic.loadUi(ui_path, self)
        set_app_icon(self)
        
        # 设置窗口标题和按钮文本
        self.setWindowTitle("编辑实验" if self.is_edit else "创建新实验")
        self.pushButton_2.setText("保存" if self.is_edit else "创建")
        
        # 如果是编辑模式，加载实验信息
        if self.is_edit:
            self.load_experiment_info()
        
        # 连接信号
        self.pushButton.clicked.connect(self.close)  # 返回按钮
        self.pushButton_2.clicked.connect(self.save_experiment)  # 保存按钮
        
        info(f"{'编辑' if self.is_edit else '创建'}实验窗口初始化完毕")
        
    def load_experiment_info(self):
        """加载实验信息"""
        try:
            with db.get_connection() as conn:
                # 管理员可以编辑任何实验，其他角色只能编辑自己的实验
                if self.user_info['role'] == 'admin':
                    cursor = conn.execute("""
                        SELECT title, description 
                        FROM experiments 
                        WHERE id = ?
                    """, (self.experiment_id,))
                else:
                    cursor = conn.execute("""
                        SELECT title, description 
                        FROM experiments 
                        WHERE id = ? AND creator_id = ?
                    """, (self.experiment_id, self.user_info['id']))
                    
                result = cursor.fetchone()
                
                if result:
                    title, description = result
                    self.lineEdit.setText(title)
                    self.textEdit.setText(description)
                else:
                    error("未找到实验信息或无权限编辑")
                    QMessageBox.warning(self, "错误", "未找到实验信息或无权限编辑")
                    self.close()
                    
        except Exception as e:
            error(f"加载实验信息失败: {str(e)}")
            exception(f"加载实验信息失败: {str(e)}")
            QMessageBox.warning(self, "错误", "加载实验信息失败")
            self.close()
            
    def save_experiment(self):
        """保存实验"""
        # 获取输入
        title = self.lineEdit.text().strip()
        description = self.textEdit.toPlainText().strip()
        
        # 验证输入
        if not title:
            QMessageBox.warning(self, "错误", "请输入实验主题")
            return
            
        if not description:
            QMessageBox.warning(self, "错误", "请输入实验描述")
            return
            
        try:
            with db.get_connection() as conn:
                if self.is_edit:
                    # 更新实验
                    if self.user_info['role'] == 'admin':
                        # 管理员可以编辑任何实验
                        cursor = conn.execute("""
                            UPDATE experiments 
                            SET title = ?, description = ?
                            WHERE id = ?
                        """, (title, description, self.experiment_id))
                    else:
                        # 其他角色只能编辑自己的实验
                        cursor = conn.execute("""
                            UPDATE experiments 
                            SET title = ?, description = ?
                            WHERE id = ? AND creator_id = ?
                        """, (title, description, self.experiment_id, self.user_info['id']))
                    
                    if cursor.rowcount == 0:
                        QMessageBox.warning(self, "错误", "未找到实验或无权限编辑")
                        return
                        
                    info(f"用户:{self.user_info['username']} 更新实验 {self.experiment_id}")
                    QMessageBox.information(self, "成功", "实验更新成功")
                else:
                    # 创建新实验
                    cursor = conn.execute("""
                        INSERT INTO experiments (title, description, creator_id, create_time)
                        VALUES (?, ?, ?, datetime('now', 'localtime'))
                    """, (title, description, self.user_info['id']))
                    
                    info(f"用户:{self.user_info['username']} 创建新实验 {cursor.lastrowid}")
                    QMessageBox.information(self, "成功", "实验创建成功")
                    
                conn.commit()
            
            # 刷新父窗口的实验列表
            if self.parent and hasattr(self.parent, 'load_all_experiments'):
                self.parent.load_all_experiments()
                
            # 关闭窗口
            self.close()
            
        except Exception as e:
            error(f"{'更新' if self.is_edit else '创建'}实验失败: {str(e)}")
            exception(f"{'更新' if self.is_edit else '创建'}实验失败: {str(e)}")
            QMessageBox.warning(self, "错误", f"{'更新' if self.is_edit else '创建'}实验失败") 
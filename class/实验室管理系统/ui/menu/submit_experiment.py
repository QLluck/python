#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
实验提交窗口实现
"""

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from utils import db, info, debug, warning, error, get_ui_path, exception, set_app_icon
from datetime import datetime

class SubmitExperimentWindow(QtWidgets.QWidget):
    """实验提交窗口类"""
    
    def __init__(self, user_info, experiment_id, parent=None, is_edit=False):
        """初始化实验提交窗口
        
        Args:
            user_info: 用户信息字典
            experiment_id: 实验ID
            parent: 父窗口实例
            is_edit: 是否是编辑模式
        """
        info(f"初始化实验提交窗口")
        super().__init__()
        
        # 保存参数
        self.user_info = user_info
        self.experiment_id = experiment_id
        self.parent = parent
        self.is_edit = is_edit
        
        # 加载UI
        ui_path = get_ui_path("menu/submit_experiment.ui")
        debug(ui_path)
        uic.loadUi(ui_path, self)
        set_app_icon(self)
        
        # 修改窗口标题和标签
        self.setWindowTitle("编辑实验" if is_edit else "提交实验")
        self.title_label.setText("编辑实验报告" if is_edit else "提交实验报告")
        self.label.setText("实验标题")
        self.label_2.setText("实验报告")
        self.pushButton_2.setText("保存" if is_edit else "提交")
        
        # 加载实验信息
        self.load_experiment_info()
        
        # 设置信号连接
        self.setup_connections()
        
    def load_experiment_info(self):
        """加载实验信息"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                if self.is_edit:
                    # 获取实验信息和提交内容
                    cursor.execute("""
                        SELECT e.title, e.description, s.content
                        FROM experiments e
                        JOIN submissions s ON e.id = s.experiment_id
                        WHERE e.id = ? AND s.student_id = ?
                    """, (self.experiment_id, self.user_info['id']))
                    result = cursor.fetchone()
                    
                    if result:
                        title, description, content = result
                        # 设置实验标题（只读）
                        self.lineEdit.setText(title)
                        self.lineEdit.setReadOnly(True)
                        # 设置实验描述为placeholder
                        self.textEdit.setPlaceholderText(
                            f"实验要求：\n{description}"
                        )
                        # 设置已提交的内容
                        self.textEdit.setText(content)
                    else:
                        error("未找到实验提交记录")
                        QMessageBox.warning(self, "错误", "未找到实验提交记录")
                        self.close()
                else:
                    # 获取实验信息
                    cursor.execute("""
                        SELECT title, description 
                        FROM experiments 
                        WHERE id = ?
                    """, (self.experiment_id,))
                    result = cursor.fetchone()
                    
                    if result:
                        title, description = result
                        # 设置实验标题（只读）
                        self.lineEdit.setText(title)
                        self.lineEdit.setReadOnly(True)
                        # 设置实验描述为placeholder
                        self.textEdit.setPlaceholderText(
                            "请在此输入实验报告内容...\n\n"
                            f"实验要求：\n{description}"
                        )
                    else:
                        error("未找到实验信息")
                        QMessageBox.warning(self, "错误", "未找到实验信息")
                        self.close()
                    
        except Exception as e:
            error(f"加载实验信息失败: {str(e)}")
            exception(f"加载实验信息失败: {str(e)}")
            QMessageBox.warning(self, "错误", "加载实验信息失败")
            self.close()
            
    def setup_connections(self):
        """设置信号连接"""
        self.pushButton.clicked.connect(self.close)  # 返回按钮
        self.pushButton_2.clicked.connect(self.submit_experiment)  # 提交按钮
        
    def submit_experiment(self):
        """提交实验"""
        # 获取实验报告内容
        report = self.textEdit.toPlainText().strip()
        
        # 验证输入
        if not report:
            QMessageBox.warning(self, "提示", "请输入实验报告内容")
            return
            
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                if self.is_edit:
                    # 更新提交记录
                    cursor.execute("""
                        UPDATE submissions 
                        SET content = ?, 
                            submit_time = ?,
                            score = NULL,
                            comment = NULL
                        WHERE experiment_id = ? AND student_id = ?
                    """, (
                        report,
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        self.experiment_id,
                        self.user_info['id']
                    ))
                    
                    if cursor.rowcount > 0:
                        conn.commit()
                        QMessageBox.information(self, "成功", "实验报告已更新！")
                    else:
                        QMessageBox.warning(self, "错误", "未找到要更新的提交记录")
                        return
                else:
                    # 检查是否已提交过
                    cursor.execute("""
                        SELECT id FROM submissions 
                        WHERE experiment_id = ? AND student_id = ?
                    """, (self.experiment_id, self.user_info['id']))
                    
                    if cursor.fetchone():
                        QMessageBox.warning(self, "提示", "您已经提交过此实验")
                        return
                    
                    # 插入提交记录
                    cursor.execute("""
                        INSERT INTO submissions (
                            experiment_id, student_id, content, 
                            submit_time, score, comment
                        ) VALUES (?, ?, ?, ?, NULL, NULL)
                    """, (
                        self.experiment_id,
                        self.user_info['id'],
                        report,
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    ))
                    
                    conn.commit()
                    QMessageBox.information(self, "成功", "实验提交成功！")
                
                # 刷新父窗口的实验列表
                if self.parent:
                    self.parent.load_experiments()
                
                # 关闭提交窗口
                self.close()
                
        except Exception as e:
            error(f"{'更新' if self.is_edit else '提交'}实验失败: {str(e)}")
            exception(f"{'更新' if self.is_edit else '提交'}实验失败: {str(e)}")
            QMessageBox.warning(self, "错误", f"{'更新' if self.is_edit else '提交'}实验失败") 
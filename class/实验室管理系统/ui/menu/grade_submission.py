#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
批改实验窗口实现
"""

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from utils import db, info, error, exception, get_ui_path, set_app_icon

class GradeSubmissionWindow(QtWidgets.QWidget):
    """批改实验窗口类"""
    
    def __init__(self, user_info, experiment_id, parent=None):
        """初始化批改实验窗口
        
        Args:
            user_info: 用户信息字典
            experiment_id: 实验ID
            parent: 父窗口实例
        """
        super().__init__()
        self.user_info = user_info
        self.experiment_id = experiment_id
        self.parent = parent
        
        # 加载UI
        ui_path = get_ui_path("menu/grade_submission.ui")
        uic.loadUi(ui_path, self)
        set_app_icon(self)
        
        # 设置窗口标题
        self.setWindowTitle("批改实验")
        
        # 加载实验信息
        self.load_submission_info()
        
        # 连接信号
        self.pushButton.clicked.connect(self.close)  # 返回按钮
        self.pushButton_2.clicked.connect(self.save_grade)  # 提交按钮
        
        info(f"用户:{user_info['username']} 打开批改实验窗口，实验ID:{experiment_id}")
        
    def load_submission_info(self):
        """加载提交信息"""
        try:
            with db.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT 
                        e.title, e.description, s.content,
                        s.score, s.comment, u.real_name
                    FROM experiments e
                    JOIN submissions s ON e.id = s.experiment_id
                    JOIN users u ON s.student_id = u.id
                    WHERE e.id = ?
                """, (self.experiment_id,))
                result = cursor.fetchone()
                
                if result:
                    title, description, content, score, comment, student_name = result
                    # 设置实验标题
                    self.lineEdit.setText(f"{title} - {student_name}")
                    self.lineEdit.setReadOnly(True)
                    
                    # 设置实验内容
                    self.textEdit.setText(content)
                    self.textEdit.setReadOnly(True)
                    
                    # 如果已有评分，显示现有评分
                    if score is not None:
                        self.lineEdit_2.setText(str(score))
                    if comment:
                        self.textEdit_2.setText(comment)
                else:
                    error("未找到提交记录")
                    QMessageBox.warning(self, "错误", "未找到提交记录")
                    self.close()
                    
        except Exception as e:
            error(f"加载提交信息失败: {str(e)}")
            exception(f"加载提交信息失败: {str(e)}")
            QMessageBox.warning(self, "错误", "加载提交信息失败")
            self.close()
            
    def save_grade(self):
        """保存评分"""
        # 获取输入
        score = self.lineEdit_2.text().strip()
        comment = self.textEdit_2.toPlainText().strip()
        
        # 验证输入
        if not score:
            QMessageBox.warning(self, "错误", "请输入分数")
            return
            
        try:
            score = float(score)
            if score < 0 or score > 100:
                QMessageBox.warning(self, "错误", "分数必须在0-100之间")
                return
        except ValueError:
            QMessageBox.warning(self, "错误", "分数必须是数字")
            return
            
        if not comment:
            QMessageBox.warning(self, "错误", "请输入评语")
            return
            
        try:
            with db.get_connection() as conn:
                cursor = conn.execute("""
                    UPDATE submissions 
                    SET score = ?, comment = ?
                    WHERE experiment_id = ?
                """, (score, comment, self.experiment_id))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    info(f"用户:{self.user_info['username']} 完成实验批改，实验ID:{self.experiment_id}")
                    QMessageBox.information(self, "成功", "批改已保存")
                    
                    # 刷新父窗口的实验列表
                    if self.parent and hasattr(self.parent, 'load_experiments'):
                        self.parent.load_experiments()
                        
                    # 关闭窗口
                    self.close()
                else:
                    QMessageBox.warning(self, "错误", "未找到要批改的提交记录")
                    
        except Exception as e:
            error(f"保存批改结果失败: {str(e)}")
            exception(f"保存批改结果失败: {str(e)}")
            QMessageBox.warning(self, "错误", "保存批改结果失败") 
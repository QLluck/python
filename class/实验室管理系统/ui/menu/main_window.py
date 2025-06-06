#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
主窗口实现
包含用户界面和业务逻辑
"""

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from utils import db, info, debug, warning, error, HashUtils, get_ui_path,exception,set_app_icon
import os
from typing import Optional, Dict, Any

class MainWindow(QtWidgets.QWidget):
    """主窗口类"""
    
    def __init__(self, user_info: Dict[str, Any], login_window=None):
        """初始化主窗口
        
        Args:
            user_info: 用户信息字典，包含用户ID、用户名、角色等
            login_window: 登录窗口实例，用于退出登录时返回
        """
        info(f"初始化主窗口")
        info(f"用户信息：{user_info}")
        super().__init__()
        
        # 保存登录窗口实例
        self.login_window = login_window
        
        # 保存子窗口实例
        self.create_experiment_window = None
        
        # 加载UI文件
        ui_path = get_ui_path("menu/main_window.ui")
        uic.loadUi(ui_path, self)
        set_app_icon(self)
        # 保存用户信息
        self.user_info = user_info
        self.role = user_info.get('role', '')
        
        # 初始化界面
        self.init_ui()
        self.setup_connections()
        self.load_user_info()
        
        # 根据角色设置权限
        self.setup_permissions()
        
        info(f"主窗口初始化完成，用户角色: {self.role}")
        
    def init_ui(self):
        """初始化界面元素"""
        # 设置窗口标题
        info(f"初始化界面元素")
        self.setWindowTitle(f"实验室管理系统 - {self.role}")
        self.label.setText(f"{self.user_info['role']}: {self.user_info['username']}")
        
        # 隐藏所有页面
        self.stackedWidget.setCurrentIndex(0)
        
    def setup_connections(self):
        """设置信号和槽的连接"""
        # 左侧菜单按钮连接
        info(f"设置信号和槽的连接")
        self.pushButton.clicked.connect(self.logout)  # 退出登录
        self.pushButton_2.clicked.connect(self.close)  # 离开系统
        self.pushButton_3.clicked.connect(lambda: self.show_page(1))  # 查看实验
        self.pushButton_4.clicked.connect(lambda: self.show_page(2))  # 实验管理
        self.pushButton_5.clicked.connect(lambda: self.show_page(3))  # 用户管理
        self.pushButton_6.clicked.connect(lambda: self.show_page(0))  # 个人信息
        
        # 搜索按钮连接
        self.search_unfinished_btn.clicked.connect(lambda: self.filter_experiments(False))  # 未完成实验搜索
        self.search_finished_btn.clicked.connect(lambda: self.filter_experiments(True))     # 已完成实验搜索
        self.search_all_exp_btn.clicked.connect(self.filter_all_experiments)  # 实验室实验搜索
        self.search_users_btn.clicked.connect(self.filter_users)  # 用户搜索
        
        # 添加按钮连接
        self.pushButton_14.clicked.connect(self.add_experiment)  # 添加实验
        self.pushButton_17.clicked.connect(self.add_user)  # 添加用户
        
        # 修改个人信息按钮连接
        self.pushButton_7.clicked.connect(self.edit_profile)
        
    def setup_permissions(self):
        """根据用户角色设置界面权限"""
        # 隐藏所有管理按钮
        info(f"设置界面权限")
        self.pushButton_4.hide()  # 实验管理
        self.pushButton_5.hide()  # 用户管理
        
        if self.role == 'student':
            # 学生可以查看实验
            pass
        elif self.role == 'teacher':
            # 教师可以管理实验和查看学生
            self.pushButton_4.show()
            self.pushButton_5.show()
        elif self.role == 'admin':
            # 管理员可以管理实验和用户
            self.pushButton_4.show()
            self.pushButton_5.show()
            
    def load_user_info(self):
        """加载并显示用户信息"""
        info(f"加载用户信息")
        try:
            # 获取用户详细信息
            user=self.user_info

            if not user:
                raise ValueError("用户信息不存在")
                
            # 显示用户信息
            self.textEdit_7.setText(user['username'])  # 账号
            self.textEdit_8.setText(user['real_name'])  # 姓名
            self.textEdit_9.setText(user['role'])  # 身份
            self.textEdit_10.setText('*' * 8)  # 密码（隐藏）
            self.textEdit_11.setText(str(user['id']))  # ID
            self.textEdit_12.setText(user['role'])  # 权限
            
        except Exception as e:
            error(f"加载用户信息失败: {str(e)}")
            exception(f"加载用户信息失败: {str(e)}")
            QMessageBox.warning(self, "错误", "加载用户信息失败")
            
    def show_page(self, index: int):
        """显示指定页面
        
        Args:
            index: 页面索引
        """
        self.stackedWidget.setCurrentIndex(index)
        
        # 加载页面数据
        if index == 1:  # 查看实验页面
            self.load_experiments()
        elif index == 2:  # 实验管理页面
            self.load_all_experiments()
        elif index == 3:  # 用户管理页面
            self.load_users()
            
    def load_experiments(self):
        """加载实验列表"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                if self.role == 'student':
                    # 首先获取学生的teacher_id
                    cursor.execute("""
                        SELECT teacher_id FROM users 
                        WHERE id = ? AND role = 'student'
                    """, (self.user_info['id'],))
                    result = cursor.fetchone()
                    if not result or not result[0]:
                        # 如果学生没有指导教师，显示空列表
                        unfinished = []
                        finished = []
                    else:
                        teacher_id = result[0]
                        # 加载未完成实验（只显示指导教师发布的实验）
                        cursor.execute("""
                            SELECT 
                                e.id, e.creator_id, e.title, e.description, e.create_time,
                                NULL as student_id, NULL as score, NULL as comment,
                                NULL as student_name,
                                (SELECT COUNT(DISTINCT s2.student_id) 
                                 FROM submissions s2 
                                 WHERE s2.experiment_id = e.id) as submit_count,
                                (SELECT COUNT(*) 
                                 FROM users 
                                 WHERE teacher_id = e.creator_id 
                                 AND role = 'student') as total_students
                            FROM experiments e
                            LEFT JOIN submissions s ON e.id = s.experiment_id AND s.student_id = ?
                            WHERE s.id IS NULL 
                            AND e.creator_id = ?
                            ORDER BY e.create_time DESC
                        """, (self.user_info['id'], teacher_id))
                        unfinished = cursor.fetchall()
                        
                        # 加载已完成实验
                        cursor.execute("""
                            SELECT 
                                e.id, e.creator_id, e.title, e.description, e.create_time,
                                s.student_id, s.score, s.comment,
                                NULL as student_name,
                                (SELECT COUNT(DISTINCT s2.student_id) 
                                 FROM submissions s2 
                                 WHERE s2.experiment_id = e.id) as submit_count,
                                (SELECT COUNT(*) 
                                 FROM users 
                                 WHERE teacher_id = e.creator_id 
                                 AND role = 'student') as total_students
                            FROM experiments e
                            JOIN submissions s ON e.id = s.experiment_id
                            WHERE s.student_id = ?
                            ORDER BY e.create_time DESC
                        """, (self.user_info['id'],))
                        finished = cursor.fetchall()
                
                elif self.role == 'teacher':
                    # 教师查看待批改和已批改的实验
                    # 未批改的实验（score IS NULL）
                    cursor.execute("""
                        SELECT 
                            e.id, e.creator_id, e.title, e.description, e.create_time,
                            s.student_id, s.score, s.comment,
                            u.real_name as student_name,
                            (SELECT COUNT(DISTINCT s2.student_id) 
                             FROM submissions s2 
                             WHERE s2.experiment_id = e.id) as submit_count,
                            (SELECT COUNT(*) 
                             FROM users 
                             WHERE teacher_id = e.creator_id 
                             AND role = 'student') as total_students
                        FROM experiments e
                        JOIN submissions s ON e.id = s.experiment_id
                        JOIN users u ON s.student_id = u.id
                        WHERE e.creator_id = ? 
                        AND s.score IS NULL
                        ORDER BY s.submit_time DESC
                    """, (self.user_info['id'],))
                    unfinished = cursor.fetchall()
                    
                    # 已批改的实验
                    cursor.execute("""
                        SELECT 
                            e.id, e.creator_id, e.title, e.description, e.create_time,
                            s.student_id, s.score, s.comment,
                            u.real_name as student_name,
                            (SELECT COUNT(DISTINCT s2.student_id) 
                             FROM submissions s2 
                             WHERE s2.experiment_id = e.id) as submit_count,
                            (SELECT COUNT(*) 
                             FROM users 
                             WHERE teacher_id = e.creator_id 
                             AND role = 'student') as total_students
                        FROM experiments e
                        JOIN submissions s ON e.id = s.experiment_id
                        JOIN users u ON s.student_id = u.id
                        WHERE e.creator_id = ? 
                        AND s.score IS NOT NULL
                        ORDER BY s.submit_time DESC
                    """, (self.user_info['id'],))
                    finished = cursor.fetchall()
                    
                else:  # admin
                    # 管理员查看所有待批改和已批改的实验
                    # 未批改的实验
                    cursor.execute("""
                        SELECT 
                            e.id, e.creator_id, e.title, e.description, e.create_time,
                            s.student_id, s.score, s.comment,
                            u.real_name as student_name,
                            (SELECT real_name FROM users WHERE id = e.creator_id) as teacher_name,
                            (SELECT COUNT(DISTINCT s2.student_id) 
                             FROM submissions s2 
                             WHERE s2.experiment_id = e.id) as submit_count,
                            (SELECT COUNT(*) 
                             FROM users 
                             WHERE teacher_id = e.creator_id 
                             AND role = 'student') as total_students
                        FROM experiments e
                        JOIN submissions s ON e.id = s.experiment_id
                        JOIN users u ON s.student_id = u.id
                        WHERE s.score IS NULL
                        ORDER BY s.submit_time DESC
                    """)
                    unfinished = cursor.fetchall()
                    
                    # 已批改的实验
                    cursor.execute("""
                        SELECT 
                            e.id, e.creator_id, e.title, e.description, e.create_time,
                            s.student_id, s.score, s.comment,
                            u.real_name as student_name,
                            (SELECT real_name FROM users WHERE id = e.creator_id) as teacher_name,
                            (SELECT COUNT(DISTINCT s2.student_id) 
                             FROM submissions s2 
                             WHERE s2.experiment_id = e.id) as submit_count,
                            (SELECT COUNT(*) 
                             FROM users 
                             WHERE teacher_id = e.creator_id 
                             AND role = 'student') as total_students
                        FROM experiments e
                        JOIN submissions s ON e.id = s.experiment_id
                        JOIN users u ON s.student_id = u.id
                        WHERE s.score IS NOT NULL
                        ORDER BY s.submit_time DESC
                    """)
                    finished = cursor.fetchall()
            
            debug(unfinished)
            debug(finished)
            # 显示实验列表
            self.display_experiments(unfinished, self.verticalLayout_2, False)
            self.display_experiments(finished, self.verticalLayout_10, True)
            
        except Exception as e:
            error(f"加载实验列表失败: {str(e)}")
            exception(f"加载实验列表失败: {str(e)}")
            QMessageBox.warning(self, "错误", "加载实验列表失败")
            
    def load_all_experiments(self):
        """加载所有实验列表"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                if self.role == 'teacher':
                    # 教师查看自己创建的实验和学生提交情况
                    cursor.execute("""
                        SELECT 
                            e.id, e.creator_id, e.title, e.description, e.create_time,
                            NULL as student_id, NULL as score, NULL as comment,
                            NULL as student_name,
                            (SELECT COUNT(DISTINCT s.student_id) 
                             FROM submissions s 
                             WHERE s.experiment_id = e.id) as submit_count,
                            (SELECT COUNT(*) 
                             FROM users 
                             WHERE teacher_id = ? 
                             AND role = 'student') as total_students
                        FROM experiments e
                        WHERE e.creator_id = ?
                        ORDER BY e.create_time DESC
                    """, (self.user_info['id'], self.user_info['id']))
                else:
                    # 管理员可以看到所有实验
                    cursor.execute("""
                        SELECT 
                            e.id, e.creator_id, e.title, e.description, e.create_time,
                            NULL as student_id, NULL as score, NULL as comment,
                            NULL as student_name,
                            (SELECT real_name FROM users WHERE id = e.creator_id) as teacher_name,
                            (SELECT COUNT(DISTINCT s.student_id) 
                             FROM submissions s 
                             WHERE s.experiment_id = e.id) as submit_count,
                            (SELECT COUNT(*) 
                             FROM users 
                             WHERE teacher_id = e.creator_id 
                             AND role = 'student') as total_students
                        FROM experiments e
                        ORDER BY e.create_time DESC
                    """)
                    
                experiments = cursor.fetchall()
            
            # 显示实验列表
            self.display_experiments(experiments, self.verticalLayout_11, False)
            
        except Exception as e:
            error(f"加载实验列表失败: {str(e)}")
            exception(f"加载实验列表失败: {str(e)}")
            QMessageBox.warning(self, "错误", "加载实验列表失败")
            
    def load_users(self):
        """加载用户列表"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                if self.role == 'teacher':
                    # 教师可以看到所有学生，并标记是否是自己的学生
                    cursor.execute("""
                        SELECT u.*, CASE WHEN u.teacher_id = ? THEN 1 ELSE 0 END as is_my_student 
                        FROM users u 
                        WHERE u.role = 'student'
                        ORDER BY is_my_student DESC, u.create_time DESC
                    """, (self.user_info['id'],))
                else:
                    # 管理员可以看到所有用户
                    cursor.execute("SELECT * FROM users")
                    
                users = cursor.fetchall()
            
            # 显示用户列表
            self.display_users(users)
            
        except Exception as e:
            error(f"加载用户列表失败: {str(e)}")
            exception(f"加载用户列表失败: {str(e)}")
            QMessageBox.warning(self, "错误", "加载用户列表失败")
            
    def display_experiments(self, experiments, layout, is_finished: bool = False):
        """显示实验列表
        
        Args:
            experiments: 实验信息列表
            layout: 要显示到的布局
            is_finished: 是否是已完成/已批改实验
        """
        # 清空现有内容
        self.clear_layout(layout)
        
        # 添加顶部间距
        spacer_top = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        layout.addItem(spacer_top)
        
        for exp in experiments:
            # 创建实验信息框
            frame = QtWidgets.QFrame()
            frame.setFrameShape(QtWidgets.QFrame.Box)
            frame.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            frame.setMinimumHeight(90)  # 增加最小高度
            frame.setMaximumHeight(120)  # 增加最大高度
            frame.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border: 1px solid #dddddd;
                    border-radius: 6px;
                }
            """)
            
            # 创建布局
            v_layout = QtWidgets.QVBoxLayout(frame)
            v_layout.setContentsMargins(15, 12, 15, 12)  # 增加内边距
            v_layout.setSpacing(6)  # 增加垂直间距
            
            # 创建水平布局用于标题和按钮
            h_layout = QtWidgets.QHBoxLayout()
            h_layout.setSpacing(10)  # 增加水平间距
            
            # 左侧信息部分
            info_layout = QtWidgets.QVBoxLayout()
            info_layout.setSpacing(4)  # 增加信息间距
            
            # 第一行：标题和状态
            title_layout = QtWidgets.QHBoxLayout()
            title_layout.setSpacing(10)
            
            # 实验标题（限制长度）
            title = exp[2]
            if len(title) > 30:  # 限制标题长度
                title = title[:30] + "..."
            title_label = QtWidgets.QLabel(f"实验: {title}")
            title_label.setStyleSheet("""
                font-size: 14px;
                font-weight: bold;
                color: #333333;
                padding: 2px 0;
            """)
            title_layout.addWidget(title_label)
            
            # 显示提交情况
            submit_count = exp[-2] if len(exp) > 8 else 0  # 提交人数
            total_students = exp[-1] if len(exp) > 8 else 0  # 总人数
            
            # 如果是教师或管理员视图，显示学生姓名
            if self.role in ['teacher', 'admin'] and exp[8]:  # student_name
                student_info = f"提交学生: {exp[8]}"
                if exp[6] is not None:  # 如果有分数
                    student_info += f" | 分数: {exp[6]}"
                student_label = QtWidgets.QLabel(student_info)
                student_label.setStyleSheet("""
                    color: #666666;
                    font-size: 13px;
                    padding: 2px 0;
                """)
                title_layout.addWidget(student_label)
            elif self.role == 'student' and is_finished:  # 学生查看已完成实验
                score_info = f"分数: {exp[6]}" if exp[6] is not None else "未批改"
                score_label = QtWidgets.QLabel(score_info)
                score_label.setStyleSheet("""
                    color: #666666;
                    font-size: 13px;
                    padding: 2px 0;
                """)
                title_layout.addWidget(score_label)
            
            # 显示提交统计
            if total_students > 0:
                progress = f"({submit_count}/{total_students})"
                if self.role == 'admin':
                    teacher_name = exp[9]  # teacher_name
                    progress = f"教师: {teacher_name} " + progress
                
                status_label = QtWidgets.QLabel(progress)
                status_label.setStyleSheet("""
                    color: #666666;
                    font-size: 13px;
                    padding: 2px 0;
                """)
                title_layout.addWidget(status_label)
            
            title_layout.addStretch()
            info_layout.addLayout(title_layout)
            
            # 第二行：描述（限制长度）
            if exp[3]:  # 实验描述
                desc = exp[3]
                if len(desc) > 50:  # 限制描述长度
                    desc = desc[:50] + "..."
                desc_label = QtWidgets.QLabel(f"描述: {desc}")
                desc_label.setStyleSheet("""
                    color: #666666;
                    font-size: 13px;
                    padding: 2px 0;
                """)
                info_layout.addWidget(desc_label)
            
            h_layout.addLayout(info_layout, stretch=1)
            
            # 右侧按钮部分
            button_layout = QtWidgets.QHBoxLayout()
            button_layout.setSpacing(8)  # 按钮间距
            
            # 根据用户角色显示不同的按钮
            if self.role == 'student':
                if not is_finished:  # 未完成实验显示提交按钮
                    submit_btn = QtWidgets.QPushButton("提交实验")
                    submit_btn.setFixedWidth(90)  # 增加按钮宽度
                    submit_btn.setFixedHeight(30)  # 设置按钮高度
                    submit_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #4CAF50;
                            color: white;
                            border: none;
                            border-radius: 4px;
                            padding: 5px;
                            font-size: 13px;
                        }
                        QPushButton:hover {
                            background-color: #45a049;
                        }
                    """)
                    submit_btn.clicked.connect(lambda checked, eid=exp[0]: self.submit_experiment(eid))
                    button_layout.addWidget(submit_btn)
                else:  # 已完成实验
                    if exp[6] is None:  # 如果还没有评分
                        # 编辑按钮
                        edit_btn = QtWidgets.QPushButton("编辑")
                        edit_btn.setFixedWidth(70)
                        edit_btn.setFixedHeight(30)
                        edit_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #2196F3;
                                color: white;
                                border: none;
                                border-radius: 4px;
                                padding: 5px;
                                font-size: 13px;
                            }
                            QPushButton:hover {
                                background-color: #1976D2;
                            }
                        """)
                        edit_btn.clicked.connect(lambda checked, eid=exp[0]: self.edit_submission(eid))
                        button_layout.addWidget(edit_btn)
                        
                        # 删除按钮
                        delete_btn = QtWidgets.QPushButton("删除")
                        delete_btn.setFixedWidth(70)
                        delete_btn.setFixedHeight(30)
                        delete_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #F44336;
                                color: white;
                                border: none;
                                border-radius: 4px;
                                padding: 5px;
                                font-size: 13px;
                            }
                            QPushButton:hover {
                                background-color: #D32F2F;
                            }
                        """)
                        delete_btn.clicked.connect(lambda checked, eid=exp[0]: self.delete_submission(eid))
                        button_layout.addWidget(delete_btn)
                    else:  # 如果已经评分
                        # 查看按钮
                        view_btn = QtWidgets.QPushButton("查看")
                        view_btn.setFixedWidth(70)
                        view_btn.setFixedHeight(30)
                        view_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #757575;
                                color: white;
                                border: none;
                                border-radius: 4px;
                                padding: 5px;
                                font-size: 13px;
                            }
                            QPushButton:hover {
                                background-color: #616161;
                            }
                        """)
                        view_btn.clicked.connect(lambda checked, eid=exp[0]: self.view_submission(eid))
                        button_layout.addWidget(view_btn)
            else:
                # 教师和管理员的按钮
                if layout == self.verticalLayout_11:  # 实验管理页面
                    # 编辑按钮
                    edit_btn = QtWidgets.QPushButton("编辑")
                    edit_btn.setFixedWidth(70)  # 增加按钮宽度
                    edit_btn.setFixedHeight(30)  # 设置按钮高度
                    edit_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #2196F3;
                            color: white;
                            border: none;
                            border-radius: 4px;
                            padding: 5px;
                            font-size: 13px;
                        }
                        QPushButton:hover {
                            background-color: #1976D2;
                        }
                    """)
                    edit_btn.clicked.connect(lambda checked, eid=exp[0]: self.edit_experiment(eid))
                    button_layout.addWidget(edit_btn)
                    
                    # 删除按钮
                    delete_btn = QtWidgets.QPushButton("删除")
                    delete_btn.setFixedWidth(70)  # 增加按钮宽度
                    delete_btn.setFixedHeight(30)  # 设置按钮高度
                    delete_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #F44336;
                            color: white;
                            border: none;
                            border-radius: 4px;
                            padding: 5px;
                            font-size: 13px;
                        }
                        QPushButton:hover {
                            background-color: #D32F2F;
                        }
                    """)
                    delete_btn.clicked.connect(lambda checked, eid=exp[0]: self.delete_experiment(eid))
                    button_layout.addWidget(delete_btn)
                else:  # 查看实验页面（批改实验）
                    if not is_finished:  # 未批改的实验
                        # 批改按钮
                        grade_btn = QtWidgets.QPushButton("批改")
                        grade_btn.setFixedWidth(70)  # 增加按钮宽度
                        grade_btn.setFixedHeight(30)  # 设置按钮高度
                        grade_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #4CAF50;
                                color: white;
                                border: none;
                                border-radius: 4px;
                                padding: 5px;
                                font-size: 13px;
                            }
                            QPushButton:hover {
                                background-color: #45a049;
                            }
                        """)
                        grade_btn.clicked.connect(lambda checked, eid=exp[0]: self.grade_submission(eid))
                        button_layout.addWidget(grade_btn)
                        
                        # 打回按钮
                        return_btn = QtWidgets.QPushButton("打回")
                        return_btn.setFixedWidth(70)  # 增加按钮宽度
                        return_btn.setFixedHeight(30)  # 设置按钮高度
                        return_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #F44336;
                                color: white;
                                border: none;
                                border-radius: 4px;
                                padding: 5px;
                                font-size: 13px;
                            }
                            QPushButton:hover {
                                background-color: #D32F2F;
                            }
                        """)
                        return_btn.clicked.connect(lambda checked, eid=exp[0]: self.return_submission(eid))
                        button_layout.addWidget(return_btn)
                    else:  # 已批改的实验
                        # 重新批改按钮
                        regrade_btn = QtWidgets.QPushButton("重新批改")
                        regrade_btn.setFixedWidth(90)  # 增加按钮宽度
                        regrade_btn.setFixedHeight(30)  # 设置按钮高度
                        regrade_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #4CAF50;
                                color: white;
                                border: none;
                                border-radius: 4px;
                                padding: 5px;
                                font-size: 13px;
                            }
                            QPushButton:hover {
                                background-color: #45a049;
                            }
                        """)
                        regrade_btn.clicked.connect(lambda checked, eid=exp[0]: self.grade_submission(eid))
                        button_layout.addWidget(regrade_btn)
            
            h_layout.addLayout(button_layout)
            v_layout.addLayout(h_layout)
            
            layout.addWidget(frame)
            
            # 添加间隔
            spacer = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
            layout.addItem(spacer)
            
        # 添加底部间距
        spacer_bottom = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        layout.addItem(spacer_bottom)
            
    def display_users(self, users):
        """显示用户列表
        
        Args:
            users: 用户信息列表
        """
        # 清空现有内容
        self.clear_layout(self.verticalLayout_12)
        
        # 添加弹性空间到顶部
        spacer_top = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_12.addItem(spacer_top)
        
        for user in users:
            # 创建用户信息框
            frame = QtWidgets.QFrame()
            frame.setFrameShape(QtWidgets.QFrame.Box)
            frame.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            frame.setMinimumHeight(60)  # 设置最小高度
            
            # 创建布局
            v_layout = QtWidgets.QVBoxLayout(frame)
            h_layout = QtWidgets.QHBoxLayout()
            
            # 添加用户信息
            info_layout = QtWidgets.QVBoxLayout()
            
            name_label = QtWidgets.QLabel(f"用户名: {user[1]} | 姓名: {user[4]}")
            name_label.setWordWrap(True)
            info_layout.addWidget(name_label)
            
            role_label = QtWidgets.QLabel(f"角色: {user[3]}")
            role_label.setStyleSheet("color: #666666; font-size: 12px;")
            info_layout.addWidget(role_label)
            
            h_layout.addLayout(info_layout, stretch=1)
            
            # 添加按钮
            if self.role == 'admin':
                button_layout = QtWidgets.QHBoxLayout()
                
                edit_btn = QtWidgets.QPushButton("编辑")
                edit_btn.setFixedWidth(80)
                edit_btn.clicked.connect(lambda checked, uid=user[0]: self.edit_user(uid))
                button_layout.addWidget(edit_btn)
                
                delete_btn = QtWidgets.QPushButton("删除")
                delete_btn.setFixedWidth(80)
                delete_btn.clicked.connect(lambda checked, uid=user[0]: self.delete_user(uid))
                button_layout.addWidget(delete_btn)
                
                h_layout.addLayout(button_layout)
            elif self.role == 'teacher' and user[3] == 'student':  # 如果是教师且显示的是学生
                button_layout = QtWidgets.QHBoxLayout()
                
                # 判断是否是自己的学生
                is_my_student = user[-1] if len(user) > 7 else (user[5] == self.user_info['id'])
                
                if is_my_student:
                    # 如果是自己的学生，显示移除按钮
                    remove_btn = QtWidgets.QPushButton("移除学生")
                    remove_btn.setFixedWidth(120)  # 增加按钮宽度
                    remove_btn.clicked.connect(lambda checked, uid=user[0]: self.remove_student(uid))
                    button_layout.addWidget(remove_btn)
                else:
                    # 如果不是自己的学生，显示添加按钮
                    add_btn = QtWidgets.QPushButton("添加学生")
                    add_btn.setFixedWidth(120)  # 增加按钮宽度
                    add_btn.clicked.connect(lambda checked, uid=user[0]: self.add_student(uid))
                    button_layout.addWidget(add_btn)
                
                h_layout.addLayout(button_layout)
            
            v_layout.addLayout(h_layout)
            
            self.verticalLayout_12.addWidget(frame)
            
            # 添加间隔
            spacer = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
            self.verticalLayout_12.addItem(spacer)
            
        # 添加弹性空间到底部
        spacer_bottom = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_12.addItem(spacer_bottom)
            
    def clear_layout(self, layout):
        """清空布局中的所有部件
        
        Args:
            layout: 要清空的布局
        """
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
                
    def filter_experiments(self, is_finished: bool):
        """过滤实验列表
        
        Args:
            is_finished: 是否是已完成/已批改实验
        """
        search_text = self.lineEdit_2.text() if is_finished else self.lineEdit_4.text()
        info(f"搜索{'已' if is_finished else '未'}完成实验，关键词：{search_text}")
        
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                if self.role == 'student':
                    # 首先获取学生的teacher_id
                    cursor.execute("""
                        SELECT teacher_id FROM users 
                        WHERE id = ? AND role = 'student'
                    """, (self.user_info['id'],))
                    result = cursor.fetchone()
                    if not result or not result[0]:
                        # 如果学生没有指导教师，显示空列表
                        experiments = []
                    else:
                        teacher_id = result[0]
                        if is_finished:
                            # 搜索已完成实验
                            cursor.execute("""
                                SELECT 
                                    e.id, e.creator_id, e.title, e.description, e.create_time,
                                    s.student_id, s.score, s.comment,
                                    NULL as student_name,
                                    (SELECT COUNT(DISTINCT s2.student_id) 
                                     FROM submissions s2 
                                     WHERE s2.experiment_id = e.id) as submit_count,
                                    (SELECT COUNT(*) 
                                     FROM users 
                                     WHERE teacher_id = e.creator_id 
                                     AND role = 'student') as total_students
                                FROM experiments e
                                JOIN submissions s ON e.id = s.experiment_id
                                WHERE s.student_id = ? 
                                AND (e.title LIKE ? OR e.description LIKE ?)
                                ORDER BY e.create_time DESC
                            """, (self.user_info['id'], f"%{search_text}%", f"%{search_text}%"))
                        else:
                            # 搜索未完成实验
                            cursor.execute("""
                                SELECT 
                                    e.id, e.creator_id, e.title, e.description, e.create_time,
                                    NULL as student_id, NULL as score, NULL as comment,
                                    NULL as student_name,
                                    (SELECT COUNT(DISTINCT s2.student_id) 
                                     FROM submissions s2 
                                     WHERE s2.experiment_id = e.id) as submit_count,
                                    (SELECT COUNT(*) 
                                     FROM users 
                                     WHERE teacher_id = e.creator_id 
                                     AND role = 'student') as total_students
                                FROM experiments e
                                LEFT JOIN submissions s ON e.id = s.experiment_id AND s.student_id = ?
                                WHERE s.id IS NULL 
                                AND e.creator_id = ?
                                AND (e.title LIKE ? OR e.description LIKE ?)
                                ORDER BY e.create_time DESC
                            """, (self.user_info['id'], teacher_id, f"%{search_text}%", f"%{search_text}%"))
                
                elif self.role == 'teacher':
                    if is_finished:
                        # 搜索已批改的实验
                        cursor.execute("""
                            SELECT 
                                e.id, e.creator_id, e.title, e.description, e.create_time,
                                s.student_id, s.score, s.comment,
                                u.real_name as student_name,
                                (SELECT COUNT(DISTINCT s2.student_id) 
                                 FROM submissions s2 
                                 WHERE s2.experiment_id = e.id) as submit_count,
                                (SELECT COUNT(*) 
                                 FROM users 
                                 WHERE teacher_id = e.creator_id 
                                 AND role = 'student') as total_students
                            FROM experiments e
                            JOIN submissions s ON e.id = s.experiment_id
                            JOIN users u ON s.student_id = u.id
                            WHERE e.creator_id = ? 
                            AND s.score IS NOT NULL
                            AND (e.title LIKE ? OR e.description LIKE ? OR u.real_name LIKE ?)
                            ORDER BY s.submit_time DESC
                        """, (self.user_info['id'], f"%{search_text}%", f"%{search_text}%", f"%{search_text}%"))
                    else:
                        # 搜索未批改的实验
                        cursor.execute("""
                            SELECT 
                                e.id, e.creator_id, e.title, e.description, e.create_time,
                                s.student_id, s.score, s.comment,
                                u.real_name as student_name,
                                (SELECT COUNT(DISTINCT s2.student_id) 
                                 FROM submissions s2 
                                 WHERE s2.experiment_id = e.id) as submit_count,
                                (SELECT COUNT(*) 
                                 FROM users 
                                 WHERE teacher_id = e.creator_id 
                                 AND role = 'student') as total_students
                            FROM experiments e
                            JOIN submissions s ON e.id = s.experiment_id
                            JOIN users u ON s.student_id = u.id
                            WHERE e.creator_id = ? 
                            AND s.score IS NULL
                            AND (e.title LIKE ? OR e.description LIKE ? OR u.real_name LIKE ?)
                            ORDER BY s.submit_time DESC
                        """, (self.user_info['id'], f"%{search_text}%", f"%{search_text}%", f"%{search_text}%"))
                
                else:  # admin
                    if is_finished:
                        # 搜索已批改的实验
                        cursor.execute("""
                            SELECT 
                                e.id, e.creator_id, e.title, e.description, e.create_time,
                                s.student_id, s.score, s.comment,
                                u.real_name as student_name,
                                (SELECT real_name FROM users WHERE id = e.creator_id) as teacher_name,
                                (SELECT COUNT(DISTINCT s2.student_id) 
                                 FROM submissions s2 
                                 WHERE s2.experiment_id = e.id) as submit_count,
                                (SELECT COUNT(*) 
                                 FROM users 
                                 WHERE teacher_id = e.creator_id 
                                 AND role = 'student') as total_students
                            FROM experiments e
                            JOIN submissions s ON e.id = s.experiment_id
                            JOIN users u ON s.student_id = u.id
                            WHERE s.score IS NOT NULL
                            AND (e.title LIKE ? OR e.description LIKE ? OR u.real_name LIKE ?)
                            ORDER BY s.submit_time DESC
                        """, (f"%{search_text}%", f"%{search_text}%", f"%{search_text}%"))
                    else:
                        # 搜索未批改的实验
                        cursor.execute("""
                            SELECT 
                                e.id, e.creator_id, e.title, e.description, e.create_time,
                                s.student_id, s.score, s.comment,
                                u.real_name as student_name,
                                (SELECT real_name FROM users WHERE id = e.creator_id) as teacher_name,
                                (SELECT COUNT(DISTINCT s2.student_id) 
                                 FROM submissions s2 
                                 WHERE s2.experiment_id = e.id) as submit_count,
                                (SELECT COUNT(*) 
                                 FROM users 
                                 WHERE teacher_id = e.creator_id 
                                 AND role = 'student') as total_students
                            FROM experiments e
                            JOIN submissions s ON e.id = s.experiment_id
                            JOIN users u ON s.student_id = u.id
                            WHERE s.score IS NULL
                            AND (e.title LIKE ? OR e.description LIKE ? OR u.real_name LIKE ?)
                            ORDER BY s.submit_time DESC
                        """, (f"%{search_text}%", f"%{search_text}%", f"%{search_text}%"))
                
                experiments = cursor.fetchall()
            
            # 显示搜索结果
            layout = self.verticalLayout_10 if is_finished else self.verticalLayout_2
            self.display_experiments(experiments, layout, is_finished)
            
        except Exception as e:
            error(f"搜索实验失败: {str(e)}")
            exception(f"搜索实验失败: {str(e)}")
            QMessageBox.warning(self, "错误", "搜索实验失败")
            
    def filter_all_experiments(self):
        """过滤所有实验列表"""
        search_text = self.lineEdit_5.text()
        info(f"搜索所有实验，关键词：{search_text}")
        
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                if self.role == 'teacher':
                    # 教师只能搜索自己创建的实验
                    cursor.execute("""
                        SELECT 
                            e.id, e.creator_id, e.title, e.description, e.create_time,
                            NULL as student_id, NULL as score, NULL as comment,
                            NULL as student_name,
                            (SELECT COUNT(DISTINCT s.student_id) 
                             FROM submissions s 
                             WHERE s.experiment_id = e.id) as submit_count,
                            (SELECT COUNT(*) 
                             FROM users 
                             WHERE teacher_id = ? 
                             AND role = 'student') as total_students
                        FROM experiments e
                        WHERE e.creator_id = ?
                        AND (e.title LIKE ? OR e.description LIKE ?)
                        ORDER BY e.create_time DESC
                    """, (self.user_info['id'], self.user_info['id'], 
                         f"%{search_text}%", f"%{search_text}%"))
                else:
                    # 管理员可以搜索所有实验
                    cursor.execute("""
                        SELECT 
                            e.id, e.creator_id, e.title, e.description, e.create_time,
                            NULL as student_id, NULL as score, NULL as comment,
                            NULL as student_name,
                            (SELECT real_name FROM users WHERE id = e.creator_id) as teacher_name,
                            (SELECT COUNT(DISTINCT s.student_id) 
                             FROM submissions s 
                             WHERE s.experiment_id = e.id) as submit_count,
                            (SELECT COUNT(*) 
                             FROM users 
                             WHERE teacher_id = e.creator_id 
                             AND role = 'student') as total_students
                        FROM experiments e
                        WHERE e.title LIKE ? OR e.description LIKE ?
                        ORDER BY e.create_time DESC
                    """, (f"%{search_text}%", f"%{search_text}%"))
                    
                experiments = cursor.fetchall()
            
            # 显示搜索结果
            self.display_experiments(experiments, self.verticalLayout_11, False)
            
        except Exception as e:
            error(f"搜索实验失败: {str(e)}")
            exception(f"搜索实验失败: {str(e)}")
            QMessageBox.warning(self, "错误", "搜索实验失败")
            
    def filter_users(self):
        """过滤用户列表"""
        search_text = self.lineEdit_7.text()
        info(f"搜索用户，关键词：{search_text}")
        
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                if self.role == 'teacher':
                    # 教师可以看到所有学生，并标记是否是自己的学生
                    cursor.execute("""
                        SELECT u.*, CASE WHEN u.teacher_id = ? THEN 1 ELSE 0 END as is_my_student 
                        FROM users u 
                        WHERE u.role = 'student'
                        AND (u.username LIKE ? OR u.real_name LIKE ? OR u.student_id LIKE ?)
                        ORDER BY is_my_student DESC, u.create_time DESC
                    """, (self.user_info['id'], f"%{search_text}%", f"%{search_text}%", f"%{search_text}%"))
                else:
                    # 管理员可以搜索所有用户
                    cursor.execute("""
                        SELECT * FROM users 
                        WHERE username LIKE ? OR real_name LIKE ? OR student_id LIKE ?
                    """, (f"%{search_text}%", f"%{search_text}%", f"%{search_text}%"))
                    
                users = cursor.fetchall()
            
            # 显示搜索结果
            self.display_users(users)
            
        except Exception as e:
            error(f"搜索用户失败: {str(e)}")
            exception(f"搜索用户失败: {str(e)}")
            QMessageBox.warning(self, "错误", "搜索用户失败")
        
    def add_experiment(self):
        """添加新实验"""
        from ui.menu.create_experiment import CreateExperimentWindow
        # 创建新窗口并保存实例
        self.create_experiment_window = CreateExperimentWindow(self.user_info, self)
        self.create_experiment_window.show()
        
    def edit_experiment(self, experiment_id: int):
        """编辑实验
        
        Args:
            experiment_id: 实验ID
        """
        info(f"用户:{self.user_info['username']} 编辑实验 {experiment_id}")
        from ui.menu.create_experiment import CreateExperimentWindow
        # 创建编辑实验窗口
        self.create_experiment_window = CreateExperimentWindow(
            user_info=self.user_info,
            parent=self,
            experiment_id=experiment_id  # 传入实验ID表示编辑模式
        )
        self.create_experiment_window.show()
        
    def delete_experiment(self, experiment_id: int):
        """删除实验
        
        Args:
            experiment_id: 实验ID
        """
        info(f"用户:{self.user_info['username']} 请求删除实验 {experiment_id}")
        
        try:
            # 首先检查是否有权限删除
            with db.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT title, creator_id 
                    FROM experiments 
                    WHERE id = ?
                """, (experiment_id,))
                result = cursor.fetchone()
                
                if not result:
                    QMessageBox.warning(self, "错误", "未找到要删除的实验")
                    return
                    
                title, creator_id = result
                
                # 检查权限
                if creator_id != self.user_info['id'] and self.role != 'admin':
                    QMessageBox.warning(self, "错误", "您没有权限删除此实验")
                    return
                
                # 显示确认对话框
                reply = QMessageBox.question(
                    self, 
                    '确认删除',
                    f'确定要删除实验"{title}"吗？\n删除后将同时删除所有学生的提交记录，此操作不可恢复。',
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                
                if reply == QMessageBox.Yes:
                    info(f"用户:{self.user_info['username']} 确认删除实验 {experiment_id}")
                    
                    # 开始删除操作
                    cursor.execute("BEGIN TRANSACTION")
                    try:
                        # 先删除相关的提交记录
                        cursor.execute("""
                            DELETE FROM submissions 
                            WHERE experiment_id = ?
                        """, (experiment_id,))
                        
                        # 再删除实验
                        cursor.execute("""
                            DELETE FROM experiments 
                            WHERE id = ?
                        """, (experiment_id,))
                        
                        # 提交事务
                        conn.commit()
                        
                        QMessageBox.information(self, "成功", "实验已删除")
                        
                        # 刷新实验列表
                        self.load_all_experiments()
                        
                    except Exception as e:
                        # 出错时回滚事务
                        cursor.execute("ROLLBACK")
                        raise e
                        
        except Exception as e:
            error(f"删除实验失败: {str(e)}")
            exception(f"删除实验失败: {str(e)}")
            QMessageBox.warning(self, "错误", "删除实验失败")
        
    def submit_experiment(self, experiment_id: int):
        """提交实验
        
        Args:
            experiment_id: 实验ID
        """
        from ui.menu.submit_experiment import SubmitExperimentWindow
        # 创建提交实验窗口
        self.submit_experiment_window = SubmitExperimentWindow(
            user_info=self.user_info,
            experiment_id=experiment_id,
            parent=self
        )
        self.submit_experiment_window.show()
        
    def add_user(self):
        """添加新用户"""
        from ui.menu.user_information import UserInformationWindow
        # 创建添加用户窗口
        self.user_information_window = UserInformationWindow(
            user_info=self.user_info,
            parent=self
        )
        self.user_information_window.show()
        
    def edit_user(self, user_id: int):
        """编辑用户信息
        
        Args:
            user_id: 用户ID
        """
        from ui.menu.user_information import UserInformationWindow
        # 创建编辑用户窗口
        self.user_information_window = UserInformationWindow(
            user_info=self.user_info,
            edit_user_id=user_id,
            parent=self
        )
        self.user_information_window.show()
        
    def delete_user(self, user_id: int):
        """删除用户
        
        Args:
            user_id: 用户ID
        """
        try:
            # 首先获取用户信息
            with db.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT username, real_name, role 
                    FROM users 
                    WHERE id = ?
                """, (user_id,))
                result = cursor.fetchone()
                
                if not result:
                    QMessageBox.warning(self, "错误", "未找到要删除的用户")
                    return
                    
                username, real_name, role = result
                
                # 不能删除自己
                if user_id == self.user_info['id']:
                    QMessageBox.warning(self, "错误", "不能删除当前登录用户")
                    return
                    
                # 显示确认对话框
                reply = QMessageBox.question(
                    self, 
                    '确认删除',
                    f'确定要删除用户"{username}({real_name})"吗？\n' + 
                    ('该用户的所有实验提交记录也将被删除。' if role == 'student' else '') +
                    '\n此操作不可恢复。',
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                
                if reply == QMessageBox.Yes:
                    info(f"用户:{self.user_info['username']} 确认删除用户 {username}")
                    
                    # 开始删除操作
                    cursor.execute("BEGIN TRANSACTION")
                    try:
                        # 如果是学生，删除其所有实验提交
                        if role == 'student':
                            cursor.execute("""
                                DELETE FROM submissions 
                                WHERE student_id = ?
                            """, (user_id,))
                            
                        # 如果是教师，将其学生的teacher_id设为NULL
                        elif role == 'teacher':
                            cursor.execute("""
                                UPDATE users 
                                SET teacher_id = NULL 
                                WHERE teacher_id = ?
                            """, (user_id,))
                            
                        # 删除用户
                        cursor.execute("""
                            DELETE FROM users 
                            WHERE id = ?
                        """, (user_id,))
                        
                        # 提交事务
                        conn.commit()
                        
                        QMessageBox.information(self, "成功", "用户已删除")
                        
                        # 刷新用户列表
                        self.load_users()
                        
                    except Exception as e:
                        # 出错时回滚事务
                        cursor.execute("ROLLBACK")
                        raise e
                        
        except Exception as e:
            error(f"删除用户失败: {str(e)}")
            exception(f"删除用户失败: {str(e)}")
            QMessageBox.warning(self, "错误", "删除用户失败")
        
    def edit_profile(self):
        """编辑个人信息"""
        from ui.menu.user_information import UserInformationWindow
        # 创建编辑个人信息窗口
        self.user_information_window = UserInformationWindow(
            user_info=self.user_info,
            edit_user_id=self.user_info['id'],  # 编辑自己的信息
            parent=self
        )
        self.user_information_window.show()
        
    def logout(self):
        """退出登录"""
        info("用户请求退出登录")
        reply = QMessageBox.question(
            self, '确认', '确定要退出登录吗？',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            info("用户确认退出登录")
            if self.login_window:
                # 清空登录窗口的输入框
                self.login_window.lineEdit_7.clear()  # 清空用户名
                self.login_window.lineEdit_5.clear()  # 清空密码
                self.login_window.clear_error()       # 清空错误信息
                
                # 显示登录窗口
                self.login_window.show()
            else:
                warning("登录窗口实例不存在，创建新的登录窗口")
                from ui.login.login_window import LoginWindow
                self.login_window = LoginWindow()
                self.login_window.show()
            
            # 关闭主窗口
            self.close()
            debug("退出登录完成")

    def add_student(self, student_id: int):
        """添加学生到自己的学生列表
        
        Args:
            student_id: 学生ID
        """
        try:
            with db.get_connection() as conn:
                # 更新学生的teacher_id
                cursor = conn.execute(
                    "UPDATE users SET teacher_id = ? WHERE id = ? AND role = 'student'",
                    (self.user_info['id'], student_id)
                )
                conn.commit()
                
                if cursor.rowcount > 0:
                    QMessageBox.information(self, "成功", "已成功添加该学生")
                    # 刷新用户列表
                    self.load_users()
                else:
                    QMessageBox.warning(self, "失败", "添加学生失败")
                    
        except Exception as e:
            error(f"添加学生失败: {str(e)}")
            exception(f"添加学生失败: {str(e)}")
            QMessageBox.warning(self, "错误", "添加学生失败")

    def remove_student(self, student_id: int):
        """将学生从自己的学生列表中移除
        
        Args:
            student_id: 学生ID
        """
        try:
            with db.get_connection() as conn:
                # 将学生的teacher_id设为NULL
                cursor = conn.execute(
                    "UPDATE users SET teacher_id = NULL WHERE id = ? AND teacher_id = ?",
                    (student_id, self.user_info['id'])
                )
                conn.commit()
                
                if cursor.rowcount > 0:
                    QMessageBox.information(self, "成功", "已成功移除该学生")
                    # 刷新用户列表
                    self.load_users()
                else:
                    QMessageBox.warning(self, "失败", "移除学生失败")
                    
        except Exception as e:
            error(f"移除学生失败: {str(e)}")
            exception(f"移除学生失败: {str(e)}")
            QMessageBox.warning(self, "错误", "移除学生失败")

    def grade_submission(self, submission_id: int):
        """批改实验提交
        
        Args:
            submission_id: 提交ID
        """
        info(f"批改实验提交 {submission_id}")
        from ui.menu.grade_submission import GradeSubmissionWindow
        # 创建批改实验窗口
        self.grade_submission_window = GradeSubmissionWindow(
            user_info=self.user_info,
            experiment_id=submission_id,
            parent=self
        )
        self.grade_submission_window.show()
        
    def edit_submission(self, experiment_id: int):
        """编辑实验提交
        
        Args:
            experiment_id: 实验ID
        """
        info(f"用户:{self.user_info['username']} 编辑实验提交 {experiment_id}")
        from ui.menu.submit_experiment import SubmitExperimentWindow
        # 创建提交实验窗口，传入编辑模式参数
        self.submit_experiment_window = SubmitExperimentWindow(
            user_info=self.user_info,
            experiment_id=experiment_id,
            parent=self,
            is_edit=True  # 标记为编辑模式
        )
        self.submit_experiment_window.show()
        
    def delete_submission(self, experiment_id: int):
        """删除实验提交
        
        Args:
            experiment_id: 实验ID
        """
        reply = QMessageBox.question(
            self, '确认删除',
            '确定要删除这个实验提交吗？删除后将不可恢复。',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            info(f"用户:{self.user_info['username']}删除实验提交 {experiment_id}")
            try:
                with db.get_connection() as conn:
                    cursor = conn.cursor()
                    # 删除提交记录
                    cursor.execute("""
                        DELETE FROM submissions 
                        WHERE experiment_id = ? AND student_id = ?
                    """, (experiment_id, self.user_info['id']))
                    
                    conn.commit()
                    
                    if cursor.rowcount > 0:
                        QMessageBox.information(self, "成功", "实验提交已删除")
                        # 刷新实验列表
                        self.load_experiments()
                    else:
                        QMessageBox.warning(self, "错误", "未找到要删除的提交记录")
                        
            except Exception as e:
                error(f"删除实验提交失败: {str(e)}")
                exception(f"删除实验提交失败: {str(e)}")
                QMessageBox.warning(self, "错误", "删除实验提交失败")

    def return_submission(self, experiment_id: int):
        """打回学生的实验提交
        
        Args:
            experiment_id: 实验ID
        """
        info(f"用户:{self.user_info['username']} 打回实验提交 {experiment_id}")
        reply = QMessageBox.question(
            self, '确认打回',
            '确定要打回这个实验提交吗？打回后学生需要重新提交。',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                with db.get_connection() as conn:
                    cursor = conn.cursor()
                    # 删除提交记录
                    cursor.execute("""
                        DELETE FROM submissions 
                        WHERE experiment_id = ?
                    """, (experiment_id,))
                    
                    conn.commit()
                    
                    if cursor.rowcount > 0:
                        QMessageBox.information(self, "成功", "已打回学生的实验提交")
                        # 刷新实验列表
                        self.load_experiments()
                    else:
                        QMessageBox.warning(self, "错误", "未找到要打回的提交记录")
                        
            except Exception as e:
                error(f"打回实验提交失败: {str(e)}")
                exception(f"打回实验提交失败: {str(e)}")
                QMessageBox.warning(self, "错误", "打回实验提交失败")

    def view_submission(self, experiment_id: int):
        """查看已批改的实验提交
        
        Args:
            experiment_id: 实验ID
        """
        info(f"用户:{self.user_info['username']} 查看实验提交 {experiment_id}")
        from ui.menu.grade_submission import GradeSubmissionWindow
        # 创建查看窗口（复用批改窗口的UI，但所有字段都设为只读）
        self.view_window = GradeSubmissionWindow(
            user_info=self.user_info,
            experiment_id=experiment_id,
            parent=self
        )
        # 设置所有输入字段为只读
        self.view_window.lineEdit_2.setReadOnly(True)  # 分数
        self.view_window.textEdit_2.setReadOnly(True)  # 评语
        # 隐藏提交按钮
        self.view_window.pushButton_2.hide()
        # 修改返回按钮文字
        self.view_window.pushButton.setText("关闭")
        self.view_window.show()

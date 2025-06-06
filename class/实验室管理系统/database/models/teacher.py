#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
教师模型类
继承自用户基类，实现教师特有的功能
"""

from .user import User

class Teacher(User):
    """
    教师类
    
    主要功能：
    1. 课程管理（创建、修改、删除课程）
    2. 实验任务管理（发布、修改实验任务）
    3. 学生成绩管理（批改作业、录入成绩）
    4. 查看学生实验报告
    """
    
    def __init__(self):
        super().__init__()
        self.role = 'teacher'
        self.courses = []  # 该教师负责的课程列表
    
    # 在此处实现教师特有的方法 
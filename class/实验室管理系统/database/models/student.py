#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
学生模型类
继承自用户基类，实现学生特有的功能
"""

from .user import User

class Student(User):
    """
    学生类
    
    主要功能：
    1. 查看课程信息
    2. 查看实验任务
    3. 提交实验报告
    4. 查看实验成绩
    """
    
    def __init__(self):
        super().__init__()
        self.role = 'student'
        self.student_id = None  # 学号
        self.enrolled_courses = []  # 已选课程列表
    
    # 在此处实现学生特有的方法 
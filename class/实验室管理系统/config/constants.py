#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
常量定义文件
包含状态码、角色类型等常量
"""

# 用户角色
ROLE_ADMIN = 'admin'
ROLE_TEACHER = 'teacher'
ROLE_STUDENT = 'student'

# 状态码
STATUS_SUCCESS = 200
STATUS_ERROR = 500
STATUS_UNAUTHORIZED = 401
STATUS_NOT_FOUND = 404

# 实验状态
EXPERIMENT_STATUS_DRAFT = 'draft'
EXPERIMENT_STATUS_PUBLISHED = 'published'
EXPERIMENT_STATUS_CLOSED = 'closed'

# 在此处添加其他常量定义 
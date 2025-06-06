#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
管理员模型类
继承自用户基类，实现管理员特有的功能
"""

from .user import User

class Admin(User):
    """
    管理员类
    
    主要功能：
    1. 用户管理（添加、删除、修改用户信息）
    2. 系统管理（系统设置、数据备份）
    3. 日志管理
    """
    
    def __init__(self):
        super().__init__()
        self.role = 'admin'
    
    # 在此处实现管理员特有的方法 
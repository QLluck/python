#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
路径管理工具
用于处理开发环境和打包环境下的文件路径
"""

import os
import sys

def get_root_path():
    """
    获取应用程序根目录
    在开发环境和打包环境下都能正确工作
    """
    if getattr(sys, 'frozen', False):
        # 打包环境下的路径
        return os.path.dirname(sys.executable)
    else:
        # 开发环境下的路径
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_resource_path(relative_path):
    """
    获取资源文件的绝对路径
    
    Args:
        relative_path: 相对于项目根目录的路径
        
    Returns:
        str: 资源文件的绝对路径
    """
    base_path = get_root_path()
    return os.path.join(base_path, relative_path)

def get_config_path():
    """
    获取配置文件目录
    """
    return get_resource_path('config')

def get_database_path():
    """
    获取数据库文件路径
    """
    db_dir = get_resource_path('database')
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    return os.path.join(db_dir, 'database.db')

def get_log_path():
    """
    获取日志文件目录
    """
    log_dir = get_resource_path('logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir

def get_ui_path(ui_file):
    """
    获取UI文件的路径
    
    Args:
        ui_file: UI文件名
        
    Returns:
        str: UI文件的绝对路径
    """
    return get_resource_path(os.path.join('ui', ui_file)) 
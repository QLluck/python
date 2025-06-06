#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
全局配置文件
包含数据库配置、文件路径等设置
"""

from utils.path_helper import get_database_path, get_resource_path, get_log_path

# 数据库配置
DATABASE = {
    'path': get_database_path()
}

# 文件上传配置
UPLOAD = {
    'path': get_resource_path('uploads'),
    'allowed_extensions': ['txt', 'pdf', 'doc', 'docx']
}

# 日志配置
LOG = {
    'path': get_log_path(),
    'level': 'INFO'
}

# UI资源配置
UI = {
    'resources_path': get_resource_path('ui/resources'),
    'icons_path': get_resource_path('ui/resources/icons'),
    'styles_path': get_resource_path('ui/resources/styles')
}

# 在此处添加其他配置项 
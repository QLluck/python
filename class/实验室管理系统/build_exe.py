#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
打包脚本
使用 PyInstaller 将应用打包成可执行文件
"""

import PyInstaller.__main__
import os

def main():
    """
    打包主函数
    """
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 定义资源文件
    datas = [
        ('ui/resources/ui_files/*.ui', 'ui/resources/ui_files'),
        ('ui/resources/icons/*', 'ui/resources/icons'),
        ('ui/resources/styles/*', 'ui/resources/styles'),
        ('config/*.py', 'config'),
        ('database/migrations/*.sql', 'database/migrations')
    ]
    
    # 将资源文件路径转换为绝对路径
    datas = [(os.path.join(current_dir, src), dst) for src, dst in datas]
    
    # PyInstaller 参数
    params = [
        'main.py',  # 主程序入口
        '--name=实验室管理系统',  # 生成的exe名称
        '--windowed',  # 使用GUI模式
        '--icon=ui/resources/icons/app.ico',  # 应用图标
        '--clean',  # 清理临时文件
        '--noconfirm',  # 不确认覆盖
        '--add-data=' + ';'.join(datas[0]),  # UI文件
        '--add-data=' + ';'.join(datas[1]),  # 图标文件
        '--add-data=' + ';'.join(datas[2]),  # 样式文件
        '--add-data=' + ';'.join(datas[3]),  # 配置文件
        '--add-data=' + ';'.join(datas[4]),  # 数据库迁移文件
    ]
    
    # 运行打包
    PyInstaller.__main__.run(params)

if __name__ == '__main__':
    main() 
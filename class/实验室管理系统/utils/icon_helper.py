import os
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget
import utils.path_helper
import logging
import sys
def get_icon_path(icon_name: str) -> str:
    """获取图标文件的完整路径"""
    
    return utils.path_helper.get_resource_path("resources/icons/"+icon_name)

def set_app_icon(widget: QWidget, icon_name: str = 'app_icon.svg'):
    """设置窗口和应用程序图标"""
    icon_path = get_icon_path(icon_name)
    if os.path.exists(icon_path):
        widget.setWindowIcon(QIcon(icon_path))
    else:
        logging.StreamHandler(f"Warning: Icon file not found at {icon_path}") 
        sys.exit(1)
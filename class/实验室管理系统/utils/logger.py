import logging
import os
import sys
from datetime import datetime
from typing import Optional
from logging.handlers import RotatingFileHandler
import colorama
from colorama import Fore, Back, Style

# 初始化colorama，使其在Windows上也能正常工作
colorama.init()

class ColoredFormatter(logging.Formatter):
    """自定义的彩色日志格式化器"""
    
    # 定义不同级别日志的颜色
    COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Back.WHITE
    }
    
    def format(self, record):
        # 如果是错误或严重级别，添加额外的错误信息
        if record.levelno >= logging.ERROR and record.exc_info:
            record.exc_text = self.formatException(record.exc_info)
            
        # 获取对应的颜色
        color = self.COLORS.get(record.levelname, '')
        
        # 设置记录的颜色
        record.levelname = f"{color}{record.levelname}{Style.RESET_ALL}"
        record.msg = f"{color}{record.msg}{Style.RESET_ALL}"
        
        return super().format(record)

class Logger:
    """日志管理器"""
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if Logger._initialized:
            return
            
        Logger._initialized = True
        
        # 创建logger
        self.logger = logging.getLogger('LabManager')
        self.logger.setLevel(logging.DEBUG)
        
        # 设置日志格式
        console_formatter = ColoredFormatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 配置控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.DEBUG)
        
        # 配置文件处理器
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f'lab_manager_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.DEBUG)
        
        # 添加处理器
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    @classmethod
    def get_logger(cls):
        """获取日志记录器实例"""
        if cls._instance is None:
            cls._instance = Logger()
        return cls._instance.logger

# 创建便捷的全局函数
def debug(msg: str, *args, **kwargs):
    Logger.get_logger().debug(msg, *args, **kwargs)

def info(msg: str, *args, **kwargs):
    Logger.get_logger().info(msg, *args, **kwargs)

def warning(msg: str, *args, **kwargs):
    Logger.get_logger().warning(msg, *args, **kwargs)

def error(msg: str, *args, **kwargs):
    Logger.get_logger().error(msg, *args, **kwargs)

def critical(msg: str, *args, **kwargs):
    Logger.get_logger().critical(msg, *args, **kwargs)

def exception(msg: str, *args, **kwargs):
    """记录异常信息，包含完整的堆栈跟踪"""
    Logger.get_logger().exception(msg, *args, **kwargs)

# 使用示例
if __name__ == '__main__':
    debug("这是一条调试信息")
    info("这是一条普通信息")
    warning("这是一条警告信息")
    error("这是一条错误信息")
    critical("这是一条严重错误信息")
    
    try:
        1/0
    except Exception as e:
        exception("发生了一个异常") 
import hashlib
import re
from datetime import datetime

def hash_password(password):
    """对密码进行哈希处理"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_isbn(isbn):
    """验证ISBN格式"""
    # 移除所有连字符和空格
    isbn = isbn.replace('-', '').replace(' ', '')
    
    if len(isbn) == 13:  # ISBN-13
        if not isbn.isdigit():
            return False
        # 检查校验位
        sum = 0
        for i in range(12):
            if i % 2 == 0:
                sum += int(isbn[i])
            else:
                sum += int(isbn[i]) * 3
        check = (10 - (sum % 10)) % 10
        return int(isbn[-1]) == check
    
    elif len(isbn) == 10:  # ISBN-10
        if not isbn[:-1].isdigit():
            return False
        if isbn[-1].upper() == 'X':
            check_digit = 10
        else:
            check_digit = int(isbn[-1])
        
        sum = 0
        for i in range(9):
            sum += int(isbn[i]) * (10 - i)
        sum += check_digit
        
        return sum % 11 == 0
    
    return False

def format_date(date_obj):
    """格式化日期"""
    if isinstance(date_obj, str):
        date_obj = datetime.strptime(date_obj, '%Y-%m-%d %H:%M:%S')
    return date_obj.strftime('%Y-%m-%d %H:%M:%S')

def calculate_fine(borrow_date, return_date=None):
    """计算超期罚款
    
    Args:
        borrow_date: 借书日期
        return_date: 还书日期，如果为None则使用当前日期
        
    Returns:
        超期天数和罚款金额
    """
    if isinstance(borrow_date, str):
        borrow_date = datetime.strptime(borrow_date, '%Y-%m-%d %H:%M:%S')
    
    if return_date is None:
        return_date = datetime.now()
    elif isinstance(return_date, str):
        return_date = datetime.strptime(return_date, '%Y-%m-%d %H:%M:%S')
    
    # 允许借阅30天
    allowed_days = 30
    days_diff = (return_date - borrow_date).days
    
    if days_diff <= allowed_days:
        return 0, 0
    
    overdue_days = days_diff - allowed_days
    # 每超期一天罚款0.5元
    fine = overdue_days * 0.5
    
    return overdue_days, fine 
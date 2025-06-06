import re
from typing import Tuple

class ValidationUtils:
    # 只允许英文字母和数字的正则表达式模式
    USERNAME_PATTERN = r'^[a-zA-Z0-9]+$' #^是从头开始， $符号是表示到结尾
    PASSWORD_PATTERN = r'^[a-zA-Z0-9]+$'
    
    @classmethod
    def validate_username(cls, username: str) -> Tuple[bool, str]:
        """验证用户名是否符合规则：只能包含英文字母和数字
        
        Args:
            username: 要验证的用户名
            
        Returns:
            Tuple[bool, str]: (是否有效, 错误信息)
        """
        if not username:
            return False, "用户名不能为空"
            
        if len(username) < 4:
            return False, "用户名长度不能小于4个字符"
            
        if len(username) > 20:
            return False, "用户名长度不能超过20个字符"
            
        if not re.match(cls.USERNAME_PATTERN, username):
            return False, "用户名只能包含英文字母和数字"
            
        return True, ""
        
    @classmethod
    def validate_password(cls, password: str) -> Tuple[bool, str]:
        """验证密码是否符合规则：只能包含英文字母和数字
        
        Args:
            password: 要验证的密码
            
        Returns:
            Tuple[bool, str]: (是否有效, 错误信息)
        """
        if not password:
            return False, "密码不能为空"
            
        if len(password) < 6:
            return False, "密码长度不能小于6个字符"
            
        if len(password) > 20:
            return False, "密码长度不能超过20个字符"
            
        if not re.match(cls.PASSWORD_PATTERN, password):#匹配成功返回mathch对象，否则返回False
            return False, "密码只能包含英文字母和数字"
            
        return True, "" 
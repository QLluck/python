import re
import bcrypt
from config import PASSWORD_RULES, PHONE_PATTERN

class Validators:
    @staticmethod
    def validate_password(password):
        if len(password) < PASSWORD_RULES['min_length']:
            return False, f"密码长度必须至少为{PASSWORD_RULES['min_length']}个字符"
        
        if PASSWORD_RULES['require_uppercase'] and not re.search(r'[A-Z]', password):
            return False, "密码必须包含大写字母"
        
        if PASSWORD_RULES['require_lowercase'] and not re.search(r'[a-z]', password):
            return False, "密码必须包含小写字母"
        
        if PASSWORD_RULES['require_digit'] and not re.search(r'\d', password):
            return False, "密码必须包含数字"
        
        if PASSWORD_RULES['require_special'] and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "密码必须包含特殊字符"
        
        return True, "密码验证通过"

    @staticmethod
    def validate_phone(phone):
        if not re.match(PHONE_PATTERN, phone):
            return False, "请输入有效的手机号码"
        return True, "手机号验证通过"

    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    @staticmethod
    def verify_password(password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed) 
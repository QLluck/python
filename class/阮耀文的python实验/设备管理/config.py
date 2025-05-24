import os
from dotenv import load_dotenv

load_dotenv()

# 数据库配置
DB_CONFIG = {
    'type': 'sqlite',
    'database': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.db')
}

# 密码规则
PASSWORD_RULES = {
    'min_length': 5,
    'require_uppercase': False,
    'require_lowercase': False,
    'require_digit': False,
    'require_special': False
}

# 手机号规则
PHONE_PATTERN = r'^1[3-9]\d{9}$'

# 登录尝试次数限制
MAX_LOGIN_ATTEMPTS = 3 
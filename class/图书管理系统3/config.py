import os

# 数据库配置
DATABASE_NAME = 'library.db'
DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), DATABASE_NAME)

# 用户角色
ROLE_ADMIN = 'admin'
ROLE_USER = 'user'

# 图书状态
BOOK_STATUS_AVAILABLE = 'available'
BOOK_STATUS_BORROWED = 'borrowed' 
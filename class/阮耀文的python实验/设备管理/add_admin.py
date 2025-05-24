import sys
import os

# 添加父目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_utils import DatabaseConnection
from utils.validators import Validators

def add_admin(username, password, phone):
    # 验证密码
    is_valid, message = Validators.validate_password(password)
    if not is_valid:
        print(f"错误: {message}")
        return False

    # 验证手机号
    is_valid, message = Validators.validate_phone(phone)
    if not is_valid:
        print(f"错误: {message}")
        return False

    try:
        # 哈希密码
        hashed_password = Validators.hash_password(password)
        
        # 连接数据库
        db = DatabaseConnection()
        
        # 检查用户名是否已存在
        result = db.execute_query("SELECT id FROM users WHERE username = %s", (username,))
        if result:
            print("错误: 用户名已存在")
            return False

        # 插入新管理员
        query = """
            INSERT INTO users (role, username, password, phone)
            VALUES ('admin', %s, %s, %s)
        """
        db.execute_query(query, (username, hashed_password, phone))
        print("成功: 管理员账号已创建")
        return True
    except Exception as e:
        print(f"错误: {str(e)}")
        return False

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("使用方法: python add_admin.py <用户名> <密码> <手机号>")
        print("示例: python add_admin.py admin123 Admin@123 13800138000")
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]
    phone = sys.argv[3]
    
    add_admin(username, password, phone) 
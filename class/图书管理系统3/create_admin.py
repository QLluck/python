from database import db
from models import User
from utils import hash_password
from config import ROLE_ADMIN

def create_admin_user():
    """创建管理员账号"""
    try:
        # 连接数据库
        db.connect()
        
        # 检查管理员是否已存在
        db.cursor.execute('SELECT * FROM users WHERE username = ?', ('admin',))
        if db.cursor.fetchone():
            print("管理员账号已存在")
            return
            
        # 创建管理员用户
        admin = User(
            username='admin',
            password=hash_password('admin'),
            role=ROLE_ADMIN,
            name='Administrator'
        )
        admin.save()
        print("管理员账号创建成功")
        
    except Exception as e:
        print(f"创建管理员账号失败: {str(e)}")
    finally:
        db.disconnect()

if __name__ == '__main__':
    create_admin_user() 
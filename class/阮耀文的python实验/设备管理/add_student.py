import bcrypt
import sqlite3
import os
import sys
from pathlib import Path
from database.db_utils import DatabaseConnection
from utils.validators import Validators

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from config import DB_CONFIG
except ImportError as e:
    print(f"错误：无法导入配置文件：{str(e)}")
    sys.exit(1)

def init_database():
    """初始化数据库"""
    try:
        print("开始初始化数据库...")
        # 连接SQLite数据库（如果不存在会自动创建）
        conn = sqlite3.connect(DB_CONFIG['database'])
        cursor = conn.cursor()

        # 创建用户表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT CHECK(role IN ('student', 'admin')) NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("数据库初始化成功")
    except Exception as e:
        print(f"错误：数据库初始化失败：{str(e)}")
        sys.exit(1)

def add_student():
    try:
        print("开始添加学生账号...")
        # 连接数据库
        db = DatabaseConnection()
        
        # 学生信息
        username = '2415929710'
        password = '12345'
        role = 'student'
        
        print(f"正在检查用户是否存在：{username}")
        # 检查用户是否已存在
        check_query = "SELECT * FROM users WHERE username = %s AND role = %s"
        existing_user = db.execute_query(check_query, (username, role))
        
        if existing_user:
            print(f"用户 {username} 已存在")
            return
        
        print("正在对密码进行哈希处理...")
        # 对密码进行哈希处理
        hashed_password = Validators.hash_password(password)
        print("密码哈希处理完成")
        
        print("正在插入新用户...")
        # 插入新用户
        insert_query = """
        INSERT INTO users (role, username, password, created_at) 
        VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
        """
        result = db.execute_query(insert_query, (role, username, hashed_password))
        print(f"插入结果：{result}")
        
        print(f"成功添加学生账号：{username}")
        
        # 验证是否添加成功
        print("正在验证账号是否添加成功...")
        verify_query = "SELECT * FROM users WHERE username = %s AND role = %s"
        user = db.execute_query(verify_query, (username, role))
        if user:
            print(f"验证成功：找到用户 {username}")
        else:
            print(f"验证失败：未找到用户 {username}")
        
    except Exception as e:
        print(f"添加学生账号时出错：{str(e)}")

if __name__ == '__main__':
    print("开始添加学生账号...")
    print(f"当前工作目录：{os.getcwd()}")
    print(f"数据库路径：{DB_CONFIG['database']}")
    
    # 添加学生账号
    add_student() 
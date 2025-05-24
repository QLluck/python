import sqlite3
import sys
import os
import bcrypt

# 添加父目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DB_CONFIG

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

        # 创建设备表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                total_qty INTEGER NOT NULL,
                available_qty INTEGER NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 创建借用记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS borrow_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                device_id INTEGER NOT NULL,
                borrow_date DATE NOT NULL,
                return_date DATE,
                status TEXT CHECK(status IN ('申请中', '借用中', '已归还')) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (device_id) REFERENCES devices(id)
            )
        """)

        # 检查是否已存在管理员账号
        cursor.execute("SELECT * FROM users WHERE role = 'admin'")
        if not cursor.fetchone():
            # 创建默认管理员账号
            password = "admin"
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            cursor.execute("""
                INSERT INTO users (role, username, password, phone)
                VALUES ('admin', 'admin', ?, '13800000000')
            """, (hashed_password,))

        conn.commit()
        cursor.close()
        conn.close()
        print("数据库初始化成功")
    except Exception as e:
        print(f"错误：数据库初始化失败：{str(e)}")
        raise e

if __name__ == '__main__':
    init_database() 
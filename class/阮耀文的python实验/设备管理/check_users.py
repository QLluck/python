import sqlite3
import os
import sys
from pathlib import Path

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from config import DB_CONFIG
except ImportError as e:
    print(f"错误：无法导入配置文件：{str(e)}")
    sys.exit(1)

def check_database():
    """检查数据库状态"""
    # 检查数据库文件是否存在
    db_path = Path(DB_CONFIG['database'])
    if not db_path.exists():
        print(f"错误：数据库文件不存在：{db_path}")
        return

    try:
        # 连接数据库
        conn = sqlite3.connect(DB_CONFIG['database'])
        cursor = conn.cursor()
        
        # 检查users表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            print("错误：users表不存在")
            return

        # 获取所有用户
        cursor.execute("""
            SELECT id, role, username, phone, created_at 
            FROM users 
            ORDER BY id
        """)
        users = cursor.fetchall()
        
        if not users:
            print("数据库中没有任何用户")
            return
            
        print("\n=== 用户列表 ===")
        print("ID\t角色\t用户名\t\t手机号\t\t创建时间")
        print("-" * 70)
        for user in users:
            user_id, role, username, phone, created_at = user
            role_display = "管理员" if role == "admin" else "学生"
            phone = phone or "未设置"
            print(f"{user_id}\t{role_display}\t{username}\t{phone}\t{created_at}")
            
        # 显示用户统计
        cursor.execute("SELECT role, COUNT(*) FROM users GROUP BY role")
        stats = cursor.fetchall()
        print("\n=== 用户统计 ===")
        for role, count in stats:
            role_display = "管理员" if role == "admin" else "学生"
            print(f"{role_display}账号数量：{count}")
            
    except Exception as e:
        print(f"错误：{str(e)}")
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

if __name__ == "__main__":
    print(f"数据库路径：{DB_CONFIG['database']}")
    check_database() 
import sqlite3
from config import DATABASE_PATH

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        """连接到数据库"""
        try:
            self.connection = sqlite3.connect(DATABASE_PATH)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print(f"数据库连接错误: {e}")
            raise

    def disconnect(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()

    def commit(self):
        """提交事务"""
        if self.connection:
            self.connection.commit()

    def init_database(self):
        """初始化数据库表"""
        try:
            self.connect()
            
            # 创建用户表
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL,
                    name TEXT,
                    email TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # 创建图书表
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    isbn TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    author TEXT,
                    publisher TEXT,
                    status TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # 创建借阅记录表
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS borrowings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    borrow_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    return_date TIMESTAMP,
                    status TEXT NOT NULL,
                    FOREIGN KEY (book_id) REFERENCES books (id),
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')

            self.commit()
        except sqlite3.Error as e:
            print(f"初始化数据库错误: {e}")
            raise
        finally:
            self.disconnect()

    def create_tables(self):
        """创建数据库表"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                name TEXT,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isbn TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                author TEXT,
                publisher TEXT,
                status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS borrowings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                borrow_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                return_date TIMESTAMP,
                status TEXT NOT NULL,
                FOREIGN KEY (book_id) REFERENCES books (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        self.commit()

# 创建全局数据库实例
db = Database()

# 初始化数据库
if __name__ == '__main__':
    db.init_database() 
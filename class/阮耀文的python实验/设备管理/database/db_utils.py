import sqlite3
from config import DB_CONFIG

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def get_connection(self):
        if self.connection is None:
            print(f"创建新的数据库连接：{DB_CONFIG['database']}")
            self.connection = sqlite3.connect(DB_CONFIG['database'])
            # 设置row_factory使查询结果返回字典
            self.connection.row_factory = sqlite3.Row
        return self.connection

    def close_connection(self):
        if self.connection:
            print("关闭数据库连接")
            self.connection.close()
            self.connection = None

    def execute_query(self, query, params=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            print(f"执行SQL：{query}")
            print(f"参数：{params}")
            # 将MySQL的%s占位符替换为SQLite的?占位符
            query = query.replace('%s', '?')
            cursor.execute(query, params or ())
            if query.strip().upper().startswith('SELECT'):
                # 将结果转换为字典列表
                results = cursor.fetchall()
                if results:
                    columns = [column[0] for column in cursor.description]
                    return [dict(zip(columns, row)) for row in results]
                return []
            else:
                print("提交事务")
                conn.commit()
                print(f"影响的行数：{cursor.rowcount}")
                return cursor.rowcount
        except Exception as e:
            print(f"执行SQL出错：{str(e)}")
            if not query.strip().upper().startswith('SELECT'):
                print("回滚事务")
                conn.rollback()
            raise e
        finally:
            cursor.close()

    def execute_many(self, query, params_list):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # 将MySQL的%s占位符替换为SQLite的?占位符
            query = query.replace('%s', '?')
            cursor.executemany(query, params_list)
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close() 
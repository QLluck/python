#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据库管理工具类
提供数据库连接和所有基本操作
"""

import sqlite3                  # 导入SQLite数据库模块
from typing import List, Tuple, Dict, Any, Optional  # 导入类型提示
from datetime import datetime  # 导入日期时间处理
import os                     # 导入操作系统功能
from contextlib import contextmanager  # 导入上下文管理器
from utils.path_helper import get_database_path, get_resource_path  # 导入路径工具
from utils.logger import info, debug, warning, error, exception  # 导入日志工具

class DatabaseUtils:
    """
    数据库管理工具类
    实现数据库的连接、初始化和所有数据库操作
    """
    
    _instance = None
    
    def __new__(cls):
        """单例模式实现，确保只创建一个数据库连接实例"""#确保只有存在一个实例对象
        if cls._instance is None:
            cls._instance = super().__new__(cls) #如果首次创建，则创建一个实例
        return cls._instance
    
    def __init__(self):
        """如果已经初始化过，就直接返回"""
        if hasattr(self, 'initialized'):
            return
            
        self.db_path = get_database_path()
        self.initialized = True
        self.init_db()
        
    @contextmanager
    def get_connection(self) -> sqlite3.Connection:
        """
        获取数据库连接的上下文管理器
        
        使用方法:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            
        Returns:
            sqlite3.Connection: 数据库连接对象
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            debug("数据库连接已建立")
            yield conn
        except Exception as e:
            error(f"数据库连接错误: {str(e)}")
            exception(f"数据库连接错误: {str(e)}")
            raise e
        finally:
            if conn:
                conn.close()
                debug("数据库连接已关闭")
    
    def init_db(self):
        """初始化数据库，执行初始化脚本"""
        info(f"初始化数据库: {self.db_path}")
        
        try:
            # 检查数据库文件是否存在
            db_exists = os.path.exists(self.db_path)
            
            # 确保数据库目录存在
            os.makedirs(os.path.dirname(os.path.abspath(self.db_path)), exist_ok=True)
            
            # 获取并执行数据库初始化脚本
            with open(get_resource_path('database/migrations/init_db.sql'), 'r', encoding='utf-8') as f:
                init_script = f.read()
                
            with self.get_connection() as conn:
                conn.executescript(init_script)
                conn.commit()
                
            # 如果是新数据库，执行数据初始化脚本
            if not db_exists:
                with open(get_resource_path('database/migrations/init_data.sql'), 'r', encoding='utf-8') as f:
                    init_data_script = f.read()
                    
                with self.get_connection() as conn:
                    conn.executescript(init_data_script)
                    conn.commit()
                    
        except Exception as e:
            error("初始化数据库失败")
            exception(f"初始化数据库失败: {str(e)}")
            raise e
    
    def execute(self, sql: str, params: Tuple = None) -> sqlite3.Cursor:
        """
        执行SQL语句
        
        Args:
            sql: SQL语句
            params: SQL参数元组
            
        Returns:
            sqlite3.Cursor: 数据库游标
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                conn.commit()
                return cursor
            except Exception as e:
                error(f"执行SQL语句失败: {str(e)}")
                exception(f"执行SQL语句失败: {str(e)}")
                raise e
    
    def execute_many(self, sql: str, params_list: List[Tuple]):
        """
        执行多条SQL语句
        
        Args:
            sql: SQL语句
            params_list: SQL参数列表
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.executemany(sql, params_list)
                conn.commit()
            except Exception as e:
                error(f"执行多条SQL语句失败: {str(e)}")
                exception(f"执行多条SQL语句失败: {str(e)}")
                raise e
    
    def query_one(self, sql: str, params: Tuple = None) -> Optional[Tuple]:
        """
        查询单条记录
        
        Args:
            sql: SQL语句
            params: SQL参数元组
            
        Returns:
            Optional[Tuple]: 查询结果元组，如果没有结果返回 None
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                return cursor.fetchone()
            except Exception as e:
                error(f"查询单条记录失败: {str(e)}")
                exception(f"查询单条记录失败: {str(e)}")
                raise e
    
    def query_all(self, sql: str, params: Tuple = None) -> List[Tuple]:
        """
        查询多条记录
        
        Args:
            sql: SQL语句
            params: SQL参数元组
            
        Returns:
            List[Tuple]: 查询结果列表
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                return cursor.fetchall()
            except Exception as e:
                error(f"查询多条记录失败: {str(e)}")
                exception(f"查询多条记录失败: {str(e)}")
                raise e
    
    def insert(self, table: str, data: Dict[str, Any]) -> int:
        """
        插入数据
        
        Args:
            table: 表名
            data: 要插入的数据字典
            
        Returns:
            int: 新插入记录的ID
        """
        fields = ','.join(data.keys())#把data字典的key值用逗号连接起来 {"a"="b","c"="d"}  ->  "a,c"
        placeholders = ','.join(['?' for _ in data])#把data字典的key值用逗号连接起来 {"a"="b","c"="d"}  ->  "?,?"
        sql = f"INSERT INTO {table} ({fields}) VALUES ({placeholders})"#把fields和placeholders连接起来 {"a"="b","c"="d"}  ->  "INSERT INTO table_name (a,c) VALUES (?,?)"
        info(f"执行SQL语句: {sql}")
        info(f"列表{list(data.values())}")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql, list(data.values()))
                conn.commit()
                debug(f"执行SQL语句成功: {sql}")
                return cursor.lastrowid
            except Exception as e:
                error(f"执行SQL语句失败: {str(e)}")
                exception(f"执行SQL语句失败: {str(e)}")
                raise e

    def update(self, table: str, data: Dict[str, Any], condition: Dict[str, Any]):
        """
        更新数据
        
        Args:
            table: 表名
            data: 要更新的数据字典
            condition: 更新条件字典
        """
        set_clause = ','.join([f"{k}=?" for k in data.keys()])#把data字典的key值用逗号连接起来 {"a"="b","c"="d"}  ->  "a=?,c=?"
        where_clause = ' AND '.join([f"{k}=?" for k in condition.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        
        params = list(data.values()) + list(condition.values())
        self.execute(sql, params)
    
    def delete(self, table: str, condition: Dict[str, Any]):
        """
        删除数据
        
        Args:
            table: 表名
            condition: 删除条件字典
        """
        where_clause = ' AND '.join([f"{k}=?" for k in condition.keys()])
        sql = f"DELETE FROM {table} WHERE {where_clause}"
        
        self.execute(sql, list(condition.values()))
    
    # 用户相关的便捷方法
    def get_user_by_username(self, username: str) -> Optional[Tuple]:
        """根据用户名查询用户"""
        return self.query_one(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )
    
    def get_all_users(self, role: Optional[str] = None) -> List[Tuple]:
        """获取所有用户，可选按角色筛选"""
        if role:
            return self.query_all(
                "SELECT * FROM users WHERE role = ?",
                (role,)
            )
        else:
            return self.query_all("SELECT * FROM users")
    
    def get_teacher_students(self, teacher_id: int) -> List[Tuple]:
        """获取教师的所有学生
        
        Args:
            teacher_id: 教师ID
            
        Returns:
            List[Tuple]: 学生信息列表
        """
        return self.query_all(
            """
            SELECT * FROM users 
            WHERE teacher_id = ? AND role = 'student'
            ORDER BY create_time DESC
            """,
            (teacher_id,)
        )
        
    def assign_teacher(self, student_id: int, teacher_id: int) -> bool:
        """为学生分配指导教师
        
        Args:
            student_id: 学生ID
            teacher_id: 教师ID
            
        Returns:
            bool: 是否分配成功
        """
        try:
            # 验证教师存在且角色正确
            teacher = self.query_one(
                "SELECT * FROM users WHERE id = ? AND role IN ('teacher', 'admin')",
                (teacher_id,)
            )
            if not teacher:
                raise ValueError("指定的教师不存在或角色不正确")
                
            # 验证学生存在且角色正确
            student = self.query_one(
                "SELECT * FROM users WHERE id = ? AND role = 'student'",
                (student_id,)
            )
            if not student:
                raise ValueError("指定的学生不存在或角色不正确")
                
            # 更新学生的指导教师
            self.update(
                "users",
                {"teacher_id": teacher_id},
                {"id": student_id}
            )
            return True
            
        except Exception as e:
            error(f"分配教师失败: {str(e)}")
            return False
            
    def create_user(self, username: str, password: str, role: str, 
                   real_name: str = None, student_id: str = None) -> Optional[int]:
        """创建新用户
        
        Args:
            username: 用户名
            password: 密码
            role: 角色（admin/teacher/student）
            real_name: 真实姓名
            student_id: 学号（仅学生需要）
            
        Returns:
            Optional[int]: 新用户的ID，如果创建失败返回 None
        """
        try:
            # 准备用户数据
            user_data = {
                "username": username,
                "password": password,
                "role": role,
                "real_name": real_name,
                "student_id": student_id,
                "create_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # 插入用户记录
            user_id = self.insert("users", user_data)
            
            # 如果是教师或管理员，设置teacher_id为自己的id
            if role in ('teacher', 'admin'):
                self.update(
                    "users",
                    {"teacher_id": user_id},
                    {"id": user_id}
                )
                
            return user_id
            
        except Exception as e:
            error(f"创建用户失败: {str(e)}")
            return None
    
    # 实验相关操作
    def get_experiments_by_teacher(self, teacher_id: int) -> List[Tuple]:
        """获取教师创建的所有实验
        
        Args:
            teacher_id: 教师ID
            
        Returns:
            List[Tuple]: 实验信息列表
        """
        with self.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM experiments WHERE creator_id = ? ORDER BY create_time DESC",
                (teacher_id,)
            )
            return cursor.fetchall()
    
    def get_experiment_by_id(self, experiment_id: int) -> Optional[Tuple]:
        """根据ID获取实验详情
        
        Args:
            experiment_id: 实验ID
            
        Returns:
            Optional[Tuple]: 实验信息，如果不存在返回 None
        """
        with self.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM experiments WHERE id = ?",
                (experiment_id,)
            )
            return cursor.fetchone()
    
    # 提交相关操作
    def get_submissions_by_experiment(self, experiment_id: int) -> List[Tuple]:
        """获取实验的所有提交
        
        Args:
            experiment_id: 实验ID
            
        Returns:
            List[Tuple]: 提交信息列表
        """
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT s.*, u.username, u.real_name 
                FROM submissions s
                JOIN users u ON s.student_id = u.id
                WHERE s.experiment_id = ?
                ORDER BY s.submit_time DESC
                """,
                (experiment_id,)
            )
            return cursor.fetchall()
    
    def get_student_submissions(self, student_id: int) -> List[Tuple]:
        """获取学生的所有提交
        
        Args:
            student_id: 学生ID
            
        Returns:
            List[Tuple]: 提交信息列表
        """
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT s.*, e.title as experiment_title
                FROM submissions s
                JOIN experiments e ON s.experiment_id = e.id
                WHERE s.student_id = ?
                ORDER BY s.submit_time DESC
                """,
                (student_id,)
            )
            return cursor.fetchall()
    
    # 通用查询方法
    def execute_query(self, query: str, params: Tuple = ()) -> List[Tuple]:
        """执行自定义查询
        
        Args:
            query: SQL查询语句
            params: 查询参数元组
            
        Returns:
            List[Tuple]: 查询结果列表
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchall()
    
    def execute_update(self, query: str, params: Tuple = ()) -> int:
        """执行更新操作
        
        Args:
            query: SQL更新语句
            params: 更新参数元组
            
        Returns:
            int: 受影响的行数
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            conn.commit()
            return cursor.rowcount

# 创建全局数据库实例
db = DatabaseUtils()

# 导出全局实例
__all__ = ['DatabaseUtils', 'db']
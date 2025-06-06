#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
用户基类
定义所有用户共有的属性和方法
"""

from datetime import datetime
from utils import DatabaseUtils 
from utils import ValidationUtils
import utils
class User:
    """
    用户基类
    
    属性：
    - id: 用户ID
    - username: 用户名
    - password: 密码
    - role: 角色（admin/teacher/student）
    - real_name: 真实姓名
    - teacher_id: 指导教师ID
    - create_time: 创建时间
    """
    
    def __init__(self):
        self.id = None
        self.username = None
        self.password = None
        self.role = None
        self.real_name = None
        self.create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        utils.debug(f"{self.create_time}")
        self.student_id = None
        self.teacher_id = None
        self.db = DatabaseUtils()
        utils.debug(f"用户对象初始化:完成")
    @classmethod
    def get_by_username(cls, username: str):
        """
        根据用户名获取用户
        
        Args:
            username: 用户名
            
        Returns:
            User: 用户对象，如果不存在返回 None
        """
        db = DatabaseUtils()
        user_data = db.get_user_by_username(username)
        if not user_data:
            return None
        utils.debug(f"获取用户数据: {user_data[0]}")
        user = cls()
        user.id = user_data[0]
        user.username = user_data[1]
        user.password = user_data[2]
        user.role = user_data[3]
        user.real_name = user_data[4]
        user.student_id = user_data[5]
        user.teacher_id = user_data[6]
        user.create_time = datetime.strptime(user_data[7], '%Y-%m-%d %H:%M:%S')
        return user
    
    def login(self, username: str, password: str) -> bool:
        """
        用户登录方法
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            bool: 登录是否成功
        """
        # 验证用户名和密码格式

            
        # 查询用户
       
        user_data = self.db.execute_query(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
        
        if not user_data:
            return False
            
        # 登录成功，更新用户信息
        utils.debug(f"用户信息: {user_data[0]}")
        user = user_data[0]
        self.id = user[0]
        self.username = user[1]
        self.password = user[2]
        self.role = user[3]
        self.real_name = user[4]
        self.student_id = user[5]
        self.teacher_id = user[6]
        self.create_time = datetime.strptime(user[7], '%Y-%m-%d %H:%M:%S')
        return True
    
    def register(self, username: str, password: str, role: str, real_name: str = None) -> bool:
        """
        注册新用户
        
        Args:
            username: 用户名
            password: 密码
            role: 角色
            real_name: 真实姓名
            
        Returns:
            bool: 注册是否成功
        """
        # 验证用户名和密码格式

            
        # 检查用户名是否已存在
        if self.db.get_user_by_username(username):
            utils.warning(f"用户名 {username} 已存在")
            utils.exception(f"用户名 {username} 已存在")
            raise ValueError("用户名已存在")
            
        # 插入新用户
        try:
            self.db.execute_update(
                """
                INSERT INTO users (username, password, role, real_name, create_time)
                VALUES (?, ?, ?, ?, ?)
                """,
                (username, password, role, real_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            )
            return True
        except Exception as e:
            utils.warning(f"注册失败: {str(e)}")
            utils.exception(f"注册失败: {str(e)}")
            raise ValueError(f"注册失败: {str(e)}")
    
    def logout(self):
        """用户登出方法"""
        self.id = None
        self.username = None
        self.password = None
        self.role = None
        self.real_name = None
        self.teacher_id = None
        self.student_id = None
        self.create_time = None

    def change_password(self, old_password: str, new_password: str) -> bool:
        """
        修改密码
        
        Args:
            old_password: 旧密码
            new_password: 新密码
            
        Returns:
            bool: 修改是否成功
        """
        # 验证旧密码
        if not self.password == old_password:
            raise ValueError("旧密码错误")
            
        # 验证新密码格式
        is_valid, error_msg = ValidationUtils.validate_password(new_password)
        if not is_valid:
            raise ValueError(error_msg)
            
        # 更新密码
        try:
            self.db.execute_update(
                "UPDATE users SET password = ? WHERE id = ?",
                (new_password, self.id)
            )
            self.password = new_password
            return True
        except Exception as e:
            raise ValueError(f"修改密码失败: {str(e)}")
    
    def get_info(self) -> dict:
        """
        获取用户信息
        
        Returns:
            dict: 用户信息字典
        """
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'role': self.role,
            'real_name': self.real_name,
            'create_time': self.create_time,
            'student_id': self.student_id,
            'teacher_id': self.teacher_id
        }
    
    def update_info(self, info_dict: dict) -> bool:
        """
        更新用户信息
        
        Args:
            info_dict: 包含要更新的信息的字典
            
        Returns:
            bool: 更新是否成功
        """
        try:
            update_fields = []
            update_values = []
            
            # 构建更新字段
            if 'real_name' in info_dict:
                update_fields.append("real_name = ?")
                update_values.append(info_dict['real_name'])
                
            if not update_fields:
                return False
                
            # 添加用户ID
            update_values.append(self.id)
            
            # 执行更新
            query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"
            self.db.execute_update(query, tuple(update_values))
            
            # 更新对象属性
            if 'real_name' in info_dict:
                self.real_name = info_dict['real_name']
                
            return True
        except Exception as e:
            raise ValueError(f"更新信息失败: {str(e)}")

# 在此处实现用户模型相关代码 
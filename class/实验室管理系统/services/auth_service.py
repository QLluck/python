#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
认证服务
处理用户登录、注册、权限验证等功能
"""

import hashlib
from datetime import datetime
from database import db
from utils.logger import debug, error, info, warning

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        """对密码进行哈希处理"""
        return hashlib.sha256(password.encode()).hexdigest()
        #sha256 算法将密码进行加密,  password.encode() 转换成字节序列 
        #hexdigest() 是将哈希值转换成十六进制字符串
    @staticmethod
    def verify_login(username: str, password: str) -> tuple[bool, str, str]:
        """
        验证用户登录
         
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            tuple[bool, str, str]: (是否成功, 错误消息, 用户角色)
        """
        try:
            # 查询用户
            hashed_password = AuthService.hash_password(password)
            result = db.query_one(
                "SELECT role FROM users WHERE username = ? AND password = ?",
                (username, hashed_password)
            )
            
            if not result:
                warning(f"{username}尝试登录，但是密码错误")
                return False, "用户名或密码错误", ""
            
            # 更新最后登录时间
            db.update(
                'users',
                {'last_login': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
                {'username': username}
            )
            
            role = result[0] #查询表第一个字段
            info(f"用户 {username} 登录成功，角色：{role}")
            return True, "", role
            
        except Exception as e:
            error(f"登录验证失败: {str(e)}")
            return False, f"系统错误: {str(e)}", ""
    
    @staticmethod
    def register_user(username: str, password: str, role: str = "student", real_name: str = "") -> tuple[bool, str]:
        """
        注册新用户
        
        Args:
            username: 用户名
            password: 密码
            role: 用户角色，默认为student
            real_name: 真实姓名，可选
            
        Returns:
            tuple[bool, str]: (是否成功, 错误消息)
        """
        try:
            # 检查用户名是否已存在
            result = db.query_one(
                "SELECT 1 FROM users WHERE username = ?",
                (username,)
            )
            
            if result:
                return False, "用户名已存在"
            
            # 插入新用户
            hashed_password = AuthService.hash_password(password)
            user_data = {
                'username': username,
                'password': hashed_password,
                'role': role,
                'real_name': real_name,
                'create_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            db.insert('users', user_data)
            
            info(f"新用户注册成功: {username}, 角色: {role}")
            return True, ""
            
        except Exception as e:
            error(f"用户注册失败: {str(e)}")
            return False, f"系统错误: {str(e)}"
            
    @staticmethod
    def change_password(username: str, old_password: str, new_password: str) -> tuple[bool, str]:
        """
        修改用户密码
        
        Args:
            username: 用户名
            old_password: 旧密码
            new_password: 新密码
            
        Returns:
            tuple[bool, str]: (是否成功, 错误消息)
        """
        try:
            # 验证旧密码
            old_hashed = AuthService.hash_password(old_password)
            result = db.query_one(
                "SELECT 1 FROM users WHERE username = ? AND password = ?",
                (username, old_hashed)
            )
            
            if not result:
                return False, "原密码错误"
            
            # 更新密码
            new_hashed = AuthService.hash_password(new_password)
            db.update(
                'users',
                {'password': new_hashed},
                {'username': username}
            )
            
            info(f"用户 {username} 密码修改成功")
            return True, ""
            
        except Exception as e:
            error(f"密码修改失败: {str(e)}")
            return False, f"系统错误: {str(e)}" 
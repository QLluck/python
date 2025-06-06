#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
哈希加密工具类
提供密码加密和验证功能
"""

import hashlib
import os
import base64
from typing import Tuple
from .logger import debug, info, warning, error

class HashUtils:
    """
    哈希加密工具类
    使用 SHA-256 算法，并添加随机盐值
    """
    
    SALT_LENGTH = 16  # 盐值长度（字节）
    
    @classmethod
    def generate_salt(cls) -> bytes:
        """生成随机盐值
        
        Returns:
            bytes: 随机盐值
        """
        return os.urandom(cls.SALT_LENGTH)
    
    @classmethod
    def hash_password(cls, password: str) -> Tuple[str, str]:
        """对密码进行哈希加密
        
        Args:
            password: 原始密码
            
        Returns:
            Tuple[str, str]: (加密后的密码, Base64编码的盐值)
        """
        # 生成随机盐值
        info(f"对密码进行哈希加密")
        salt = cls.generate_salt()
        
        try:
            # 将密码和盐值组合并进行哈希
            password_bytes = password.encode('utf-8')
            hash_obj = hashlib.sha256()
            hash_obj.update(salt)
            hash_obj.update(password_bytes)
            hashed_password = hash_obj.hexdigest()
            
            # 将盐值转换为Base64字符串
            salt_b64 = base64.b64encode(salt).decode('utf-8')
            
            debug(f"密码加密成功: {password} -> {hashed_password}")
            return hashed_password, salt_b64
            
        except Exception as e:
            error(f"密码加密失败: {str(e)}")
            raise e
    
    @classmethod
    def verify_password(cls, password: str, hashed_password: str, salt_b64: str) -> bool:
        """验证密码是否正确
        
        Args:
            password: 要验证的密码
            hashed_password: 存储的哈希密码
            salt_b64: Base64编码的盐值
            
        Returns:
            bool: 密码是否正确

        """
        info(f"验证密码的哈希值是否正确")
        try:
            # 将Base64盐值转换回bytes
            salt = base64.b64decode(salt_b64.encode('utf-8'))
            
            # 使用相同的盐值对输入的密码进行哈希
            password_bytes = password.encode('utf-8')
            hash_obj = hashlib.sha256()
            hash_obj.update(salt)
            hash_obj.update(password_bytes)
            computed_hash = hash_obj.hexdigest()
            
            # 比较计算的哈希值和存储的哈希值
            is_valid = computed_hash == hashed_password
            debug(f"密码验证{'成功' if is_valid else '失败'}")
            return is_valid
            
        except Exception as e:
            error(f"密码验证失败: {str(e)}")
            return False
    
    @classmethod
    def hash_string(cls, text: str) -> str:
        """对字符串进行简单的哈希（不使用盐值）
        
        Args:
            text: 要哈希的字符串
            
        Returns:
            str: 哈希后的字符串
        """
        try:
            hash_obj = hashlib.sha256()
            hash_obj.update(text.encode('utf-8'))
            return hash_obj.hexdigest()
        except Exception as e:
            error(f"字符串哈希失败: {str(e)}")
            raise e 
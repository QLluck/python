#!/usr/bin/env python3
"""
创建大尺寸测试图像（模拟真实医学图像场景）
"""

import cv2
import numpy as np
from pathlib import Path

def create_large_test_image():
    """创建一个 1288x2932 的测试图像（与日志中的尺寸一致）"""
    
    # 读取一张小图像
    small_img_path = Path("archive/Original Images/Original Images/Monkey Pox/M31_02.jpg")
    if not small_img_path.exists():
        print(f"❌ 找不到源图像: {small_img_path}")
        return None
    
    small_img = cv2.imread(str(small_img_path))
    print(f"📸 源图像尺寸: {small_img.shape}")
    
    # 放大到目标尺寸 (1288, 2932)
    target_size = (2932, 1288)  # (width, height)
    large_img = cv2.resize(small_img, target_size, interpolation=cv2.INTER_CUBIC)
    
    print(f"🔍 放大后尺寸: {large_img.shape}")
    
    # 添加一些噪声和细节，使其更真实
    noise = np.random.normal(0, 5, large_img.shape).astype(np.int16)
    large_img = np.clip(large_img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    # 保存
    output_path = Path("test_images/large_test.jpg")
    output_path.parent.mkdir(exist_ok=True)
    cv2.imwrite(str(output_path), large_img)
    
    print(f"✅ 已保存大图像到: {output_path}")
    print(f"📊 文件大小: {output_path.stat().st_size / 1024:.1f} KB")
    
    return output_path

if __name__ == "__main__":
    create_large_test_image()

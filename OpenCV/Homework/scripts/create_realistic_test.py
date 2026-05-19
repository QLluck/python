#!/usr/bin/env python3
"""
创建真实的测试图像：包含明显的物体和背景
"""

import cv2
import numpy as np
from pathlib import Path

def create_realistic_test_image():
    """创建一个真实的测试图像"""
    
    # 创建大图像
    h, w = 1288, 2932
    img = np.ones((h, w), dtype=np.uint8) * 220  # 亮背景
    
    # 添加几个深色"病变"区域
    lesions = [
        # (center_x, center_y, radius, center_intensity, edge_intensity)
        (700, 400, 120, 60, 140),   # 大病变
        (1800, 600, 80, 70, 150),   # 中等病变
        (1200, 900, 60, 50, 130),   # 小病变
    ]
    
    for cx, cy, radius, center_val, edge_val in lesions:
        # 创建渐变圆形
        for r in range(radius, 0, -5):
            # 从边缘到中心的渐变
            intensity = edge_val + (center_val - edge_val) * (radius - r) / radius
            cv2.circle(img, (cx, cy), r, int(intensity), -1)
    
    # 添加一些纹理噪声
    noise = np.random.normal(0, 8, img.shape).astype(np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    # 添加一些"血管"结构
    for i in range(5):
        pt1 = (np.random.randint(0, w), np.random.randint(0, h))
        pt2 = (np.random.randint(0, w), np.random.randint(0, h))
        cv2.line(img, pt1, pt2, 180, 3)
    
    # 转换为 BGR
    img_bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    
    # 保存
    output_path = Path("test_images/realistic_test.jpg")
    cv2.imwrite(str(output_path), img_bgr)
    
    print(f"✅ 已创建真实测试图像: {output_path}")
    print(f"📊 图像尺寸: {w}x{h}")
    print(f"📍 病变位置:")
    for i, (cx, cy, radius, center_val, edge_val) in enumerate(lesions, 1):
        print(f"   病变 {i}: 中心({cx}, {cy}), 半径{radius}, 灰度{center_val}-{edge_val}")
    print(f"\n💡 测试建议:")
    print(f"   - 点击病变中心 (700, 400) - 应该分割整个病变")
    print(f"   - 点击背景 (100, 100) - 应该只分割背景")
    print(f"   - 点击病变边缘 (820, 400) - 测试边界检测")
    
    return output_path

if __name__ == "__main__":
    create_realistic_test_image()

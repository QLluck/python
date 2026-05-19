#!/usr/bin/env python3
"""
简单测试：直接测试 floodFill 行为
"""

import cv2
import numpy as np

# 创建简单测试图像
img = np.ones((400, 400), dtype=np.uint8) * 200  # 背景 200

# 添加一个深色圆形（中心 50，边缘渐变到 150）
center = (200, 200)
for r in range(80, 0, -5):
    intensity = 50 + (80 - r) * 1.25
    cv2.circle(img, center, r, int(intensity), -1)

print("测试图像:")
print(f"  尺寸: {img.shape}")
print(f"  中心值: {img[200, 200]}")
print(f"  边缘值: {img[200, 280]}")
print(f"  背景值: {img[50, 50]}")

# 测试不同阈值的 floodFill
print("\n测试 floodFill (梯度模式):")
print(f"  {'阈值':<10} {'分割像素':<12} {'占比'}")

for T in [10, 20, 30, 40, 50]:
    mask = np.zeros((402, 402), np.uint8)
    flags = 8 | (255 << 8)
    
    cv2.floodFill(
        img.copy(),
        mask,
        (200, 200),
        255,
        (T,),
        (T,),
        flags
    )
    
    result = mask[1:-1, 1:-1]
    pixel_count = np.sum(result > 0)
    percentage = (pixel_count / (400 * 400)) * 100
    
    print(f"  {T:<10} {pixel_count:<12} {percentage:.2f}%")

# 测试固定范围模式
print("\n测试 floodFill (固定范围模式):")
print(f"  {'阈值':<10} {'分割像素':<12} {'占比'}")

for T in [10, 20, 30, 40, 50]:
    mask = np.zeros((402, 402), np.uint8)
    flags = 8 | cv2.FLOODFILL_FIXED_RANGE | (255 << 8)
    
    cv2.floodFill(
        img.copy(),
        mask,
        (200, 200),
        255,
        (T,),
        (T,),
        flags
    )
    
    result = mask[1:-1, 1:-1]
    pixel_count = np.sum(result > 0)
    percentage = (pixel_count / (400 * 400)) * 100
    
    print(f"  {T:<10} {pixel_count:<12} {percentage:.2f}%")

print("\n结论:")
print("  梯度模式应该随阈值变化而变化")
print("  如果所有阈值结果相同，说明有其他问题")

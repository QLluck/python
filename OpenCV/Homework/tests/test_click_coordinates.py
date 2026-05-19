#!/usr/bin/env python3
"""
诊断点击坐标问题
"""

import cv2
import numpy as np
import requests
from pathlib import Path
import base64

def test_click_coordinates():
    """测试点击坐标是否准确"""
    
    # 创建一个带有明显标记的测试图像
    h, w = 800, 1200
    img = np.ones((h, w, 3), dtype=np.uint8) * 200
    
    # 在特定位置画圆圈和坐标
    test_points = [
        (100, 100, "左上"),
        (600, 400, "中心"),
        (1100, 700, "右下"),
    ]
    
    for x, y, label in test_points:
        # 画圆圈
        cv2.circle(img, (x, y), 30, (0, 0, 255), 3)
        # 画十字
        cv2.line(img, (x-40, y), (x+40, y), (0, 0, 255), 2)
        cv2.line(img, (x, y-40), (x, y+40), (0, 0, 255), 2)
        # 写坐标
        cv2.putText(img, f"({x},{y})", (x-50, y-50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(img, label, (x-30, y+60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
    # 保存测试图像
    test_path = Path("test_images/coordinate_test.jpg")
    cv2.imwrite(str(test_path), img)
    print(f"✅ 创建坐标测试图像: {test_path}")
    print(f"📐 图像尺寸: {w}x{h}")
    
    # 测试每个点
    print(f"\n{'测试点':<15} {'发送坐标':<15} {'种子值':<10} {'分割像素':<12} {'状态'}")
    print("-"*70)
    
    url = "http://localhost:8000/api/ml/click-segment"
    
    with open(test_path, 'rb') as f:
        image_data = f.read()
    
    for x, y, label in test_points:
        files = {'file': ('test.jpg', image_data, 'image/jpeg')}
        data = {
            'click_x': x,
            'click_y': y,
            'max_side': 1280
        }
        
        try:
            response = requests.post(url, files=files, data=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    debug_info = result.get('debug_info', {})
                    click_pos = debug_info.get('click_position', {})
                    seed_value = debug_info.get('seed_value', 'N/A')
                    seg_pixels = debug_info.get('segmented_pixels', 0)
                    
                    # 检查坐标是否匹配
                    if click_pos.get('x') == x and click_pos.get('y') == y:
                        status = "✅ 坐标正确"
                    else:
                        status = f"❌ 坐标偏移: ({click_pos.get('x')}, {click_pos.get('y')})"
                    
                    print(f"{label:<15} ({x},{y})<10 {seed_value:<10} {seg_pixels:<12} {status}")
                else:
                    print(f"{label:<15} ({x},{y})<10 错误: {result.get('error')}")
            else:
                print(f"{label:<15} ({x},{y})<10 HTTP {response.status_code}")
        except Exception as e:
            print(f"{label:<15} ({x},{y})<10 异常: {str(e)[:30]}")
    
    print("\n💡 说明:")
    print("  - 如果种子值接近 200（背景色），说明坐标正确")
    print("  - 如果种子值接近 0（红色标记），说明点击在标记上")
    print("  - 如果坐标偏移，需要检查前端坐标转换")

if __name__ == "__main__":
    test_click_coordinates()

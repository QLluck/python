#!/usr/bin/env python3
"""
测试真实图像的点击分割
"""

import cv2
import numpy as np
import requests
from pathlib import Path

def test_realistic_image():
    """测试真实图像"""
    
    image_path = Path("test_images/realistic_test.jpg")
    
    if not image_path.exists():
        print("❌ 测试图像不存在")
        return
    
    # 读取图像
    img = cv2.imread(str(image_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    
    print("="*60)
    print("真实图像点击分割测试")
    print("="*60)
    print(f"\n📸 图像: {w}x{h}")
    
    # 测试点击位置
    test_clicks = [
        (700, 400, "病变中心"),
        (820, 400, "病变边缘"),
        (100, 100, "背景"),
        (1800, 600, "另一个病变"),
    ]
    
    url = "http://localhost:8000/api/ml/click-segment"
    
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    print(f"\n{'位置':<20} {'种子值':<10} {'分割像素':<12} {'占比':<10} {'耗时'}")
    print("-"*70)
    
    for click_x, click_y, desc in test_clicks:
        seed_val = gray[click_y, click_x]
        
        files = {'file': ('test.jpg', image_data, 'image/jpeg')}
        data = {
            'click_x': click_x,
            'click_y': click_y,
            'max_side': 1280
        }
        
        try:
            response = requests.post(url, files=files, data=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    perf = result.get('performance', {})
                    total_ms = perf.get('total_ms', 0)
                    
                    # 解码 mask 来计算像素数
                    import base64
                    mask_b64 = result.get('mask_b64', '')
                    mask_bytes = base64.b64decode(mask_b64)
                    mask_array = np.frombuffer(mask_bytes, dtype=np.uint8)
                    mask = cv2.imdecode(mask_array, cv2.IMREAD_GRAYSCALE)
                    
                    if mask is not None:
                        pixel_count = np.sum(mask > 0)
                        percentage = (pixel_count / (h * w)) * 100
                        
                        status = "✅"
                        if percentage < 0.1:
                            status = "⚠️  太小"
                        elif percentage > 20:
                            status = "⚠️  太大"
                        
                        print(f"{desc:<20} {seed_val:<10} {pixel_count:<12} {percentage:<10.2f}% {total_ms}ms {status}")
                    else:
                        print(f"{desc:<20} {seed_val:<10} {'解码失败':<12}")
                else:
                    print(f"{desc:<20} {seed_val:<10} 错误: {result.get('error')}")
            else:
                print(f"{desc:<20} {seed_val:<10} HTTP {response.status_code}")
        except Exception as e:
            print(f"{desc:<20} {seed_val:<10} 异常: {str(e)[:30]}")
    
    print("\n" + "="*60)
    print("💡 分析:")
    print("  - 病变中心: 应该分割整个病变区域 (1-5%)")
    print("  - 病变边缘: 可能分割部分病变")
    print("  - 背景: 应该分割大部分背景 (>50%)")
    print("="*60)

if __name__ == "__main__":
    test_realistic_image()

#!/usr/bin/env python3
"""
性能测试脚本：测试优化后的分割性能
"""

import time
import requests
from pathlib import Path

def test_click_segment_performance():
    """测试点击分割的性能"""
    
    # 使用测试图像 - 尝试多个目录
    test_dirs = [
        Path("test_images"),
        Path("archive/Original Images/Original Images/Monkey Pox"),
        Path("archive/Original Images/Original Images/Others"),
    ]
    
    test_images = []
    for test_dir in test_dirs:
        if test_dir.exists():
            test_images.extend(list(test_dir.glob("*.jpg")))
            test_images.extend(list(test_dir.glob("*.png"))[:5])  # 限制 PNG 数量
            if test_images:
                break
    
    if not test_images:
        print("❌ 没有找到测试图像")
        return
    
    # 使用第一张图像
    test_image = test_images[0]
    print(f"📸 使用测试图像: {test_image.name}")
    print(f"📁 图像路径: {test_image}")
    
    # 准备请求
    url = "http://localhost:8000/api/ml/click-segment"
    
    # 读取图像
    with open(test_image, 'rb') as f:
        image_data = f.read()
    
    # 获取图像尺寸
    import cv2
    img = cv2.imread(str(test_image))
    h, w = img.shape[:2]
    print(f"📐 图像尺寸: {w}x{h}")
    
    # 测试多个点击位置（基于实际图像尺寸）
    test_clicks = [
        (w // 2, h // 2),      # 中心
        (w // 3, h // 3),      # 左上区域
        (2 * w // 3, 2 * h // 3),  # 右下区域
    ]
    
    print("\n" + "="*60)
    print("性能测试结果")
    print("="*60)
    
    times = []
    
    for i, (click_x, click_y) in enumerate(test_clicks, 1):
        print(f"\n测试 {i}/3: 点击位置 ({click_x}, {click_y})")
        
        files = {'file': ('test.jpg', image_data, 'image/jpeg')}
        data = {
            'click_x': click_x,
            'click_y': click_y,
            'max_side': 1280
        }
        
        start = time.time()
        response = requests.post(url, files=files, data=data)
        elapsed = time.time() - start
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                perf = result.get('performance', {})
                total_ms = perf.get('total_ms', 0)
                image_size = perf.get('image_size', 'unknown')
                
                times.append(total_ms)
                
                print(f"  ✅ 成功")
                print(f"  📊 图像尺寸: {image_size}")
                print(f"  ⏱️  总耗时: {total_ms} ms ({elapsed:.2f}s)")
                print(f"  🎯 置信度: {result.get('confidence', 0):.2f}")
            else:
                print(f"  ❌ 失败: {result.get('error')}")
        else:
            print(f"  ❌ HTTP 错误: {response.status_code}")
    
    # 统计结果
    if times:
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print("\n" + "="*60)
        print("📈 性能统计")
        print("="*60)
        print(f"  平均耗时: {avg_time:.0f} ms")
        print(f"  最快耗时: {min_time:.0f} ms")
        print(f"  最慢耗时: {max_time:.0f} ms")
        
        # 对比优化前的性能（7-9秒）
        old_avg = 8000  # ms
        speedup = old_avg / avg_time
        
        print(f"\n🚀 性能提升:")
        print(f"  优化前: ~{old_avg} ms")
        print(f"  优化后: ~{avg_time:.0f} ms")
        print(f"  提速: {speedup:.1f}x")
        
        if speedup >= 20:
            print(f"  🎉 优秀！达到预期目标 (20-50x)")
        elif speedup >= 10:
            print(f"  ✅ 良好！接近预期目标")
        elif speedup >= 5:
            print(f"  ⚠️  一般，还有优化空间")
        else:
            print(f"  ❌ 需要进一步优化")

if __name__ == "__main__":
    print("🔬 开始性能测试...")
    print("请确保服务器正在运行 (http://localhost:8000)")
    print()
    
    try:
        test_click_segment_performance()
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

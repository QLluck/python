#!/usr/bin/env python3
"""
诊断脚本：检查点击分割的实际行为
"""

import cv2
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

from app.core.segment import segment_region_grow, SegmentParams
from app.ml.predictor import Predictor


def diagnose_click_segmentation():
    """诊断点击分割问题"""
    
    print("="*60)
    print("点击分割诊断")
    print("="*60)
    
    # 1. 加载测试图像
    test_image_path = Path("test_images/large_test.jpg")
    if not test_image_path.exists():
        print("❌ 测试图像不存在")
        return
    
    img = cv2.imread(str(test_image_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    
    print(f"\n📸 图像信息:")
    print(f"  尺寸: {w}x{h}")
    print(f"  灰度范围: [{gray.min()}, {gray.max()}]")
    print(f"  平均值: {gray.mean():.1f}")
    print(f"  标准差: {gray.std():.1f}")
    
    # 2. 测试点击位置
    click_x, click_y = w // 2, h // 2
    seed_value = gray[click_y, click_x]
    
    print(f"\n🎯 点击信息:")
    print(f"  坐标: ({click_x}, {click_y})")
    print(f"  种子值: {seed_value}")
    
    # 3. 使用 ML 预测参数
    predictor = Predictor()
    try:
        predictor.load_models()
        print(f"  ✅ ML 模型已加载")
    except:
        print(f"  ⚠️  ML 模型未加载，使用启发式")
    
    prediction = predictor.predict_for_click(gray, click_x, click_y)
    predicted_T = prediction["parameters"]["grow_T"]
    
    print(f"\n🤖 ML 预测:")
    print(f"  预测阈值: {predicted_T:.1f}")
    print(f"  置信度: {prediction['confidence']:.2f}")
    
    # 4. 测试不同阈值
    test_thresholds = [10, 20, 30, predicted_T, 40, 50]
    
    print(f"\n🧪 测试不同阈值:")
    print(f"  {'阈值':<10} {'分割像素':<12} {'占比':<10} {'状态'}")
    print(f"  {'-'*10} {'-'*12} {'-'*10} {'-'*20}")
    
    results = []
    for T in test_thresholds:
        params = SegmentParams(method="region_grow", grow_T=int(T))
        mask = segment_region_grow(gray, params, manual_seed=(click_x, click_y))
        
        pixel_count = np.sum(mask > 0)
        percentage = (pixel_count / (h * w)) * 100
        
        # 判断状态
        if pixel_count < 100:
            status = "❌ 太小（几乎没分割）"
        elif percentage < 1:
            status = "⚠️  偏小"
        elif percentage < 10:
            status = "✅ 正常"
        elif percentage < 30:
            status = "⚠️  偏大"
        else:
            status = "❌ 太大（过度分割）"
        
        print(f"  {T:<10.1f} {pixel_count:<12} {percentage:<10.2f}% {status}")
        results.append((T, mask, pixel_count, percentage))
    
    # 5. 可视化结果
    print(f"\n📊 生成可视化对比图...")
    
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    fig.suptitle(f'点击分割诊断 - 点击位置: ({click_x}, {click_y}), 种子值: {seed_value}', 
                 fontsize=14, fontweight='bold')
    
    # 显示原图
    ax = axes[0, 0]
    ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    ax.plot(click_x, click_y, 'r+', markersize=20, markeredgewidth=3)
    ax.set_title('原图 + 点击位置', fontsize=10)
    ax.axis('off')
    
    # 显示灰度图
    ax = axes[0, 1]
    ax.imshow(gray, cmap='gray')
    ax.plot(click_x, click_y, 'r+', markersize=20, markeredgewidth=3)
    ax.set_title(f'灰度图\n种子值: {seed_value}', fontsize=10)
    ax.axis('off')
    
    # 显示局部区域
    ax = axes[0, 2]
    crop_size = 200
    x1 = max(0, click_x - crop_size)
    y1 = max(0, click_y - crop_size)
    x2 = min(w, click_x + crop_size)
    y2 = min(h, click_y + crop_size)
    local_region = gray[y1:y2, x1:x2]
    ax.imshow(local_region, cmap='gray')
    ax.plot(click_x - x1, click_y - y1, 'r+', markersize=15, markeredgewidth=2)
    ax.set_title(f'局部区域 ({crop_size*2}x{crop_size*2})', fontsize=10)
    ax.axis('off')
    
    # 显示直方图
    ax = axes[0, 3]
    ax.hist(gray.ravel(), bins=50, color='gray', alpha=0.7)
    ax.axvline(seed_value, color='r', linestyle='--', linewidth=2, label=f'种子值: {seed_value}')
    ax.axvline(seed_value - predicted_T, color='b', linestyle=':', linewidth=1, label=f'阈值范围')
    ax.axvline(seed_value + predicted_T, color='b', linestyle=':', linewidth=1)
    ax.set_title('灰度直方图', fontsize=10)
    ax.legend(fontsize=8)
    ax.set_xlabel('灰度值')
    ax.set_ylabel('像素数')
    
    # 显示不同阈值的结果
    for idx in range(4):
        if idx < len(results):
            T, mask, pixel_count, percentage = results[idx + 2]  # 跳过前两个
            
            # 创建叠加图
            overlay = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            overlay[mask > 0] = overlay[mask > 0] * 0.5 + np.array([255, 0, 0]) * 0.5
            
            ax = axes[1, idx]
            ax.imshow(overlay)
            ax.plot(click_x, click_y, 'g+', markersize=15, markeredgewidth=2)
            ax.set_title(f'T={T:.0f}\n{pixel_count} 像素 ({percentage:.1f}%)', fontsize=10)
            ax.axis('off')
    
    plt.tight_layout()
    
    output_path = Path('test_images/click_diagnosis.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✅ 诊断图已保存: {output_path}")
    plt.close()  # 关闭图形，不显示
    print(f"\n🔍 边界检测分析:")
    median_val = np.median(gray)
    lower = int(max(0, 0.7 * median_val))
    upper = int(min(255, 1.3 * median_val))
    edges = cv2.Canny(gray, lower, upper)
    edge_count = np.sum(edges > 0)
    edge_percentage = (edge_count / (h * w)) * 100
    
    print(f"  Canny 阈值: [{lower}, {upper}]")
    print(f"  边缘像素: {edge_count} ({edge_percentage:.2f}%)")
    
    # 7. 分析问题
    print(f"\n🔬 问题分析:")
    
    # 检查是否有过度分割
    _, best_mask, best_count, best_pct = results[3]  # 使用预测阈值的结果
    
    if best_count < 100:
        print(f"  ❌ 问题1: 分割结果太小（{best_count} 像素）")
        print(f"     可能原因:")
        print(f"     - 阈值太小 (当前: {predicted_T:.1f})")
        print(f"     - 边界检测太严格")
        print(f"     - 种子点位置不佳")
    elif best_pct > 30:
        print(f"  ❌ 问题2: 过度分割（{best_pct:.1f}%）")
        print(f"     可能原因:")
        print(f"     - 阈值太大 (当前: {predicted_T:.1f})")
        print(f"     - 图像对比度低")
        print(f"     - 边界不清晰")
    else:
        print(f"  ✅ 分割结果正常")
    
    # 检查图像特征
    if gray.std() < 20:
        print(f"  ⚠️  图像对比度很低 (std={gray.std():.1f})")
        print(f"     建议: 增加预处理对比度增强")
    
    if edge_percentage < 1:
        print(f"  ⚠️  边缘很少 ({edge_percentage:.2f}%)")
        print(f"     建议: 调整 Canny 阈值或使用其他边界检测")


if __name__ == "__main__":
    diagnose_click_segmentation()

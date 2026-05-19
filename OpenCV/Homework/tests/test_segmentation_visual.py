#!/usr/bin/env python3
"""
可视化测试脚本：对比不同算法的分割效果
"""

import cv2
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from app.core.segment import segment_region_grow, SegmentParams


def create_test_image():
    """创建一个测试图像，包含不同灰度的区域"""
    img = np.ones((400, 600), dtype=np.uint8) * 200  # 背景：亮灰色
    
    # 添加一个深色圆形病变（中心深，边缘渐变）
    center = (200, 200)
    for r in range(80, 0, -5):
        intensity = 50 + (80 - r) * 1.5  # 从边缘150到中心50的渐变
        cv2.circle(img, center, r, int(intensity), -1)
    
    # 添加一个浅色区域
    cv2.rectangle(img, (400, 100), (550, 250), 180, -1)
    
    # 添加一些噪声
    noise = np.random.normal(0, 5, img.shape).astype(np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    return img


def test_segmentation_comparison():
    """对比测试不同的分割方法"""
    
    # 创建测试图像
    img = create_test_image()
    
    # 测试点：点击在深色病变的中心
    click_x, click_y = 200, 200
    
    # 测试不同的阈值
    thresholds = [15, 25, 35, 45]
    
    # 创建图形
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('边界感知分割算法测试\n点击位置: 深色病变中心', fontsize=14, fontweight='bold')
    
    # 显示原图
    ax = axes[0, 0]
    ax.imshow(img, cmap='gray')
    ax.plot(click_x, click_y, 'r+', markersize=15, markeredgewidth=2)
    circle = Circle((click_x, click_y), 5, color='red', fill=False, linewidth=2)
    ax.add_patch(circle)
    ax.set_title('原始图像\n(红色标记为点击位置)', fontsize=10)
    ax.axis('off')
    
    # 显示边缘检测结果
    ax = axes[0, 1]
    edges = cv2.Canny(img, 50, 150)
    ax.imshow(edges, cmap='gray')
    ax.set_title('Canny 边缘检测\n(算法会在这些边界处停止)', fontsize=10)
    ax.axis('off')
    
    # 显示梯度
    ax = axes[0, 2]
    gx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
    gradient = np.sqrt(gx**2 + gy**2)
    ax.imshow(gradient, cmap='hot')
    ax.set_title('梯度强度\n(亮处为边界)', fontsize=10)
    ax.axis('off')
    
    # 测试不同阈值的分割效果
    for idx, T in enumerate(thresholds):
        params = SegmentParams(
            method="region_grow",
            grow_T=T,
        )
        
        mask = segment_region_grow(img, params, manual_seed=(click_x, click_y))
        
        # 创建叠加图
        overlay = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        overlay[mask > 0] = overlay[mask > 0] * 0.5 + np.array([255, 0, 0]) * 0.5
        
        ax = axes[1, idx] if idx < 3 else None
        if ax:
            ax.imshow(overlay)
            ax.plot(click_x, click_y, 'g+', markersize=12, markeredgewidth=2)
            
            # 计算分割区域大小
            area = np.sum(mask > 0)
            percentage = (area / (img.shape[0] * img.shape[1])) * 100
            
            ax.set_title(f'阈值 T={T}\n分割面积: {area} 像素 ({percentage:.1f}%)', fontsize=10)
            ax.axis('off')
    
    plt.tight_layout()
    
    # 保存结果
    output_path = Path('test_images/segmentation_comparison.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✅ 对比图已保存到: {output_path}")
    
    # 显示图形
    plt.show()


def test_gradient_vs_fixed_mode():
    """对比梯度模式和固定范围模式"""
    
    print("\n" + "="*60)
    print("算法模式对比")
    print("="*60)
    
    print("\n1. 固定范围模式 (FLOODFILL_FIXED_RANGE):")
    print("   - 比较每个像素与种子点的差异")
    print("   - 只接受与种子点相似的像素")
    print("   - 问题：无法跟随渐变，容易在渐变区域停止")
    print("   - 示例：种子=100, T=15 → 只接受 [85, 115]")
    
    print("\n2. 梯度模式 (默认模式，不使用 FIXED_RANGE):")
    print("   - 比较相邻像素之间的差异")
    print("   - 可以跟随渐变，逐步扩展")
    print("   - 优势：能够完整分割渐变区域")
    print("   - 示例：100→105→110→115... 逐步扩展")
    
    print("\n3. 边界感知增强:")
    print("   - 使用 Canny 边缘检测")
    print("   - 在强边界处停止扩展")
    print("   - 形态学后处理去除噪声")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    print("🔬 分割算法可视化测试")
    print()
    
    # 显示算法说明
    test_gradient_vs_fixed_mode()
    
    print("\n正在生成对比图...")
    test_segmentation_comparison()
    
    print("\n✅ 测试完成！")
    print("💡 提示：打开生成的图片查看不同阈值的分割效果")

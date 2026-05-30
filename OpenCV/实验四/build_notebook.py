#!/usr/bin/env python3
"""生成实验四 Jupyter Notebook"""
import json

def code(lines):
    """创建一个 code cell."""
    source = "\n".join(lines) + "\n"
    return {
        "cell_type": "code",
        "metadata": {},
        "source": [source],
        "outputs": [],
        "execution_count": None,
    }

def md(text):
    """创建一个 markdown cell."""
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [text],
    }

cells = []

# ========== 标题 ==========
cells.append(md("""# 实验四：图像分割与特征描述

**实验目的**：掌握图像分割的基本方法（阈值法、边缘法、区域法），理解全局特征与局部特征的提取与应用。"""))

# ========== 环境准备 ==========
cells.append(md("## 0. 环境准备"))

cells.append(code([
    "import cv2",
    "import numpy as np",
    "import matplotlib.pyplot as plt",
    "import sys",
    "",
    "# 设置中文字体",
    "plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Heiti SC', 'SimHei', 'DejaVu Sans']",
    "plt.rcParams['axes.unicode_minus'] = False",
    "",
    "print(f'Python: {sys.version.split()[0]}')",
    "print(f'OpenCV: {cv2.__version__}')",
    "print(f'NumPy: {np.__version__}')",
]))

# ========== 实验1 ==========
cells.append(md("""---

## 实验1：图像分割

对图1（低对比度医学图像）、图2（自然场景图像）、图3（不均衡曝光图像）各使用两种不同类型的分割算法。"""))

# --- 图1 ---
cells.append(md("### 1.1 图1 — 自适应阈值法 + Canny边缘检测"))

cells.append(code([
    "# ===== 图1：低对比度医学图像 =====",
    "img1 = cv2.imread('图1低对比度医学图像.png')",
    "gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)",
    "",
    "# --- 方法1: 自适应阈值法 (Gaussian) ---",
    "adaptive_thresh = cv2.adaptiveThreshold(",
    "    gray1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,",
    "    cv2.THRESH_BINARY, 11, 2)",
    "",
    "# --- 方法2: Canny 边缘检测 ---",
    "edges = cv2.Canny(gray1, 50, 150)",
    "",
    "# 将 Canny 边缘叠加到自适应阈值结果上（红色边缘）",
    "overlay = cv2.cvtColor(adaptive_thresh, cv2.COLOR_GRAY2BGR)",
    "overlay[edges > 0] = [0, 0, 255]",
    "",
    "# 可视化",
    "fig, axes = plt.subplots(1, 3, figsize=(15, 5))",
    "axes[0].imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))",
    "axes[0].set_title('Original (低对比度医学图像)')",
    "axes[0].axis('off')",
    "axes[1].imshow(adaptive_thresh, cmap='gray')",
    "axes[1].set_title('Adaptive Threshold (Gaussian, block=11)')",
    "axes[1].axis('off')",
    "axes[2].imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))",
    "axes[2].set_title('Canny Edge Overlay (red edges)')",
    "axes[2].axis('off')",
    "plt.tight_layout()",
    "plt.savefig('实验1_图1_阈值法与Canny.png', dpi=150, bbox_inches='tight')",
    "plt.show()",
]))

# --- 图2 ---
cells.append(md("### 1.2 图2 — Otsu全局阈值法 + 分水岭算法"))

cells.append(code([
    "# ===== 图2：自然场景图像 =====",
    "img2 = cv2.imread('图2自然场景图像.png')",
    "gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)",
    "",
    "# --- 方法1: Otsu 全局阈值法 ---",
    "_, otsu = cv2.threshold(gray2, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)",
    "",
    "# --- 方法2: 分水岭算法 ---",
    "# 噪声去除",
    "kernel = np.ones((3, 3), np.uint8)",
    "opening = cv2.morphologyEx(otsu, cv2.MORPH_OPEN, kernel, iterations=2)",
    "# 确定背景区域",
    "sure_bg = cv2.dilate(opening, kernel, iterations=3)",
    "# 距离变换",
    "dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)",
    "# 确定前景区域",
    "_, sure_fg = cv2.threshold(dist_transform, 0.4 * dist_transform.max(), 255, 0)",
    "sure_fg = np.uint8(sure_fg)",
    "# 未知区域",
    "unknown = cv2.subtract(sure_bg, sure_fg)",
    "# 连通组件标记",
    "_, markers = cv2.connectedComponents(sure_fg)",
    "markers = markers + 1",
    "markers[unknown == 255] = 0",
    "# 分水岭",
    "markers = cv2.watershed(img2, markers)",
    "watershed_result = img2.copy()",
    "watershed_result[markers == -1] = [0, 0, 255]  # 红色边界",
    "",
    "# 可视化",
    "fig, axes = plt.subplots(1, 3, figsize=(15, 5))",
    "axes[0].imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))",
    "axes[0].set_title('Original (自然场景图像)')",
    "axes[0].axis('off')",
    "axes[1].imshow(otsu, cmap='gray')",
    "axes[1].set_title('Otsu Threshold')",
    "axes[1].axis('off')",
    "axes[2].imshow(cv2.cvtColor(watershed_result, cv2.COLOR_BGR2RGB))",
    "axes[2].set_title('Watershed Segmentation')",
    "axes[2].axis('off')",
    "plt.tight_layout()",
    "plt.savefig('实验1_图2_Otsu与分水岭.png', dpi=150, bbox_inches='tight')",
    "plt.show()",
]))

# --- 图3 ---
cells.append(md("### 1.3 图3 — 局部自适应阈值 + Sobel边缘检测"))

cells.append(code([
    "# ===== 图3：不均衡曝光图像 =====",
    "img3 = cv2.imread('图3不均衡曝光图像.png')",
    "gray3 = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)",
    "",
    "# --- 方法1: 局部自适应阈值 ---",
    "adaptive_thresh3 = cv2.adaptiveThreshold(",
    "    gray3, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,",
    "    cv2.THRESH_BINARY, 15, 3)",
    "",
    "# --- 方法2: Sobel 边缘检测 ---",
    "sobelx = cv2.Sobel(gray3, cv2.CV_64F, 1, 0, ksize=3)",
    "sobely = cv2.Sobel(gray3, cv2.CV_64F, 0, 1, ksize=3)",
    "sobel = cv2.magnitude(sobelx, sobely)",
    "sobel = np.uint8(np.clip(sobel, 0, 255))",
    "",
    "# 可视化",
    "fig, axes = plt.subplots(1, 3, figsize=(16, 5))",
    "axes[0].imshow(cv2.cvtColor(img3, cv2.COLOR_BGR2RGB))",
    "axes[0].set_title('Original (不均衡曝光图像)')",
    "axes[0].axis('off')",
    "axes[1].imshow(adaptive_thresh3, cmap='gray')",
    "axes[1].set_title('Adaptive Threshold (Gaussian, block=15)')",
    "axes[1].axis('off')",
    "axes[2].imshow(sobel, cmap='gray')",
    "axes[2].set_title('Sobel Edge Detection')",
    "axes[2].axis('off')",
    "plt.tight_layout()",
    "plt.savefig('实验1_图3_自适应阈值与Sobel.png', dpi=150, bbox_inches='tight')",
    "plt.show()",
]))

# --- 实验1 分析 ---
cells.append(md("""### 1.4 算法选择依据与对比分析

**图1（低对比度医学图像）——自适应阈值 + Canny边缘检测**
- **选择依据**：医学图像对比度低，全局阈值无法有效区分前景和背景。自适应阈值根据局部邻域计算阈值，能保留局部细节；Canny 边缘检测通过双阈值和非极大值抑制提取精确边缘。
- **自适应阈值优点**：对光照不均匀有鲁棒性，能保留局部细节；**缺点**：对噪声敏感，块大小选择影响结果。
- **Canny优点**：边缘定位精确，抗噪声能力强；**缺点**：只能提取边缘，不能直接得到闭合区域。

**图2（自然场景图像）——Otsu全局阈值 + 分水岭算法**
- **选择依据**：自然场景通常具有明显的物体与背景分界，Otsu 通过最大化类间方差自动确定阈值；分水岭算法能基于距离变换进一步分离粘连物体。
- **Otsu优点**：自适应选择阈值，计算简单高效；**缺点**：对光照不均敏感，要求直方图呈双峰分布。
- **分水岭优点**：能得到闭合的分割区域，适合分离接触的物体；**缺点**：容易过分割，对噪声敏感。

**图3（不均衡曝光图像）——自适应阈值 + Sobel边缘检测**
- **选择依据**：曝光不均导致图像不同区域亮度差异大，自适应阈值可针对局部区域调整；Sobel 算子利用一阶微分检测边缘，对灰度渐变有较好响应。
- **自适应阈值优点**：能处理曝光不均的情况，保留明暗区域的信息；**缺点**：块大小和常数 C 需要仔细调整。
- **Sobel优点**：计算速度快，对噪声有一定平滑作用；**缺点**：边缘定位不如 Canny 精确，无法处理弱边缘。"""))

# ========== 实验2 ==========
cells.append(md("""---

## 实验2：全局特征提取

使用图2（自然场景图像）提取 RGB、HSV、Lab 三种颜色空间的全局特征。"""))

cells.append(code([
    "# ===== 实验2：全局颜色特征提取 =====",
    "img_exp2 = cv2.imread('图6自然图像.jpg')",
    "",
    "# 转换颜色空间",
    "img_rgb = cv2.cvtColor(img_exp2, cv2.COLOR_BGR2RGB)",
    "img_hsv = cv2.cvtColor(img_exp2, cv2.COLOR_BGR2HSV)",
    "img_lab = cv2.cvtColor(img_exp2, cv2.COLOR_BGR2Lab)",
    "",
    "# 计算各颜色空间各通道的均值和标准差",
    "color_spaces = {",
    "    'RGB': (img_rgb, ['R', 'G', 'B']),",
    "    'HSV': (img_hsv, ['H', 'S', 'V']),",
    "    'Lab': (img_lab, ['L', 'a', 'b']),",
    "}",
    "",
    "for name, (img_cs, channels) in color_spaces.items():",
    "    sep = '=' * 45",
    "    print(f'\\n{sep}')",
    "    print(f'  {name} Color Space')",
    "    print(sep)",
    "    for i, ch_name in enumerate(channels):",
    "        ch_data = img_cs[:, :, i].astype(np.float64)",
    "        print(f'  {ch_name} channel: mean={ch_data.mean():.2f}, std={ch_data.std():.2f}')",
    "",
    "# --- 可视化：各通道图像 ---",
    "fig, axes = plt.subplots(3, 4, figsize=(16, 10))",
    "for row, (name, (img_cs, channels)) in enumerate(color_spaces.items()):",
    "    if name == 'RGB':",
    "        axes[row, 0].imshow(img_cs)",
    "    elif name == 'HSV':",
    "        axes[row, 0].imshow(cv2.cvtColor(img_cs, cv2.COLOR_HSV2RGB))",
    "    else:",
    "        axes[row, 0].imshow(cv2.cvtColor(img_cs, cv2.COLOR_Lab2RGB))",
    "    axes[row, 0].set_title(f'{name}')",
    "    axes[row, 0].axis('off')",
    "    for col, ch_name in enumerate(channels):",
    "        axes[row, col + 1].imshow(img_cs[:, :, col], cmap='gray')",
    "        axes[row, col + 1].set_title(f'{ch_name}')",
    "        axes[row, col + 1].axis('off')",
    "plt.suptitle('Three Color Spaces — Per-Channel Visualization', fontsize=16)",
    "plt.tight_layout()",
    "plt.savefig('实验2_颜色空间可视化.png', dpi=150, bbox_inches='tight')",
    "plt.show()",
    "",
    "# --- 直方图 ---",
    "fig, axes = plt.subplots(3, 3, figsize=(15, 10))",
    "hist_configs = [",
    "    (img_rgb, ['R', 'G', 'B'], ['red', 'green', 'blue']),",
    "    (img_hsv, ['H', 'S', 'V'], ['purple', 'green', 'gray']),",
    "    (img_lab, ['L', 'a', 'b'], ['black', 'green', 'yellow']),",
    "]",
    "space_names = ['RGB', 'HSV', 'Lab']",
    "for row_idx, (img_cs, ch_names, colors) in enumerate(hist_configs):",
    "    for col_idx in range(3):",
    "        hist = cv2.calcHist([img_cs[:, :, col_idx]], [0], None, [256], [0, 256])",
    "        axes[row_idx, col_idx].plot(hist, color=colors[col_idx])",
    "        axes[row_idx, col_idx].set_title(f'{space_names[row_idx]} — {ch_names[col_idx]}')",
    "        axes[row_idx, col_idx].set_xlim([0, 256])",
    "plt.suptitle('Per-Channel Histograms', fontsize=16)",
    "plt.tight_layout()",
    "plt.savefig('实验2_直方图.png', dpi=150, bbox_inches='tight')",
    "plt.show()",
]))

cells.append(md("""### 2.1 颜色空间适用性分析

**各颜色空间特点**：
- **RGB**：直观且与显示设备兼容，三个通道分别对应红、绿、蓝。但 RGB 三通道高度相关（光照变化时三个通道同时增减），适合光照条件稳定的场合。
- **HSV**：将色调（H）、饱和度（S）与亮度（V）分离。H 通道描述颜色本质，对光照变化和阴影具有较好的不变性；S 表示颜色的纯度。适合颜色识别和基于颜色的图像检索。
- **Lab**：L 独立表示亮度，a（绿-红轴）和 b（蓝-黄轴）描述颜色对立维度，接近人眼视觉感知。具有感知均匀性（欧氏距离正比于人眼感知的颜色差异），适合颜色差异度量和场景分类。

**结论**：对于自然场景彩色图像，HSV 和 Lab 比 RGB 更适合颜色特征提取。HSV 的 H 通道对光照不变，适合颜色分割/检测；Lab 的 a/b 通道具有感知均匀性，适合颜色差异计算。推荐根据任务选择颜色空间：颜色检索用 HSV，颜色度量用 Lab。"""))

# ========== 实验3 ==========
cells.append(md("""---

## 实验3：局部特征提取

### 3.1 SIFT 特征匹配

使用图4（标准Lena）和图5（旋转缩放后的Lena）进行SIFT特征提取与匹配。"""))

cells.append(code([
    "# ===== 实验3.1: SIFT 特征匹配 =====",
    "img4 = cv2.imread('图4标准Lena图像.png')",
    "img5 = cv2.imread('图5旋转缩放后的Lena图像.png')",
    "gray4 = cv2.cvtColor(img4, cv2.COLOR_BGR2GRAY)",
    "gray5 = cv2.cvtColor(img5, cv2.COLOR_BGR2GRAY)",
    "",
    "# SIFT 检测器",
    "sift = cv2.SIFT_create()",
    "kp1, des1 = sift.detectAndCompute(gray4, None)",
    "kp2, des2 = sift.detectAndCompute(gray5, None)",
    "print(f'图4 SIFT 关键点: {len(kp1)}')",
    "print(f'图5 SIFT 关键点: {len(kp2)}')",
    "",
    "# BFMatcher + knnMatch",
    "bf = cv2.BFMatcher()",
    "raw_matches = bf.knnMatch(des1, des2, k=2)",
    "",
    "# Lowe's ratio test (NNDR < 0.7)",
    "good_matches = []",
    "for m, n in raw_matches:",
    "    if m.distance < 0.7 * n.distance:",
    "        good_matches.append(m)",
    "print(f'Lowe ratio test 后匹配数: {len(good_matches)}')",
    "",
    "# 计算匹配正确率 (findHomography + RANSAC)",
    "if len(good_matches) >= 4:",
    "    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)",
    "    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)",
    "    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)",
    "    if mask is not None:",
    "        inliers = mask.ravel().tolist()",
    "        inlier_count = sum(inliers)",
    "        accuracy = inlier_count / len(good_matches) * 100",
    "        print(f'RANSAC 内点数: {inlier_count}')",
    "        print(f'匹配正确率: {accuracy:.2f}%')",
    "        draw_params = dict(matchColor=(0, 255, 0), singlePointColor=None,",
    "                           matchesMask=inliers, flags=2)",
    "    else:",
    "        accuracy = 0",
    "        inlier_count = 0",
    "        draw_params = dict(matchColor=(0, 255, 0), singlePointColor=None, flags=2)",
    "else:",
    "    print('匹配点不足4对，无法计算单应性矩阵')",
    "    accuracy = 0",
    "    inlier_count = 0",
    "    draw_params = dict(matchColor=(0, 255, 0), singlePointColor=None, flags=2)",
    "",
    "# 绘制匹配图",
    "match_img = cv2.drawMatches(img4, kp1, img5, kp2, good_matches[:100], None, **draw_params)",
    "cv2.imwrite('实验3_SIFT匹配连线图.png', match_img)",
    "",
    "plt.figure(figsize=(16, 8))",
    "plt.imshow(cv2.cvtColor(match_img, cv2.COLOR_BGR2RGB))",
    "plt.title(f'SIFT Feature Matching (inliers: {inlier_count}, accuracy: {accuracy:.2f}%)')",
    "plt.axis('off')",
    "plt.tight_layout()",
    "plt.show()",
]))

cells.append(md("### 3.2 Harris 角点检测"))

cells.append(code([
    "# ===== 实验3.2: Harris 角点检测 =====",
    "gray4_f = np.float32(gray4)",
    "dst = cv2.cornerHarris(gray4_f, blockSize=2, ksize=3, k=0.04)",
    "dst = cv2.dilate(dst, None)",
    "",
    "# 三种阈值",
    "thresholds = [0.01, 0.05, 0.1]",
    "corner_counts = []",
    "",
    "fig, axes = plt.subplots(1, 3, figsize=(18, 6))",
    "for i, factor in enumerate(thresholds):",
    "    thresh = factor * dst.max()",
    "    corner_img = img4.copy()",
    "    corner_img[dst > thresh] = [0, 0, 255]",
    "    cnt = np.sum(dst > thresh)",
    "    corner_counts.append(cnt)",
    "    axes[i].imshow(cv2.cvtColor(corner_img, cv2.COLOR_BGR2RGB))",
    "    axes[i].set_title(f'Threshold = {factor} * max\\nCorner count = {cnt}')",
    "    axes[i].axis('off')",
    "plt.suptitle('Harris Corner Detection — Three Thresholds', fontsize=16)",
    "plt.tight_layout()",
    "plt.savefig('实验3_Harris角点检测.png', dpi=150, bbox_inches='tight')",
    "plt.show()",
    "",
    "for factor, cnt in zip(thresholds, corner_counts):",
    "    print(f'Threshold factor: {factor}, corner count: {cnt}')",
]))

cells.append(md("""### 3.3 Harris 与 SIFT 对比分析

**Harris 角点检测**
- 基于图像灰度梯度的协方差矩阵，检测角点（两个方向梯度变化都大的点）。
- **优点**：计算效率高，实现简单，角点分布密集，适合实时跟踪和光流估计。
- **缺点**：不具备尺度不变性和旋转不变性，对图像缩放/旋转后角点位置会改变。

**SIFT（尺度不变特征变换）**
- 通过 DoG（高斯差分）金字塔在多尺度空间中检测极值点，并使用梯度方向直方图构建描述符。
- **优点**：具有尺度不变性、旋转不变性，对光照变化、视角变化和噪声有较强鲁棒性，描述符维度高（128维），区分性强。
- **缺点**：计算复杂度高，特征点相对稀疏，受专利限制（OpenCV 4.x 需从 opencv-contrib 编译或使用主仓库内置版本）。

**分布差异**：Harris 角点集中在纹理丰富、角落分明的区域（如 Lena 的眼睛、帽檐边缘），分布较密集；SIFT 关键点分布在多尺度的显著区域，更加稀疏但每个点携带丰富的局部描述信息。SIFT 在图4和图5的匹配中表现出良好的旋转和缩放不变性，而 Harris 在图像变换后角点会发生变化。"""))

# ========== 构建 Notebook ==========
notebook = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "version": "3.10.0",
        },
    },
    "cells": cells,
}

output_path = "实验四_图像分割与特征描述.ipynb"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print(f"Notebook saved to: {output_path}")
print(f"Total cells: {len(cells)}")

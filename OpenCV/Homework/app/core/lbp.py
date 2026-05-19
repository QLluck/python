

from __future__ import annotations

import numpy as np


def uniform_lbp_image(gray: np.ndarray, radius: int = 1, neighbors: int = 8) -> np.ndarray:
  
    
    # 参数检查：目前只支持 8 邻域、半径 1 的简单版本
    # 这是最常用的配置，计算快速且效果好
    if neighbors != 8 or radius != 1:
        # 如果传入其他参数，强制使用 8 邻域、半径 1
        radius = 1
        neighbors = 8
    
    # 获取图像的高度和宽度
    h, w = gray.shape
    
    # 边缘扩展：在图像四周加一圈像素
    # 为什么要扩展？因为边缘像素没有完整的 8 个邻居
    # mode="edge" 表示用边缘像素的值来填充（比如最上面一行复制到上方）
    padded = np.pad(gray.astype(np.int32), 1, mode="edge")
    
    # 创建输出数组，用于存储 LBP 编码
    # 初始值全为 0
    out = np.zeros((h, w), dtype=np.int32)
    
    # 定义 8 个邻居的相对位置（相对于中心像素）
    # 顺序：左上、上、右上、右、右下、下、左下、左（顺时针）
    #   0  1  2
    #   7  ·  3
    #   6  5  4
    offsets = [
        (-1, -1),  # 0: 左上
        (-1,  0),  # 1: 上
        (-1,  1),  # 2: 右上
        ( 0,  1),  # 3: 右
        ( 1,  1),  # 4: 右下
        ( 1,  0),  # 5: 下
        ( 1, -1),  # 6: 左下
        ( 0, -1),  # 7: 左
    ]
    
    # 提取中心像素（去掉扩展的边缘）
    # padded[1:h+1, 1:w+1] 就是原始图像的位置
    c = padded[1 : h + 1, 1 : w + 1]
    
    # 遍历 8 个邻居，计算 LBP 编码
    for i, (dy, dx) in enumerate(offsets):
        # 提取第 i 个邻居的所有像素
        # dy, dx 是相对偏移量
        n = padded[1 + dy : h + 1 + dy, 1 + dx : w + 1 + dx]
        
        # 比较邻居和中心像素的亮度
        # n >= c 返回布尔数组（True/False）
        # .astype(np.int32) 转换为整数（True→1, False→0）
        # << i 是左移操作，相当于乘以 2^i
        # 
        # 举例：如果这是第 3 个邻居（i=3）
        # - 如果邻居 >= 中心，得到 1，左移 3 位 → 1000 (二进制) = 8 (十进制)
        # - 如果邻居 < 中心，得到 0，左移 3 位 → 0000 (二进制) = 0 (十进制)
        # 
        # |= 是按位或操作，把每个邻居的贡献累加到 out 中
        # 最终 out 的每个像素都是一个 8 位二进制数
        out |= (n >= c).astype(np.int32) << i
    
    # 归一化到 0-255 范围，用于可视化
    # % 256 是取模操作，确保值在 0-255 范围内
    # 为什么要取模？因为 LBP 编码可能是 0-255 的任意值
    vis = (out % 256).astype(np.uint8)
    
    # 返回可视化图像
    # 不同的纹理模式会显示为不同的灰度值
    # 可以进一步用伪彩色映射（colormap）来显示，更直观
    return vis

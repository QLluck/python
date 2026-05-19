import cv2
import numpy as np
import matplotlib.pyplot as plt

# 统一绘图函数

def show_image1(imgs, titles,rows,cols):
    plt.figure(figsize=(20, 12), dpi=150)  # 超大图

    for i in range(len(imgs)):
        plt.subplot(rows, cols, i+1)
        plt.imshow(imgs[i], cmap="gray")
        plt.title(titles[i], fontsize=14)
        plt.axis("off")
    plt.tight_layout()
    plt.show()

img = cv2.imread("test_image.jpg", cv2.IMREAD_GRAYSCALE)
_, binary_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)


kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))


img_list = []
title_list = []

# 迭代次数：1、2、3（列）
iter_list = [1, 2, 3]

# 行1：腐蚀 Erosion
for it in iter_list:
    erode = cv2.erode(binary_img, kernel, iterations=it)
    img_list.append(erode)
    title_list.append(f"Erosion\nIter={it}")

# 行2：膨胀 Dilation
for it in iter_list:
    dilate = cv2.dilate(binary_img, kernel, iterations=it)
    img_list.append(dilate)
    title_list.append(f"Dilation\nIter={it}")

# 行3：开运算 Opening
for it in iter_list:
    open_img = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel, iterations=it)
    img_list.append(open_img)
    title_list.append(f"Opening\nIter={it}")

# 行4：闭运算 Closing
for it in iter_list:
    close_img = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel, iterations=it)
    img_list.append(close_img)
    title_list.append(f"Closing\nIter={it}")


show_image1(img_list, title_list, rows=4, cols=3)


img_bg_noise = cv2.imread("noisy_image.jpg", cv2.IMREAD_GRAYSCALE)
img_blur = cv2.medianBlur(img_bg_noise, 3)  # 中值滤波适配椒盐噪声
_, binary_bg = cv2.threshold(img_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

op_types = [cv2.MORPH_ERODE, cv2.MORPH_DILATE, cv2.MORPH_OPEN, cv2.MORPH_CLOSE]
op_names = ["Erode", "Dilate", "Opening", "Closing"]

img_list = []
title_list = []
# 纵轴：迭代 1~3 次
for it in range(1, 6):
    # 横轴：4种形态学操作
    for op, name in zip(op_types, op_names):
        res = cv2.morphologyEx(binary_bg, op, kernel, iterations=it)
        img_list.append(res)
        title_list.append(f"{name}\nIter = {it}")


show_image1(img_list, title_list,5,4)


img_bg_noise = cv2.imread("noisy_image2.jpg", cv2.IMREAD_GRAYSCALE)
img_blur = cv2.medianBlur(img_bg_noise, 3)  # 中值滤波适配椒盐噪声
_, binary_bg = cv2.threshold(img_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

op_types = [cv2.MORPH_ERODE, cv2.MORPH_DILATE, cv2.MORPH_OPEN, cv2.MORPH_CLOSE]
op_names = ["Erode", "Dilate", "Opening", "Closing"]

img_list = []
title_list = []
# 纵轴：迭代 1~3 次
for it in range(1, 6):
    # 横轴：4种形态学操作
    for op, name in zip(op_types, op_names):
        res = cv2.morphologyEx(binary_bg, op, kernel, iterations=it)
        img_list.append(res)
        title_list.append(f"{name}\nIter = {it}")


show_image1(img_list, title_list,5,4)


def butterworth_highpass(img, d0, n):
    rows, cols = img.shape
    crow, ccol = rows//2, cols//2
    # 傅里叶变换
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    # 构造高通滤波器
    u, v = np.meshgrid(np.arange(cols), np.arange(rows))
    d = np.sqrt((u - ccol)**2 + (v - crow)**2)
    h = 1 / (1 + (d0 / (d + 1e-8))**(2*n))
    # 滤波
    fshift_filtered = fshift * h
    # 逆变换
    f_ishift = np.fft.ifftshift(fshift_filtered)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    # 归一化
    img_back = cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    return img_back
# 1. 读取灰度图像
img = cv2.imread("edge_test.png", cv2.IMREAD_GRAYSCALE)
img = cv2.GaussianBlur(img, (3, 3), 0)  # 先平滑去噪，减少伪边缘

# 2. 形态学梯度边缘检测
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

img_list = []
title_list = []

for it in range(1, 4):
    # 形态学梯度
    grad = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel, iterations=it)
    
    # 拉普拉斯
    lap = cv2.Laplacian(img, cv2.CV_64F)
    lap = cv2.convertScaleAbs(lap)
    
    # 巴特沃斯
    bw = butterworth_highpass(img, d0=40, n=2)
    
    # 加入列表
    img_list.append(grad)
    img_list.append(lap)
    img_list.append(bw)
    
    title_list.append(f"Gradient\nIter {it}")
    title_list.append(f"Laplacian\nIter {it}")
    title_list.append(f"Butterworth\nIter {it}")


show_image1(img_list, title_list, rows=3, cols=3)





# 1. 读取
fingerprint = cv2.imread("fingerprint.png", cv2.IMREAD_GRAYSCALE)

# 2. 先去噪！关键！
blur = cv2.GaussianBlur(fingerprint, (3,3), 0)

# 3. 二值化（正常黑白，不反转）
binary_fp = cv2.adaptiveThreshold(
    blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2))
kernel_skeleton = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

def skeletonize(img):
    img = img.copy()
    skel = np.zeros_like(img)
    while True:
        erode = cv2.erode(img, kernel_skeleton)
        temp = cv2.dilate(erode, kernel_skeleton)
        temp = cv2.subtract(img, temp)
        skel = cv2.bitwise_or(skel, temp)
        img = erode
        if cv2.countNonZero(img) == 0:
            break
    return skel

# fp_skeleton = skeletonize(fp_enhanced)

# show_image1(
#     [fingerprint, binary_fp, fp_open, fp_enhanced, fp_skeleton],
#     ["Original", "Binary", "Open Iter2", "Close Iter3", "Skeleton"],
#     rows=1, cols=5
# )



iters = [1, 2, 3]
img_list = []
title_list = []

for it in iters:
    # 二值图
    img_list.append(binary_fp)
    title_list.append(f"Binary\nIter={it}")

    # 开运算：去背景噪点
    open_img = cv2.morphologyEx(binary_fp, cv2.MORPH_OPEN, kernel, iterations=it)
    img_list.append(open_img)
    title_list.append(f"Opening\nIter={it}")

    # 闭运算：连接断裂纹线
    close_img = cv2.morphologyEx(open_img, cv2.MORPH_CLOSE, kernel, iterations=it)
    img_list.append(close_img)
    title_list.append(f"Closing\nIter={it}")

    # 增强结果 = 开 + 闭
    enhanced_img = close_img
    img_list.append(enhanced_img)
    title_list.append(f"Enhanced\nIter={it}")

    # 指纹骨架
    skeleton_img = skeletonize(enhanced_img)
    img_list.append(skeleton_img)
    title_list.append(f"Skeleton\nIter={it}")

show_image1(img_list, title_list, rows=3, cols=5)
import cv2
car = cv2.imread('car.png')
car
cv2.imshow('car',car)
cv2.waitKey(3000)
cv2.destroyAllWindows()
import numpy as np
import cv2
import matplotlib.pyplot as plt
carhui = cv2.cvtColor(car,cv2.COLOR_RGB2GRAY) #调用cvtColor函数 转换为灰度图
cv2.imshow('car',carhui)
cv2.waitKey(3000) 
cv2.destroyAllWindows()
cv2.imwrite('test_image.jpg',carhui) #保存灰度图
car.shape
# car=plt.imread('car.png')
plt.imshow(car[100:500,300:700])
plt.imshow(car)
plt.imshow(car[460:500,450:550])
plt.imshow(car[175:300,400:600])

import cv2
# 1. 创建窗口
cv2.namedWindow('video', cv2.WINDOW_NORMAL)
cv2.resizeWindow('video', 640, 480)

# 2. 打开摄像头
cap = cv2.VideoCapture(0)

# 3. 循环读取帧
while cap.isOpened():  # 更安全的循环条件
    ret, frame = cap.read()
    if not ret:
        print("无法读取摄像头帧，退出")
        break
    
    # 显示当前帧
    cv2.imshow('video', frame)
    
    # 关键：waitKey(1) 每1ms检查一次按键，保证画面流畅
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # 按 q 键退出
        break

# 4. 释放资源
cap.release()
cv2.destroyAllWindows()
# macOS/Jupyter 额外释放，避免窗口残留
cv2.waitKey(1)

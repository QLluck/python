# 导入os模块，用于与操作系统进行交互，例如设置环境变量、文件操作等
import os 

# 导入numpy库，通常用于数值计算，处理数组和矩阵等数据结构
import numpy as np 

# 导入torch库，这是PyTorch深度学习框架的主模块，用于各种深度学习任务
import torch 

# 导入torch.nn模块，提供了神经网络相关的类和函数，如各种层、损失函数等
import torch.nn as nn 

# 从torch.utils.data模块中导入Dataset和DataLoader类
# Dataset用于封装数据集，DataLoader用于加载数据集中的数据，提供批量加载、打乱顺序等功能
from torch.utils.data import Dataset, DataLoader 

# 导入torch.optim模块，通常简写为optimizer，提供了各种优化算法，如SGD、Adam等，用于训练模型时更新模型参数
import torch.optim as optimizer 

batch_size = 16
# 批次的大小
lr = 1e-4
# 优化器的学习率
max_epochs = 100
os.environ['CUDA_VISIBLE_DEVICES'] = '0' # 指明调用的GPU为0,1号

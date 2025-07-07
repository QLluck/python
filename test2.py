import numpy as np
import matplotlib
matplotlib.use('Agg')  # 使用Agg后端（无GUI）
import matplotlib.pyplot as plt

# 设置图片清晰度
plt.rcParams['figure.dpi'] = 300

# 生成输入数据
z = np.linspace(-6, 6, 1000)

# 定义激活函数
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def relu(z):
    return np.maximum(0, z)

def tanh(z):
    return (np.exp(z) - np.exp(-z)) / (np.exp(z) + np.exp(-z))

# 计算输出
y_sigmoid = sigmoid(z)
y_relu = relu(z)
y_tanh = tanh(z)

# 创建图形和子图
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 绘制Sigmoid函数
axes[0].plot(z, y_sigmoid, label='Sigmoid', color='#5DA5DA', linewidth=2)
axes[0].axhline(y=0, color='k', linestyle='--', alpha=0.3)
axes[0].axhline(y=1, color='k', linestyle='--', alpha=0.3)
axes[0].axvline(x=0, color='k', linestyle='--', alpha=0.3)
axes[0].set_title('Sigmoid Activation Function', fontsize=14)
axes[0].set_xlabel('z', fontsize=12)
axes[0].set_ylabel('f(z)', fontsize=12)
axes[0].set_ylim(-0.1, 1.1)
axes[0].text(-5, 0.8, r'$f(z) = \frac{1}{1+e^{-z}}$', fontsize=12)
axes[0].text(-5, 0.6, 'Output Range: [0, 1]', fontsize=11)
axes[0].text(-5, 0.4, 'Characteristics: Compresses to probability range, prone to vanishing gradients', fontsize=11)
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# 绘制ReLU函数
axes[1].plot(z, y_relu, label='ReLU', color='#FAA43A', linewidth=2)
axes[1].axhline(y=0, color='k', linestyle='--', alpha=0.3)
axes[1].axvline(x=0, color='k', linestyle='--', alpha=0.3)
axes[1].set_title('ReLU Activation Function', fontsize=14)
axes[1].set_xlabel('z', fontsize=12)
axes[1].set_ylabel('f(z)', fontsize=12)
axes[1].set_ylim(-1, 6)
axes[1].text(-5, 4, r'$f(z) = max(0, z)$', fontsize=12)
axes[1].text(-5, 3, 'Output Range: [0, +∞)', fontsize=11)
axes[1].text(-5, 2, 'Characteristics: Unilateral inhibition, mitigates vanishing gradients', fontsize=11)
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# 绘制Tanh函数
axes[2].plot(z, y_tanh, label='Tanh', color='#60BD68', linewidth=2)
axes[2].axhline(y=0, color='k', linestyle='--', alpha=0.3)
axes[2].axhline(y=1, color='k', linestyle='--', alpha=0.3)
axes[2].axhline(y=-1, color='k', linestyle='--', alpha=0.3)
axes[2].axvline(x=0, color='k', linestyle='--', alpha=0.3)
axes[2].set_title('Tanh Activation Function', fontsize=14)
axes[2].set_xlabel('z', fontsize=12)
axes[2].set_ylabel('f(z)', fontsize=12)
axes[2].set_ylim(-1.1, 1.1)
axes[2].text(-5, 0.8, r'$f(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}$', fontsize=12)
axes[2].text(-5, 0.6, 'Output Range: [-1, 1]', fontsize=11)
axes[2].text(-5, 0.4, 'Characteristics: Zero-centered output, suitable for symmetric data', fontsize=11)
axes[2].legend()
axes[2].grid(True, alpha=0.3)

# 调整布局
plt.tight_layout()
plt.savefig('activation_functions.png', bbox_inches='tight')
# plt.show()  # 注释掉show()，避免GUI渲染
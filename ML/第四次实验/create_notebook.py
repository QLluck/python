#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
创建SVM实验Jupyter Notebook
"""

import json

# 创建notebook结构
notebook = {
    "cells": [],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.8.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# 定义所有的单元格
cells = [
    # Cell 1: 标题
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# SVM支持向量机实验\n",
            "\n",
            "## 实验目标\n",
            "1. 掌握支持向量机（SVM）的基本原理与数学模型\n",
            "2. 熟悉SVM在不同数据集上的分类任务实现\n",
            "3. 学习SVM核函数的选择及超参数调优方法\n",
            "4. 培养数据预处理、模型训练及结果分析的能力\n",
            "5. 培养对训练结果进行可视化的能力\n",
            "\n",
            "---"
        ]
    },
    
    # Cell 2: 导入库
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 导入所需的库\n",
            "import numpy as np\n",
            "import pandas as pd\n",
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "from sklearn import datasets\n",
            "from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score\n",
            "from sklearn.preprocessing import StandardScaler\n",
            "from sklearn.svm import SVC\n",
            "from sklearn.metrics import classification_report, confusion_matrix, accuracy_score\n",
            "from sklearn.decomposition import PCA\n",
            "from imblearn.over_sampling import SMOTE\n",
            "import warnings\n",
            "import os\n",
            "\n",
            "# 忽略警告信息\n",
            "warnings.filterwarnings('ignore')\n",
            "\n",
            "# 设置随机种子，确保结果可复现\n",
            "np.random.seed(42)\n",
            "\n",
            "# 设置中文字体，避免图表中文显示问题\n",
            "plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei']  # Mac和Windows\n",
            "plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题\n",
            "\n",
            "# 设置图表风格\n",
            "sns.set_style('whitegrid')\n",
            "\n",
            "# 创建文件夹用于保存图片\n",
            "if not os.path.exists('figures'):\n",
            "    os.makedirs('figures')\n",
            "if not os.path.exists('data'):\n",
            "    os.makedirs('data')\n",
            "\n",
            "print('所有库导入成功！')\n",
            "print('实验环境准备完毕！')"
        ]
    },
    
    # Cell 3: 数据集介绍
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 一、数据集介绍\n",
            "\n",
            "### 数据集1：Iris鸢尾花数据集（线性可分）\n",
            "- **来源**：经典的机器学习数据集，由Fisher在1936年收集\n",
            "- **样本数量**：150个样本\n",
            "- **特征数量**：4个特征\n",
            "  - sepal length (cm)：花萼长度\n",
            "  - sepal width (cm)：花萼宽度\n",
            "  - petal length (cm)：花瓣长度\n",
            "  - petal width (cm)：花瓣宽度\n",
            "- **标签**：3个类别（Setosa、Versicolour、Virginica）\n",
            "- **特点**：部分类别线性可分，适合测试线性核SVM\n",
            "\n",
            "### 数据集2：乳腺癌数据集（非线性可分）\n",
            "- **来源**：威斯康星大学医院的乳腺癌诊断数据\n",
            "- **样本数量**：569个样本\n",
            "- **特征数量**：30个特征（从细胞核图像中提取的特征）\n",
            "  - 包括半径、纹理、周长、面积、光滑度等\n",
            "- **标签**：2个类别（恶性malignant、良性benign）\n",
            "- **特点**：特征维度高，非线性可分，适合测试RBF核SVM\n",
            "\n",
            "---"
        ]
    },
    
    # Cell 4: 加载数据集1
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 加载Iris数据集\n",
            "print('='*60)\n",
            "print('加载数据集1：Iris鸢尾花数据集')\n",
            "print('='*60)\n",
            "\n",
            "iris = datasets.load_iris()\n",
            "X_iris = iris.data\n",
            "y_iris = iris.target\n",
            "\n",
            "# 为了便于可视化，我们只选择前两个特征\n",
            "X_iris_2d = X_iris[:, :2]  # 只使用花萼长度和花萼宽度\n",
            "\n",
            "# 创建DataFrame方便查看\n",
            "iris_df = pd.DataFrame(X_iris, columns=iris.feature_names)\n",
            "iris_df['target'] = y_iris\n",
            "iris_df['target_name'] = iris_df['target'].map({0: 'Setosa', 1: 'Versicolour', 2: 'Virginica'})\n",
            "\n",
            "print(f'\\n数据集形状：{X_iris.shape}')\n",
            "print(f'特征数量：{X_iris.shape[1]}')\n",
            "print(f'样本数量：{X_iris.shape[0]}')\n",
            "print(f'类别数量：{len(np.unique(y_iris))}')\n",
            "print(f'\\n各类别样本数量：')\n",
            "print(iris_df['target_name'].value_counts())\n",
            "print(f'\\n前5行数据：')\n",
            "print(iris_df.head())"
        ]
    },
    
    # Cell 5: 可视化Iris数据集
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 可视化Iris数据集的分布\n",
            "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
            "\n",
            "# 左图：使用前两个特征的散点图\n",
            "colors = ['red', 'blue', 'green']\n",
            "for i, target_name in enumerate(['Setosa', 'Versicolour', 'Virginica']):\n",
            "    mask = iris_df['target'] == i\n",
            "    axes[0].scatter(iris_df[mask]['sepal length (cm)'], \n",
            "                   iris_df[mask]['sepal width (cm)'],\n",
            "                   c=colors[i], label=target_name, alpha=0.6, s=50)\n",
            "axes[0].set_xlabel('花萼长度 (cm)', fontsize=12)\n",
            "axes[0].set_ylabel('花萼宽度 (cm)', fontsize=12)\n",
            "axes[0].set_title('Iris数据集分布图（前两个特征）', fontsize=14, fontweight='bold')\n",
            "axes[0].legend()\n",
            "axes[0].grid(True, alpha=0.3)\n",
            "\n",
            "# 右图：特征相关性热力图\n",
            "corr_matrix = iris_df.iloc[:, :4].corr()\n",
            "sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', \n",
            "            square=True, ax=axes[1], cbar_kws={'shrink': 0.8})\n",
            "axes[1].set_title('特征相关性热力图', fontsize=14, fontweight='bold')\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.savefig('figures/01_iris_data_distribution.png', dpi=300, bbox_inches='tight')\n",
            "plt.show()\n",
            "\n",
            "print('Iris数据集可视化完成！')"
        ]
    },
    
    # Cell 6: 加载数据集2
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 加载乳腺癌数据集\n",
            "print('\\n' + '='*60)\n",
            "print('加载数据集2：乳腺癌数据集')\n",
            "print('='*60)\n",
            "\n",
            "cancer = datasets.load_breast_cancer()\n",
            "X_cancer = cancer.data\n",
            "y_cancer = cancer.target\n",
            "\n",
            "# 创建DataFrame\n",
            "cancer_df = pd.DataFrame(X_cancer, columns=cancer.feature_names)\n",
            "cancer_df['target'] = y_cancer\n",
            "cancer_df['target_name'] = cancer_df['target'].map({0: 'malignant', 1: 'benign'})\n",
            "\n",
            "print(f'\\n数据集形状：{X_cancer.shape}')\n",
            "print(f'特征数量：{X_cancer.shape[1]}')\n",
            "print(f'样本数量：{X_cancer.shape[0]}')\n",
            "print(f'类别数量：{len(np.unique(y_cancer))}')\n",
            "print(f'\\n各类别样本数量：')\n",
            "print(cancer_df['target_name'].value_counts())\n",
            "print(f'\\n前5行数据（部分特征）：')\n",
            "print(cancer_df.iloc[:, :5].head())"
        ]
    }
]

# 继续添加更多单元格...
notebook["cells"] = cells

# 保存notebook
with open('SVM实验_part1.json', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=2)

print("Notebook part 1 created successfully!")

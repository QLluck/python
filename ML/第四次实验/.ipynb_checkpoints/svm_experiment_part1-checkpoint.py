#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SVM实验 - 主实验脚本
可以在Jupyter Notebook中逐步运行，也可以直接运行生成报告
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import datasets
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.decomposition import PCA
from imblearn.over_sampling import SMOTE
import warnings
import os

# 忽略警告信息
warnings.filterwarnings('ignore')

# 设置随机种子，确保结果可复现
np.random.seed(42)

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 设置图表风格
sns.set_style('whitegrid')

# 创建文件夹
os.makedirs('figures', exist_ok=True)
os.makedirs('data', exist_ok=True)

print('='*60)
print('SVM支持向量机实验')
print('='*60)
print('实验环境准备完毕！\n')


# ============================================================
# 第一部分：数据加载与探索
# ============================================================

def load_and_explore_data():
    """加载并探索数据集"""
    print('\n' + '='*60)
    print('第一部分：数据加载与探索')
    print('='*60)
    
    # 加载Iris数据集
    print('\n1. 加载Iris鸢尾花数据集（线性可分）')
    print('-'*60)
    iris = datasets.load_iris()
    X_iris = iris.data
    y_iris = iris.target
    
    iris_df = pd.DataFrame(X_iris, columns=iris.feature_names)
    iris_df['target'] = y_iris
    iris_df['target_name'] = iris_df['target'].map({0: 'Setosa', 1: 'Versicolour', 2: 'Virginica'})
    
    print(f'数据集形状：{X_iris.shape}')
    print(f'特征数量：{X_iris.shape[1]}')
    print(f'样本数量：{X_iris.shape[0]}')
    print(f'类别数量：{len(np.unique(y_iris))}')
    print(f'\n各类别样本数量：')
    print(iris_df['target_name'].value_counts())
    
    # 加载乳腺癌数据集
    print('\n2. 加载乳腺癌数据集（非线性可分）')
    print('-'*60)
    cancer = datasets.load_breast_cancer()
    X_cancer = cancer.data
    y_cancer = cancer.target
    
    cancer_df = pd.DataFrame(X_cancer, columns=cancer.feature_names)
    cancer_df['target'] = y_cancer
    cancer_df['target_name'] = cancer_df['target'].map({0: 'malignant', 1: 'benign'})
    
    print(f'数据集形状：{X_cancer.shape}')
    print(f'特征数量：{X_cancer.shape[1]}')
    print(f'样本数量：{X_cancer.shape[0]}')
    print(f'类别数量：{len(np.unique(y_cancer))}')
    print(f'\n各类别样本数量：')
    print(cancer_df['target_name'].value_counts())
    
    return iris, cancer, iris_df, cancer_df


def visualize_data(iris_df, cancer_df):
    """可视化数据分布"""
    print('\n3. 数据可视化')
    print('-'*60)
    
    # Iris数据集可视化
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    colors = ['red', 'blue', 'green']
    for i, target_name in enumerate(['Setosa', 'Versicolour', 'Virginica']):
        mask = iris_df['target'] == i
        axes[0].scatter(iris_df[mask]['sepal length (cm)'], 
                       iris_df[mask]['sepal width (cm)'],
                       c=colors[i], label=target_name, alpha=0.6, s=50)
    axes[0].set_xlabel('Sepal Length (cm)', fontsize=12)
    axes[0].set_ylabel('Sepal Width (cm)', fontsize=12)
    axes[0].set_title('Iris Dataset Distribution', fontsize=14, fontweight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    corr_matrix = iris_df.iloc[:, :4].corr()
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                square=True, ax=axes[1], cbar_kws={'shrink': 0.8})
    axes[1].set_title('Iris Feature Correlation Heatmap', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('figures/01_iris_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 乳腺癌数据集可视化（使用PCA降维）
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # PCA降维到2维
    pca = PCA(n_components=2, random_state=42)
    X_cancer_pca = pca.fit_transform(cancer_df.iloc[:, :30])
    
    for i, target_name in enumerate(['malignant', 'benign']):
        mask = cancer_df['target'] == i
        axes[0].scatter(X_cancer_pca[mask, 0], X_cancer_pca[mask, 1],
                       label=target_name, alpha=0.6, s=50)
    axes[0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})', fontsize=12)
    axes[0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})', fontsize=12)
    axes[0].set_title('Breast Cancer Dataset Distribution (PCA)', fontsize=14, fontweight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # 类别分布
    cancer_df['target_name'].value_counts().plot(kind='bar', ax=axes[1], color=['salmon', 'lightblue'])
    axes[1].set_title('Breast Cancer Class Distribution', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Class', fontsize=12)
    axes[1].set_ylabel('Number of Samples', fontsize=12)
    axes[1].set_xticklabels(['Malignant', 'Benign'], rotation=0)
    
    plt.tight_layout()
    plt.savefig('figures/02_cancer_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print('数据可视化完成！')


# ============================================================
# 第二部分：数据预处理
# ============================================================

def preprocess_data(iris, cancer):
    """数据预处理"""
    print('\n' + '='*60)
    print('第二部分：数据预处理')
    print('='*60)
    
    # Iris数据集预处理
    print('\n1. Iris数据集预处理')
    print('-'*60)
    X_iris = iris.data
    y_iris = iris.target
    
    # 划分训练集和测试集
    X_iris_train, X_iris_test, y_iris_train, y_iris_test = train_test_split(
        X_iris, y_iris, test_size=0.3, random_state=42, stratify=y_iris
    )
    
    # 特征标准化
    scaler_iris = StandardScaler()
    X_iris_train_scaled = scaler_iris.fit_transform(X_iris_train)
    X_iris_test_scaled = scaler_iris.transform(X_iris_test)
    
    print(f'训练集大小：{X_iris_train.shape}')
    print(f'测试集大小：{X_iris_test.shape}')
    print(f'标准化完成！')
    
    # 乳腺癌数据集预处理
    print('\n2. 乳腺癌数据集预处理')
    print('-'*60)
    X_cancer = cancer.data
    y_cancer = cancer.target
    
    X_cancer_train, X_cancer_test, y_cancer_train, y_cancer_test = train_test_split(
        X_cancer, y_cancer, test_size=0.3, random_state=42, stratify=y_cancer
    )
    
    scaler_cancer = StandardScaler()
    X_cancer_train_scaled = scaler_cancer.fit_transform(X_cancer_train)
    X_cancer_test_scaled = scaler_cancer.transform(X_cancer_test)
    
    print(f'训练集大小：{X_cancer_train.shape}')
    print(f'测试集大小：{X_cancer_test.shape}')
    print(f'标准化完成！')
    
    return (X_iris_train_scaled, X_iris_test_scaled, y_iris_train, y_iris_test,
            X_cancer_train_scaled, X_cancer_test_scaled, y_cancer_train, y_cancer_test,
            scaler_iris, scaler_cancer)


if __name__ == '__main__':
    # 运行数据加载和预处理
    iris, cancer, iris_df, cancer_df = load_and_explore_data()
    visualize_data(iris_df, cancer_df)
    data = preprocess_data(iris, cancer)
    
    print('\n' + '='*60)
    print('第一阶段完成：数据准备完毕！')
    print('='*60)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SVM实验 - 模型训练与评估
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import cross_val_score
import warnings

warnings.filterwarnings('ignore')


# ============================================================
# 第三部分：模型训练
# ============================================================

def train_svm_models(X_train, y_train, X_test, y_test, dataset_name):
    """训练不同核函数的SVM模型"""
    print('\n' + '='*60)
    print(f'第三部分：{dataset_name} - SVM模型训练')
    print('='*60)
    
    # 定义不同的核函数
    kernels = ['linear', 'poly', 'rbf']
    kernel_names = ['线性核', '多项式核', '高斯核(RBF)']
    models = {}
    results = {}
    
    for kernel, kernel_name in zip(kernels, kernel_names):
        print(f'\n{kernel_name}SVM训练中...')
        print('-'*60)
        
        # 创建SVM模型
        if kernel == 'poly':
            # 多项式核，设置degree=3
            svm = SVC(kernel=kernel, degree=3, random_state=42)
        else:
            svm = SVC(kernel=kernel, random_state=42)
        
        # 训练模型
        svm.fit(X_train, y_train)
        
        # 预测
        y_pred = svm.predict(X_test)
        
        # 计算准确率
        accuracy = accuracy_score(y_test, y_pred)
        
        # 交叉验证
        cv_scores = cross_val_score(svm, X_train, y_train, cv=5)
        
        # 保存结果
        models[kernel] = svm
        results[kernel] = {
            'accuracy': accuracy,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'y_pred': y_pred,
            'support_vectors': svm.n_support_
        }
        
        print(f'测试集准确率：{accuracy:.4f}')
        print(f'交叉验证准确率：{cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})')
        print(f'支持向量数量：{svm.n_support_}')
    
    return models, results


def evaluate_models(models, results, X_test, y_test, dataset_name, class_names):
    """评估模型性能"""
    print('\n' + '='*60)
    print(f'第四部分：{dataset_name} - 模型性能评估')
    print('='*60)
    
    kernels = ['linear', 'poly', 'rbf']
    kernel_names = ['线性核', '多项式核', '高斯核(RBF)']
    
    for kernel, kernel_name in zip(kernels, kernel_names):
        print(f'\n{kernel_name}SVM评估结果：')
        print('-'*60)
        
        y_pred = results[kernel]['y_pred']
        
        # 打印分类报告
        print('\n分类报告：')
        print(classification_report(y_test, y_pred, target_names=class_names))
        
        # 混淆矩阵
        cm = confusion_matrix(y_test, y_pred)
        print('\n混淆矩阵：')
        print(cm)


def plot_confusion_matrices(results, y_test, dataset_name, class_names):
    """绘制混淆矩阵"""
    print(f'\n绘制{dataset_name}混淆矩阵...')
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 4))
    kernels = ['linear', 'poly', 'rbf']
    kernel_names = ['Linear', 'Polynomial', 'RBF']
    
    for idx, (kernel, kernel_name) in enumerate(zip(kernels, kernel_names)):
        y_pred = results[kernel]['y_pred']
        cm = confusion_matrix(y_test, y_pred)
        
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=class_names, yticklabels=class_names,
                   ax=axes[idx], cbar_kws={'shrink': 0.8})
        axes[idx].set_title(f'{kernel_name} SVM\nAccuracy: {results[kernel]["accuracy"]:.4f}', 
                           fontsize=12, fontweight='bold')
        axes[idx].set_xlabel('Predicted Label', fontsize=10)
        axes[idx].set_ylabel('True Label', fontsize=10)
    
    plt.tight_layout()
    filename = f'figures/03_{dataset_name}_confusion_matrices.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()
    print(f'混淆矩阵已保存：{filename}')


def plot_model_comparison(results_iris, results_cancer):
    """对比不同模型的性能"""
    print('\n绘制模型性能对比图...')
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    kernels = ['linear', 'poly', 'rbf']
    kernel_names = ['Linear', 'Polynomial', 'RBF']
    
    # Iris数据集对比
    iris_accuracies = [results_iris[k]['accuracy'] for k in kernels]
    iris_cv_means = [results_iris[k]['cv_mean'] for k in kernels]
    
    x = np.arange(len(kernel_names))
    width = 0.35
    
    axes[0].bar(x - width/2, iris_accuracies, width, label='Test Accuracy', color='skyblue')
    axes[0].bar(x + width/2, iris_cv_means, width, label='CV Accuracy', color='lightcoral')
    axes[0].set_xlabel('Kernel Type', fontsize=12)
    axes[0].set_ylabel('Accuracy', fontsize=12)
    axes[0].set_title('Iris Dataset - Kernel Comparison', fontsize=14, fontweight='bold')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(kernel_names)
    axes[0].legend()
    axes[0].grid(True, alpha=0.3, axis='y')
    axes[0].set_ylim([0.8, 1.0])
    
    # 乳腺癌数据集对比
    cancer_accuracies = [results_cancer[k]['accuracy'] for k in kernels]
    cancer_cv_means = [results_cancer[k]['cv_mean'] for k in kernels]
    
    axes[1].bar(x - width/2, cancer_accuracies, width, label='Test Accuracy', color='skyblue')
    axes[1].bar(x + width/2, cancer_cv_means, width, label='CV Accuracy', color='lightcoral')
    axes[1].set_xlabel('Kernel Type', fontsize=12)
    axes[1].set_ylabel('Accuracy', fontsize=12)
    axes[1].set_title('Breast Cancer Dataset - Kernel Comparison', fontsize=14, fontweight='bold')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(kernel_names)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3, axis='y')
    axes[1].set_ylim([0.8, 1.0])
    
    plt.tight_layout()
    plt.savefig('figures/04_model_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    print('模型性能对比图已保存：figures/04_model_comparison.png')


def plot_decision_boundary(X, y, model, title, filename, feature_names=None):
    """绘制决策边界（仅适用于2D数据）"""
    # 只使用前两个特征
    X_2d = X[:, :2]
    
    # 创建网格
    h = 0.02
    x_min, x_max = X_2d[:, 0].min() - 1, X_2d[:, 0].max() + 1
    y_min, y_max = X_2d[:, 1].min() - 1, X_2d[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    
    # 预测
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    # 绘图
    plt.figure(figsize=(10, 7))
    plt.contourf(xx, yy, Z, alpha=0.3, cmap='RdYlBu')
    
    # 绘制数据点
    scatter = plt.scatter(X_2d[:, 0], X_2d[:, 1], c=y, cmap='RdYlBu', 
                         edgecolors='black', s=50, alpha=0.7)
    
    # 绘制支持向量
    plt.scatter(model.support_vectors_[:, 0], model.support_vectors_[:, 1],
               s=200, linewidth=1.5, facecolors='none', edgecolors='green',
               label='Support Vectors')
    
    if feature_names:
        plt.xlabel(feature_names[0], fontsize=12)
        plt.ylabel(feature_names[1], fontsize=12)
    else:
        plt.xlabel('Feature 1', fontsize=12)
        plt.ylabel('Feature 2', fontsize=12)
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.colorbar(scatter)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    print('这是模型训练模块，请从主程序运行')

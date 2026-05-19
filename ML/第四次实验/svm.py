#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SVM实验 - 超参数调优
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
import warnings

warnings.filterwarnings('ignore')


# ============================================================
# 第五部分：超参数调优
# ============================================================

def hyperparameter_tuning(X_train, y_train, X_test, y_test, dataset_name):
    """使用网格搜索进行超参数调优"""
    print('\n' + '='*60)
    print(f'第五部分：{dataset_name} - 超参数调优')
    print('='*60)
    
    # 定义参数网格
    param_grid = {
        'C': [0.1, 1, 10, 100],
        'gamma': [0.001, 0.01, 0.1, 1],
        'kernel': ['rbf']
    }
    
    print('\n参数搜索空间：')
    print(f'C: {param_grid["C"]}')
    print(f'gamma: {param_grid["gamma"]}')
    print(f'kernel: {param_grid["kernel"]}')
    
    # 创建网格搜索对象
    print('\n开始网格搜索...')
    grid_search = GridSearchCV(
        SVC(random_state=42),
        param_grid,
        cv=5,
        scoring='accuracy',
        n_jobs=-1,
        verbose=1
    )
    
    # 执行网格搜索
    grid_search.fit(X_train, y_train)
    
    # 最佳参数
    print('\n最佳参数：')
    print(grid_search.best_params_)
    
    # 最佳模型性能
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f'\n最佳模型交叉验证准确率：{grid_search.best_score_:.4f}')
    print(f'最佳模型测试集准确率：{accuracy:.4f}')
    
    # 返回结果
    results = {
        'best_params': grid_search.best_params_,
        'best_score': grid_search.best_score_,
        'test_accuracy': accuracy,
        'cv_results': grid_search.cv_results_,
        'best_model': best_model
    }
    
    return results


def plot_hyperparameter_heatmap(tuning_results, dataset_name):
    """绘制超参数调优热力图"""
    print(f'\n绘制{dataset_name}超参数调优热力图...')
    
    cv_results = tuning_results['cv_results']
    
    # 提取C和gamma的值
    C_values = [0.1, 1, 10, 100]
    gamma_values = [0.001, 0.01, 0.1, 1]
    
    # 创建准确率矩阵
    scores = np.zeros((len(gamma_values), len(C_values)))
    
    for i, gamma in enumerate(gamma_values):
        for j, C in enumerate(C_values):
            # 找到对应的索引
            idx = None
            for k, params in enumerate(cv_results['params']):
                if params['C'] == C and params['gamma'] == gamma:
                    idx = k
                    break
            if idx is not None:
                scores[i, j] = cv_results['mean_test_score'][idx]
    
    # 绘制热力图
    plt.figure(figsize=(10, 7))
    sns.heatmap(scores, annot=True, fmt='.4f', cmap='YlGnBu',
                xticklabels=C_values, yticklabels=gamma_values,
                cbar_kws={'label': 'CV Accuracy'})
    plt.xlabel('C (Penalty Parameter)', fontsize=12)
    plt.ylabel('gamma (Kernel Parameter)', fontsize=12)
    plt.title(f'{dataset_name} - RBF Kernel Hyperparameter Tuning', fontsize=14, fontweight='bold')
    
    # 标记最佳参数
    best_C = tuning_results['best_params']['C']
    best_gamma = tuning_results['best_params']['gamma']
    best_C_idx = C_values.index(best_C)
    best_gamma_idx = gamma_values.index(best_gamma)
    plt.scatter(best_C_idx + 0.5, best_gamma_idx + 0.5, 
               marker='*', s=500, color='red', 
               label=f'Best (C={best_C}, gamma={best_gamma})')
    plt.legend(loc='upper left', bbox_to_anchor=(1.15, 1))
    
    plt.tight_layout()
    filename = f'figures/05_{dataset_name}_hyperparameter_tuning.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()
    print(f'超参数调优热力图已保存：{filename}')


def plot_parameter_comparison(tuning_results_iris, tuning_results_cancer):
    """对比两个数据集的最佳参数"""
    print('\n绘制参数对比图...')
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # C参数对比
    datasets = ['Iris', 'Cancer']
    C_values = [
        tuning_results_iris['best_params']['C'],
        tuning_results_cancer['best_params']['C']
    ]
    gamma_values = [
        tuning_results_iris['best_params']['gamma'],
        tuning_results_cancer['best_params']['gamma']
    ]
    
    x = np.arange(len(datasets))
    
    axes[0].bar(x, C_values, color=['skyblue', 'lightcoral'], alpha=0.7)
    axes[0].set_xlabel('数据集', fontsize=12)
    axes[0].set_ylabel('C值', fontsize=12)
    axes[0].set_title('Best C Parameter Comparison', fontsize=14, fontweight='bold')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(datasets)
    axes[0].grid(True, alpha=0.3, axis='y')
    
    # 在柱子上标注数值
    for i, v in enumerate(C_values):
        axes[0].text(i, v + max(C_values)*0.02, str(v), 
                    ha='center', va='bottom', fontweight='bold')
    
    axes[1].bar(x, gamma_values, color=['skyblue', 'lightcoral'], alpha=0.7)
    axes[1].set_xlabel('Dataset', fontsize=12)
    axes[1].set_ylabel('gamma Value', fontsize=12)
    axes[1].set_title('Best gamma Parameter Comparison', fontsize=14, fontweight='bold')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(datasets)
    axes[1].grid(True, alpha=0.3, axis='y')
    
    for i, v in enumerate(gamma_values):
        axes[1].text(i, v + max(gamma_values)*0.02, str(v), 
                    ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('figures/06_parameter_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    print('参数对比图已保存：figures/06_parameter_comparison.png')


def compare_before_after_tuning(results_before, results_after, dataset_name):
    """对比调优前后的性能"""
    print(f'\n{dataset_name} - 调优前后性能对比：')
    print('-'*60)
    
    before_acc = results_before['rbf']['accuracy']
    after_acc = results_after['test_accuracy']
    improvement = (after_acc - before_acc) * 100
    
    print(f'调优前准确率：{before_acc:.4f}')
    print(f'调优后准确率：{after_acc:.4f}')
    print(f'性能提升：{improvement:.2f}%')
    
    return {
        'before': before_acc,
        'after': after_acc,
        'improvement': improvement
    }


def plot_tuning_improvement(comparison_iris, comparison_cancer):
    """绘制调优前后的性能提升图"""
    print('\n绘制调优前后性能提升图...')
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Iris数据集
    categories = ['Before Tuning', 'After Tuning']
    iris_values = [comparison_iris['before'], comparison_iris['after']]
    
    bars1 = axes[0].bar(categories, iris_values, color=['lightblue', 'lightgreen'], alpha=0.7)
    axes[0].set_ylabel('Accuracy', fontsize=12)
    axes[0].set_title('Iris Dataset - Before vs After Tuning', fontsize=14, fontweight='bold')
    axes[0].set_ylim([0.9, 1.0])
    axes[0].grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars1, iris_values):
        height = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2., height + 0.005,
                    f'{val:.4f}', ha='center', va='bottom', fontweight='bold')
    
    # 乳腺癌数据集
    cancer_values = [comparison_cancer['before'], comparison_cancer['after']]
    
    bars2 = axes[1].bar(categories, cancer_values, color=['lightblue', 'lightgreen'], alpha=0.7)
    axes[1].set_ylabel('Accuracy', fontsize=12)
    axes[1].set_title('Breast Cancer Dataset - Before vs After Tuning', fontsize=14, fontweight='bold')
    axes[1].set_ylim([0.9, 1.0])
    axes[1].grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars2, cancer_values):
        height = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2., height + 0.005,
                    f'{val:.4f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('figures/07_tuning_improvement.png', dpi=300, bbox_inches='tight')
    plt.show()
    print('调优前后性能提升图已保存：figures/07_tuning_improvement.png')


if __name__ == '__main__':
    print('这是超参数调优模块，请从主程序运行')


"""
SVM实验 - 完整主程序
整合所有实验步骤，生成完整的实验报告
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC

# 导入自定义模块
from svm_experiment_part1 import load_and_explore_data, visualize_data, preprocess_data
from svm_experiment_part2 import (train_svm_models, evaluate_models, 
                                   plot_confusion_matrices, plot_model_comparison,
                                   plot_decision_boundary)
from svm_experiment_part3 import (hyperparameter_tuning, plot_hyperparameter_heatmap,
                                   plot_parameter_comparison, compare_before_after_tuning,
                                   plot_tuning_improvement)


def plot_decision_boundaries_all_kernels(X_train, y_train, models, scaler, iris):
    """绘制所有核函数的决策边界"""
    print('\n绘制决策边界（使用前两个特征）...')
    
    # 只使用前两个特征重新训练模型
    X_train_2d = X_train[:, :2]
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    kernels = ['linear', 'poly', 'rbf']
    kernel_names = ['Linear', 'Polynomial', 'RBF']
    
    for idx, (kernel, kernel_name) in enumerate(zip(kernels, kernel_names)):
        # 使用前两个特征训练模型
        if kernel == 'poly':
            model_2d = SVC(kernel=kernel, degree=3, random_state=42)
        else:
            model_2d = SVC(kernel=kernel, random_state=42)
        
        model_2d.fit(X_train_2d, y_train)
        
        # 创建网格
        h = 0.02
        x_min, x_max = X_train_2d[:, 0].min() - 1, X_train_2d[:, 0].max() + 1
        y_min, y_max = X_train_2d[:, 1].min() - 1, X_train_2d[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))
        
        # 预测
        Z = model_2d.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        
        # 绘制决策边界
        axes[idx].contourf(xx, yy, Z, alpha=0.3, cmap='RdYlBu')
        
        # 绘制数据点
        scatter = axes[idx].scatter(X_train_2d[:, 0], X_train_2d[:, 1], 
                                   c=y_train, cmap='RdYlBu', 
                                   edgecolors='black', s=50, alpha=0.7)
        
        # 绘制支持向量
        axes[idx].scatter(model_2d.support_vectors_[:, 0], 
                         model_2d.support_vectors_[:, 1],
                         s=200, linewidth=1.5, facecolors='none', 
                         edgecolors='green', label='Support Vectors')
        
        axes[idx].set_xlabel(iris.feature_names[0], fontsize=11)
        axes[idx].set_ylabel(iris.feature_names[1], fontsize=11)
        axes[idx].set_title(f'{kernel_name} SVM Decision Boundary\nSupport Vectors: {len(model_2d.support_vectors_)}', 
                           fontsize=12, fontweight='bold')
        axes[idx].legend(loc='upper right')
        axes[idx].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('figures/08_decision_boundaries.png', dpi=300, bbox_inches='tight')
    plt.show()
    print('决策边界图已保存：figures/08_decision_boundaries.png')


def main():
    """主函数：运行完整的SVM实验"""
    print('\n')
    print('*'*60)
    print('*' + ' '*58 + '*')
    print('*' + ' '*15 + 'SVM支持向量机实验' + ' '*15 + '*')
    print('*' + ' '*58 + '*')
    print('*'*60)
    print('\n')
    
    # ============================================================
    # 第一阶段：数据准备
    # ============================================================
    iris, cancer, iris_df, cancer_df = load_and_explore_data()
    visualize_data(iris_df, cancer_df)
    
    (X_iris_train, X_iris_test, y_iris_train, y_iris_test,
     X_cancer_train, X_cancer_test, y_cancer_train, y_cancer_test,
     scaler_iris, scaler_cancer) = preprocess_data(iris, cancer)
    
    # ============================================================
    # 第二阶段：模型训练与评估
    # ============================================================
    
    # Iris数据集
    models_iris, results_iris = train_svm_models(
        X_iris_train, y_iris_train, X_iris_test, y_iris_test, 'Iris数据集'
    )
    
    evaluate_models(models_iris, results_iris, X_iris_test, y_iris_test, 
                   'Iris数据集', iris.target_names)
    
    plot_confusion_matrices(results_iris, y_iris_test, 'iris', iris.target_names)
    
    # 乳腺癌数据集
    models_cancer, results_cancer = train_svm_models(
        X_cancer_train, y_cancer_train, X_cancer_test, y_cancer_test, '乳腺癌数据集'
    )
    
    evaluate_models(models_cancer, results_cancer, X_cancer_test, y_cancer_test,
                   '乳腺癌数据集', ['malignant', 'benign'])
    
    plot_confusion_matrices(results_cancer, y_cancer_test, 'cancer', ['Malignant', 'Benign'])
    
    # 模型性能对比
    plot_model_comparison(results_iris, results_cancer)
    
    # 绘制决策边界
    plot_decision_boundaries_all_kernels(X_iris_train, y_iris_train, 
                                        models_iris, scaler_iris, iris)
    
    # ============================================================
    # 第三阶段：超参数调优
    # ============================================================
    
    # Iris数据集调优
    tuning_results_iris = hyperparameter_tuning(
        X_iris_train, y_iris_train, X_iris_test, y_iris_test, 'Iris数据集'
    )
    plot_hyperparameter_heatmap(tuning_results_iris, 'iris')
    
    # 乳腺癌数据集调优
    tuning_results_cancer = hyperparameter_tuning(
        X_cancer_train, y_cancer_train, X_cancer_test, y_cancer_test, '乳腺癌数据集'
    )
    plot_hyperparameter_heatmap(tuning_results_cancer, 'cancer')
    
    # 参数对比
    plot_parameter_comparison(tuning_results_iris, tuning_results_cancer)
    
    # 调优前后对比
    comparison_iris = compare_before_after_tuning(
        results_iris, tuning_results_iris, 'Iris数据集'
    )
    comparison_cancer = compare_before_after_tuning(
        results_cancer, tuning_results_cancer, '乳腺癌数据集'
    )
    
    plot_tuning_improvement(comparison_iris, comparison_cancer)
    
    # ============================================================
    # 实验总结
    # ============================================================
    print('\n' + '='*60)
    print('实验总结')
    print('='*60)
    
    print('\n【Iris数据集实验结果】')
    print('-'*60)
    print('1. 不同核函数性能：')
    for kernel in ['linear', 'poly', 'rbf']:
        print(f'   {kernel}核: 准确率={results_iris[kernel]["accuracy"]:.4f}')
    print(f'\n2. 最佳参数：C={tuning_results_iris["best_params"]["C"]}, '
          f'gamma={tuning_results_iris["best_params"]["gamma"]}')
    print(f'3. 调优后准确率：{tuning_results_iris["test_accuracy"]:.4f}')
    
    print('\n【乳腺癌数据集实验结果】')
    print('-'*60)
    print('1. 不同核函数性能：')
    for kernel in ['linear', 'poly', 'rbf']:
        print(f'   {kernel}核: 准确率={results_cancer[kernel]["accuracy"]:.4f}')
    print(f'\n2. 最佳参数：C={tuning_results_cancer["best_params"]["C"]}, '
          f'gamma={tuning_results_cancer["best_params"]["gamma"]}')
    print(f'3. 调优后准确率：{tuning_results_cancer["test_accuracy"]:.4f}')
    
    print('\n' + '='*60)
    print('所有实验完成！图片已保存到 figures/ 文件夹')
    print('='*60)
    
    # 返回所有结果用于生成报告
    return {
        'iris': {
            'data': iris,
            'models': models_iris,
            'results': results_iris,
            'tuning': tuning_results_iris,
            'comparison': comparison_iris
        },
        'cancer': {
            'data': cancer,
            'models': models_cancer,
            'results': results_cancer,
            'tuning': tuning_results_cancer,
            'comparison': comparison_cancer
        }
    }


if __name__ == '__main__':
    # 运行完整实验
    all_results = main()
    
    # 生成Word报告
    print('\n正在生成Word实验报告...')
    try:
        from generate_report import generate_word_report
        generate_word_report(all_results)
        print('Word报告生成成功：SVM实验报告.docx')
    except Exception as e:
        print(f'Word报告生成失败：{e}')
        print('请手动运行 generate_report.py 生成报告')

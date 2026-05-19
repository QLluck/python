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

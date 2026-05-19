#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
构建完整的Jupyter Notebook
"""

import json
import os

def create_complete_notebook():
    """创建完整的SVM实验Notebook"""
    
    # 基础结构
    notebook = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    # 读取Python脚本内容
    scripts = []
    for filename in ['svm_experiment_part1.py', 'svm_experiment_part2.py', 
                     'svm_experiment_part3.py', 'main.py']:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                scripts.append(f.read())
    
    # 创建单元格列表
    cells = []
    
    # 标题单元格
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": ["# SVM支持向量机实验\n", "\n", "**实验目标**：\n", 
                   "1. 掌握SVM基本原理\n", "2. 实现不同核函数的SVM\n", 
                   "3. 学习超参数调优\n", "4. 培养数据分析和可视化能力\n"]
    })
    
    # 导入库
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 导入必要的库\n",
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
            "import warnings\n",
            "import os\n",
            "\n",
            "warnings.filterwarnings('ignore')\n",
            "np.random.seed(42)\n",
            "plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei']\n",
            "plt.rcParams['axes.unicode_minus'] = False\n",
            "sns.set_style('whitegrid')\n",
            "os.makedirs('figures', exist_ok=True)\n",
            "print('环境准备完毕！')"
        ]
    })
    
    # 运行完整实验
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": ["## 运行完整实验\n", "\n", 
                   "执行下面的单元格将运行完整的SVM实验，包括数据加载、模型训练、超参数调优和报告生成。\n"]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 运行完整实验\n",
            "# 如果遇到导入错误，请确保所有.py文件在同一目录下\n",
            "import sys\n",
            "sys.path.append('.')\n",
            "\n",
            "# 方法1：直接运行main.py\n",
            "# %run main.py\n",
            "\n",
            "# 方法2：逐步运行（推荐，可以看到每一步的输出）\n",
            "print('开始SVM实验...')\n",
            "print('请继续运行下面的单元格')"
        ]
    })
    
    # 添加分步实验单元格
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": ["## 第一步：数据加载\n"]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from svm_experiment_part1 import load_and_explore_data, visualize_data, preprocess_data\n",
            "\n",
            "# 加载数据\n",
            "iris, cancer, iris_df, cancer_df = load_and_explore_data()\n",
            "\n",
            "# 可视化\n",
            "visualize_data(iris_df, cancer_df)\n",
            "\n",
            "# 预处理\n",
            "data = preprocess_data(iris, cancer)\n",
            "(X_iris_train, X_iris_test, y_iris_train, y_iris_test,\n",
            " X_cancer_train, X_cancer_test, y_cancer_train, y_cancer_test,\n",
            " scaler_iris, scaler_cancer) = data"
        ]
    })
    
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": ["## 第二步：模型训练\n"]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from svm_experiment_part2 import (train_svm_models, evaluate_models, \n",
            "                                   plot_confusion_matrices, plot_model_comparison)\n",
            "\n",
            "# 训练Iris数据集\n",
            "models_iris, results_iris = train_svm_models(\n",
            "    X_iris_train, y_iris_train, X_iris_test, y_iris_test, 'Iris数据集'\n",
            ")\n",
            "\n",
            "# 评估\n",
            "evaluate_models(models_iris, results_iris, X_iris_test, y_iris_test, \n",
            "               'Iris数据集', iris.target_names)\n",
            "\n",
            "# 混淆矩阵\n",
            "plot_confusion_matrices(results_iris, y_iris_test, 'iris', iris.target_names)"
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 训练乳腺癌数据集\n",
            "models_cancer, results_cancer = train_svm_models(\n",
            "    X_cancer_train, y_cancer_train, X_cancer_test, y_cancer_test, '乳腺癌数据集'\n",
            ")\n",
            "\n",
            "# 评估\n",
            "evaluate_models(models_cancer, results_cancer, X_cancer_test, y_cancer_test,\n",
            "               '乳腺癌数据集', ['malignant', 'benign'])\n",
            "\n",
            "# 混淆矩阵\n",
            "plot_confusion_matrices(results_cancer, y_cancer_test, 'cancer', ['恶性', '良性'])\n",
            "\n",
            "# 性能对比\n",
            "plot_model_comparison(results_iris, results_cancer)"
        ]
    })
    
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": ["## 第三步：超参数调优\n"]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from svm_experiment_part3 import (hyperparameter_tuning, plot_hyperparameter_heatmap,\n",
            "                                   compare_before_after_tuning, plot_tuning_improvement)\n",
            "\n",
            "# Iris数据集调优\n",
            "tuning_results_iris = hyperparameter_tuning(\n",
            "    X_iris_train, y_iris_train, X_iris_test, y_iris_test, 'Iris数据集'\n",
            ")\n",
            "plot_hyperparameter_heatmap(tuning_results_iris, 'iris')\n",
            "\n",
            "# 乳腺癌数据集调优\n",
            "tuning_results_cancer = hyperparameter_tuning(\n",
            "    X_cancer_train, y_cancer_train, X_cancer_test, y_cancer_test, '乳腺癌数据集'\n",
            ")\n",
            "plot_hyperparameter_heatmap(tuning_results_cancer, 'cancer')"
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 调优前后对比\n",
            "comparison_iris = compare_before_after_tuning(results_iris, tuning_results_iris, 'Iris数据集')\n",
            "comparison_cancer = compare_before_after_tuning(results_cancer, tuning_results_cancer, '乳腺癌数据集')\n",
            "plot_tuning_improvement(comparison_iris, comparison_cancer)"
        ]
    })
    
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": ["## 第四步：生成Word报告\n"]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from generate_report import generate_word_report\n",
            "\n",
            "# 生成报告\n",
            "generate_word_report()\n",
            "print('\\n实验完成！Word报告已生成：SVM实验报告.docx')"
        ]
    })
    
    # 保存notebook
    notebook["cells"] = cells
    
    with open('SVM实验.ipynb', 'w', encoding='utf-8') as f:
        json.dump(notebook, f, ensure_ascii=False, indent=2)
    
    print("完整的Jupyter Notebook已创建：SVM实验.ipynb")
    print(f"总共 {len(cells)} 个单元格")


if __name__ == '__main__':
    create_complete_notebook()

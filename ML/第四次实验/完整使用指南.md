# 🎓 SVM实验 - 完整使用指南

## 📋 目录
1. [快速开始](#快速开始)
2. [项目结构](#项目结构)
3. [安装步骤](#安装步骤)
4. [运行实验](#运行实验)
5. [实验内容](#实验内容)
6. [常见问题](#常见问题)

---

## 🚀 快速开始

### 第一步：测试环境
```bash
python3 test_environment.py
```

### 第二步：安装依赖
```bash
pip install -r requirements.txt
```

### 第三步：运行实验
```bash
# 方法1：使用Jupyter Notebook（推荐）
jupyter notebook
# 然后打开 SVM实验.ipynb

# 方法2：直接运行Python脚本
python3 main.py
```

---

## 📁 项目结构

```
第四次实验/
│
├── 📘 文档文件
│   ├── README.md                  # 项目说明
│   ├── 快速开始.md                # 快速开始指南
│   ├── 实验计划.md                # 详细实验计划
│   ├── 项目交付清单.md            # 项目交付清单
│   └── requirements.txt           # 依赖库列表
│
├── 💻 代码文件
│   ├── main.py                    # 主程序（运行完整实验）
│   ├── svm_experiment_part1.py    # 第1部分：数据加载与预处理
│   ├── svm_experiment_part2.py    # 第2部分：模型训练与评估
│   ├── svm_experiment_part3.py    # 第3部分：超参数调优
│   ├── generate_report.py         # Word报告生成器
│   ├── build_notebook.py          # Notebook构建脚本
│   └── test_environment.py        # 环境测试脚本
│
├── 📓 Jupyter Notebook
│   └── SVM实验.ipynb              # 交互式实验笔记本
│
└── 📊 输出文件（运行后生成）
    ├── figures/                   # 图片文件夹
    │   ├── 01_iris_distribution.png
    │   ├── 02_cancer_distribution.png
    │   ├── 03_iris_confusion_matrices.png
    │   ├── 03_cancer_confusion_matrices.png
    │   ├── 04_model_comparison.png
    │   ├── 05_iris_hyperparameter_tuning.png
    │   ├── 05_cancer_hyperparameter_tuning.png
    │   ├── 06_parameter_comparison.png
    │   ├── 07_tuning_improvement.png
    │   └── 08_decision_boundaries.png
    │
    └── SVM实验报告.docx           # Word实验报告
```

---

## 🔧 安装步骤

### 1. 检查Python版本
```bash
python3 --version
# 需要 Python 3.7 或更高版本
```

### 2. 安装依赖库
```bash
# 方法1：使用pip安装（推荐）
pip install -r requirements.txt

# 方法2：手动安装
pip install numpy pandas matplotlib seaborn scikit-learn python-docx jupyter
```

### 3. 验证安装
```bash
python3 test_environment.py
```

如果看到 "🎉 恭喜！所有测试通过"，说明环境配置成功！

---

## 🎯 运行实验

### 方法1：Jupyter Notebook（推荐⭐）

**优点**：交互式、可视化效果好、便于调试

```bash
# 1. 启动Jupyter
jupyter notebook

# 2. 在浏览器中打开 SVM实验.ipynb

# 3. 依次运行每个单元格（Shift + Enter）
```

**运行顺序**：
1. 导入库和环境设置
2. 数据加载与可视化
3. 数据预处理
4. 模型训练（Iris数据集）
5. 模型训练（乳腺癌数据集）
6. 超参数调优
7. 生成Word报告

---

### 方法2：Python脚本

**优点**：一键运行、自动化程度高

```bash
# 运行完整实验（推荐）
python3 main.py
```

**分步运行**：
```bash
# 步骤1：数据准备
python3 svm_experiment_part1.py

# 步骤2：模型训练
python3 svm_experiment_part2.py

# 步骤3：超参数调优
python3 svm_experiment_part3.py

# 步骤4：生成报告
python3 generate_report.py
```

---

### 方法3：仅生成Word报告

如果已经运行过实验并生成了图片：

```bash
python3 generate_report.py
```

---

## 📚 实验内容

### 实验目标
1. ✅ 掌握SVM基本原理与数学模型
2. ✅ 实现不同核函数的SVM（线性核、多项式核、RBF核）
3. ✅ 学习超参数调优方法（网格搜索）
4. ✅ 培养数据预处理能力
5. ✅ 培养结果可视化能力

### 数据集

**数据集1：Iris鸢尾花数据集**
- 样本数：150
- 特征数：4（花萼长度、花萼宽度、花瓣长度、花瓣宽度）
- 类别数：3（Setosa、Versicolour、Virginica）
- 特点：部分线性可分

**数据集2：乳腺癌数据集**
- 样本数：569
- 特征数：30（细胞核特征）
- 类别数：2（恶性、良性）
- 特点：高维、非线性可分

### 实验步骤

1. **数据加载与探索**
   - 加载数据集
   - 查看数据基本信息
   - 可视化数据分布
   - 分析特征相关性

2. **数据预处理**
   - 划分训练集和测试集（70%/30%）
   - 特征标准化（StandardScaler）

3. **模型训练**
   - 线性核SVM
   - 多项式核SVM（degree=3）
   - RBF核SVM

4. **模型评估**
   - 准确率
   - 交叉验证（5折）
   - 混淆矩阵
   - 分类报告

5. **超参数调优**
   - 网格搜索（GridSearchCV）
   - 调优参数：C（惩罚系数）、gamma（核函数参数）
   - 参数范围：C=[0.1, 1, 10, 100], gamma=[0.001, 0.01, 0.1, 1]

6. **结果可视化**
   - 数据分布图
   - 混淆矩阵热力图
   - 决策边界图
   - 超参数调优热力图
   - 性能对比图

7. **报告生成**
   - 自动生成Word报告
   - 包含四个部分：算法描述、程序清单、实验结果、疑难小结

---

## ❓ 常见问题

### Q1: 中文显示为方框怎么办？

**A**: 修改字体设置

```python
# Mac系统
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

# Windows系统
plt.rcParams['font.sans-serif'] = ['SimHei']

# Linux系统
plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
```

---

### Q2: 导入模块失败

**A**: 确保安装了所有依赖

```bash
# 重新安装依赖
pip install -r requirements.txt

# 或者单独安装缺失的库
pip install scikit-learn
```

---

### Q3: Jupyter Notebook中图片不显示

**A**: 在第一个代码单元格中添加

```python
%matplotlib inline
```

---

### Q4: 网格搜索运行太慢

**A**: 减少参数网格或使用并行计算

```python
# 方法1：减少参数
param_grid = {
    'C': [1, 10],           # 从4个减少到2个
    'gamma': [0.01, 0.1]    # 从4个减少到2个
}

# 方法2：使用并行计算
GridSearchCV(..., n_jobs=-1)  # 使用所有CPU核心
```

---

### Q5: 内存不足

**A**: 减少交叉验证折数

```python
GridSearchCV(..., cv=3)  # 从5折改为3折
```

---

### Q6: Word报告生成失败

**A**: 检查python-docx是否安装

```bash
pip install python-docx
```

---

### Q7: 图片保存失败

**A**: 检查文件夹权限

```bash
# 手动创建文件夹
mkdir figures
chmod 755 figures
```

---

## 📊 预期结果

### Iris数据集
- 线性核准确率：~95%
- 多项式核准确率：~96%
- RBF核准确率：~97%
- 最佳参数：C=10, gamma=0.1
- 运行时间：~2分钟

### 乳腺癌数据集
- 线性核准确率：~96%
- 多项式核准确率：~97%
- RBF核准确率：~98%
- 最佳参数：C=10, gamma=0.01
- 运行时间：~3分钟

### 总运行时间
- 完整实验：5-10分钟
- 主要时间：超参数网格搜索

---

## 🎨 输出文件说明

### 图片文件（figures/文件夹）

1. **01_iris_distribution.png**
   - Iris数据集分布图
   - 特征相关性热力图

2. **02_cancer_distribution.png**
   - 乳腺癌数据集PCA降维图
   - 类别分布柱状图

3. **03_iris_confusion_matrices.png**
   - Iris数据集三种核函数的混淆矩阵

4. **03_cancer_confusion_matrices.png**
   - 乳腺癌数据集三种核函数的混淆矩阵

5. **04_model_comparison.png**
   - 两个数据集的模型性能对比

6. **05_iris_hyperparameter_tuning.png**
   - Iris数据集超参数调优热力图

7. **05_cancer_hyperparameter_tuning.png**
   - 乳腺癌数据集超参数调优热力图

8. **06_parameter_comparison.png**
   - 两个数据集最佳参数对比

9. **07_tuning_improvement.png**
   - 调优前后性能提升对比

10. **08_decision_boundaries.png**
    - 三种核函数的决策边界可视化

### Word报告（SVM实验报告.docx）

**第一部分：算法描述、数据集介绍与实验方案**
- SVM算法原理
- 核函数介绍
- 数据集详细描述
- 实验方案设计

**第二部分：程序清单**
- 完整Python代码
- 详细中文注释
- 核心代码示例

**第三部分：实验结果**
- 所有可视化图表
- 性能指标分析
- 结果对比说明

**第四部分：疑难小结**
- 遇到的问题及解决方法
- 实验心得体会
- 算法优缺点总结
- 未来改进方向

---

## 💡 使用技巧

### 技巧1：快速测试
```bash
# 先运行测试脚本，确保环境正常
python3 test_environment.py
```

### 技巧2：分步调试
```bash
# 如果遇到问题，可以分步运行
python3 svm_experiment_part1.py  # 只运行数据准备
```

### 技巧3：查看中间结果
```python
# 在Jupyter中可以随时查看变量
print(iris_df.head())
print(results_iris)
```

### 技巧4：自定义参数
```python
# 修改超参数搜索范围
param_grid = {
    'C': [0.1, 1, 10, 100, 1000],  # 扩大搜索范围
    'gamma': [0.0001, 0.001, 0.01, 0.1, 1]
}
```

---

## 📖 学习资源

- **scikit-learn官方文档**: https://scikit-learn.org/stable/modules/svm.html
- **《统计学习方法》**: 李航著，第7章支持向量机
- **《机器学习》**: 周志华著，第6章支持向量机
- **Jupyter教程**: https://jupyter.org/documentation

---

## ✅ 检查清单

运行实验前，请确认：

- [ ] Python版本 >= 3.7
- [ ] 所有依赖库已安装
- [ ] 所有.py文件在同一目录
- [ ] 有足够的磁盘空间（至少50MB）
- [ ] 有网络连接（首次下载数据集）

运行实验后，应该生成：

- [ ] figures/文件夹（包含10张图片）
- [ ] SVM实验报告.docx
- [ ] 控制台输出了实验结果

---

## 🎓 适用场景

✅ 大学机器学习课程作业  
✅ SVM算法学习与实践  
✅ 数据分析项目参考  
✅ 机器学习入门教程  

---

## 📞 获取帮助

如果遇到问题：

1. 查看 `快速开始.md`
2. 查看 `实验计划.md`
3. 运行 `python3 test_environment.py` 检查环境
4. 查看代码中的详细注释
5. 检查控制台的错误信息

---

## 🎉 开始实验

一切准备就绪！现在可以开始你的SVM实验之旅了！

```bash
# 推荐使用Jupyter Notebook
jupyter notebook
```

祝实验顺利！🚀

---

**最后更新**: 2026年5月  
**版本**: 1.0  
**作者**: 机器学习实验项目

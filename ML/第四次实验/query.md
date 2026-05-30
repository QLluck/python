# SVM实验项目重构提示词

## 环境说明
- 使用 conda 环境：`source ~/anaconda3/bin/activate && conda activate ml`
- 代码分析和实验在 **Jupyter Notebook** 中完成，所有图表保存到 `figures/` 文件夹
- 最终实验报告输出为 **Markdown 文件**（`实验报告.md`）

## 项目要求
整体风格：**简单实现，不要太复杂**。一个 notebook + 一个 md 报告即可，不需要拆分成多个 .py 文件。

---

## 一、实验目标

1. 掌握支持向量机（SVM）的基本原理与数学模型
2. 熟悉 SVM 在不同数据集上的分类任务实现（线性核、多项式核、RBF核）
3. 学习 SVM 核函数的选择及超参数调优方法（C、gamma，网格搜索+交叉验证）
4. 培养数据预处理、模型训练及结果分析的能力
5. 培养对训练结果进行可视化的能力

---

## 二、实验内容

### 2.1 数据准备
- 使用 sklearn 内置的 **Iris 数据集**（线性可分）和 **Breast Cancer 数据集**（非线性可分）
- 在 notebook 中说明每个数据集的来源、特征含义、标签含义
- 对数据做 **StandardScaler 特征标准化**，分析数据分布（散点图、相关热力图、类别分布图）
- 按 7:3 划分训练集/测试集（stratify 保持类别比例）

### 2.2 算法实现
- 分别训练 **Linear SVM**、**Polynomial SVM（degree=3）**、**RBF SVM** 三种模型
- 输出分类准确率、混淆矩阵（热力图）、分类报告（precision/recall/f1-score）
- 使用 **网格搜索（GridSearchCV）** 对 RBF 核的 C 和 gamma 进行调优，搜索范围：C=[0.1,1,10,100], gamma=[0.001,0.01,0.1,1]
- 绘制超参数热力图、调优前后性能对比图

### 2.3 进阶要求（可选，但建议加上，很简单）
- 在 Iris 数据集上取前两个特征，绘制三种核函数的 **决策边界**，并标记 **支持向量**
- 对比调优前后的准确率

### 2.4 实验总结
- 在 notebook 末尾用 markdown 单元格总结实验结果、遇到的问题及改进方向

---

## 三、输出文件

1. **`SVM实验.ipynb`** — 完整的 Jupyter Notebook，包含所有代码和运行结果（图片内嵌在 notebook 中，同时保存到 figures/ 文件夹）
2. **`figures/`** — 保存所有图表的 PNG 文件（dpi=150 即可，不用 300）
3. **`实验报告.md`** — 实验报告，包含以下四个部分：
   - **1. 算法描述与实验方案**：SVM 原理简介、数据集说明、实验设计
   - **2. 程序清单**：关键代码片段 + 注释说明（直接从 notebook 摘录即可）
   - **3. 实验结果**：贴入关键图表截图，附上文字分析
   - **4. 疑难小结**：实验中遇到的问题、心得体会、算法适用场景总结

---

## 四、技术要求

- 使用 sklearn 的 `SVC`、`GridSearchCV`、`StandardScaler`、`confusion_matrix`、`classification_report`
- 所有图表使用 matplotlib + seaborn，中文字体设置为 `Arial Unicode MS` 或 `SimHei`
- 设置 `np.random.seed(42)` 保证可复现
- 代码注释用中文，简洁即可，不需要过度注释
- 不要引入 imbalanced-learn（SMOTE 如果太麻烦就跳过，用 class_weight='balanced' 示范一下就行）

---

## 五、注意事项

- **简单第一**：不要搞复杂的模块拆分，一个 notebook 从头到尾跑完就行
- 报告中的图片引用路径使用相对路径 `figures/xxx.png`
- notebook 中每个大步骤之间用 markdown 单元格做标题分隔
- 最终确保 notebook 从头运行到尾不出错，所有图片正常保存

# 提示词：聚类算法实验作业

请帮我完成一个机器学习聚类算法的实验作业，要求用 Jupyter Notebook（.ipynb）实现，并生成一份 Markdown 格式的实验报告。**整体保持简洁，代码注释清晰，不要过度复杂。**

---

## 环境要求

- 使用 `source ~/anaconda3/bin/activate && conda activate ml` 激活环境
- 所有图表保存到本地 `./figures/` 目录下
- Python 版本和主要库版本在报告中注明

---

## 一、实验目的

1. 掌握常见聚类算法（K-means、DBSCAN、层次聚类）的基本原理、实现流程及优缺点
2. 编程实现聚类算法
3. 通过实验对比不同聚类算法的性能差异
4. 提升数据预处理、结果可视化和算法调参的能力

---

## 二、实验内容

### 2.1 数据准备

1. **数据集选择**：使用 sklearn 生成合成数据集，至少包含以下三种类型：
   - 高斯分布数据（`make_blobs`）
   - 月牙形数据（`make_moons`）
   - 环形数据（`make_circles`）
   
   在报告中阐述每种数据集的特征和适用场景。

2. **数据预处理**：
   - 使用 `StandardScaler` 进行 Z-score 标准化
   - 分析并可视化标准化前后的数据分布

### 2.2 算法实现

对每种数据集，分别实现以下三种聚类算法，并对比性能：

1. **K-means 聚类**
   - 使用肘部法则（Elbow Method）选择最佳 K 值
   - 可视化不同 K 值下的 SSE 曲线
   - 输出轮廓系数（Silhouette Score）和 Calinski-Harabasz 指数

2. **DBSCAN 密度聚类**
   - 调整 `eps`（半径）和 `min_samples`（最小样本数）两个关键参数
   - 对比不同参数组合下的聚类效果
   - 输出轮廓系数和 Calinski-Harabasz 指数

3. **层次聚类（Agglomerative Clustering）**
   - 尝试不同连接方式：Ward、Average、Complete
   - 尝试不同距离度量：欧氏距离、余弦距离（在数据标准化后，欧氏距离与余弦距离等价，可只演示欧氏距离+不同linkage）
   - 绘制树状图（dendrogram）
   - 输出轮廓系数和 Calinski-Harabasz 指数

### 2.3 可视化要求

- 每种算法聚类结果用散点图展示，不同簇用不同颜色
- K-means 标注簇中心位置
- 层次聚类绘制树状图
- 汇总三种算法在三种数据集上的性能对比表格

### 2.4 性能度量指标

- 轮廓系数（Silhouette Score）
- Calinski-Harabasz 指数

---

## 三、输出文件

### 3.1 Jupyter Notebook（clustering_experiment.ipynb）

- 结构清晰：Markdown 标题 + 说明文字 + 代码 + 输出图表
- 每个实验步骤有对应标题和简要说明
- 代码注释充分（中文注释）
- 所有图片用 `plt.savefig('./figures/xxx.png', dpi=150, bbox_inches='tight')` 保存到本地

### 3.2 实验报告（report.md）

按照以下格式组织：

```
# 聚类算法实验报告

## 一、实验目的
（简述）

## 二、算法与数据集描述
- 三种算法的原理简述、优缺点
- 所选数据集的描述

## 三、实验方案
- 整体实验流程概述
- 参数调优策略

## 四、程序清单
（列出 notebook 中的主要代码模块及功能说明）

## 五、实验结果
- 各算法的聚类效果截图/描述
- 性能指标对比表
- 参数调优过程与结果分析

## 六、疑难小结
- 实验中遇到的问题
- 心得体会
- 算法的适用场景与局限性总结
```

---

## 四、注意事项

1. **不要过度复杂**，每个算法用 sklearn 现成接口即可，不需要手写实现
2. 代码运行结果（图表、指标）直接嵌入 notebook，图表同步保存到 `./figures/`
3. 报告中提到的截图路径对应 `./figures/` 中的图片
4. notebook 和报告要互相呼应，报告是对 notebook 结果的总结分析
5. 随机种子统一设为 `random_state=42`，确保可复现

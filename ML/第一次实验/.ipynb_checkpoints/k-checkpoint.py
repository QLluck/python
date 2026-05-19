# ======================
# 导入所需库
# ======================
import pandas as pd                 # 用于读取csv、处理表格数据
import numpy as np                  # 数值计算
from sklearn.neighbors import KNeighborsClassifier   # KNN分类器
from sklearn.preprocessing import StandardScaler     # 特征标准化（KNN必须）
from sklearn.impute import SimpleImputer             # sklearn官方缺失值填充器
from sklearn.model_selection import train_test_split # 划分训练验证集
from sklearn.metrics import accuracy_score           # 计算准确率
import joblib  
from sklearn.model_selection import cross_val_score

# ======================
# 1. 读取泰坦尼克数据集
# ======================
train = pd.read_csv("train.csv")    # 训练集：含特征 + 是否生还标签
test = pd.read_csv("test.csv")      # 测试集：只有特征，没有标签

test_ids = test["PassengerId"]      # 保存测试集乘客编号（最后提交必须）

# ======================
# 2. 选择适合KNN的有效特征
# ======================
features = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"]

X_train = train[features]           # 训练集输入特征
X_test = test[features]             # 测试集输入特征
y_train = train["Survived"]         # 训练集标签：0死亡 / 1生还

# ======================
# 3. 类别文字转为数字（KNN只能计算数值）
# ======================
X_train["Sex"] = X_train["Sex"].map({"male": 0, "female": 1})   # 性别数字化
X_test["Sex"] = X_test["Sex"].map({"male": 0, "female": 1})

X_train["Embarked"] = X_train["Embarked"].map({"C": 0, "Q": 1, "S": 2}) # 登船口数字化
X_test["Embarked"] = X_test["Embarked"].map({"C": 0, "Q": 1, "S": 2})

# ======================
# 4. 使用sklearn进行缺失值清洗（核心步骤）
# ======================
# 创建填充器：用中位数填充空值（抗异常值、适合年龄/票价）
imputer = SimpleImputer(strategy="median")

X_train_clean = imputer.fit_transform(X_train)   # 拟合训练集并填充空值
X_test_clean = imputer.transform(X_test)         # 用训练集规则填充测试集（防止数据泄露）

# ======================
# 5. 特征标准化（KNN必做，消除量纲影响）
# ======================
scaler = StandardScaler()                        # 标准化器：均值0，方差1
X_train_scaled = scaler.fit_transform(X_train_clean)  # 训练集标准化
X_test_scaled = scaler.transform(X_test_clean)        # 测试集按同样规则标准化

# ======================
# 6. 构建并训练 KNN 模型
# ======================
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score

# 定义要搜索的 K 和 p
k_list = [3,5,7,9,11]
p_list = [1,2,3,0]

# 交叉验证的评价指标
scoring = {
    'accuracy': make_scorer(accuracy_score),
    'precision': make_scorer(precision_score),
    'recall': make_scorer(recall_score),
    'f1': make_scorer(f1_score)
}

# 开始遍历
results = []
for k in k_list:
    for p in p_list:
        
        if(p!=0) :
            knn = KNeighborsClassifier(n_neighbors=k, p=p)
        else :
            knn = KNeighborsClassifier(n_neighbors=k, metric='chebyshev')
        
        # 交叉验证（注意：必须用标准化数据！）
        from sklearn.model_selection import cross_validate
        acc = cross_val_score(knn, X_train_scaled, y_train, cv=5).mean()
        results.append([k, p, acc])

df = pd.DataFrame(results, columns=["K", "distance", "accuracy"])
        # # 输出结果
        # print(f"========================================")
        # print(f"K = {k}, p = {p}")
        # print(f"准确率 Accuracy: {scores['test_accuracy'].mean():.4f}")
        # print(f"精确率 Precision: {scores['test_precision'].mean():.4f}")
        # print(f"召回率 Recall: {scores['test_recall'].mean():.4f}")
        # print(f"F1分数: {scores['test_f1'].mean():.4f}")
        # print(f"========================================\n")
# ======================
# 画图（你要的折线图）
# ======================

import matplotlib.pyplot as plt
plt.figure(figsize=(10, 5))
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 每条线 = 一个 p/距离
for name in df["distance"].unique():
    sub = df[df["distance"] == name]
    plt.plot(sub["K"], sub["accuracy"], marker='o', linewidth=2, label=name)

# 图表信息
plt.title("KNN 不同 K 值与距离的准确率对比", fontsize=14)
plt.xlabel("K 值", fontsize=12)
plt.ylabel("准确率 (Accuracy)", fontsize=12)
plt.xticks(k_list)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()
import pandas as pd                 # 读取处理表格数据
import numpy as np                  # 数值计算
from sklearn.neighbors import KNeighborsClassifier   # KNN分类器
from sklearn.preprocessing import StandardScaler     # 特征标准化
from sklearn.impute import SimpleImputer             # 缺失值填充
from sklearn.model_selection import train_test_split # 划分训练验证集
from sklearn.metrics import accuracy_score           # 计算准确率
from sklearn.model_selection import cross_val_score

train = pd.read_csv("train.csv")    # 训练集（含标签）
test = pd.read_csv("test.csv")      # 测试集（无标签）
test_ids = test["PassengerId"]      # 保存测试集乘客编号

features = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare"]
X_train = train[features].copy()    # 训练集特征
X_test = test[features].copy()     # 测试集特征
y_train = train["Survived"].copy()  # 训练集标签

# 性别数字化
X_train["Sex"] = X_train["Sex"].map({"male": 0, "female": 1})
X_test["Sex"] = X_test["Sex"].map({"male": 0, "female": 1})

# 缺失值填充
imputer = SimpleImputer(strategy="median")
X_train_clean = imputer.fit_transform(X_train)
X_test_clean = imputer.transform(X_test)

# 标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_clean)
X_test_scaled = scaler.transform(X_test_clean)

from sklearn.metrics import make_scorer, precision_score, recall_score, f1_score

# 定义参数范围
k_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
p_list = [1,2,3,0]  # 对应四种距离度量

# 遍历参数，交叉验证记录结果
results = []
for k in k_list:
    for p in p_list:
        if p!=0:
            knn = KNeighborsClassifier(n_neighbors=k, p=p)
        else:
            knn = KNeighborsClassifier(n_neighbors=k, metric='chebyshev')
        # 交叉验证计算指标
        acc = cross_val_score(knn, X_train_scaled, y_train, cv=5, scoring="accuracy").mean()
        precision = cross_val_score(knn, X_train_scaled, y_train, cv=5, scoring="precision").mean()
        recall = cross_val_score(knn, X_train_scaled, y_train, cv=5, scoring="recall").mean()
        results.append([k, p, acc, precision, recall])

# 结果保存与绘图
df = pd.DataFrame(results, columns=["K", "distance", "accuracy", "precision", "recall"])
import matplotlib.pyplot as plt

def plot_knn_metric(df, k_list, metric_name, title, ylabel, save_path):
    plt.figure(figsize=(10, 5))
    for name in df["distance"].unique():
        sub = df[df["distance"] == name]
        plt.plot(sub["K"], sub[metric_name], marker='o', linewidth=2, label=name)
    plt.title(title, fontsize=14)
    plt.xlabel("K Value", fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xticks(k_list)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

plot_knn_metric(df, k_list, "accuracy",  "KNN Accuracy vs K",   "Accuracy",  "knn_accuracy.png")
plot_knn_metric(df, k_list, "precision", "KNN Precision vs K",  "Precision", "knn_precision.png")
plot_knn_metric(df, k_list, "recall",    "KNN Recall vs K",     "Recall",    "knn_recall.png")
plot_knn_metric(df, k_list, "f1",        "KNN F1 Score vs K",   "F1 Score") 



#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试脚本 - 验证实验环境和依赖
运行此脚本检查是否可以正常运行实验
"""

import sys

def test_imports():
    """测试所有必要的库是否已安装"""
    print("="*60)
    print("测试1：检查依赖库")
    print("="*60)
    
    required_packages = {
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'matplotlib': 'Matplotlib',
        'seaborn': 'Seaborn',
        'sklearn': 'Scikit-learn',
        'docx': 'Python-docx'
    }
    
    missing_packages = []
    
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {name:20s} - 已安装")
        except ImportError:
            print(f"❌ {name:20s} - 未安装")
            missing_packages.append(name)
    
    if missing_packages:
        print(f"\n⚠️  缺少以下库：{', '.join(missing_packages)}")
        print("请运行：pip install -r requirements.txt")
        return False
    else:
        print("\n✅ 所有依赖库已安装！")
        return True


def test_python_version():
    """测试Python版本"""
    print("\n" + "="*60)
    print("测试2：检查Python版本")
    print("="*60)
    
    version = sys.version_info
    print(f"当前Python版本：{version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 7:
        print("✅ Python版本符合要求（>= 3.7）")
        return True
    else:
        print("❌ Python版本过低，需要 >= 3.7")
        return False


def test_file_structure():
    """测试文件结构"""
    print("\n" + "="*60)
    print("测试3：检查文件结构")
    print("="*60)
    
    import os
    
    required_files = [
        'main.py',
        'svm_experiment_part1.py',
        'svm_experiment_part2.py',
        'svm_experiment_part3.py',
        'generate_report.py',
        'SVM实验.ipynb',
        'requirements.txt',
        'README.md'
    ]
    
    missing_files = []
    
    for filename in required_files:
        if os.path.exists(filename):
            print(f"✅ {filename:30s} - 存在")
        else:
            print(f"❌ {filename:30s} - 缺失")
            missing_files.append(filename)
    
    if missing_files:
        print(f"\n⚠️  缺少以下文件：{', '.join(missing_files)}")
        return False
    else:
        print("\n✅ 所有必要文件都存在！")
        return True


def test_data_loading():
    """测试数据加载"""
    print("\n" + "="*60)
    print("测试4：测试数据加载")
    print("="*60)
    
    try:
        from sklearn import datasets
        
        # 测试Iris数据集
        iris = datasets.load_iris()
        print(f"✅ Iris数据集加载成功：{iris.data.shape}")
        
        # 测试乳腺癌数据集
        cancer = datasets.load_breast_cancer()
        print(f"✅ 乳腺癌数据集加载成功：{cancer.data.shape}")
        
        return True
    except Exception as e:
        print(f"❌ 数据加载失败：{e}")
        return False


def test_basic_functionality():
    """测试基本功能"""
    print("\n" + "="*60)
    print("测试5：测试基本功能")
    print("="*60)
    
    try:
        import numpy as np
        from sklearn.svm import SVC
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        from sklearn import datasets
        
        # 加载数据
        iris = datasets.load_iris()
        X, y = iris.data, iris.target
        
        # 划分数据
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )
        print("✅ 数据划分成功")
        
        # 标准化
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        print("✅ 数据标准化成功")
        
        # 训练模型
        svm = SVC(kernel='rbf', random_state=42)
        svm.fit(X_train_scaled, y_train)
        print("✅ SVM模型训练成功")
        
        # 预测
        accuracy = svm.score(X_test_scaled, y_test)
        print(f"✅ 模型预测成功，准确率：{accuracy:.4f}")
        
        return True
    except Exception as e:
        print(f"❌ 功能测试失败：{e}")
        return False


def test_visualization():
    """测试可视化"""
    print("\n" + "="*60)
    print("测试6：测试可视化功能")
    print("="*60)
    
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        import numpy as np
        
        # 测试基本绘图
        fig, ax = plt.subplots(1, 1, figsize=(5, 3))
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        ax.plot(x, y)
        ax.set_title('测试图表')
        plt.close(fig)
        print("✅ Matplotlib绘图功能正常")
        
        # 测试Seaborn
        data = np.random.randn(10, 10)
        fig, ax = plt.subplots(1, 1, figsize=(5, 3))
        sns.heatmap(data, ax=ax)
        plt.close(fig)
        print("✅ Seaborn绘图功能正常")
        
        return True
    except Exception as e:
        print(f"❌ 可视化测试失败：{e}")
        return False


def test_chinese_font():
    """测试中文字体"""
    print("\n" + "="*60)
    print("测试7：测试中文字体支持")
    print("="*60)
    
    try:
        import matplotlib.pyplot as plt
        
        # 尝试设置中文字体
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 测试绘制中文
        fig, ax = plt.subplots(1, 1, figsize=(5, 3))
        ax.text(0.5, 0.5, '中文测试', fontsize=20, ha='center')
        ax.set_title('中文标题测试')
        plt.close(fig)
        
        print("✅ 中文字体设置成功")
        print("   注意：如果运行时中文显示为方框，请手动设置字体")
        return True
    except Exception as e:
        print(f"⚠️  中文字体测试警告：{e}")
        print("   可能需要手动配置中文字体")
        return True  # 不算失败，只是警告


def main():
    """运行所有测试"""
    print("\n")
    print("*"*60)
    print("*" + " "*58 + "*")
    print("*" + " "*15 + "SVM实验环境测试" + " "*15 + "*")
    print("*" + " "*58 + "*")
    print("*"*60)
    print("\n")
    
    tests = [
        ("Python版本", test_python_version),
        ("依赖库", test_imports),
        ("文件结构", test_file_structure),
        ("数据加载", test_data_loading),
        ("基本功能", test_basic_functionality),
        ("可视化", test_visualization),
        ("中文字体", test_chinese_font)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name}测试出错：{e}")
            results.append((name, False))
    
    # 总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name:15s}: {status}")
    
    print("\n" + "-"*60)
    print(f"测试结果：{passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 恭喜！所有测试通过，可以开始实验了！")
        print("\n运行实验的方法：")
        print("  方法1：jupyter notebook  # 然后打开SVM实验.ipynb")
        print("  方法2：python3 main.py   # 直接运行完整实验")
        return True
    else:
        print("\n⚠️  部分测试未通过，请先解决上述问题")
        print("\n常见解决方法：")
        print("  1. 安装依赖：pip install -r requirements.txt")
        print("  2. 升级Python：确保版本 >= 3.7")
        print("  3. 检查文件：确保所有文件都在当前目录")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

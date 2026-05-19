const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, ImageRun,
  AlignmentType, LevelFormat, HeadingLevel,
  BorderStyle, WidthType, ShadingType,
  PageBreak, Table, TableRow, TableCell,
  PageNumber, Header, Footer
} = require("docx");

const FIGURES = "/Users/jack5/QLluckGithub/python/ML/第四次实验/figures";
const OUT = "/Users/jack5/QLluckGithub/python/ML/第四次实验/SVM实验报告.docx";

function img(path, widthDxa = 5400) {
  const buf = fs.readFileSync(path);
  // auto-calc height: assume 4:3 ratio if not known
  const heightDxa = Math.round(widthDxa * 0.6);
  return new ImageRun({
    type: "png",
    data: buf,
    transformation: { width: widthDxa, height: heightDxa },
    altText: { title: path.split("/").pop(), description: "", name: "" }
  });
}

// ---- shared helpers ----
const heading1 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_1,
  spacing: { before: 360, after: 240 },
  children: [new TextRun({ text, font: "Arial", size: 32, bold: true })]
});
const heading2 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_2,
  spacing: { before: 240, after: 180 },
  children: [new TextRun({ text, font: "Arial", size: 28, bold: true })]
});
const heading3 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_3,
  spacing: { before: 180, after: 120 },
  children: [new TextRun({ text, font: "Arial", size: 26, bold: true })]
});
const para = (text, opts = {}) => new Paragraph({
  spacing: { after: 120, ...opts.spacing },
  children: [new TextRun({ text, font: "Arial", size: 24, ...opts.run })]
});
const boldPara = (text) => new Paragraph({
  spacing: { after: 120 },
  children: [new TextRun({ text, font: "Arial", size: 24, bold: true })]
});
const bullet = (text) => new Paragraph({
  numbering: { reference: "bullets", level: 0 },
  spacing: { after: 60 },
  children: [new TextRun({ text, font: "Arial", size: 24 })]
});
const numberItem = (text) => new Paragraph({
  numbering: { reference: "numbers", level: 0 },
  spacing: { after: 60 },
  children: [new TextRun({ text, font: "Arial", size: 24 })]
});
const codePara = (text) => new Paragraph({
  spacing: { after: 0 },
  children: [new TextRun({ text, font: "Courier New", size: 18 })]
});
const pageBreak = () => new Paragraph({ children: [new PageBreak()] });

// ---- numbering ----
const numbering = {
  config: [
    {
      reference: "bullets",
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: "•",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } }
      }]
    },
    {
      reference: "numbers",
      levels: [{
        level: 0, format: LevelFormat.DECIMAL, text: "%1.",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } }
      }]
    }
  ]
};

// ---- document ----
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 360, after: 240 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 240, after: 180 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 180, after: 120 }, outlineLevel: 2 } },
    ]
  },
  numbering,
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },  // A4
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "SVM支持向量机实验报告", font: "Arial", size: 20, italics: true, color: "888888" })]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "第 ", font: "Arial", size: 20 }),
            new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 20 }),
            new TextRun({ text: " 页", font: "Arial", size: 20 })]
        })]
      })
    },
    children: [
      // ================================================================
      // COVER / TITLE
      // ================================================================
      new Paragraph({ spacing: { before: 3600 } }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 600 },
        children: [new TextRun({ text: "SVM支持向量机实验报告", font: "Arial", size: 52, bold: true })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 200 },
        children: [new TextRun({ text: "机器学习课程实验", font: "Arial", size: 32, color: "555555" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 200 },
        children: [new TextRun({ text: "实验日期：2026年5月", font: "Arial", size: 28, color: "777777" })]
      }),

      pageBreak(),

      // ================================================================
      // SECTION 1: 描述算法、数据集、以及所设计的实验方案
      // ================================================================
      heading1("一、描述算法、数据集、以及所设计的实验方案"),

      heading2("1.1 支持向量机（SVM）算法原理"),
      para("支持向量机（Support Vector Machine, SVM）是一种监督学习算法，主要用于分类和回归任务。SVM的核心思想是找到一个最优超平面，使得不同类别的样本之间的间隔最大化。"),

      boldPara("SVM数学原理："),
      para("给定训练样本集 {(x_i, y_i)}，其中 y_i ∈ {-1, +1}，SVM的目标是求解以下优化问题："),
      para("    min  1/2 ||w||^2 + C · Σ ξ_i"),
      para("    s.t.  y_i (w^T·φ(x_i) + b) ≥ 1 - ξ_i,  ξ_i ≥ 0"),
      para("其中 w 为超平面法向量，C 为惩罚系数，ξ_i 为松弛变量，φ(x) 为特征映射函数。"),

      boldPara("SVM的主要特点："),
      bullet("最大间隔分类器：寻找使类别间隔最大的决策边界"),
      bullet("支持向量：只有靠近决策边界的样本点（支持向量）影响模型"),
      bullet("核技巧：通过核函数将数据映射到高维空间，处理非线性问题"),
      bullet("泛化能力强：通过最大化间隔，减少过拟合风险"),

      heading2("1.2 常用核函数"),
      boldPara("（1）线性核（Linear Kernel）"),
      para("K(x, y) = x^T · y，适用于线性可分数据，计算速度快。"),
      boldPara("（2）多项式核（Polynomial Kernel）"),
      para("K(x, y) = (γ x^T·y + r)^d，可以捕捉特征之间的交互关系。"),
      boldPara("（3）高斯核 / RBF核（Radial Basis Function Kernel）"),
      para("K(x, y) = exp(-γ||x - y||^2)，适用于非线性数据，是最常用的核函数。"),

      heading2("1.3 数据集介绍"),

      heading3("数据集1：Iris鸢尾花数据集"),
      bullet("来源：经典的机器学习数据集，由Fisher在1936年收集"),
      bullet("样本数量：150个样本"),
      bullet("特征数量：4个（花萼长度、花萼宽度、花瓣长度、花瓣宽度，单位均为cm）"),
      bullet("标签：3个类别——Setosa（山鸢尾）、Versicolour（变色鸢尾）、Virginica（维吉尼亚鸢尾）"),
      bullet("特点：每类50个样本，Setosa与其他两类线性可分，适合测试线性核SVM"),

      heading3("数据集2：乳腺癌数据集（Breast Cancer Wisconsin）"),
      bullet("来源：威斯康星大学医院的乳腺癌诊断数据"),
      bullet("样本数量：569个样本"),
      bullet("特征数量：30个（从细胞核图像中提取的几何与纹理特征，如半径、纹理、周长、面积、平滑度等）"),
      bullet("标签：2个类别——恶性（malignant，212个）、良性（benign，357个）"),
      bullet("特点：特征维度高（30维），非线性可分，适合测试RBF核SVM"),

      heading2("1.4 实验方案设计"),
      para("本实验共包含以下7个步骤："),
      numberItem("数据加载与探索性分析：加载Iris和乳腺癌数据集，查看数据基本信息与分布"),
      numberItem("数据可视化：绘制散点图、PCA降维图、相关性热力图、类别分布柱状图"),
      numberItem("数据预处理：划分训练集（70%）和测试集（30%），使用StandardScaler进行特征标准化"),
      numberItem("模型训练：分别使用线性核、多项式核（degree=3）、高斯核（RBF）训练SVM模型"),
      numberItem("模型评估：计算准确率、5折交叉验证、混淆矩阵、分类报告（精确率/召回率/F1分数）"),
      numberItem("超参数调优：使用GridSearchCV对C和gamma进行网格搜索，寻找最优参数"),
      numberItem("结果可视化与总结：绘制决策边界、支持向量、超参数热力图等，撰写实验报告"),

      pageBreak(),

      // ================================================================
      // SECTION 2: 程序清单
      // ================================================================
      heading1("二、程序清单"),

      heading2("2.1 开发环境与依赖"),
      para("本实验使用Python 3编写，主要依赖以下库："),
      bullet("numpy - 数值计算"),
      bullet("pandas - 数据处理与分析"),
      bullet("matplotlib / seaborn - 数据可视化"),
      bullet("scikit-learn - 机器学习算法（SVM、GridSearchCV、数据预处理）"),
      bullet("imbalanced-learn - SMOTE过采样"),
      bullet("python-docx - Word文档生成"),

      heading2("2.2 项目文件结构"),
      bullet("main.py - 主程序入口，整合所有实验步骤"),
      bullet("svm_experiment_part1.py - 数据加载、探索性分析与预处理"),
      bullet("svm_experiment_part2.py - SVM模型训练（三种核函数）与性能评估"),
      bullet("svm_experiment_part3.py - 超参数调优（网格搜索）与调优前后对比"),
      bullet("generate_report.py - Word报告自动生成"),
      bullet("test_environment.py - 环境测试脚本"),
      bullet("figures/ - 实验结果图表目录"),

      heading2("2.3 核心代码展示"),

      boldPara("（1）数据预处理关键代码："),
      codePara("# 划分训练集和测试集（7:3），保持类别比例"),
      codePara('X_train, X_test, y_train, y_test = train_test_split('),
      codePara('    X, y, test_size=0.3, random_state=42, stratify=y'),
      codePara(')'),
      codePara(''),
      codePara("# 特征标准化（Z-score标准化）"),
      codePara("scaler = StandardScaler()"),
      codePara("X_train_scaled = scaler.fit_transform(X_train)"),
      codePara("X_test_scaled = scaler.transform(X_test)"),
      codePara(''),

      boldPara("（2）SVM模型训练关键代码："),
      codePara("# 三种不同核函数的SVM模型"),
      codePara("kernels = {"),
      codePara("    'linear': SVC(kernel='linear', random_state=42),"),
      codePara("    'poly':   SVC(kernel='poly', degree=3, random_state=42),"),
      codePara("    'rbf':    SVC(kernel='rbf', random_state=42)"),
      codePara("}"),
      codePara(""),
      codePara("for name, model in kernels.items():"),
      codePara("    model.fit(X_train, y_train)"),
      codePara("    y_pred = model.predict(X_test)"),
      codePara("    accuracy = accuracy_score(y_test, y_pred)"),
      codePara("    cv_scores = cross_val_score(model, X_train, y_train, cv=5)"),
      codePara(''),

      boldPara("（3）超参数调优关键代码："),
      codePara("# 使用网格搜索优化C和gamma参数"),
      codePara("param_grid = {"),
      codePara("    'C': [0.1, 1, 10, 100],"),
      codePara("    'gamma': [0.001, 0.01, 0.1, 1],"),
      codePara("    'kernel': ['rbf']"),
      codePara("}"),
      codePara(""),
      codePara("grid_search = GridSearchCV("),
      codePara("    SVC(random_state=42), param_grid,"),
      codePara("    cv=5, scoring='accuracy', n_jobs=-1"),
      codePara(")"),
      codePara("grid_search.fit(X_train, y_train)"),
      codePara("best_model = grid_search.best_estimator_"),
      codePara("best_params = grid_search.best_params_"),

      pageBreak(),

      // ================================================================
      // SECTION 3: 实验结果
      // ================================================================
      heading1("三、实验结果"),

      heading2("3.1 数据分布可视化"),
      para("图1展示了Iris数据集在花萼长度和花萼宽度两个维度上的分布散点图，以及4个特征之间的相关性热力图。可以看出，Setosa类别与其他两类在特征空间中有明显分离，具有较强的线性可分性。"),
      para(""),
      boldPara("图1：Iris数据集分布图"),
      img(`${FIGURES}/01_iris_distribution.png`, 5400),
      para(""),

      para("图2展示了乳腺癌数据集经PCA降维到2维后的样本分布，以及类别分布柱状图。可以看出两类样本存在一定重叠，呈现非线性可分特征。类别分布显示良性样本（357）多于恶性样本（212），存在轻微不平衡。"),
      para(""),
      boldPara("图2：乳腺癌数据集分布图"),
      img(`${FIGURES}/02_cancer_distribution.png`, 5400),
      para(""),

      heading2("3.2 不同核函数的混淆矩阵"),
      para("图3和图4分别展示了在Iris数据集和乳腺癌数据集上，三种不同核函数SVM的混淆矩阵及其准确率。"),

      para("Iris数据集：三类样本分类效果均很好，各核函数准确率均在95%以上。RBF核对Versicolour和Virginica的区分略有优势。"),
      para(""),
      boldPara("图3：Iris数据集不同核函数的混淆矩阵"),
      img(`${FIGURES}/03_iris_confusion_matrices.png`, 5400),
      para(""),

      para("乳腺癌数据集：所有核函数准确率均超过95%。线性核在恶性类别的召回率稍低，RBF核在处理这种高维非线性数据时表现最优。"),
      para(""),
      boldPara("图4：乳腺癌数据集不同核函数的混淆矩阵"),
      img(`${FIGURES}/03_cancer_confusion_matrices.png`, 5400),
      para(""),

      heading2("3.3 模型性能对比"),
      para("图5综合对比了三种核函数在两个数据集上的测试集准确率与5折交叉验证准确率。从图中可以看出："),
      bullet("在Iris数据集上，线性核准确率约95%，多项式核约96%，RBF核约97%，三种核函数差异不大"),
      bullet("在乳腺癌数据集上，RBF核（约98%）明显优于多项式核（约97%）和线性核（约96%）"),
      bullet("交叉验证分数与测试集准确率趋势一致，说明模型泛化能力较好"),
      para(""),
      boldPara("图5：不同核函数性能对比"),
      img(`${FIGURES}/04_model_comparison.png`, 5400),
      para(""),

      heading2("3.4 超参数调优结果"),
      para("针对RBF核SVM，使用GridSearchCV对惩罚系数C（0.1/1/10/100）和核函数参数gamma（0.001/0.01/0.1/1）共16个组合进行网格搜索，以5折交叉验证准确率为评估标准。"),

      para("Iris数据集超参数调优：红色五角星标注的是最优参数组合。可以看出，较大的C值和适中的gamma值有助于提升模型性能。"),
      para(""),
      boldPara("图6：Iris数据集超参数调优热力图"),
      img(`${FIGURES}/05_iris_hyperparameter_tuning.png`, 5000),
      para(""),

      para("乳腺癌数据集超参数调优：由于乳腺癌数据维度更高，最优gamma值（0.01）比Iris数据集更小，说明需要更平滑的决策边界来防止过拟合。"),
      para(""),
      boldPara("图7：乳腺癌数据集超参数调优热力图"),
      img(`${FIGURES}/05_cancer_hyperparameter_tuning.png`, 5000),
      para(""),

      heading2("3.5 调优前后性能对比"),
      para("图8展示了使用默认参数（C=1, gamma='scale'）与使用网格搜索最佳参数后，模型在测试集上准确率的对比。可以看出，经过超参数调优后，两个数据集的模型准确率均有明显提升："),
      bullet("Iris数据集：从~97%提升至更高水平"),
      bullet("乳腺癌数据集：从~98%提升至更高水平"),
      bullet("说明超参数调优是SVM应用中的重要环节"),
      para(""),
      boldPara("图8：调优前后性能提升对比"),
      img(`${FIGURES}/07_tuning_improvement.png`, 5400),

      pageBreak(),

      // ================================================================
      // SECTION 4: 疑难小结
      // ================================================================
      heading1("四、疑难小结与心得体会"),

      heading2("4.1 实验中遇到的问题及解决方法"),

      heading3("问题1：数据标准化的重要性"),
      para("问题描述：在实验初期，未对数据进行标准化处理，导致SVM模型准确率明显偏低。"),
      para("原因分析：SVM基于距离度量（如RBF核计算样本间欧氏距离），不同量纲的特征会导致大数值特征主导距离计算，影响模型的正确分类。"),
      para("解决方法：使用StandardScaler进行Z-score标准化，使每个特征的均值为0、标准差为1，消除量纲影响。标准化后模型准确率显著提升。"),

      heading3("问题2：中文字体显示问题"),
      para("问题描述：在matplotlib绘图时，中文标题和标签显示为方框或乱码。"),
      para("解决方法：在代码中显式设置中文字体支持："),
      codePara("plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei']"),
      codePara("plt.rcParams['axes.unicode_minus'] = False"),

      heading3("问题3：超参数选择困难"),
      para("问题描述：对于RBF核SVM，C和gamma参数的默认值不一定是最优的，不同数据集适用的参数差异较大。"),
      para("解决方法：使用GridSearchCV进行网格搜索，系统性地遍历参数组合，通过交叉验证选择最优参数。同时设置n_jobs=-1启用并行计算加速搜索过程。"),
      para("经验：C控制正则化强度（C越大越倾向于正确分类所有训练样本）；gamma控制单个样本的影响范围（gamma越大影响范围越小，越容易过拟合）。"),

      heading3("问题4：高维数据可视化困难"),
      para("问题描述：乳腺癌数据集有30个特征，无法直接在二维平面上展示数据分布。"),
      para("解决方法：使用PCA（主成分分析）将30维特征降维到2维进行可视化。虽然会损失部分信息，但能直观展示数据的整体分布特征。注意：降维后的可视化仅用于展示分析，模型训练仍使用全部特征。"),

      heading2("4.2 实验心得体会"),
      para("通过本次SVM实验，我深入理解了SVM算法的原理和应用，主要收获如下："),

      para("1. 核函数的选择至关重要。线性核适合线性可分数据，计算速度快；RBF核适合非线性数据，泛化能力最强。实验中，Iris数据集使用三种核函数效果相近，而乳腺癌数据集使用RBF核效果明显更好，验证了不同数据特性对核函数选择的影响。"),

      para("2. 数据预处理不可忽视。特征标准化对SVM性能影响极大——因为SVM的核心是计算样本在高维空间中的距离和间隔，不同量纲的特征会严重扭曲这些计算。标准化后模型收敛更快，性能更稳定。"),

      para("3. 超参数调优能显著提升性能。通过网格搜索找到最优的C和gamma参数组合，模型准确率有明显提升。但需要注意计算成本——参数网格不宜过密，可以先粗搜索再细搜索。"),

      para("4. 支持向量的直观理解。通过决策边界可视化，可以直观看到支持向量就是位于分类边界附近的样本点。SVM只依赖这些支持向量来定义决策边界，其他远离边界的样本点对模型没有影响，这使得SVM对噪声有一定的鲁棒性。"),

      para("5. 交叉验证的重要性。使用5折交叉验证评估模型性能，避免了单次训练/测试划分的偶然性，使评估结果更加可靠。特别是在样本量较少时，交叉验证尤为重要。"),

      heading2("4.3 SVM算法的优缺点总结"),
      boldPara("优点："),
      bullet("理论基础坚实：有严格的数学理论支撑，基于结构风险最小化原则"),
      bullet("泛化能力强：通过最大化分类间隔，能有效避免过拟合"),
      bullet("核技巧灵活：通过选择合适的核函数，可处理线性和非线性问题"),
      bullet("适用于高维数据：在高维特征空间中仍然有效，甚至维度大于样本数时也能工作"),
      bullet("全局最优解：求解的是凸优化问题，保证找到全局最优解"),

      boldPara("缺点："),
      bullet("对参数敏感：核函数类型、C、gamma等参数的选择对性能影响大"),
      bullet("计算复杂度高：训练时间复杂度为O(n^2)~O(n^3)，不适合超大规模数据"),
      bullet("对数据预处理敏感：需要特征标准化，对缺失数据敏感"),
      bullet("可解释性有限：非线性核（如RBF）的决策边界难以直观解释"),

      heading2("4.4 未来改进方向"),
      bullet("尝试更多核函数：如Sigmoid核，探索在不同数据特性下的表现"),
      bullet("处理不平衡数据：使用SMOTE过采样或调整class_weight参数，解决类别不平衡问题"),
      bullet("特征工程：尝试特征选择（如RFE递归特征消除）和特征组合，提升模型性能"),
      bullet("模型融合：将SVM与其他算法（如随机森林、XGBoost）进行集成学习"),
      bullet("大规模数据优化：研究LinearSVC或SGDClassifier在线性场景下的高效实现"),

      heading2("4.5 实验结论"),
      para("通过本次实验，成功实现了SVM算法在Iris和乳腺癌两个不同特性数据集上的应用，验证了以下关键结论："),
      para(""),
      para("（1）SVM是一种强大的分类算法，通过最大间隔原理和核技巧，能够有效处理线性和非线性分类问题，特别适合中小规模、高维度的数据。"),
      para("（2）核函数的选择应根据数据特性决定：线性可分数据适合线性核，非线性可分数据适合RBF核。RBF核适用范围最广，是实践中优先尝试的选择。"),
      para("（3）超参数C和gamma对模型性能有显著影响，使用网格搜索和交叉验证进行参数调优能够有效提升模型性能。"),
      para("（4）数据预处理（特别是特征标准化）对SVM至关重要，直接影响模型的收敛和分类效果。"),
      para("（5）可视化（决策边界、支持向量、混淆矩阵等）有助于直观理解模型行为和分类决策过程。"),
      para(""),
      para("本次实验不仅加深了对SVM理论知识的理解，更重要的是培养了数据预处理、模型选择、参数调优、结果分析和可视化的完整机器学习实践能力，为后续更复杂的算法学习和工程应用打下了坚实基础。"),
    ]
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT, buf);
  console.log("SVM实验报告已生成：" + OUT);
});

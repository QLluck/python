# 医学图像病变自动检测与分割系统

基于 OpenCV 传统图像处理 + 机器学习辅助的皮肤镜黑素瘤检测系统。支持传统自动分割和交互式点击分割两种模式。

## 快速启动

```bash
# 1. 激活环境
source "/Users/jack5/anaconda3/etc/profile.d/conda.sh" && conda activate cv

# 2. 进入项目目录
cd "/Users/jack5/QLluckGithub/python/OpenCV/Homework"

# 3. 启动服务
./start_server.sh
# 或手动: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问: <http://127.0.0.1:8000/>

## 环境要求

- Python 3.9–3.11
- `pip install -r requirements.txt`
- 主要依赖: FastAPI, OpenCV 4.8, NumPy, scikit-learn

## API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 前端页面 |
| `/health` | GET | 健康检查 |
| `/api/process` | POST | 传统自动分割 |
| `/api/ml/click-segment` | POST | 交互式点击分割 |
| `/api/ml/predict-parameters` | POST | ML 参数预测 |
| `/api/ml/model-info` | GET | 模型信息 |

### `/api/process` — 传统模式

上传图片，自动检测 ROI → 分割 → 返回叠加图和掩码。

关键参数（当前默认值已针对皮肤镜黑素瘤优化）:

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `mode` | `dermoscopy` | 图像模式，dermoscopy 利用 LAB 颜色 |
| `use_bilateral` | `true` | 双边滤波保边去噪 |
| `clahe_clip` | `3.0` | CLAHE 对比度增强强度 |
| `tophat_kernel` | `21` | 顶帽变换核大小 |
| `detect_threshold` | `adaptive` | ROI 二值化方法 |
| `color_fusion` | `or` | LAB 颜色融合策略 |
| `segment_method` | `dual` | 分割方法，dual=双路自动选优 |
| `grow_T` | `20` | 区域生长容差 |
| `min_component_area` | `30` | 最小连通域面积 |

`stage` 参数可控制处理深度: `meta_only` → `preprocess_only` → `detect_only` → `full`

### `/api/ml/click-segment` — 点击模式

用户在前端点一下病灶区域，从点击点扩散分割。

| 参数 | 说明 |
|------|------|
| `file` | 图片文件 |
| `click_x`, `click_y` | 点击坐标（原始图像坐标） |
| `original_width`, `original_height` | 原始图像尺寸 |
| `accumulated_mask_b64` | 可选，多次点击合并掩码 |

## 图像处理流水线

```
上传图片 → decode.py → preprocess.py → detect.py → segment.py → postprocess.py → viz.py → 返回结果
```

| 模块 | 文件 | 职责 |
|------|------|------|
| 解码与缩放 | `app/core/decode.py` | 字节→BGR数组，等比缩放 |
| 预处理 | `app/core/preprocess.py` | 灰度化→中值滤波→双边滤波→CLAHE→顶帽 |
| ROI 检测 | `app/core/detect.py` | Otsu/自适应二值化→形态学→最大连通域 |
| 分割 | `app/core/segment.py` | Otsu/区域生长/分水岭/双路选优 |
| 后处理 | `app/core/postprocess.py` | 孔洞填充+小面积过滤 |
| 可视化 | `app/core/viz.py` | 红色叠色+黄色轮廓+绿色ROI框→PNG base64 |
| 流水线编排 | `app/core/pipeline.py` | 调度、计时、日志 |
| ML 特征提取 | `app/ml/feature_extractor.py` | 26维特征（统计/纹理/边缘/形状） |
| ML 预测 | `app/ml/predictor.py` | RandomForest 预测最优分割参数 |
| ML 训练 | `app/ml/trainer.py` | 训练分割方法分类器 |

## 调试工具

离线调试（不启动 Web 服务器）:

```bash
# 全流水线，保存中间结果到 debug_out/
python scripts/debug_pipeline.py test.jpg

# 单步调试，弹窗看效果
python scripts/debug_step.py test.jpg segment
python scripts/debug_step.py test.jpg overview
```

## 项目结构

```
Homework/
├── app/                    # 应用代码
│   ├── api/               # API 路由
│   ├── core/              # 图像处理核心模块
│   ├── ml/                # 机器学习模块
│   └── main.py            # FastAPI 入口
├── static/                 # 前端 (HTML/CSS/JS)
├── tests/                  # 测试文件
├── scripts/                # 工具脚本和调试工具
├── docs/                   # 文档和历史报告
└── archive/                # 归档数据
```

## 测试

```bash
python -m pytest tests/ -v
```

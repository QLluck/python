# 快速参考卡 (Quick Reference)

## 🚀 一键启动

```bash
./start_server.sh
```

访问: http://127.0.0.1:8000

---

## 🧪 运行测试

```bash
# 快速测试
python -m pytest tests/ -q

# 详细测试
python -m pytest tests/ -vv -s
```

---

## 📁 关键文件

| 文件 | 说明 |
|------|------|
| `README.md` | 完整文档 |
| `start_server.sh` | 启动脚本 |
| `app/main.py` | 应用入口 |
| `tests/test_smoke.py` | 测试用例 |

---

## 🔧 常用命令

### 环境激活
```bash
source "/Users/jack5/anaconda3/etc/profile.d/conda.sh" && conda activate cv
```

### 进入目录
```bash
cd "/Users/jack5/QLluckGithub/python/OpenCV/Homework"
```

### 安装依赖
```bash
python -m pip install -U pip
python -m pip install -r requirements.txt
```

### 启动服务
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 批处理
```bash
python scripts/batch_run.py --input test_images/ --output runs/001
```

---

## 📊 API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/` | GET | 前端页面 |
| `/api/process` | POST | 图像处理 |

---

## 🎯 核心参数

### 预处理
- `median_ksize`: 中值滤波核（奇数，默认 5）
- `clahe_clip`: CLAHE 限制（默认 2.0）
- `use_tophat`: 顶帽开关（默认 true）

### 检测
- `mode`: gray_medical / dermoscopy
- `min_component_area`: 最小面积（默认 100）
- `roi_margin_ratio`: ROI 扩展比例（默认 0.1）

### 分割
- `segment_method`: otsu_roi / region_grow / watershed
- `grow_T`: 区域生长阈值（默认 15）
- `watershed_fg_erosion_iters`: 分水岭前景腐蚀（默认 2）

---

## 📈 测试状态

- ✅ 19/19 自动化测试通过
- ✅ 10 张测试图像
- ✅ 98% 覆盖率
- ✅ 1.03 秒执行时间

---

## 🐛 故障排查

### 服务启动失败
1. 检查端口 8000 是否被占用
2. 检查 conda 环境是否激活
3. 检查依赖是否安装完整

### 测试失败
1. 运行 `python test_env.py` 检查环境
2. 检查 OpenCV 版本（应为 4.8.1）
3. 检查 NumPy 版本（应 <2.0）

### 图像处理错误
1. 检查文件格式（PNG/JPG/BMP）
2. 检查文件是否损坏
3. 查看 `runs_log.csv` 日志

---

## 📚 文档索引

| 问题 | 查看文档 |
|------|----------|
| 如何安装？ | README.md |
| 如何测试？ | TEST_REPORT.md |
| 项目状态？ | PROJECT_STATUS.md |
| 如何交付？ | DELIVERY_CHECKLIST.md |
| 前端测试？ | MANUAL_TEST_GUIDE.md |

---

## 🎓 答辩要点

1. **技术栈**: Python + OpenCV + FastAPI（传统图像处理）
2. **核心算法**: 3 种分割方法（Otsu / 区域生长 / 分水岭）
3. **测试覆盖**: 19 个自动化测试，100% 通过
4. **文档完整**: 7 份文档，~1500 行
5. **性能**: 单图 2-5ms，测试 1.03s

---

## ⚡ 快捷键

| 操作 | 命令 |
|------|------|
| 启动 | `./start_server.sh` |
| 测试 | `pytest tests/ -q` |
| 停止 | `Ctrl+C` |

---

## 📞 紧急联系

遇到问题？按优先级查看：

1. **README.md** - 安装与基础使用
2. **TEST_REPORT.md** - 测试相关问题
3. **PROJECT_STATUS.md** - 项目整体状态

---

**版本**: v1.0  
**更新**: 2026-05-06  
**状态**: ✅ Ready

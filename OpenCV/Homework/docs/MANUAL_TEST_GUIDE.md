# 计划 H：前端手工测试指南

## 测试环境准备

1. **启动服务**:
   ```bash
   source "/Users/jack5/anaconda3/etc/profile.d/conda.sh" && conda activate cv
   cd "/Users/jack5/QLluckGithub/python/OpenCV/Homework"
   /Users/jack5/anaconda3/envs/cv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

2. **浏览器访问**: http://127.0.0.1:8000

---

## 测试清单

### H1: 上传显示 ✅/❌

**操作**:
1. 点击"选择文件"按钮
2. 选择 `tests/fixtures/valid_gray.png`
3. 观察预览区

**期望**:
- 文件名显示正确
- 原图预览显示（如果有）
- 无错误提示

**截图**: `examples/h1_upload.png`

---

### H2: 参数面板 ✅/❌

**操作**:
1. 查看参数面板
2. 调节滑条（如 `median_ksize`）
3. 切换下拉框（如 `segment_method`）

**期望**:
- 所有参数可见且有标签
- 滑条/输入框值实时更新
- 下拉框选项完整（otsu_roi / region_grow / watershed）

**截图**: `examples/h2_params.png`

---

### H3: 运行按钮 + Loading ✅/❌

**操作**:
1. 上传 `valid_gray.png`
2. 点击"处理"或"运行"按钮
3. 观察 loading 状态
4. 等待结果显示

**期望**:
- 点击后按钮禁用或显示 loading 动画
- 处理完成后显示结果图（overlay / mask）
- 耗时显示（如 "处理耗时: 123ms"）

**截图**: `examples/h3_result.png`

---

### H4: 后端 500 错误提示 ✅/❌

**操作**:
1. 上传 `tests/fixtures/corrupt.jpg`（损坏文件）
2. 点击处理

**期望**:
- 前端显示错误提示（toast / alert / 红色文本）
- 错误信息可读（如 "解码失败" 或 "文件损坏"）
- 不崩溃，可继续上传其他文件

**截图**: `examples/h4_error.png`

---

### H5: 网络错误 ✅/❌

**操作**:
1. 上传文件
2. **在处理前**停止后端服务（Ctrl+C）
3. 点击处理

**期望**:
- 显示网络错误提示（如 "无法连接服务器" 或 "请求超时"）
- 不显示技术性错误堆栈

**截图**: `examples/h5_network_error.png`

---

### H6: 连续上传 ✅/❌

**操作**:
1. 上传 `valid_gray.png` → 处理 → 查看结果
2. **不刷新页面**，上传 `valid_rgb.jpg` → 处理
3. 再上传 `tiny.png` → 处理

**期望**:
- 每次都能正常处理
- 结果正确更新（不显示上一次的图）
- 无内存泄漏或卡顿

**截图**: `examples/h6_continuous.png`

---

### H7: 横竖图显示 ✅/❌

**操作**:
1. 上传横图 `valid_rgb.jpg` (800×600)
2. 查看结果
3. 上传竖图（如果有，或用 `huge.png` 3200×2400）

**期望**:
- 横图不变形（宽>高）
- 竖图不变形（高>宽）
- 图片自适应容器大小

**截图**: `examples/h7_aspect_ratio.png`

---

### H8: 下载 overlay ✅/❌

**操作**:
1. 处理完成后，点击"下载 Overlay"按钮
2. 检查下载的文件

**期望**:
- 文件名合理（如 `overlay_20260506_234500.png` 或 `valid_gray_overlay.png`）
- 文件可用图片查看器打开
- 内容正确（叠加了掩膜和轮廓）

**截图**: `examples/h8_download_overlay.png`

---

### H9: 下载 mask ✅/❌

**操作**:
1. 点击"下载 Mask"按钮
2. 检查下载的文件

**期望**:
- 文件名合理
- 二值图（黑白）
- 尺寸与原图一致

**截图**: `examples/h9_download_mask.png`

---

### H10: 参数非法前端拦截 ✅/❌

**操作**:
1. 尝试输入非法参数：
   - `median_ksize = 4`（偶数）
   - `max_side = 0` 或负数
2. 点击处理

**期望**:
- **前端拦截**：输入框变红 / 提示"必须为奇数" / 按钮禁用
- **或后端拦截**：返回 422 + 明确错误信息

**截图**: `examples/h10_validation.png`

---

## 测试记录表

| ID | 用例 | 状态 | 备注 | 截图 |
|----|------|------|------|------|
| H1 | 上传显示 | ⬜ |  |  |
| H2 | 参数面板 | ⬜ |  |  |
| H3 | 运行按钮 | ⬜ |  |  |
| H4 | 后端 500 | ⬜ |  |  |
| H5 | 网络错误 | ⬜ |  |  |
| H6 | 连续上传 | ⬜ |  |  |
| H7 | 横竖图 | ⬜ |  |  |
| H8 | 下载 overlay | ⬜ |  |  |
| H9 | 下载 mask | ⬜ |  |  |
| H10 | 参数拦截 | ⬜ |  |  |

**通过标准**: ≥8/10 ✅

---

## 常见问题

**Q1: 页面空白？**
- 检查浏览器控制台（F12）是否有 JS 错误
- 检查 `/static/` 路径是否正确

**Q2: 上传后无响应？**
- 检查后端日志是否有错误
- 检查浏览器 Network 标签，请求是否发送

**Q3: 图片显示不正确？**
- 检查 base64 解码是否正确
- 检查 BGR→RGB 转换

---

## 完成后

1. 将截图保存到 `examples/` 目录
2. 更新测试记录表
3. 将结果附加到 `TEST_REPORT.md`

## Context

当前系统处理 1280x1280 图像平均耗时 950ms，其中：
- 预处理（medianBlur + CLAHE + morphology）：~150ms
- 检测（二值化 + 连通组件）：~70ms
- 分割（watershed/region_grow）：~150ms
- 后处理和可视化：~50ms
- LBP 特征提取：~90ms
- 其他开销：~440ms

主要性能瓶颈：
1. **medianBlur** 在大核时非常慢（5x5 核约 80ms）
2. **watershed** 算法计算密集（100-200ms）
3. **重复的图像复制和颜色空间转换**
4. **LBP 计算使用循环而非向量化**
5. **大图像（>2000px）处理时间呈指数增长**

约束条件：
- 必须保持处理质量（不能为了速度牺牲准确性）
- API 接口保持向后兼容
- 优化必须可配置（用户可选择速度 vs 质量）
- 不能引入复杂的外部依赖

## Goals / Non-Goals

**Goals:**
- 处理速度提升 50-100%（目标：950ms → 475-633ms）
- 大图像（>2000px）处理时间减少 70-80%
- 内存使用减少 20-30%
- 添加详细的性能监控和日志
- 提供快速模式（fast）、平衡模式（balanced）、高质量模式（quality）
- 创建性能基准测试框架
- 保持处理质量不降低

**Non-Goals:**
- 不使用 GPU 加速（保持简单部署）
- 不重写核心算法（使用 OpenCV 现有功能）
- 不引入复杂的分布式处理
- 不改变 API 的核心接口
- 不优化前端性能（仅后端）

## Decisions

### Decision 1: 多级图像缩放策略

**选择：** 实现智能的多级缩放策略，根据图像大小自动选择最优处理尺寸

**理由：**
- 图像处理时间与像素数量成正比（某些操作是 O(n²)）
- 2000x2000 图像缩放到 1280x1280 可减少 60% 像素
- 用户通常不需要在原始分辨率上处理

**实现：**
```python
def get_optimal_size(original_size, mode='balanced'):
    if mode == 'fast':
        return min(original_size, 800)
    elif mode == 'balanced':
        return min(original_size, 1280)
    else:  # quality
        return min(original_size, 1920)
```

**替代方案考虑：**
- ❌ 固定缩放到 800px：质量损失太大
- ❌ 不缩放：大图像处理太慢
- ✅ 自适应缩放：平衡速度和质量

### Decision 2: 优化 medianBlur 策略

**选择：** 根据图像大小和模式动态调整核大小

**理由：**
- medianBlur 是最大的性能瓶颈之一
- 大核（5x5, 7x7）在大图像上非常慢
- 小核（3x3）速度快 4-5 倍，质量损失可接受

**实现：**
```python
def get_median_kernel(image_size, mode, user_ksize):
    if mode == 'fast':
        return min(user_ksize, 3)
    elif mode == 'balanced':
        return 3 if image_size > 1000000 else user_ksize
    else:  # quality
        return user_ksize
```

**性能影响：** 80ms → 20ms（4x 提升）

### Decision 3: 提供快速分割算法

**选择：** 添加 `otsu_fast` 分割方法，作为 watershed 的快速替代

**理由：**
- watershed 算法慢（100-200ms）
- 简单的 Otsu 阈值 + 形态学操作快得多（20-30ms）
- 对于大多数医学图像，简单方法效果足够好

**实现：**
```python
def segment_fast(gray_roi):
    # Otsu 阈值
    _, binary = cv2.threshold(gray_roi, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # 简单的形态学清理
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=1)
    return binary
```

**性能影响：** 150ms → 30ms（5x 提升）

### Decision 4: 减少图像复制

**选择：** 使用 in-place 操作和视图，避免不必要的 `.copy()`

**理由：**
- 每次 `.copy()` 都会分配新内存并复制数据
- 1280x1280 RGB 图像复制需要 ~5MB 内存和 ~5ms 时间
- 大多数情况下可以使用视图或 in-place 操作

**实现：**
```python
# 之前
scaled = bgr.copy()

# 之后
if m <= max_side:
    return bgr, 1.0  # 不复制
```

**性能影响：** 节省 10-20ms 和 20-30% 内存

### Decision 5: 向量化 LBP 计算

**选择：** 使用 NumPy 广播和向量化操作替代循环

**理由：**
- 当前实现使用 8 次循环，每次都有数组操作
- NumPy 向量化操作比 Python 循环快 10-100 倍
- 可以使用 `np.roll` 或切片实现邻域操作

**实现：**
```python
# 使用 NumPy 切片和广播
def lbp_vectorized(gray):
    h, w = gray.shape
    lbp = np.zeros((h-2, w-2), dtype=np.uint8)
    
    # 8 个邻域的比较，一次性完成
    center = gray[1:-1, 1:-1]
    lbp |= (gray[0:-2, 0:-2] >= center).astype(np.uint8) << 0
    lbp |= (gray[0:-2, 1:-1] >= center).astype(np.uint8) << 1
    # ... 其他 6 个方向
    
    return lbp
```

**性能影响：** 90ms → 30ms（3x 提升）

### Decision 6: 性能监控架构

**选择：** 使用装饰器模式 + 上下文管理器记录性能指标

**理由：**
- 装饰器可以自动记录函数级别的性能
- 上下文管理器适合记录代码块的性能
- 与现有 structlog 集成良好
- 最小化对现有代码的侵入

**实现：**
```python
@performance_monitor("preprocess")
def preprocess_gray(bgr, params):
    # ... 实现
    
# 或使用上下文管理器
with perf_timer("segment"):
    mask = segment_roi(gray_roi, params)
```

**数据收集：**
- 每个步骤的耗时（ms）
- 内存使用（MB）
- 图像尺寸
- 参数配置
- 输出到 structlog

### Decision 7: 性能模式配置

**选择：** 提供三种预设模式 + 自定义配置

**模式定义：**

| 参数 | Fast | Balanced | Quality |
|------|------|----------|---------|
| max_side | 800 | 1280 | 1920 |
| median_ksize | 3 | 3/5 | 5/7 |
| segment_method | otsu_fast | otsu_roi | watershed |
| use_bilateral | false | false | true |
| morph_iterations | 1 | 2 | 3 |

**API 接口：**
```python
POST /api/process?performance_mode=fast
```

**向后兼容：** 默认使用 `balanced` 模式

### Decision 8: 缓存策略

**选择：** 不实现请求级缓存，仅优化内部数据流

**理由：**
- 每个请求的图像都不同，缓存命中率低
- 缓存会增加内存使用和复杂度
- 专注于算法优化更有效

**替代方案：**
- ❌ Redis 缓存：增加部署复杂度
- ❌ 内存缓存：命中率低，内存浪费
- ✅ 优化数据流：减少中间变量

## Risks / Trade-offs

### Risk 1: 快速模式质量下降

**风险：** 使用小核和简单算法可能降低处理质量

**缓解措施：**
- 提供三种模式，用户可选择
- 默认使用 balanced 模式（质量和速度平衡）
- 在文档中明确说明各模式的权衡
- 添加质量指标（如果有 ground truth）

### Risk 2: 性能监控开销

**风险：** 添加性能监控可能增加处理时间

**缓解措施：**
- 使用高效的计时方法（`time.perf_counter()`）
- 异步写入日志
- 可通过环境变量禁用详细监控
- 监控开销 < 5ms（< 1% 总时间）

### Risk 3: 内存优化可能引入 bug

**风险：** 减少复制可能导致意外的数据修改

**缓解措施：**
- 仔细审查所有 in-place 操作
- 添加单元测试验证数据完整性
- 使用 `np.shares_memory()` 检查数据共享
- 在关键位置保留必要的复制

### Risk 4: 向后兼容性

**风险：** 性能优化可能改变输出结果

**缓解措施：**
- 默认使用 balanced 模式（接近当前行为）
- 添加回归测试比较优化前后的输出
- 允许用户选择 quality 模式获得原始行为
- 在文档中说明差异

### Risk 5: 不同图像类型的表现差异

**风险：** 优化可能在某些图像类型上效果不佳

**缓解措施：**
- 在多种图像类型上测试（医学图像、皮肤镜图像）
- 提供自适应参数选择
- 允许用户覆盖自动选择
- 收集用户反馈持续改进

## Trade-offs

### Speed vs Quality

**Trade-off：** 快速模式牺牲一些质量换取速度

**决策：** 提供多种模式，让用户选择

**理由：** 不同场景有不同需求（实时预览 vs 最终处理）

### Memory vs Speed

**Trade-off：** 某些优化（如缓存）可能增加内存使用

**决策：** 优先减少内存使用，不实现大规模缓存

**理由：** 服务器内存有限，多用户并发时内存更重要

### Complexity vs Maintainability

**Trade-off：** 过度优化会增加代码复杂度

**决策：** 只优化明确的瓶颈，保持代码可读性

**理由：** 可维护性长期更重要

## Migration Plan

### Phase 1: 基础优化（Week 1）
1. 实现智能图像缩放
2. 优化 medianBlur 策略
3. 减少图像复制
4. 添加性能监控

**验证：** 运行现有测试，确保无回归

### Phase 2: 算法优化（Week 2）
1. 实现快速分割算法
2. 向量化 LBP 计算
3. 优化检测算法
4. 优化数据流

**验证：** 性能基准测试，确保达到目标

### Phase 3: 配置和监控（Week 3）
1. 实现性能模式配置
2. 完善性能监控
3. 添加性能报告
4. 创建性能文档

**验证：** 端到端测试，用户验收

### Rollback Strategy

如果优化导致问题：
1. 通过环境变量禁用优化（`ENABLE_PERFORMANCE_OPTIMIZATION=false`）
2. 回滚到 balanced 模式
3. 逐个禁用优化功能
4. 完全回滚代码（Git revert）

### Monitoring

部署后监控：
- 平均处理时间
- P50, P95, P99 延迟
- 错误率
- 内存使用
- 用户反馈

## Open Questions

1. **是否需要 GPU 加速？**
   - 当前决定：不需要（保持简单）
   - 重新评估条件：如果 CPU 优化后仍不满足需求

2. **是否需要异步处理？**
   - 当前决定：暂不需要（单个请求优化优先）
   - 重新评估条件：如果需要支持批量处理

3. **是否需要分布式处理？**
   - 当前决定：不需要（单机性能足够）
   - 重新评估条件：如果并发用户数 > 100

4. **性能目标是否现实？**
   - 需要通过原型验证
   - 如果无法达到 50% 提升，调整目标或方法

5. **是否需要 A/B 测试？**
   - 当前决定：不需要（内部优化）
   - 重新评估条件：如果影响用户体验

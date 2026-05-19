## Why

当前 OpenCV 图像处理系统存在严重的性能问题，影响用户体验。处理 1280x1280 图像需要约 950ms，大图像（>2000px）处理时间超过 3 秒，导致用户等待时间过长。此外，缺乏性能监控和优化机制，无法识别瓶颈。需要系统性的性能优化来提升处理速度 50% 以上，同时保持处理质量。

## What Changes

- 实现智能图像缩放策略，自动处理大图像
- 优化核心算法（预处理、检测、分割、LBP）减少计算量
- 减少不必要的图像复制和颜色空间转换
- 添加性能监控和日志系统，记录每个步骤的耗时
- 提供快速模式和高质量模式的配置选项
- 优化 NumPy 操作，使用向量化替代循环
- 实现中间结果缓存机制
- 添加内存使用监控和优化
- 创建性能基准测试套件
- 提供性能优化最佳实践文档

## Capabilities

### New Capabilities

- `image-scaling-strategy`: 智能图像缩放策略，根据图像大小自动选择最优缩放参数，支持多级缩放策略
- `algorithm-optimization`: 核心算法优化，包括预处理、检测、分割、LBP 的性能优化实现
- `performance-monitoring`: 性能监控系统，记录每个处理步骤的耗时、内存使用、吞吐量等指标
- `fast-mode-config`: 快速模式配置，提供预设的性能优化参数组合，可在速度和质量间平衡
- `memory-optimization`: 内存优化策略，减少图像复制、优化数据结构、实现智能缓存
- `performance-benchmarking`: 性能基准测试框架，自动化测试不同场景下的性能表现

### Modified Capabilities

- `image-preprocessing`: 优化预处理流程，减少不必要的操作，添加快速模式支持
- `roi-detection`: 优化检测算法，减少重复计算，提升检测速度
- `image-segmentation`: 提供更快的分割算法选项，优化 watershed 性能
- `api-processing`: 添加超时控制、响应压缩、异步处理支持

## Impact

### 代码影响
- `app/core/preprocess.py` - 添加快速模式，优化滤波器参数
- `app/core/detect.py` - 优化轮廓检测，减少重复计算
- `app/core/segment.py` - 添加快速分割算法，优化 watershed
- `app/core/lbp.py` - 向量化计算，减少循环
- `app/core/decode.py` - 增强智能缩放逻辑
- `app/core/pipeline.py` - 添加性能监控，优化数据流
- `app/api/routes.py` - 添加超时控制，响应压缩
- `app/config.py` - 添加性能配置选项

### API 影响
- 添加新的查询参数：`performance_mode` (fast/balanced/quality)
- 响应中添加性能指标：`timings`, `memory_usage`
- 保持向后兼容，默认使用 balanced 模式

### 依赖影响
- 可能需要 `orjson` 用于更快的 JSON 序列化
- 可能需要 `psutil` 用于内存监控
- 所有优化都基于现有依赖（NumPy, OpenCV）

### 系统影响
- 预期处理速度提升 50-100%
- 内存使用减少 20-30%
- 大图像处理时间减少 70-80%
- 添加性能日志可能增加少量磁盘 I/O

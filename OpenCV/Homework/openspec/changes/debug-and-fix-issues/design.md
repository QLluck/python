## Context

当前 OpenCV 图像处理项目已实现基础功能，包括：
- **核心模块**: decode、preprocess、detect、segment、postprocess、viz、lbp、metrics、pipeline
- **API 层**: FastAPI 路由（/health、/api/process）
- **现有状态**: 基础功能可用，但缺乏系统性的质量保障

**已识别的问题类型**:
1. **代码质量**: 缺乏类型注解、文档字符串不完整、代码风格不统一
2. **错误处理**: 异常处理不一致、错误信息不清晰、缺乏统一的错误响应格式
3. **性能**: 未进行性能分析、潜在的内存泄漏、算法效率未优化
4. **安全**: 输入验证不完善、文件上传缺乏大小限制、资源消耗无限制
5. **日志**: 日志不结构化、缺乏关键操作记录、难以追踪问题
6. **兼容性**: 未测试不同 Python/OpenCV 版本、跨平台问题未知

**约束**:
- 不能破坏现有 API 接口
- 性能开销需控制在 5% 以内
- 必须保持向后兼容
- 改动需要渐进式，不能一次性重构所有代码

## Goals / Non-Goals

**Goals:**
- 建立自动化代码质量检查流程（linting、formatting、type checking）
- 实现统一的异常处理和错误响应机制
- 建立结构化日志系统，便于问题追踪和监控
- 识别并修复性能瓶颈和内存泄漏
- 加强输入验证和安全防护
- 提高代码可维护性（类型注解、文档字符串）
- 建立代码审查检查清单和最佳实践

**Non-Goals:**
- 不进行大规模架构重构（保持现有模块结构）
- 不改变现有 API 接口签名（保持向后兼容）
- 不实现实时监控仪表板（仅日志和基础指标）
- 不进行算法替换（仅优化现有算法）
- 不实现分布式追踪（单体应用无需）

## Decisions

### 1. 代码质量工具链: Black + Ruff + mypy

**决策**: 使用 Black（格式化）+ Ruff（linting）+ mypy（类型检查）作为代码质量工具链

**理由**:
- **Black**: 零配置、确定性格式化，消除代码风格争议
- **Ruff**: 极快的 Python linter（比 flake8/pylint 快 10-100 倍），整合多种规则
- **mypy**: 业界标准的静态类型检查器，支持渐进式类型注解

**配置**:
```toml
# pyproject.toml
[tool.black]
line-length = 100
target-version = ['py39', 'py310', 'py311']

[tool.ruff]
line-length = 100
select = ["E", "F", "W", "I", "N", "UP", "B", "A", "C4", "PT"]
ignore = ["E501"]  # Black handles line length

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false  # Gradual adoption
```

**替代方案**:
- pylint + flake8: 功能强大但速度慢，配置复杂
- 仅 Black: 无法检查代码质量问题（未使用变量、导入顺序等）

### 2. 异常处理架构: 自定义异常层次 + 统一错误处理器

**决策**: 创建自定义异常层次结构，使用 FastAPI 异常处理器统一错误响应

**异常层次**:
```python
# app/core/exceptions.py
class AppException(Exception):
    """Base exception for all application errors."""
    def __init__(self, message: str, code: str, status_code: int = 500):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)

class ValidationError(AppException):
    """Input validation errors."""
    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR", 400)

class ImageDecodeError(AppException):
    """Image decoding errors."""
    def __init__(self, message: str):
        super().__init__(message, "IMAGE_DECODE_ERROR", 400)

class ProcessingError(AppException):
    """Image processing errors."""
    def __init__(self, message: str):
        super().__init__(message, "PROCESSING_ERROR", 500)

class ResourceLimitError(AppException):
    """Resource limit exceeded."""
    def __init__(self, message: str):
        super().__init__(message, "RESOURCE_LIMIT_ERROR", 413)
```

**统一错误响应格式**:
```json
{
  "ok": false,
  "error": {
    "message": "Image decode failed",
    "code": "IMAGE_DECODE_ERROR",
    "details": {"filename": "test.png"}
  },
  "timestamp": "2026-05-07T10:30:00Z"
}
```

**理由**:
- 清晰的异常层次便于分类处理
- 统一的错误响应格式便于客户端解析
- 包含错误码便于国际化和文档化

**替代方案**:
- 使用标准异常: 缺乏业务语义，难以区分错误类型
- 返回错误码而非异常: 破坏 Python 惯用法，难以追踪调用栈

### 3. 日志系统: structlog + JSON 格式

**决策**: 使用 structlog 实现结构化日志，输出 JSON 格式

**配置**:
```python
# app/core/logging.py
import structlog

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)
```

**日志级别使用**:
- **DEBUG**: 详细的调试信息（参数值、中间结果）
- **INFO**: 关键操作（图像处理开始/完成、API 请求）
- **WARNING**: 可恢复的问题（使用默认值、降级处理）
- **ERROR**: 错误但不影响其他请求（单个请求失败）
- **CRITICAL**: 系统级错误（服务无法启动）

**理由**:
- JSON 格式便于日志聚合和分析（ELK、Splunk）
- 结构化日志便于查询和过滤
- structlog 性能优秀，支持上下文绑定

**替代方案**:
- 标准 logging: 非结构化，难以解析和查询
- 纯文本日志: 难以机器处理，查询效率低

### 4. 性能分析策略: 分层分析 + 持续监控

**决策**: 使用多层次性能分析工具，建立性能基线

**工具选择**:
- **cProfile**: 函数级性能分析（识别热点函数）
- **memory_profiler**: 逐行内存分析（识别内存泄漏）
- **py-spy**: 生产环境采样分析（低开销）
- **pytest-benchmark**: 回归测试（防止性能退化）

**性能基线**:
```python
# 建立基线指标
PERFORMANCE_BASELINES = {
    "decode_1024x1024": 0.05,  # 50ms
    "preprocess_1024x1024": 0.10,  # 100ms
    "segment_1024x1024": 0.50,  # 500ms
    "full_pipeline_1024x1024": 2.0,  # 2s
}
```

**监控指标**:
- 处理时间（P50、P95、P99）
- 内存使用（峰值、平均）
- 吞吐量（请求/秒）
- 错误率

**理由**:
- 分层分析覆盖不同场景（开发、测试、生产）
- 基线指标便于检测性能退化
- 持续监控确保长期性能稳定

### 5. 输入验证策略: Pydantic + 自定义验证器

**决策**: 使用 Pydantic 进行参数验证，添加自定义验证器处理复杂规则

**验证层次**:
1. **类型验证**: Pydantic 自动类型检查
2. **范围验证**: Field 约束（ge、le、gt、lt）
3. **业务验证**: 自定义 validator（如奇数核大小）
4. **安全验证**: 文件大小、类型、内容检查

**示例**:
```python
from pydantic import BaseModel, Field, validator

class ProcessRequest(BaseModel):
    max_side: int = Field(ge=64, le=4096, default=1280)
    median_ksize: int = Field(ge=1, le=31, default=5)
    
    @validator('median_ksize')
    def validate_odd_kernel(cls, v):
        if v % 2 == 0:
            raise ValueError('Kernel size must be odd')
        return v
```

**文件上传安全**:
- 最大文件大小: 10MB
- 允许的 MIME 类型: image/png, image/jpeg, image/bmp
- 内容验证: 实际解码验证（防止伪造扩展名）

**理由**:
- Pydantic 与 FastAPI 原生集成
- 声明式验证清晰易维护
- 自动生成 OpenAPI 文档

### 6. 兼容性测试策略: 矩阵测试 + 条件导入

**决策**: 使用 CI 矩阵测试多版本，代码中使用条件导入处理版本差异

**测试矩阵**:
```yaml
# .github/workflows/test.yml
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11']
    opencv-version: ['4.5', '4.6', '4.7', '4.8']
    os: [ubuntu-latest, macos-latest]
```

**条件导入示例**:
```python
import sys
if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias
```

**理由**:
- 矩阵测试确保多版本兼容
- 条件导入处理 API 差异
- 早期发现兼容性问题

### 7. 代码审查检查清单: 自动化 + 人工审查

**决策**: 建立分层检查清单，自动化检查 + 人工审查

**自动化检查**（PR 必须通过）:
- [ ] Black 格式化通过
- [ ] Ruff linting 无错误
- [ ] mypy 类型检查通过（新代码）
- [ ] 所有测试通过
- [ ] 代码覆盖率不下降

**人工审查检查清单**:
- [ ] 错误处理是否完善
- [ ] 日志记录是否充分
- [ ] 性能影响是否可接受
- [ ] 安全问题是否考虑
- [ ] 文档是否更新
- [ ] 边界条件是否处理

**理由**:
- 自动化检查提高效率
- 人工审查关注业务逻辑和设计
- 分层检查确保质量

## Risks / Trade-offs

### 风险 1: 添加类型注解可能引入新错误
**影响**: 错误的类型注解可能误导开发者

**缓解措施**:
- 渐进式添加类型注解（从新代码开始）
- mypy 配置为 `disallow_untyped_defs = false`（允许未注解代码）
- 代码审查重点检查类型注解正确性
- 运行时不依赖类型注解（仅静态检查）

### 风险 2: 结构化日志增加性能开销
**影响**: JSON 序列化可能影响性能

**缓解措施**:
- 使用高性能 JSON 库（orjson）
- 异步日志写入（不阻塞主线程）
- 生产环境使用 INFO 级别（减少日志量）
- 性能测试验证开销 < 5%

### 风险 3: 严格的输入验证可能拒绝合法请求
**影响**: 过于严格的验证可能影响可用性

**缓解措施**:
- 验证规则基于实际使用场景
- 提供清晰的错误信息指导用户修正
- 保留宽松模式选项（开发环境）
- 收集用户反馈调整验证规则

### 风险 4: 性能分析工具影响生产性能
**影响**: 持续性能监控可能增加开销

**缓解措施**:
- 生产环境使用低开销工具（py-spy 采样）
- 性能分析按需启动（不是默认开启）
- 使用采样而非全量追踪
- 监控指标聚合后再上报

### Trade-off 1: 代码质量 vs 开发速度
**选择**: 优先代码质量，接受初期开发速度下降

**理由**:
- 长期看，高质量代码减少维护成本
- 自动化工具减少人工检查时间
- 清晰的错误处理减少调试时间

### Trade-off 2: 详细日志 vs 性能开销
**选择**: 关键路径记录 INFO 日志，详细信息使用 DEBUG

**理由**:
- 生产环境 INFO 级别足够追踪问题
- DEBUG 日志可按需启用
- 结构化日志便于后期分析

### Trade-off 3: 严格验证 vs 灵活性
**选择**: 默认严格验证，提供清晰错误信息

**理由**:
- 严格验证防止无效输入浪费资源
- 清晰错误信息帮助用户快速修正
- 安全优先于便利性

## Migration Plan

### 阶段 1: 工具配置和基础设施（第 1-2 天）
1. 安装开发工具（black、ruff、mypy、structlog）
2. 创建配置文件（pyproject.toml、.pylintrc）
3. 配置 pre-commit hooks
4. 更新 CI 流程添加代码质量检查

### 阶段 2: 异常处理和日志系统（第 3-4 天）
1. 创建 app/core/exceptions.py 自定义异常
2. 创建 app/core/logging.py 日志配置
3. 在 main.py 添加全局异常处理器
4. 更新核心模块使用新异常和日志

### 阶段 3: 输入验证和安全加固（第 5-6 天）
1. 创建 app/core/validators.py 验证器
2. 增强 ProcessRequest 模型验证
3. 添加文件上传大小限制中间件
4. 实现资源限制（内存、超时）

### 阶段 4: 性能分析和优化（第 7-9 天）
1. 创建性能分析脚本（scripts/profile.py）
2. 运行 cProfile 识别热点函数
3. 运行 memory_profiler 检查内存泄漏
4. 优化识别的性能瓶颈
5. 建立性能基线和回归测试

### 阶段 5: 代码质量改进（第 10-12 天）
1. 运行 Black 格式化所有代码
2. 修复 Ruff 报告的问题
3. 为核心模块添加类型注解
4. 完善文档字符串
5. 代码审查和重构

### 阶段 6: 兼容性测试和文档（第 13-14 天）
1. 配置 CI 矩阵测试
2. 修复兼容性问题
3. 创建代码审查检查清单
4. 编写开发者文档
5. 更新 README 和贡献指南

### 回滚策略
- 所有改动通过 feature flags 控制（可快速禁用）
- 保留旧的错误处理逻辑（渐进式迁移）
- 日志系统向后兼容（同时支持旧格式）
- 性能优化独立提交（可单独回滚）

## Open Questions

1. **是否需要实现分布式追踪**（如 OpenTelemetry）？
   - 当前方案: 结构化日志 + 请求 ID
   - 考虑: 如果未来扩展为微服务，可能需要

2. **错误监控服务选择**？
   - 选项: Sentry、Rollbar、自建
   - 待定: 根据预算和需求决定

3. **性能监控仪表板**？
   - 当前方案: 日志 + 基础指标
   - 考虑: 是否需要 Grafana + Prometheus

4. **代码覆盖率目标**？
   - 提议: 80% 总体覆盖率
   - 待定: 核心模块是否需要更高覆盖率（90%+）

5. **是否需要 API 版本控制**？
   - 当前: 单一版本 API
   - 考虑: 未来破坏性变更时的迁移策略

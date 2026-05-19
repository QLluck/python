## Context

当前项目是一个基于 OpenCV 的医学图像处理系统，包含：
- **核心模块** (`app/core/`): decode、preprocess、detect、segment、postprocess、viz、lbp、metrics、pipeline
- **API 层** (`app/api/`): FastAPI 路由和端点
- **现有测试**: 基础 pytest 和 httpx 依赖已存在，但缺乏系统化测试覆盖

**当前状态**:
- 无单元测试覆盖核心算法
- 无集成测试验证完整流程
- 无性能基准和监控
- 无边界测试和异常处理验证
- 无图像质量回归检测机制

**约束**:
- Python 3.9-3.11
- OpenCV 通过 conda 安装
- FastAPI 异步架构
- 需要保持测试运行时间在合理范围（< 10 分钟）

## Goals / Non-Goals

**Goals:**
- 建立分层测试架构（单元 → 集成 → API → 性能）
- 实现 80%+ 代码覆盖率
- 创建可复用的测试夹具和工具函数
- 建立性能基准和回归检测
- 实现 CI/CD 自动化测试流程
- 提供清晰的测试数据管理方案

**Non-Goals:**
- 不实现 UI 自动化测试（项目无前端）
- 不进行压力测试到系统崩溃（仅合理负载测试）
- 不替换现有的手动验证流程（测试是补充）
- 不实现跨平台兼容性测试（专注 macOS/Linux）

## Decisions

### 1. 测试框架选择: pytest + 插件生态

**决策**: 使用 pytest 作为核心测试框架，配合 pytest-cov、pytest-asyncio、pytest-benchmark 等插件

**理由**:
- pytest 已在项目依赖中，无需引入新框架
- 丰富的插件生态支持异步、覆盖率、性能测试
- 简洁的测试语法和强大的 fixture 机制
- 与 FastAPI 官方推荐测试方案一致

**替代方案**:
- unittest: 过于冗长，缺乏现代特性
- nose2: 社区活跃度低，插件少

### 2. 测试目录结构: 按测试类型分层

**决策**: 采用 `tests/{unit,integration,api,performance}/` 分层结构

```
tests/
├── unit/              # 单元测试（按模块镜像 app/core/）
│   ├── test_decode.py
│   ├── test_preprocess.py
│   ├── test_detect.py
│   ├── test_segment.py
│   ├── test_postprocess.py
│   ├── test_viz.py
│   ├── test_lbp.py
│   └── test_metrics.py
├── integration/       # 集成测试
│   ├── test_pipeline.py
│   └── test_end_to_end.py
├── api/              # API 测试
│   └── test_routes.py
├── performance/      # 性能测试
│   ├── test_benchmarks.py
│   └── test_load.py
├── fixtures/         # 测试数据和夹具
│   ├── images/       # 测试图像库
│   ├── expected/     # 金标准结果
│   └── conftest.py   # 共享 fixtures
└── conftest.py       # 全局 pytest 配置
```

**理由**:
- 清晰的关注点分离
- 便于选择性运行测试（`pytest tests/unit/`）
- 符合测试金字塔原则（单元测试最多，性能测试最少）

**替代方案**:
- 按模块镜像结构: 难以区分测试类型，集成测试无明确位置

### 3. 测试数据管理: Git LFS + 分类存储

**决策**: 使用 Git LFS 管理测试图像，按用途分类存储

```
tests/fixtures/images/
├── valid/           # 正常测试图像（10-20 张）
│   ├── barcode_clear.png
│   ├── barcode_rotated.png
│   └── medical_sample.png
├── boundary/        # 边界测试图像
│   ├── tiny_10x10.png
│   ├── huge_8000x8000.png
│   ├── corrupted.png
│   └── empty.png
└── golden/          # 金标准参考图像
    └── expected_results/
```

**理由**:
- Git LFS 避免仓库膨胀（测试图像约 100MB）
- 分类存储便于测试用例选择合适数据
- 金标准数据支持回归检测

**替代方案**:
- 外部存储（S3/CDN）: 增加依赖和网络延迟
- 动态生成: 无法覆盖真实场景复杂性

### 4. API 测试策略: TestClient + 真实依赖

**决策**: 使用 FastAPI TestClient，测试时使用真实的图像处理逻辑（不 mock 核心算法）

**理由**:
- API 测试应验证真实行为，不是单元测试
- 核心算法已有单元测试覆盖，API 测试关注集成
- TestClient 提供同步接口，简化异步测试

**Mock 范围**:
- Mock: 外部服务（如果有）、文件系统（部分场景）
- 不 Mock: 核心图像处理逻辑、数据库（使用测试数据库）

### 5. 性能测试方案: pytest-benchmark + locust

**决策**: 
- 使用 pytest-benchmark 进行微基准测试（单个函数性能）
- 使用 locust 进行 API 负载测试（并发、吞吐量）

**基准指标**:
- 单张图像处理时间: < 2 秒（1024x1024）
- API 响应时间: P95 < 3 秒
- 并发处理能力: 10 并发用户，成功率 > 95%
- 内存使用: 单次处理 < 500MB

**理由**:
- pytest-benchmark 集成在单元测试中，无需额外工具
- locust 提供真实的 HTTP 负载模拟
- 分离微观和宏观性能测试

**替代方案**:
- Apache JMeter: 过重，不适合 Python 项目
- 仅 pytest-benchmark: 无法测试 API 层并发性能

### 6. CI/CD 集成: GitHub Actions + 分阶段测试

**决策**: 使用 GitHub Actions，分阶段运行测试

```yaml
stages:
  1. 快速检查 (< 1 分钟): 
     - Linting (ruff/black)
     - 类型检查 (mypy)
  2. 单元测试 (2-3 分钟):
     - 所有单元测试 + 覆盖率
  3. 集成测试 (2-3 分钟):
     - 集成测试 + API 测试
  4. 性能测试 (3-5 分钟):
     - 基准测试（仅在 main 分支或手动触发）
```

**理由**:
- 快速失败原则（linting 失败立即停止）
- 并行运行节省时间
- 性能测试仅在必要时运行（避免浪费 CI 资源）

### 7. 图像质量测试: SSIM + 像素差异 + 人工审核

**决策**: 使用结构相似性指数（SSIM）和像素差异检测回归，关键场景保留人工审核

**阈值**:
- SSIM > 0.95: 通过
- 0.90 < SSIM < 0.95: 警告（需人工审核）
- SSIM < 0.90: 失败

**理由**:
- SSIM 比简单像素差异更符合人眼感知
- 阈值允许算法优化带来的微小差异
- 人工审核作为最后防线

**替代方案**:
- 仅像素完全匹配: 过于严格，阻碍算法改进
- 仅人工审核: 不可扩展，无法自动化

## Risks / Trade-offs

### 风险 1: 测试运行时间过长影响开发效率
**影响**: 开发者等待测试结果时间过长，降低迭代速度

**缓解措施**:
- 使用 pytest markers 分类测试（`@pytest.mark.slow`）
- 本地开发只运行快速测试（`pytest -m "not slow"`）
- CI 并行运行测试
- 性能测试仅在 main 分支运行

### 风险 2: 测试数据集不足导致覆盖不全
**影响**: 真实场景的边界情况未被测试覆盖

**缓解措施**:
- 初期收集 20+ 真实医学图像样本
- 持续从生产环境收集失败案例
- 使用图像增强技术生成变体（旋转、缩放、噪声）
- 定期审查测试覆盖的场景类型

### 风险 3: 金标准数据维护成本高
**影响**: 算法改进后需要更新大量金标准数据

**缓解措施**:
- 使用版本化的金标准数据（`golden/v1/`, `golden/v2/`）
- 提供工具脚本批量生成新金标准
- 仅对关键场景维护金标准（不是所有测试）
- 使用相对阈值而非绝对匹配

### 风险 4: 性能测试结果不稳定
**影响**: CI 环境性能波动导致误报

**缓解措施**:
- 使用相对性能比较（与基线对比）而非绝对值
- 多次运行取中位数
- 设置合理的性能容差（±10%）
- 在固定的 CI runner 上运行性能测试

### Trade-off 1: 测试覆盖率 vs 维护成本
**选择**: 目标 80% 覆盖率，而非 100%

**理由**: 
- 80/20 原则：80% 覆盖率捕获大部分 bug
- 剩余 20% 通常是简单代码（getter/setter）或难以测试的边界情况
- 过高覆盖率要求导致测试代码膨胀和维护负担

### Trade-off 2: 真实依赖 vs Mock
**选择**: API 测试使用真实图像处理逻辑

**理由**:
- 优点: 测试真实行为，发现集成问题
- 缺点: 测试运行较慢，依赖 OpenCV 环境
- 判断: 项目核心价值在图像处理，必须测试真实逻辑

## Migration Plan

### 阶段 1: 基础设施搭建（第 1-2 天）
1. 安装测试依赖（pytest-cov、pytest-asyncio、pytest-benchmark、locust）
2. 创建测试目录结构
3. 配置 pytest.ini 和 conftest.py
4. 设置 Git LFS 并上传初始测试图像

### 阶段 2: 单元测试（第 3-5 天）
1. 为每个核心模块编写单元测试（优先级：decode → preprocess → detect → segment）
2. 创建共享 fixtures（测试图像加载、临时目录）
3. 达到 60%+ 覆盖率

### 阶段 3: 集成和 API 测试（第 6-7 天）
1. 编写 pipeline 集成测试
2. 编写 FastAPI 端点测试
3. 达到 80%+ 覆盖率

### 阶段 4: 性能和边界测试（第 8-9 天）
1. 实现 pytest-benchmark 基准测试
2. 编写边界测试用例
3. 配置 locust 负载测试

### 阶段 5: CI/CD 集成（第 10 天）
1. 创建 GitHub Actions workflow
2. 配置覆盖率报告（codecov 或 coveralls）
3. 设置 PR 检查规则

### 回滚策略
- 测试代码独立于生产代码，可随时删除或禁用
- 如 CI 测试阻塞开发，可临时设置为非阻塞（warning only）
- 测试数据存储在独立目录，不影响现有功能

## Open Questions

1. **是否需要集成视觉回归测试工具**（如 Percy、Applitools）？
   - 当前方案: 使用 SSIM 自建
   - 考虑: 如果图像对比需求复杂，可引入专业工具

2. **性能测试的触发频率**？
   - 提议: 仅在 main 分支和 release 前运行
   - 待定: 是否需要每日定时性能测试

3. **测试数据的隐私合规性**？
   - 问题: 医学图像可能包含敏感信息
   - 方案: 使用脱敏数据或合成数据，需与团队确认

4. **是否需要测试 OpenCV 版本兼容性**？
   - 当前: 假设固定 OpenCV 版本（conda 安装）
   - 考虑: 如果支持多版本，需增加矩阵测试

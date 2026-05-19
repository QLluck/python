## Why

当前项目缺乏系统化的测试覆盖，导致代码质量难以保证、回归风险高、性能瓶颈难以发现。需要建立全面的测试体系，覆盖单元测试、集成测试、API测试、性能测试、边界测试和图像质量测试，确保医学图像处理系统的稳定性、准确性和可维护性。

## What Changes

- 建立完整的测试框架和测试基础设施
- 为所有核心模块（decode、preprocess、detect、segment、postprocess、viz、lbp、metrics）编写单元测试
- 创建端到端集成测试套件，覆盖完整的图像处理流程
- 实现 FastAPI 端点的全面 API 测试
- 建立性能基准测试和监控机制
- 设计边界测试用例集（异常输入、极端参数、损坏数据）
- 实现图像质量评估测试（准确性、一致性、回归检测）
- 创建测试数据管理方案和测试图像库
- 建立 CI/CD 集成和自动化测试流程
- 编写测试文档和最佳实践指南

## Capabilities

### New Capabilities

- `unit-testing-framework`: 单元测试框架和核心模块测试套件，覆盖 decode、preprocess、detect、segment、postprocess、viz、lbp、metrics 等模块
- `integration-testing`: 集成测试框架，测试完整的图像处理流程和模块间交互
- `api-testing`: FastAPI 端点测试，包括健康检查、图像处理、参数验证、错误处理
- `performance-testing`: 性能测试框架，包括响应时间、吞吐量、资源使用、并发测试
- `boundary-testing`: 边界和异常测试，覆盖非法输入、极端参数、损坏数据、资源限制
- `image-quality-testing`: 图像质量评估测试，包括准确性验证、一致性检查、回归检测
- `test-data-management`: 测试数据管理方案，包括测试图像库、金标准数据、测试夹具
- `test-automation`: 测试自动化和 CI/CD 集成，包括自动化运行、报告生成、覆盖率分析

### Modified Capabilities

<!-- 无现有能力需要修改 -->

## Impact

**代码影响**:
- 新增 `tests/unit/` 目录及所有单元测试文件
- 新增 `tests/integration/` 目录及集成测试
- 新增 `tests/api/` 目录及 API 测试
- 新增 `tests/performance/` 目录及性能测试
- 新增 `tests/fixtures/` 扩展测试数据集
- 新增 `tests/conftest.py` pytest 配置
- 新增 `.github/workflows/test.yml` CI/CD 配置（如使用 GitHub）
- 更新 `requirements.txt` 添加测试依赖（pytest-cov、pytest-benchmark、locust 等）

**开发流程影响**:
- 开发者需要为新功能编写测试
- PR 合并前需要通过所有测试
- 性能回归会被自动检测
- 测试覆盖率要求达到 80% 以上

**系统影响**:
- 测试运行时间增加（预计完整测试套件 5-10 分钟）
- CI/CD 流程增加测试阶段
- 需要维护测试数据集（约 100MB）

**依赖影响**:
- 新增测试框架依赖：pytest、pytest-cov、pytest-asyncio、pytest-benchmark
- 新增 API 测试依赖：httpx、pytest-httpx
- 新增性能测试依赖：locust、memory-profiler
- 新增图像处理测试依赖：scikit-image（用于 SSIM 等指标）

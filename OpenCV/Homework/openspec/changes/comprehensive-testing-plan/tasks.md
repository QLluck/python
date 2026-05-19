## 1. 基础设施搭建

- [ ] 1.1 更新 requirements.txt 添加测试依赖（pytest-cov, pytest-asyncio, pytest-benchmark, locust, memory-profiler, scikit-image）
- [ ] 1.2 创建测试目录结构（tests/unit, tests/integration, tests/api, tests/performance, tests/fixtures）
- [ ] 1.3 创建 pytest.ini 配置文件，设置测试路径、标记和覆盖率选项
- [ ] 1.4 创建 tests/conftest.py 全局配置文件
- [ ] 1.5 创建 tests/fixtures/conftest.py 共享 fixtures
- [ ] 1.6 设置 Git LFS 配置（.gitattributes）用于测试图像管理
- [ ] 1.7 创建测试图像目录结构（tests/fixtures/images/valid, boundary, golden）

## 2. 测试数据准备

- [ ] 2.1 收集或生成 10-20 张有效测试图像（包括条形码和医学图像）
- [ ] 2.2 创建边界测试图像（tiny_10x10.png, huge_8000x8000.png, corrupted.png, empty.png）
- [ ] 2.3 创建测试数据生成工具脚本（tests/fixtures/generate_test_data.py）
- [ ] 2.4 创建图像加载 fixture（load_test_image, get_random_test_image）
- [ ] 2.5 创建临时目录 fixture（tmp_output_dir）
- [ ] 2.6 创建测试数据目录文档（tests/fixtures/README.md）

## 3. 单元测试 - decode 模块

- [ ] 3.1 创建 tests/unit/test_decode.py
- [ ] 3.2 实现条形码检测测试（有效图像、无条形码、多条形码）
- [ ] 3.3 实现条形码解码测试（不同格式：QR、EAN、Code128）
- [ ] 3.4 实现边界测试（None 输入、空数组、错误数据类型）
- [ ] 3.5 添加性能基准测试（使用 pytest-benchmark）

## 4. 单元测试 - preprocess 模块

- [ ] 4.1 创建 tests/unit/test_preprocess.py
- [ ] 4.2 实现灰度转换测试（彩色到灰度、维度验证）
- [ ] 4.3 实现降噪测试（高斯模糊、中值滤波、双边滤波）
- [ ] 4.4 实现对比度增强测试（直方图均衡化、CLAHE）
- [ ] 4.5 实现形态学操作测试（腐蚀、膨胀、开运算、闭运算）
- [ ] 4.6 实现边界测试（极小图像、极大图像、异常参数）

## 5. 单元测试 - detect 模块

- [ ] 5.1 创建 tests/unit/test_detect.py
- [ ] 5.2 实现边缘检测测试（Canny、Sobel）
- [ ] 5.3 实现轮廓检测测试（findContours、轮廓过滤）
- [ ] 5.4 实现特征检测测试（角点、SIFT/ORB 特征）
- [ ] 5.5 实现空结果测试（无特征图像）

## 6. 单元测试 - segment 模块

- [ ] 6.1 创建 tests/unit/test_segment.py
- [ ] 6.2 实现二值化测试（全局阈值、Otsu 阈值）
- [ ] 6.3 实现自适应阈值测试（局部光照变化）
- [ ] 6.4 实现分水岭分割测试（接触对象分离）
- [ ] 6.5 实现区域分割测试（连通组件分析）

## 7. 单元测试 - postprocess 模块

- [ ] 7.1 创建 tests/unit/test_postprocess.py
- [ ] 7.2 实现结果过滤测试（置信度过滤、尺寸过滤）
- [ ] 7.3 实现结果平滑测试（噪声去除、边界平滑）
- [ ] 7.4 实现结果精炼测试（重叠去除、合并相邻区域）

## 8. 单元测试 - viz 模块

- [ ] 8.1 创建 tests/unit/test_viz.py
- [ ] 8.2 实现边界框绘制测试（单个、多个、不同颜色）
- [ ] 8.3 实现叠加层渲染测试（掩码叠加、透明度）
- [ ] 8.4 实现空结果可视化测试（无检测结果）
- [ ] 8.5 实现文本标注测试（标签、置信度分数）

## 9. 单元测试 - lbp 模块

- [ ] 9.1 创建 tests/unit/test_lbp.py
- [ ] 9.2 实现 LBP 特征提取测试（基本 LBP、uniform LBP）
- [ ] 9.3 实现 LBP 直方图测试（归一化、bin 数量）
- [ ] 9.4 实现多尺度 LBP 测试（不同半径和邻域点数）
- [ ] 9.5 实现 LBP 特征维度验证测试

## 10. 单元测试 - metrics 模块

- [ ] 10.1 创建 tests/unit/test_metrics.py
- [ ] 10.2 实现准确率计算测试（TP、TN、FP、FN）
- [ ] 10.3 实现精确率和召回率测试
- [ ] 10.4 实现 F1 分数测试
- [ ] 10.5 实现图像质量指标测试（PSNR、SSIM、MSE）
- [ ] 10.6 实现 IoU 计算测试（分割评估）

## 11. 集成测试 - pipeline

- [ ] 11.1 创建 tests/integration/test_pipeline.py
- [ ] 11.2 实现完整流程测试（条形码图像端到端处理）
- [ ] 11.3 实现医学图像完整流程测试
- [ ] 11.4 实现模块交互测试（preprocess → detect → segment → postprocess）
- [ ] 11.5 实现数据流验证测试（格式一致性、元数据保留）
- [ ] 11.6 实现管道配置测试（最小处理、完整处理、自定义参数）
- [ ] 11.7 实现状态管理测试（多图像顺序处理、状态重置）
- [ ] 11.8 实现资源管理测试（内存清理、文件句柄关闭）

## 12. 集成测试 - LBP 集成

- [ ] 12.1 创建 tests/integration/test_lbp_integration.py
- [ ] 12.2 实现预处理后 LBP 提取测试
- [ ] 12.3 实现分割区域 LBP 特征测试
- [ ] 12.4 实现 LBP 特征比较测试

## 13. API 测试 - 基础端点

- [ ] 13.1 创建 tests/api/test_routes.py
- [ ] 13.2 实现健康检查端点测试（/health）
- [ ] 13.3 实现根路径测试（/）
- [ ] 13.4 配置 FastAPI TestClient fixture

## 14. API 测试 - 图像上传

- [ ] 14.1 实现有效 PNG 图像上传测试
- [ ] 14.2 实现有效 JPEG 图像上传测试
- [ ] 14.3 实现无效文件类型测试（PDF、TXT）
- [ ] 14.4 实现超大图像测试（413 Payload Too Large）
- [ ] 14.5 实现损坏图像测试（400 Bad Request）

## 15. API 测试 - 图像处理端点

- [ ] 15.1 实现条形码处理端点测试
- [ ] 15.2 实现医学图像处理端点测试
- [ ] 15.3 实现自定义参数处理测试
- [ ] 15.4 实现可视化结果测试

## 16. API 测试 - 参数验证和错误处理

- [ ] 16.1 实现参数验证测试（无效阈值、无效核大小）
- [ ] 16.2 实现缺失参数测试（422 Unprocessable Entity）
- [ ] 16.3 实现错误响应格式测试（一致的错误结构）
- [ ] 16.4 实现内部错误处理测试（500 Internal Server Error）

## 17. API 测试 - 响应格式和头部

- [ ] 17.1 实现 JSON 响应格式测试（Content-Type 验证）
- [ ] 17.2 实现图像响应格式测试（image/png, image/jpeg）
- [ ] 17.3 实现响应元数据测试（处理时间、置信度）
- [ ] 17.4 实现 CORS 头部测试
- [ ] 17.5 实现安全头部测试（X-Content-Type-Options 等）

## 18. 性能测试 - 微基准

- [ ] 18.1 创建 tests/performance/test_benchmarks.py
- [ ] 18.2 实现 decode 函数基准测试
- [ ] 18.3 实现 preprocess 函数基准测试
- [ ] 18.4 实现 detect 函数基准测试
- [ ] 18.5 实现 segment 函数基准测试
- [ ] 18.6 配置基准测试阈值和比较

## 19. 性能测试 - 管道性能

- [ ] 19.1 实现单图像处理时间测试（< 2 秒目标）
- [ ] 19.2 实现批处理吞吐量测试
- [ ] 19.3 实现不同图像尺寸性能测试
- [ ] 19.4 实现内存使用测试（< 500MB 目标）
- [ ] 19.5 实现内存泄漏检测测试

## 20. 性能测试 - API 性能

- [ ] 20.1 实现健康检查响应时间测试（< 100ms）
- [ ] 20.2 实现图像处理响应时间测试（P95 < 3 秒）
- [ ] 20.3 实现并发请求测试（10 并发）

## 21. 性能测试 - 负载测试

- [ ] 21.1 创建 tests/performance/locustfile.py
- [ ] 21.2 实现 locust 用户行为定义（图像上传和处理）
- [ ] 21.3 实现渐进负载测试场景（1-50 用户）
- [ ] 21.4 实现持续负载测试场景（10 用户 10 分钟）
- [ ] 21.5 实现峰值负载测试场景（5-50 用户突增）
- [ ] 21.6 配置负载测试报告生成

## 22. 边界测试

- [ ] 22.1 创建 tests/unit/test_boundary_cases.py
- [ ] 22.2 实现无效输入测试（None、空数组、错误类型）
- [ ] 22.3 实现极端参数测试（0、255、负数、超大值）
- [ ] 22.4 实现边界图像测试（1x1、10x10、8000x8000、极端宽高比）
- [ ] 22.5 实现损坏数据测试（损坏文件、截断数据、NaN/Inf 值）
- [ ] 22.6 实现并发访问测试（线程安全）
- [ ] 22.7 实现数值稳定性测试（除零保护、溢出保护）

## 23. 图像质量测试

- [ ] 23.1 创建 tests/integration/test_image_quality.py
- [ ] 23.2 实现 SSIM 计算测试
- [ ] 23.3 实现 PSNR 计算测试
- [ ] 23.4 实现 MSE 计算测试
- [ ] 23.5 创建金标准参考图像（至少 5 张）
- [ ] 23.6 实现回归检测测试（SSIM > 0.95 阈值）
- [ ] 23.7 实现一致性测试（多次运行相同结果）
- [ ] 23.8 实现边缘保留测试
- [ ] 23.9 实现降噪效果测试
- [ ] 23.10 实现分割质量测试（IoU 计算）

## 24. 测试工具和辅助函数

- [ ] 24.1 创建 tests/utils.py 测试工具模块
- [ ] 24.2 实现图像比较工具函数（compare_images, assert_images_similar）
- [ ] 24.3 实现测试数据生成工具（generate_noisy_image, generate_rotated_variants）
- [ ] 24.4 实现性能测量装饰器（@measure_time, @measure_memory）
- [ ] 24.5 实现测试报告生成工具

## 25. CI/CD 集成

- [ ] 25.1 创建 .github/workflows/test.yml（或其他 CI 配置）
- [ ] 25.2 配置 CI 环境（Python 版本、依赖安装）
- [ ] 25.3 配置 OpenCV 安装（conda 或系统包）
- [ ] 25.4 配置测试阶段（linting → unit → integration → performance）
- [ ] 25.5 配置测试并行化（pytest-xdist）
- [ ] 25.6 配置覆盖率报告上传（codecov 或 coveralls）
- [ ] 25.7 配置测试报告归档
- [ ] 25.8 配置 PR 检查规则（必须通过测试）
- [ ] 25.9 配置性能测试触发条件（仅 main 分支）

## 26. 测试文档

- [ ] 26.1 创建 tests/README.md 测试文档
- [ ] 26.2 编写测试运行指南（本地运行、CI 运行）
- [ ] 26.3 编写测试编写指南（如何添加新测试）
- [ ] 26.4 编写测试数据管理指南（添加、更新、删除测试图像）
- [ ] 26.5 编写故障排查指南（常见测试失败原因）
- [ ] 26.6 编写性能测试指南（如何运行和解读性能测试）
- [ ] 26.7 更新项目主 README.md 添加测试章节

## 27. 测试验证和优化

- [ ] 27.1 运行完整测试套件验证所有测试通过
- [ ] 27.2 验证代码覆盖率达到 80% 以上
- [ ] 27.3 验证测试运行时间在 10 分钟内
- [ ] 27.4 优化慢速测试（标记为 @pytest.mark.slow）
- [ ] 27.5 修复任何不稳定的测试（flaky tests）
- [ ] 27.6 验证 CI 流程正常工作
- [ ] 27.7 生成最终测试报告和覆盖率报告

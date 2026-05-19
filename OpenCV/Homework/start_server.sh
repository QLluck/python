#!/bin/bash
# 快速启动服务脚本

echo "=== 医学图像病变检测与分割系统 ==="
echo ""

# 激活环境
source "/Users/jack5/anaconda3/etc/profile.d/conda.sh"
conda activate cv

# 进入项目目录
cd "/Users/jack5/QLluckGithub/python/OpenCV/Homework"

echo "✓ 环境已激活: cv"
echo "✓ 工作目录: $(pwd)"
echo ""
echo "启动服务..."
echo "访问地址: http://127.0.0.1:8000"
echo "按 Ctrl+C 停止服务"
echo ""

# 启动服务
/Users/jack5/anaconda3/envs/cv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

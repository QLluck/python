#!/usr/bin/env python3
"""最小环境测试"""
import sys
print(f"Python: {sys.version}")
print(f"Executable: {sys.executable}")

try:
    import numpy as np
    print(f"✓ NumPy {np.__version__}")
except Exception as e:
    print(f"✗ NumPy: {e}")
    sys.exit(1)

try:
    import cv2
    print(f"✓ OpenCV {cv2.__version__}")
except Exception as e:
    print(f"✗ OpenCV: {e}")
    sys.exit(1)

try:
    import fastapi
    print(f"✓ FastAPI {fastapi.__version__}")
except Exception as e:
    print(f"✗ FastAPI: {e}")
    sys.exit(1)

print("\n所有依赖正常")

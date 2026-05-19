#!/usr/bin/env python3
"""计划 B 测试：上传解码 + 元信息"""
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
FIXTURES = Path("tests/fixtures")

def test_b1_valid_png():
    """B1: 合法 PNG"""
    with open(FIXTURES / "valid_gray.png", "rb") as f:
        files = {"file": ("valid_gray.png", f, "image/png")}
        data = {"stage": "meta_only"}
        resp = client.post("/api/process", files=files, data=data)
    
    result = resp.json()
    assert result["ok"] == True, f"Expected ok=true, got {result}"
    assert "meta" in result
    assert result["meta"]["w"] > 0
    assert result["meta"]["h"] > 0
    print(f"✓ B1: PNG 解码成功 - {result['meta']['w']}x{result['meta']['h']}")

def test_b2_valid_jpg():
    """B2: 合法 JPG"""
    with open(FIXTURES / "valid_rgb.jpg", "rb") as f:
        files = {"file": ("valid_rgb.jpg", f, "image/jpeg")}
        data = {"stage": "meta_only"}
        resp = client.post("/api/process", files=files, data=data)
    
    result = resp.json()
    assert result["ok"] == True
    print(f"✓ B2: JPG 解码成功 - {result['meta']['w']}x{result['meta']['h']}")

def test_b3_corrupt():
    """B3: 损坏文件"""
    with open(FIXTURES / "corrupt.jpg", "rb") as f:
        files = {"file": ("corrupt.jpg", f, "image/jpeg")}
        resp = client.post("/api/process", files=files)
    
    result = resp.json()
    assert result["ok"] == False, "Expected ok=false for corrupt file"
    assert "error" in result
    assert any(kw in result["error"].lower() for kw in ["decode", "invalid", "failed"])
    print(f"✓ B3: 损坏文件正确拒绝 - {result['error'][:50]}")

def test_b4_non_image():
    """B4: 非图像扩展名"""
    with open(FIXTURES / "test.txt", "rb") as f:
        files = {"file": ("test.txt", f, "text/plain")}
        resp = client.post("/api/process", files=files)
    
    result = resp.json()
    assert result["ok"] == False
    print(f"✓ B4: 非图像文件正确拒绝 - {result['error'][:50]}")

def test_b5_huge_scale():
    """B5: 超大图缩放"""
    with open(FIXTURES / "huge.png", "rb") as f:
        files = {"file": ("huge.png", f, "image/png")}
        data = {"max_side": "1024", "stage": "meta_only"}
        resp = client.post("/api/process", files=files, data=data)
    
    result = resp.json()
    assert result["ok"] == True
    assert result["meta"]["scale"] < 1.0, "Expected scale < 1.0 for huge image"
    assert max(result["meta"]["w"], result["meta"]["h"]) <= 1024
    print(f"✓ B5: 大图缩放成功 - scale={result['meta']['scale']:.3f}, size={result['meta']['w']}x{result['meta']['h']}")

def test_b6_rgba():
    """B6: RGBA 处理"""
    with open(FIXTURES / "rgba.png", "rb") as f:
        files = {"file": ("rgba.png", f, "image/png")}
        data = {"stage": "meta_only"}
        resp = client.post("/api/process", files=files, data=data)
    
    result = resp.json()
    assert result["ok"] == True
    # 应该转为 3 通道
    print(f"✓ B6: RGBA 处理成功 - channels={result['meta'].get('channels', 'N/A')}")

def test_b7_empty():
    """B7: 空文件"""
    with open(FIXTURES / "empty.jpg", "rb") as f:
        files = {"file": ("empty.jpg", f, "image/jpeg")}
        resp = client.post("/api/process", files=files)
    
    result = resp.json()
    assert result["ok"] == False
    print(f"✓ B7: 空文件正确拒绝")

def test_b8_missing_file():
    """B8: 缺 file 字段"""
    resp = client.post("/api/process", data={"max_side": "1024"})
    assert resp.status_code in [400, 422], f"Expected 400/422, got {resp.status_code}"
    print(f"✓ B8: 缺少文件字段正确拒绝 - HTTP {resp.status_code}")

if __name__ == "__main__":
    tests = [
        test_b1_valid_png,
        test_b2_valid_jpg,
        test_b3_corrupt,
        test_b4_non_image,
        test_b5_huge_scale,
        test_b6_rgba,
        test_b7_empty,
        test_b8_missing_file,
    ]
    
    print("=== 计划 B 测试：上传解码 + 元信息 ===\n")
    failed = []
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"✗ {test.__name__}: {e}")
            failed.append(test.__name__)
    
    print(f"\n=== 结果：{len(tests) - len(failed)}/{len(tests)} 通过 ===")
    if failed:
        print(f"失败: {', '.join(failed)}")
        sys.exit(1)

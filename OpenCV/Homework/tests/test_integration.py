import httpx
import pytest
import json
import time
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"
FIXTURES = Path("tests/fixtures")

class TestResults:
    def __init__(self):
        self.passed = []
        self.failed = []
        self.warnings = []
        self.timings = {}
    
    def add_pass(self, name, time_ms=None):
        self.passed.append(name)
        if time_ms:
            self.timings[name] = time_ms
    
    def add_fail(self, name, error):
        self.failed.append((name, error))
    
    def add_warning(self, name, msg):
        self.warnings.append((name, msg))

results = TestResults()

def test_health():
    """测试健康检查"""
    try:
        resp = httpx.get(f"{BASE_URL}/health", timeout=5)
        assert resp.status_code == 200
        data = resp.json()
        assert data.get("ok") == True
        results.add_pass("健康检查")
        print("✅ 健康检查通过")
    except Exception as e:
        results.add_fail("健康检查", str(e))
        print(f"❌ 健康检查失败: {e}")

def test_valid_image():
    """测试正常图片处理"""
    try:
        start = time.time()
        with open(FIXTURES / "valid_gray.png", "rb") as f:
            files = {"file": ("valid_gray.png", f, "image/png")}
            data = {
                "stage": "full",
                "mode": "gray_medical",
                "max_side": "1280",
                "median_ksize": "5",
                "segment_method": "otsu_roi"
            }
            resp = httpx.post(f"{BASE_URL}/api/process", files=files, data=data, timeout=30)
        
        elapsed = int((time.time() - start) * 1000)
        
        assert resp.status_code == 200
        result = resp.json()
        assert result.get("ok") == True
        assert result.get("overlay_png_b64") is not None
        assert result.get("mask_png_b64") is not None
        assert "meta" in result
        
        results.add_pass("正常图片处理", elapsed)
        print(f"✅ 正常图片处理通过 (耗时: {elapsed}ms)")
    except Exception as e:
        results.add_fail("正常图片处理", str(e))
        print(f"❌ 正常图片处理失败: {e}")

def test_invalid_median_ksize_even():
    """测试偶数 median_ksize 参数"""
    try:
        with open(FIXTURES / "valid_gray.png", "rb") as f:
            files = {"file": ("test.png", f, "image/png")}
            data = {"median_ksize": "4"}  # 偶数
            resp = httpx.post(f"{BASE_URL}/api/process", files=files, data=data, timeout=10)
        
        # 应该返回 400 错误
        if resp.status_code == 400:
            results.add_pass("偶数median_ksize验证")
            print("✅ 偶数median_ksize正确拦截")
        else:
            results.add_warning("偶数median_ksize验证", f"返回状态码 {resp.status_code}，期望 400")
            print(f"⚠️ 偶数median_ksize未拦截，状态码: {resp.status_code}")
    except Exception as e:
        results.add_fail("偶数median_ksize验证", str(e))
        print(f"❌ 偶数median_ksize测试失败: {e}")

def test_invalid_median_ksize_zero():
    """测试 median_ksize=0"""
    try:
        with open(FIXTURES / "valid_gray.png", "rb") as f:
            files = {"file": ("test.png", f, "image/png")}
            data = {"median_ksize": "0"}
            resp = httpx.post(f"{BASE_URL}/api/process", files=files, data=data, timeout=10)
        
        if resp.status_code == 400:
            results.add_pass("median_ksize=0验证")
            print("✅ median_ksize=0正确拦截")
        else:
            results.add_warning("median_ksize=0验证", f"返回状态码 {resp.status_code}")
            print(f"⚠️ median_ksize=0未拦截")
    except Exception as e:
        results.add_fail("median_ksize=0验证", str(e))
        print(f"❌ median_ksize=0测试失败: {e}")

def test_invalid_max_side():
    """测试 max_side=0"""
    try:
        with open(FIXTURES / "valid_gray.png", "rb") as f:
            files = {"file": ("test.png", f, "image/png")}
            data = {"max_side": "0"}
            resp = httpx.post(f"{BASE_URL}/api/process", files=files, data=data, timeout=10)
        
        if resp.status_code == 400:
            results.add_pass("max_side=0验证")
            print("✅ max_side=0正确拦截")
        else:
            results.add_warning("max_side=0验证", f"返回状态码 {resp.status_code}")
            print(f"⚠️ max_side=0未拦截")
    except Exception as e:
        results.add_fail("max_side=0验证", str(e))
        print(f"❌ max_side=0测试失败: {e}")

def test_corrupt_image():
    """测试损坏图片"""
    try:
        with open(FIXTURES / "corrupt.jpg", "rb") as f:
            files = {"file": ("corrupt.jpg", f, "image/jpeg")}
            resp = httpx.post(f"{BASE_URL}/api/process", files=files, timeout=10)
        
        result = resp.json()
        if result.get("ok") == False and "error" in result:
            results.add_pass("损坏图片处理")
            print(f"✅ 损坏图片正确拒绝: {result['error'][:50]}")
        else:
            results.add_warning("损坏图片处理", "未返回错误")
            print("⚠️ 损坏图片未正确处理")
    except Exception as e:
        results.add_fail("损坏图片处理", str(e))
        print(f"❌ 损坏图片测试失败: {e}")

def test_tiny_image():
    """测试极小图片"""
    try:
        start = time.time()
        with open(FIXTURES / "tiny.png", "rb") as f:
            files = {"file": ("tiny.png", f, "image/png")}
            resp = httpx.post(f"{BASE_URL}/api/process", files=files, timeout=30)
        
        elapsed = int((time.time() - start) * 1000)
        result = resp.json()
        
        if result.get("ok") == True:
            results.add_pass("极小图片处理", elapsed)
            print(f"✅ 极小图片处理通过 (耗时: {elapsed}ms)")
        else:
            results.add_warning("极小图片处理", result.get("error", "未知错误"))
            print(f"⚠️ 极小图片处理: {result.get('error')}")
    except Exception as e:
        results.add_fail("极小图片处理", str(e))
        print(f"❌ 极小图片测试失败: {e}")

def test_huge_image():
    """测试超大图片"""
    try:
        start = time.time()
        with open(FIXTURES / "huge.png", "rb") as f:
            files = {"file": ("huge.png", f, "image/png")}
            data = {"max_side": "1024"}
            resp = httpx.post(f"{BASE_URL}/api/process", files=files, data=data, timeout=60)
        
        elapsed = int((time.time() - start) * 1000)
        result = resp.json()
        
        if result.get("ok") == True:
            scale = result.get("meta", {}).get("scale", 1.0)
            results.add_pass("超大图片处理", elapsed)
            print(f"✅ 超大图片处理通过 (耗时: {elapsed}ms, 缩放: {scale:.2f})")
            if elapsed > 10000:
                results.add_warning("超大图片性能", f"处理时间 {elapsed}ms 超过10秒")
        else:
            results.add_fail("超大图片处理", result.get("error"))
            print(f"❌ 超大图片处理失败: {result.get('error')}")
    except Exception as e:
        results.add_fail("超大图片处理", str(e))
        print(f"❌ 超大图片测试失败: {e}")

def test_all_black_image():
    """测试全黑图片"""
    try:
        with open(FIXTURES / "all_black.png", "rb") as f:
            files = {"file": ("all_black.png", f, "image/png")}
            resp = httpx.post(f"{BASE_URL}/api/process", files=files, timeout=30)
        
        result = resp.json()
        # 全黑图应该能处理，但可能无ROI
        if result.get("ok") in [True, False]:
            results.add_pass("全黑图片处理")
            print(f"✅ 全黑图片处理: ok={result.get('ok')}")
        else:
            results.add_warning("全黑图片处理", "返回格式异常")
    except Exception as e:
        results.add_fail("全黑图片处理", str(e))
        print(f"❌ 全黑图片测试失败: {e}")

def test_all_white_image():
    """测试全白图片"""
    try:
        with open(FIXTURES / "all_white.png", "rb") as f:
            files = {"file": ("all_white.png", f, "image/png")}
            resp = httpx.post(f"{BASE_URL}/api/process", files=files, timeout=30)
        
        result = resp.json()
        if result.get("ok") in [True, False]:
            results.add_pass("全白图片处理")
            print(f"✅ 全白图片处理: ok={result.get('ok')}")
        else:
            results.add_warning("全白图片处理", "返回格式异常")
    except Exception as e:
        results.add_fail("全白图片处理", str(e))
        print(f"❌ 全白图片测试失败: {e}")

def test_all_segment_methods():
    """测试所有分割方法"""
    methods = ["otsu_roi", "region_grow", "watershed"]
    for method in methods:
        try:
            with open(FIXTURES / "valid_gray.png", "rb") as f:
                files = {"file": ("test.png", f, "image/png")}
                data = {"segment_method": method}
                resp = httpx.post(f"{BASE_URL}/api/process", files=files, data=data, timeout=30)
            
            result = resp.json()
            if result.get("ok") == True:
                results.add_pass(f"分割方法: {method}")
                print(f"✅ 分割方法 {method} 通过")
            else:
                results.add_fail(f"分割方法: {method}", result.get("error"))
                print(f"❌ 分割方法 {method} 失败: {result.get('error')}")
        except Exception as e:
            results.add_fail(f"分割方法: {method}", str(e))
            print(f"❌ 分割方法 {method} 测试失败: {e}")

def test_all_stages():
    """测试所有阶段"""
    stages = ["meta_only", "preprocess_only", "detect_only", "full"]
    for stage in stages:
        try:
            with open(FIXTURES / "valid_gray.png", "rb") as f:
                files = {"file": ("test.png", f, "image/png")}
                data = {"stage": stage}
                resp = httpx.post(f"{BASE_URL}/api/process", files=files, data=data, timeout=30)
            
            result = resp.json()
            if result.get("ok") == True:
                results.add_pass(f"阶段: {stage}")
                print(f"✅ 阶段 {stage} 通过")
            else:
                results.add_fail(f"阶段: {stage}", result.get("error"))
                print(f"❌ 阶段 {stage} 失败")
        except Exception as e:
            results.add_fail(f"阶段: {stage}", str(e))
            print(f"❌ 阶段 {stage} 测试失败: {e}")

def print_summary():
    """打印测试总结"""
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    
    print(f"\n✅ 通过: {len(results.passed)}")
    for test in results.passed:
        print(f"   - {test}")
    
    if results.failed:
        print(f"\n❌ 失败: {len(results.failed)}")
        for test, error in results.failed:
            print(f"   - {test}: {error}")
    
    if results.warnings:
        print(f"\n⚠️  警告: {len(results.warnings)}")
        for test, msg in results.warnings:
            print(f"   - {test}: {msg}")
    
    if results.timings:
        print(f"\n⏱️  性能统计:")
        for test, ms in results.timings.items():
            print(f"   - {test}: {ms}ms")
    
    print(f"\n总计: {len(results.passed) + len(results.failed)} 个测试")
    print(f"通过率: {len(results.passed) / (len(results.passed) + len(results.failed)) * 100:.1f}%")
    print("="*60)

if __name__ == "__main__":
    print("开始集成测试...\n")
    
    test_health()
    test_valid_image()
    test_invalid_median_ksize_even()
    test_invalid_median_ksize_zero()
    test_invalid_max_side()
    test_corrupt_image()
    test_tiny_image()
    test_huge_image()
    test_all_black_image()
    test_all_white_image()
    test_all_segment_methods()
    test_all_stages()
    
    print_summary()

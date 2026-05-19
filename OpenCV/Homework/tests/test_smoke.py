"""Smoke tests for API and pipeline stages."""

from __future__ import annotations

import base64

import cv2
import numpy as np
import pytest
from fastapi.testclient import TestClient

from app.core.pipeline import ProcessRequest, run
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def _synthetic_blob_png() -> bytes:
    """高对比暗区（模拟病变），便于 Otsu + 形态学在各版 OpenCV 下稳定出连通域。"""
    img = np.full((256, 256, 3), 255, np.uint8)
    cv2.circle(img, (128, 128), 55, (0, 0, 0), -1)
    ok, buf = cv2.imencode(".png", img)
    assert ok
    return buf.tobytes()


def _stable_detect_params() -> dict:
    """预处理略简化，避免顶帽在近似常数背景上削弱对比导致漏检。"""
    return {"use_tophat": False, "use_blackhat": False}


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("ok") is True


def test_index(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "医学图像" in r.content.decode("utf-8")


def test_meta_only(client):
    data = _synthetic_blob_png()
    files = {"file": ("test.png", data, "image/png")}
    form = {"stage": "meta_only", "max_side": 512}
    r = client.post("/api/process", files=files, data=form)
    assert r.status_code == 200
    j = r.json()
    assert j["ok"] is True
    assert j["meta"]["w"] > 0


def test_preprocess_odd_validation(client):
    data = _synthetic_blob_png()
    files = {"file": ("test.png", data, "image/png")}
    form = {"stage": "preprocess_only", "median_ksize": "4"}
    r = client.post("/api/process", files=files, data=form)
    assert r.status_code == 400
    assert r.json().get("ok") is False


def test_full_pipeline_run_direct():
    data = _synthetic_blob_png()
    req = ProcessRequest(stage="full", min_component_area=10, max_side=512, **_stable_detect_params())
    out = run(data, "synth.png", req)
    assert out["ok"] is True
    assert out["overlay_png_b64"]
    assert out["mask_png_b64"]
    assert out["meta"]["roi"]


def test_segment_methods():
    data = _synthetic_blob_png()
    for method in ("otsu_roi", "region_grow", "watershed"):
        req = ProcessRequest(
            stage="full",
            segment_method=method,
            min_component_area=10,
            max_side=512,
            **_stable_detect_params(),
        )
        out = run(data, "synth.png", req)
        assert out["ok"] is True, (method, out.get("error"))


def test_static_assets(client):
    r = client.get("/static/style.css")
    assert r.status_code == 200


def test_corrupt_file(client):
    files = {"file": ("bad.png", b"not a png", "image/png")}
    r = client.post("/api/process", files=files, data={"stage": "meta_only"})
    assert r.status_code == 400
    assert r.json().get("ok") is False


def test_bad_extension(client):
    data = _synthetic_blob_png()
    files = {"file": ("x.gif", data, "image/gif")}
    r = client.post("/api/process", files=files, data={"stage": "meta_only"})
    assert r.status_code == 400


def test_max_side_invalid(client):
    data = _synthetic_blob_png()
    files = {"file": ("t.png", data, "image/png")}
    r = client.post("/api/process", files=files, data={"stage": "meta_only", "max_side": "0"})
    assert r.status_code == 400


def test_uniform_black_fails_detect(tmp_path):
    img = np.zeros((64, 64, 3), np.uint8)
    ok, buf = cv2.imencode(".png", img)
    assert ok
    req = ProcessRequest(stage="full", max_side=256, min_component_area=5)
    out = run(buf.tobytes(), "black.png", req, log_dir=tmp_path)
    assert out["ok"] is False


def test_return_lbp_and_gt_metrics(tmp_path):
    data = _synthetic_blob_png()
    req = ProcessRequest(
        stage="full",
        return_lbp=True,
        min_component_area=10,
        max_side=256,
        **_stable_detect_params(),
    )
    h, w = 256, 256
    gt = np.zeros((h, w), np.uint8)
    cv2.circle(gt, (128, 128), 45, 255, -1)
    ok_gt, gt_buf = cv2.imencode(".png", gt)
    assert ok_gt
    out = run(data, "synth.png", req, gt_bytes=gt_buf.tobytes(), log_dir=tmp_path)
    assert out["ok"] is True
    assert out.get("lbp_png_b64")
    m = out["meta"].get("metrics")
    assert m is not None
    assert "dice" in m


def test_clahe_extreme_no_crash(tmp_path):
    data = _synthetic_blob_png()
    req = ProcessRequest(
        stage="preprocess_only",
        clahe_clip=40.0,
        clahe_tile=2,
        max_side=256,
    )
    out = run(data, "s.png", req, log_dir=tmp_path)
    assert out["ok"] is True
    raw = base64.b64decode(out["preprocess_png_b64"])
    assert raw[:8] == b"\x89PNG\r\n\x1a\n"


def test_detect_only(client):
    data = _synthetic_blob_png()
    files = {"file": ("t.png", data, "image/png")}
    r = client.post(
        "/api/process",
        files=files,
        data={
            "stage": "detect_only",
            "min_component_area": "30",
            "use_tophat": "false",
            "use_blackhat": "false",
        },
    )
    assert r.status_code == 200
    j = r.json()
    assert j["ok"] is True
    assert j["meta"]["roi"]
    assert j.get("roi_preview_png_b64")


def test_metrics_none_without_gt(tmp_path):
    data = _synthetic_blob_png()
    req = ProcessRequest(stage="full", min_component_area=10, max_side=256, **_stable_detect_params())
    out = run(data, "s.png", req, log_dir=tmp_path)
    assert out["ok"] is True
    assert out["meta"].get("metrics") is None


def test_identical_gt_dice_one(tmp_path):
    """Same PNG mask as GT as prediction → Dice 1."""
    data = _synthetic_blob_png()
    req = ProcessRequest(
        stage="full",
        segment_method="otsu_roi",
        min_component_area=10,
        max_side=256,
        **_stable_detect_params(),
    )
    out1 = run(data, "s.png", req, log_dir=tmp_path)
    assert out1["ok"] is True
    mask_png = base64.b64decode(out1["mask_png_b64"])
    out2 = run(data, "s.png", req, gt_bytes=mask_png, log_dir=tmp_path)
    assert out2["ok"] is True
    d = out2["meta"]["metrics"]
    assert d.get("dice") == 1.0
    assert d.get("iou") == 1.0


def test_corrupt_gt_mask_still_ok(tmp_path):
    data = _synthetic_blob_png()
    req = ProcessRequest(stage="full", min_component_area=10, max_side=256, **_stable_detect_params())
    out = run(data, "s.png", req, gt_bytes=b"notpng", log_dir=tmp_path)
    assert out["ok"] is True
    assert "error" in (out["meta"].get("metrics") or {})


def test_watershed_meta_warnings_list(tmp_path):
    data = _synthetic_blob_png()
    req = ProcessRequest(
        stage="full",
        segment_method="watershed",
        watershed_fg_erosion_iters=50,
        min_component_area=10,
        max_side=256,
        **_stable_detect_params(),
    )
    out = run(data, "s.png", req, log_dir=tmp_path)
    assert out["ok"] is True
    w = out["meta"].get("warnings")
    assert isinstance(w, list)


def test_dermoscopy_mode_runs(tmp_path):
    data = _synthetic_blob_png()
    req = ProcessRequest(stage="full", mode="dermoscopy", min_component_area=10, max_side=256)
    out = run(data, "s.png", req, log_dir=tmp_path)
    assert out["ok"] in (True, False)

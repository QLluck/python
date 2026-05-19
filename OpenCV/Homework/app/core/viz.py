"""Overlays, ROI rectangle, contour drawing; RGB PNG base64."""

from __future__ import annotations

import base64
from typing import Tuple

import cv2
import numpy as np


def draw_roi(bgr: np.ndarray, roi: Tuple[int, int, int, int], color=(0, 255, 0)) -> np.ndarray:
    out = bgr.copy()
    x, y, w, h = roi
    cv2.rectangle(out, (x, y), (x + w, y + h), color, 2)
    return out


def overlay_mask(bgr: np.ndarray, mask_full: np.ndarray, color_bgr=(0, 0, 255), alpha: float = 0.45) -> np.ndarray:
    """mask_full same HxW as bgr, uint8 0/255."""
    base = bgr.astype(np.float32)
    layer = np.zeros_like(base)
    m = mask_full > 127
    layer[m] = np.array(color_bgr, dtype=np.float32)
    out = base.copy()
    out[m] = (1 - alpha) * base[m] + alpha * layer[m]
    return np.clip(out, 0, 255).astype(np.uint8)


def draw_contours(bgr: np.ndarray, mask_full: np.ndarray, color_bgr=(0, 255, 255)) -> np.ndarray:
    out = bgr.copy()
    contours, _ = cv2.findContours((mask_full > 127).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(out, contours, -1, color_bgr, 2)
    return out


def bgr_to_png_rgb_b64(bgr: np.ndarray) -> str:
    # imencode handles BGR→RGB internally for PNG output
    ok, buf = cv2.imencode(".png", bgr)
    if not ok:
        raise RuntimeError("PNG encode failed.")
    return base64.b64encode(buf.tobytes()).decode("ascii")

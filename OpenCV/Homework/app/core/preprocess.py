"""Preprocessing: grayscale path, filters, CLAHE, morphology."""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np

from app.core.exceptions import ValidationError


@dataclass
class PreprocessParams:
    median_ksize: int = 5
    use_bilateral: bool = False
    bilateral_d: int = 5
    bilateral_sigma_color: float = 50.0
    bilateral_sigma_space: float = 50.0
    clahe_clip: float = 2.0
    clahe_tile: int = 8
    use_tophat: bool = True
    tophat_kernel: int = 15
    use_blackhat: bool = False
    blackhat_kernel: int = 15


def ensure_odd_ksize(name: str, k: int) -> int:
    if k < 1:
        raise ValidationError(f"{name} must be >= 1.", details={"parameter": name, "value": k})
    if k % 2 == 0:
        raise ValidationError(f"{name} must be odd (got {k}).", details={"parameter": name, "value": k})
    return k


def to_gray(bgr: np.ndarray) -> np.ndarray:
    if bgr.ndim == 2:
        return bgr.astype(np.uint8, copy=False)
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)


def preprocess_gray(bgr: np.ndarray, p: PreprocessParams) -> np.ndarray:
    g = to_gray(bgr)

    # Save original gray for blackhat if needed (avoid redundant conversion)
    gray_original = g.copy() if p.use_blackhat else None

    # Optimize median blur for large images
    h, w = g.shape
    img_size = h * w
    mk = ensure_odd_ksize("median_ksize", p.median_ksize)

    # Use smaller kernel for large images to improve performance
    if img_size > 1000000:  # > 1MP
        mk = min(mk, 3)

    g = cv2.medianBlur(g, mk)

    if p.use_bilateral:
        g = cv2.bilateralFilter(
            g,
            p.bilateral_d,
            p.bilateral_sigma_color,
            p.bilateral_sigma_space,
        )

    tile = max(2, int(p.clahe_tile))
    clahe = cv2.createCLAHE(clipLimit=float(p.clahe_clip), tileGridSize=(tile, tile))
    g = clahe.apply(g)

    if p.use_tophat:
        tk = max(3, int(p.tophat_kernel))
        if tk % 2 == 0:
            tk += 1
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (tk, tk))
        g = cv2.morphologyEx(g, cv2.MORPH_TOPHAT, k)

    if p.use_blackhat:
        bk = max(3, int(p.blackhat_kernel))
        if bk % 2 == 0:
            bk += 1
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (bk, bk))
        # Use saved original instead of re-converting
        g = cv2.add(g, cv2.morphologyEx(gray_original, cv2.MORPH_BLACKHAT, k))

    return np.clip(g, 0, 255).astype(np.uint8)

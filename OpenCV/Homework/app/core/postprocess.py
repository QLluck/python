"""Hole filling and small component removal."""

from __future__ import annotations

import cv2
import numpy as np
from scipy import ndimage


def fill_holes(binary: np.ndarray) -> np.ndarray:
    """binary: uint8 0/255 foreground=255."""
    m = binary > 127
    filled = ndimage.binary_fill_holes(m)
    return filled.astype(np.uint8) * 255


def remove_small_components(binary: np.ndarray, min_area: int) -> np.ndarray:
    bw = (binary > 127).astype(np.uint8) * 255
    num, labels, stats, _ = cv2.connectedComponentsWithStats(bw, connectivity=8)
    out = np.zeros_like(bw)
    for i in range(1, num):
        if int(stats[i, cv2.CC_STAT_AREA]) >= min_area:
            out[labels == i] = 255
    return out


def postprocess_mask(mask_roi: np.ndarray, min_post_area: int) -> np.ndarray:
    m = fill_holes(mask_roi)
    m = remove_small_components(m, min_post_area)
    return m

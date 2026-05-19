"""Dice / IoU when optional ground-truth mask is provided."""

from __future__ import annotations

from typing import Tuple

import cv2
import numpy as np


def decode_mask_bytes(data: bytes) -> np.ndarray:
    arr = np.frombuffer(data, dtype=np.uint8)
    m = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
    if m is None:
        raise ValueError("GT mask decode failed.")
    return (m > 127).astype(np.float32)


def resize_mask_to(pred_shape_hw: Tuple[int, int], gt: np.ndarray) -> np.ndarray:
    h, w = pred_shape_hw
    if gt.shape[0] == h and gt.shape[1] == w:
        return gt
    resized = cv2.resize(gt, (w, h), interpolation=cv2.INTER_NEAREST)
    return (resized > 0.5).astype(np.float32)


def dice_iou(pred: np.ndarray, gt: np.ndarray) -> Tuple[float, float]:
    p = (pred > 127).astype(np.float32).ravel()
    g = gt.ravel()
    inter = float(np.sum(p * g))
    s = float(np.sum(p) + np.sum(g))
    dice = (2.0 * inter / s) if s > 0 else 1.0
    union = float(np.sum(np.maximum(p, g)))
    iou = (inter / union) if union > 0 else 1.0
    return dice, iou

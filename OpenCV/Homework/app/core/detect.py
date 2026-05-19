"""ROI detection: threshold, morphology, connected components."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple

import cv2
import numpy as np

Mode = Literal["gray_medical", "dermoscopy"]


@dataclass
class DetectParams:
    mode: Mode = "gray_medical"
    detect_threshold: str = "otsu"
    adaptive_block_size: int = 35
    adaptive_c: int = 2
    min_component_area: int = 100
    max_component_area_ratio: float = 0.95
    roi_margin_ratio: float = 0.1
    color_fusion: str = "and"


def _binary_from_gray(enhanced_gray: np.ndarray, detect_threshold: str, abs_block: int, abs_c: int) -> np.ndarray:
    if detect_threshold == "otsu":
        _, bw = cv2.threshold(enhanced_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        return bw
    if detect_threshold == "adaptive":
        bs = abs_block if abs_block % 2 == 1 else abs_block + 1
        bs = max(3, bs)
        return cv2.adaptiveThreshold(
            enhanced_gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            bs,
            abs_c,
        )
    raise ValueError(f"Unknown detect_threshold: {detect_threshold}")


def _lab_lesion_hint(bgr: np.ndarray) -> np.ndarray:
    """Heuristic: low L* and high a* (reddish) regions — binary hint."""
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
    L, a, _ = cv2.split(lab)
    L_inv = cv2.bitwise_not(L)
    _, t1 = cv2.threshold(L_inv, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    _, t2 = cv2.threshold(a, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return cv2.bitwise_and(t1, t2)


def detect_roi(
    bgr: np.ndarray,
    enhanced_gray: np.ndarray,
    p: DetectParams,
) -> Tuple[Tuple[int, int, int, int], np.ndarray, str]:
    """
    Returns (x, y, w, h) on full image coords, binary mask used for detection (uint8 0/255), debug note.
    """
    h, w = enhanced_gray.shape[:2]
    img_area = float(h * w)
    max_area = int(p.max_component_area_ratio * img_area)

    gray_bin = _binary_from_gray(enhanced_gray, p.detect_threshold, p.adaptive_block_size, p.adaptive_c)

    if p.mode == "dermoscopy":
        color_bin = _lab_lesion_hint(bgr)
        fusion = p.color_fusion.lower()
        if fusion == "and":
            bw = cv2.bitwise_and(gray_bin, color_bin)
        elif fusion == "or":
            bw = cv2.bitwise_or(gray_bin, color_bin)
        else:
            raise ValueError("color_fusion must be 'and' or 'or'.")
    else:
        bw = gray_bin

    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    bw = cv2.morphologyEx(bw, cv2.MORPH_OPEN, k, iterations=1)
    bw = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, k, iterations=2)

    num, labels, stats, _ = cv2.connectedComponentsWithStats((bw > 0).astype(np.uint8), connectivity=8)

    # Collect candidate information for debugging
    candidates_info = []
    best_idx = -1
    best_area = 0

    for i in range(1, num):
        area = int(stats[i, cv2.CC_STAT_AREA])
        is_too_small = area < p.min_component_area
        is_too_large = area > max_area

        candidates_info.append(
            {
                "id": i,
                "area": area,
                "filtered": is_too_small or is_too_large,
                "reason": "too_small" if is_too_small else "too_large" if is_too_large else "ok",
            }
        )

        if not (is_too_small or is_too_large) and area > best_area:
            best_area = area
            best_idx = i

    if best_idx < 0:
        total_components = num - 1
        filtered_small = sum(1 for c in candidates_info if c["reason"] == "too_small")
        filtered_large = sum(1 for c in candidates_info if c["reason"] == "too_large")

        all_areas = [c["area"] for c in candidates_info]
        largest_filtered = max(all_areas) if all_areas else 0

        warning_msg = (
            f"No lesion candidate found. "
            f"Detected {total_components} component(s), but all were filtered out. "
            f"Filtered (too small < {p.min_component_area}px): {filtered_small}, "
            f"Filtered (too large > {max_area}px): {filtered_large}. "
        )

        if filtered_small > 0 and largest_filtered > 0:
            warning_msg += (
                f"Largest component found: {largest_filtered}px. "
                f"Suggestion: Try lowering min_component_area to {max(10, largest_filtered - 20)} "
                f"or adjust preprocessing parameters."
            )
        else:
            warning_msg += "Suggestion: Try adjusting preprocessing parameters or using a different threshold method."

        warning_msg += " Falling back to full image as ROI."

        # Fallback: use full image as ROI
        return (0, 0, w, h), bw, warning_msg

    x = int(stats[best_idx, cv2.CC_STAT_LEFT])
    y = int(stats[best_idx, cv2.CC_STAT_TOP])
    rw = int(stats[best_idx, cv2.CC_STAT_WIDTH])
    rh = int(stats[best_idx, cv2.CC_STAT_HEIGHT])

    m = float(p.roi_margin_ratio)
    dx = int(round(rw * m))
    dy = int(round(rh * m))
    x0 = max(0, x - dx)
    y0 = max(0, y - dy)
    x1 = min(w, x + rw + dx)
    y1 = min(h, y + rh + dy)
    roi = (x0, y0, x1 - x0, y1 - y0)
    return roi, bw, "largest_component"

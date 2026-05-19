"""Segmentation inside ROI: Otsu/Triangle, region growing, watershed."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Literal, Optional, Tuple

import cv2
import numpy as np

from app.core.exceptions import ValidationError

SegmentMethod = Literal["otsu_roi", "region_grow", "watershed"]


@dataclass
class SegmentParams:
    method: SegmentMethod = "otsu_roi"
    threshold_kind: str = "otsu"  # otsu | triangle
    morph_kernel: int = 3
    grow_T: int = 15
    grow_G: float = 0.0
    use_gradient_gate: bool = False
    seed_strategy: str = "dark"  # dark | bright | dt_peak
    watershed_fg_erosion_iters: int = 2
    watershed_bg_dilation_iters: int = 3


def _morph_kernel(k: int) -> np.ndarray:
    kk = max(3, int(k))
    if kk % 2 == 0:
        kk += 1
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kk, kk))


def segment_otsu_triangle(gray_roi: np.ndarray, p: SegmentParams) -> np.ndarray:
    flag = cv2.THRESH_BINARY_INV + (cv2.THRESH_OTSU if p.threshold_kind == "otsu" else cv2.THRESH_TRIANGLE)
    if p.threshold_kind not in ("otsu", "triangle"):
        raise ValidationError(
            "threshold_kind must be otsu or triangle.",
            details={"threshold_kind": p.threshold_kind, "allowed": ["otsu", "triangle"]},
        )
    _, bw = cv2.threshold(gray_roi, 0, 255, flag)
    k = _morph_kernel(p.morph_kernel)
    bw = cv2.morphologyEx(bw, cv2.MORPH_OPEN, k, iterations=1)
    bw = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, k, iterations=1)
    return bw


def _sobel_mag(gray_roi: np.ndarray) -> np.ndarray:
    gx = cv2.Sobel(gray_roi, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray_roi, cv2.CV_32F, 0, 1, ksize=3)
    return cv2.magnitude(gx, gy)


def _pick_seed(gray_roi: np.ndarray, seed_strategy: str) -> Tuple[int, int]:
    h, w = gray_roi.shape
    if seed_strategy == "dark":
        idx = int(np.argmin(gray_roi))
        y, x = divmod(idx, w)
        return x, y
    if seed_strategy == "bright":
        idx = int(np.argmax(gray_roi))
        y, x = divmod(idx, w)
        return x, y
    if seed_strategy == "dt_peak":
        _, bw = cv2.threshold(gray_roi, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        dt = cv2.distanceTransform((bw > 0).astype(np.uint8), cv2.DIST_L2, 5)
        if dt.max() <= 0:
            return w // 2, h // 2
        idx = int(np.argmax(dt))
        y, x = divmod(idx, w)
        return x, y
    raise ValidationError(
        "seed_strategy must be dark, bright, or dt_peak.",
        details={"seed_strategy": seed_strategy, "allowed": ["dark", "bright", "dt_peak"]},
    )


def segment_region_grow(
    gray_roi: np.ndarray, 
    p: SegmentParams,
    manual_seed: Optional[Tuple[int, int]] = None
) -> np.ndarray:
    """
    Region growing segmentation with edge-aware boundary detection.
    Optimized with smart ROI cropping, downsampling, and floodFill.
    
    Args:
        gray_roi: Grayscale ROI image
        p: Segmentation parameters
        manual_seed: Optional (x, y) seed point. If provided, overrides seed_strategy.
    
    Returns:
        Binary segmentation mask
    """
    h, w = gray_roi.shape
    
    # Use manual seed if provided, otherwise use strategy
    if manual_seed is not None:
        sx, sy = manual_seed
        # Validate seed is within bounds
        if sx < 0 or sx >= w or sy < 0 or sy >= h:
            raise ValidationError(
                "Manual seed point is out of bounds.",
                details={"seed": (sx, sy), "image_size": (w, h)},
            )
    else:
        sx, sy = _pick_seed(gray_roi, p.seed_strategy)
    
    seed_v = float(gray_roi[sy, sx])
    T = float(p.grow_T)
    
    # ============================================================
    # 优化方案 C：智能 ROI + 降采样 + floodFill
    # ============================================================
    
    # 1. 智能 ROI 裁剪：只处理种子点周围的区域
    # 对于大图像，限制处理区域可以大幅提速
    max_roi_size = 1200  # 增大到 1200（从 800）
    
    if h > max_roi_size or w > max_roi_size:
        # 计算裁剪区域（以种子点为中心）
        half_size = max_roi_size // 2
        crop_x1 = max(0, sx - half_size)
        crop_y1 = max(0, sy - half_size)
        crop_x2 = min(w, sx + half_size)
        crop_y2 = min(h, sy + half_size)
        
        # 裁剪图像
        cropped = gray_roi[crop_y1:crop_y2, crop_x1:crop_x2]
        # 调整种子点坐标
        seed_x_crop = sx - crop_x1
        seed_y_crop = sy - crop_y1
        
        # 在裁剪区域上进行分割
        mask_crop = _region_grow_optimized(cropped, seed_x_crop, seed_y_crop, seed_v, T, p)
        
        # 将结果放回完整尺寸
        mask = np.zeros((h, w), np.uint8)
        mask[crop_y1:crop_y2, crop_x1:crop_x2] = mask_crop
        
        return mask
    else:
        # 图像不大，直接处理
        return _region_grow_optimized(gray_roi, sx, sy, seed_v, T, p)


def _region_grow_optimized(
    gray: np.ndarray,
    sx: int,
    sy: int,
    seed_v: float,
    T: float,
    p: SegmentParams
) -> np.ndarray:
    """
    优化的区域生长实现，使用 floodFill 和可选的降采样。
    
    Args:
        gray: 灰度图像
        sx, sy: 种子点坐标
        seed_v: 种子点像素值
        T: 生长阈值
        p: 分割参数
    
    Returns:
        二值分割掩码
    """
    h, w = gray.shape
    
    # 2. 降采样：对于中等大小的图像，降采样可以加速
    downsample_factor = 1
    if h * w > 500000:  # 0.5M 像素以上降采样 2x
        downsample_factor = 2
    elif h * w > 200000:  # 0.2M 像素以上降采样 1.5x
        downsample_factor = 1.5
    
    if downsample_factor > 1:
        # 降采样图像
        new_h = int(h / downsample_factor)
        new_w = int(w / downsample_factor)
        gray_small = cv2.resize(gray, (new_w, new_h), interpolation=cv2.INTER_AREA)
        
        # 调整种子点坐标
        sx_small = int(sx / downsample_factor)
        sy_small = int(sy / downsample_factor)
        
        # 确保种子点在范围内
        sx_small = max(0, min(new_w - 1, sx_small))
        sy_small = max(0, min(new_h - 1, sy_small))
        
        # 在小图上进行分割
        mask_small = _floodfill_segment(gray_small, sx_small, sy_small, T)
        
        # 上采样回原尺寸
        mask = cv2.resize(mask_small, (w, h), interpolation=cv2.INTER_NEAREST)
        
        return mask
    else:
        # 不需要降采样，直接使用 floodFill
        return _floodfill_segment(gray, sx, sy, T)


def _floodfill_segment(
    gray: np.ndarray,
    sx: int,
    sy: int,
    T: float
) -> np.ndarray:
    """
    使用 floodFill 进行快速区域生长，并使用 GrabCut 优化边界。
    
    策略：
    1. 使用 FIXED_RANGE 模式的 floodFill 快速初始分割
    2. 使用 GrabCut 优化边界（可选）
    3. 形态学操作平滑结果
    
    Args:
        gray: 灰度图像
        sx, sy: 种子点坐标
        T: 生长阈值
    
    Returns:
        二值分割掩码
    """
    h, w = gray.shape
    
    # ============================================================
    # 步骤 1: FIXED_RANGE 模式的 floodFill
    # ============================================================
    
    # 创建掩码（floodFill 需要比图像大 2 像素的掩码）
    mask = np.zeros((h + 2, w + 2), np.uint8)
    
    # 使用 8-连通 + FIXED_RANGE 模式
    flags = 8  # 8-connectivity
    flags |= cv2.FLOODFILL_FIXED_RANGE  # 固定范围模式
    flags |= (255 << 8)  # 填充值为 255
    
    # 阈值：定义与种子点的容差范围
    lo_diff = (T,)
    up_diff = (T,)
    
    # 执行 floodFill
    cv2.floodFill(
        gray.copy(),
        mask,
        (sx, sy),
        255,
        lo_diff,
        up_diff,
        flags
    )
    
    # 提取结果（去掉边界）
    result = mask[1:-1, 1:-1].copy()
    
    # ============================================================
    # 步骤 2: 形态学操作平滑边界
    # ============================================================
    
    pixel_count = np.sum(result > 0)
    
    if pixel_count > 100:  # 至少 100 个像素
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        
        # 闭运算：填充小孔洞
        result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel, iterations=1)
        
        # 开运算：去除小噪声
        result = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel, iterations=1)
        
        # ============================================================
        # 步骤 3: GrabCut 边界优化（可选，仅对中等大小的结果）
        # ============================================================
        
        # 只对合理大小的分割结果使用 GrabCut
        percentage = pixel_count / (h * w)
        
        if 0.01 < percentage < 0.5 and h * w < 1000000:  # 1-50% 且图像不太大
            try:
                # 创建 GrabCut 掩码
                # 0: 明确背景, 1: 明确前景, 2: 可能背景, 3: 可能前景
                gc_mask = np.where(result > 0, cv2.GC_FGD, cv2.GC_BGD).astype(np.uint8)
                
                # 膨胀前景区域作为"明确前景"
                kernel_large = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
                sure_fg = cv2.erode(result, kernel_large, iterations=1)
                gc_mask[sure_fg > 0] = cv2.GC_FGD
                
                # 膨胀背景区域作为"明确背景"
                sure_bg = cv2.dilate(255 - result, kernel_large, iterations=2)
                gc_mask[sure_bg > 0] = cv2.GC_BGD
                
                # 中间区域作为"可能前景"
                gc_mask[(result > 0) & (sure_fg == 0)] = cv2.GC_PR_FGD
                
                # 转换为 BGR（GrabCut 需要）
                if len(gray.shape) == 2:
                    bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
                else:
                    bgr = gray
                
                # 运行 GrabCut（只迭代 1 次，快速优化）
                bgd_model = np.zeros((1, 65), np.float64)
                fgd_model = np.zeros((1, 65), np.float64)
                
                cv2.grabCut(bgr, gc_mask, None, bgd_model, fgd_model, 1, cv2.GC_INIT_WITH_MASK)
                
                # 提取前景
                result = np.where((gc_mask == cv2.GC_FGD) | (gc_mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
                
            except Exception:
                # GrabCut 失败，使用原始结果
                pass
    
    return result


def segment_watershed(
    gray_roi: np.ndarray,
    p: SegmentParams,
) -> Tuple[np.ndarray, List[str]]:
    """Classic markers workflow: Otsu opening → distance peaks as FG, dilated opening as BG."""
    warnings: List[str] = []
    k = _morph_kernel(p.morph_kernel)
    _, bin_inv = cv2.threshold(gray_roi, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    opening = cv2.morphologyEx(bin_inv, cv2.MORPH_OPEN, k, iterations=1)
    sure_bg = cv2.dilate(opening, k, iterations=max(1, p.watershed_bg_dilation_iters))

    dist = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    dmax = float(dist.max())
    if dmax <= 0:
        warnings.append("watershed: empty distance map; falling back to Otsu in ROI.")
        sp = SegmentParams(method="otsu_roi", threshold_kind="otsu", morph_kernel=p.morph_kernel)
        return segment_otsu_triangle(gray_roi, sp), warnings

    _, sure_fg = cv2.threshold(dist, 0.35 * dmax, 255, cv2.THRESH_BINARY)
    sure_fg = np.asarray(sure_fg, dtype=np.uint8)
    sure_fg = cv2.erode(sure_fg, k, iterations=max(1, p.watershed_fg_erosion_iters))

    if cv2.countNonZero(sure_fg) == 0:
        warnings.append("watershed: empty sure foreground; falling back to Otsu in ROI.")
        sp = SegmentParams(method="otsu_roi", threshold_kind="otsu", morph_kernel=p.morph_kernel)
        return segment_otsu_triangle(gray_roi, sp), warnings

    unknown = cv2.subtract(sure_bg, sure_fg)
    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers.astype(np.int32) + 1
    markers[unknown == 255] = 0

    color_roi = cv2.cvtColor(gray_roi, cv2.COLOR_GRAY2BGR)
    markers_copy = markers.copy()
    cv2.watershed(color_roi, markers_copy)
    out = np.zeros_like(gray_roi)
    out[markers_copy > 1] = 255

    if cv2.countNonZero(out) == 0:
        warnings.append("watershed: empty output; falling back to Otsu in ROI.")
        sp = SegmentParams(method="otsu_roi", threshold_kind="otsu", morph_kernel=p.morph_kernel)
        return segment_otsu_triangle(gray_roi, sp), warnings

    if np.mean(out > 0) > 0.85:
        warnings.append("watershed: unusually large foreground; check over-segmentation risk.")

    return out, warnings


def segment_roi(gray_roi: np.ndarray, p: SegmentParams) -> Tuple[np.ndarray, List[str]]:
    warnings: List[str] = []
    if p.method == "otsu_roi":
        return segment_otsu_triangle(gray_roi, p), warnings
    if p.method == "region_grow":
        return segment_region_grow(gray_roi, p), warnings
    if p.method == "watershed":
        return segment_watershed(gray_roi, p)
    if p.method == "dual":
        # Run both Otsu and region_grow, score each, pick the better one
        mask_otsu = segment_otsu_triangle(gray_roi, p)
        mask_rg = segment_region_grow(gray_roi, p)

        score_otsu = score_segmentation(mask_otsu, gray_roi)
        score_rg = score_segmentation(mask_rg, gray_roi)

        if score_otsu >= score_rg:
            if score_otsu < 0 and score_rg >= 0:
                return mask_rg, warnings
            return mask_otsu, warnings
        else:
            if score_rg < 0 and score_otsu >= 0:
                return mask_otsu, warnings
            return mask_rg, warnings
    raise ValidationError(
        f"Unknown segment method: {p.method}",
        details={"method": p.method, "allowed": ["otsu_roi", "region_grow", "watershed", "dual"]},
    )


def analyze_color_variance(
    bgr: np.ndarray,
    click_x: int,
    click_y: int,
    patch_size: int = 120,
) -> Tuple[str, float]:
    """
    Analyze color variance around click point to decide color space.

    Returns ("lab", ratio) if color is informative, ("grayscale", ratio) otherwise.
    """
    h, w = bgr.shape[:2]
    half = patch_size // 2
    y1 = max(0, click_y - half)
    y2 = min(h, click_y + half)
    x1 = max(0, click_x - half)
    x2 = min(w, click_x + half)

    patch = bgr[y1:y2, x1:x2]
    lab_patch = cv2.cvtColor(patch, cv2.COLOR_BGR2Lab)

    std_L = float(np.std(lab_patch[:, :, 0]))
    std_a = float(np.std(lab_patch[:, :, 1]))
    std_b = float(np.std(lab_patch[:, :, 2]))

    color_ratio = (std_a + std_b) / (std_L + 1.0)

    mode = "lab" if color_ratio > 0.3 else "grayscale"
    return mode, color_ratio


def _morphological_refine(mask: np.ndarray) -> np.ndarray:
    """Enhanced morphological post-processing with hole filling."""
    if np.sum(mask > 0) < 10:
        return mask

    k_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    k_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    result = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k_close, iterations=1)
    result = cv2.morphologyEx(result, cv2.MORPH_OPEN, k_open, iterations=1)

    # Contour-based hole filling for enclosed regions < 500px
    contours, hierarchy = cv2.findContours(
        result, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
    )
    if hierarchy is not None:
        for i, (_, _, _, parent) in enumerate(hierarchy[0]):
            if parent >= 0:
                hole_area = cv2.contourArea(contours[i])
                if 0 < hole_area < 500:
                    cv2.drawContours(result, contours, i, 255, cv2.FILLED)

    return result


def segment_region_grow_color(
    bgr: np.ndarray,
    click_x: int,
    click_y: int,
    grow_T: float,
    chroma_factor: float = 0.6,
) -> np.ndarray:
    """
    Color-aware region growing using Lab-space multi-channel floodFill.

    Args:
        bgr: BGR color image
        click_x, click_y: Seed point coordinates
        grow_T: Luminance channel threshold
        chroma_factor: Multiplier for a/b channel thresholds (default 0.6)

    Returns:
        Binary segmentation mask (uint8, 0 or 255)
    """
    h, w = bgr.shape[:2]

    if click_x < 0 or click_x >= w or click_y < 0 or click_y >= h:
        raise ValidationError(
            "Seed point out of bounds.",
            details={"seed": (click_x, click_y), "image_size": (w, h)},
        )

    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2Lab)

    # Smart ROI cropping for large images
    max_roi = 1200
    if h > max_roi or w > max_roi:
        half = max_roi // 2
        cx1 = max(0, click_x - half)
        cy1 = max(0, click_y - half)
        cx2 = min(w, click_x + half)
        cy2 = min(h, click_y + half)
        lab_roi = lab[cy1:cy2, cx1:cx2]
        sx = click_x - cx1
        sy = click_y - cy1
    else:
        lab_roi = lab
        sx, sy = click_x, click_y
        cx1, cy1 = 0, 0

    rh, rw = lab_roi.shape[:2]

    # A: Bilateral filter on L channel (edge-preserving smoothing)
    L_ch, a_ch, b_ch = cv2.split(lab_roi)
    L_ch = cv2.bilateralFilter(L_ch, 5, 30, 30)
    lab_roi = cv2.merge([L_ch, a_ch, b_ch])

    # Downsample for large regions
    ds = 1
    if rh * rw > 500000:
        ds = 2
        lab_small = cv2.resize(lab_roi, (rw // ds, rh // ds), interpolation=cv2.INTER_AREA)
        sx_s, sy_s = sx // ds, sy // ds
        sx_s = max(0, min(lab_small.shape[1] - 1, sx_s))
        sy_s = max(0, min(lab_small.shape[0] - 1, sy_s))
    else:
        lab_small = lab_roi
        sx_s, sy_s = sx, sy

    sh, sw = lab_small.shape[:2]

    # B: Adaptive thresholds from local patch statistics around seed point
    patch_half = 10
    py1 = max(0, sy_s - patch_half)
    py2 = min(sh, sy_s + patch_half)
    px1 = max(0, sx_s - patch_half)
    px2 = min(sw, sx_s + patch_half)
    patch = lab_small[py1:py2, px1:px2]
    sigma_L = float(np.std(patch[:, :, 0]))
    sigma_a = float(np.std(patch[:, :, 1]))
    sigma_b = float(np.std(patch[:, :, 2]))

    L_T = int(round(np.clip(grow_T * 0.5 + 0.6 * sigma_L, 8, 50)))
    a_T = int(round(np.clip(grow_T * 0.3 + 0.5 * sigma_a, 4, 40)))
    b_T = int(round(np.clip(grow_T * 0.3 + 0.5 * sigma_b, 4, 40)))

    lo_diff = (L_T, a_T, b_T)
    up_diff = (L_T, a_T, b_T)

    flood_mask = np.zeros((sh + 2, sw + 2), np.uint8)
    flags = 8 | cv2.FLOODFILL_FIXED_RANGE | (255 << 8)

    cv2.floodFill(lab_small.copy(), flood_mask, (sx_s, sy_s), (255, 255, 255), lo_diff, up_diff, flags)

    mask_small = flood_mask[1:-1, 1:-1].copy()

    # Overflow guard: if > 40% filled, retry with halved thresholds
    fill_ratio = np.sum(mask_small > 0) / mask_small.size
    if fill_ratio > 0.4:
        L_T2 = max(5, L_T // 2)
        a_T2 = max(3, a_T // 2)
        b_T2 = max(3, b_T // 2)
        flood_mask2 = np.zeros((sh + 2, sw + 2), np.uint8)
        cv2.floodFill(
            lab_small.copy(), flood_mask2, (sx_s, sy_s), (255, 255, 255),
            (L_T2, a_T2, b_T2), (L_T2, a_T2, b_T2), flags
        )
        mask_small2 = flood_mask2[1:-1, 1:-1].copy()
        if np.sum(mask_small2 > 0) > 10:
            mask_small = mask_small2

    # Upsample if downsampled
    if ds > 1:
        mask_roi = cv2.resize(mask_small, (rw, rh), interpolation=cv2.INTER_NEAREST)
    else:
        mask_roi = mask_small

    # Enhanced morphological refinement
    mask_roi = _morphological_refine(mask_roi)

    # Place back into full-size mask
    if h > max_roi or w > max_roi:
        mask = np.zeros((h, w), np.uint8)
        mask[cy1:cy1 + rh, cx1:cx1 + rw] = mask_roi
    else:
        mask = mask_roi

    return mask


def score_segmentation(mask: np.ndarray, gray: np.ndarray) -> float:
    """
    Score segmentation quality without ground truth.

    Uses three heuristics:
    1. Area reasonableness: lesion shouldn't be too small (<1%) or too large (>60%)
    2. Compactness: 4π·area/perimeter², closer to 1 = more circular
    3. Edge alignment: boundary should align with image gradients

    Returns score in [0, 1], higher is better. Returns -1 for invalid masks.
    """
    area = float(np.sum(mask > 0))
    total = float(mask.size)
    ratio = area / total

    if ratio < 0.005 or ratio > 0.60:
        return -1.0

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return -1.0

    largest = max(contours, key=cv2.contourArea)
    perimeter = cv2.arcLength(largest, closed=True)
    contour_area = cv2.contourArea(largest)
    if perimeter < 1 or contour_area < 10:
        return -1.0

    # Compactness: 4π * area / perimeter²  (circle = 1.0)
    compactness = (4.0 * np.pi * contour_area) / (perimeter * perimeter)
    compactness = min(1.0, compactness)

    # Edge alignment: mean gradient magnitude along boundary
    dilated = cv2.dilate(mask, np.ones((3, 3), np.uint8))
    boundary = dilated.astype(np.int32) - mask.astype(np.int32)
    boundary = np.clip(boundary, 0, 255).astype(np.uint8)

    gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    grad_mag = np.sqrt(gx ** 2 + gy ** 2)

    boundary_pixels = np.sum(boundary > 0)
    if boundary_pixels > 0:
        edge_score = float(np.sum(grad_mag[boundary > 0]) / boundary_pixels)
        edge_score = min(1.0, edge_score / 30.0)  # normalize
    else:
        edge_score = 0.0

    # Area bonus: prefer mid-range coverage (10%~35%)
    if 0.10 <= ratio <= 0.35:
        area_bonus = 0.2
    else:
        area_bonus = 0.0

    score = compactness * 0.4 + edge_score * 0.4 + area_bonus
    return float(np.clip(score, 0.0, 1.0))

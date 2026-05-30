"""参数扫描脚本：系统测试所有可调参数，试图超过 raw+Triangle 的 0.7856 基准"""
from __future__ import annotations

import sys
from pathlib import Path
import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.core.preprocess import PreprocessParams, preprocess_gray
from app.core.postprocess import postprocess_mask
from app.core.segment import SegmentParams, segment_roi, segment_otsu_triangle

DATA_DIR = Path(__file__).resolve().parent / "data"
IMAGE_DIR = DATA_DIR / "image"
MASK_DIR = DATA_DIR / "mask"
image_paths = sorted(IMAGE_DIR.glob("*.jpg"))
N = len(image_paths)


def find_mask(img_path: Path) -> Path | None:
    mp = MASK_DIR / f"{img_path.stem}_segmentation.png"
    return mp if mp.exists() else None


def dice(pred, gt):
    pb = (pred > 127).astype(np.uint8)
    gb = (gt > 127).astype(np.uint8)
    inter = float(np.sum(pb & gb))
    total = float(np.sum(pb) + np.sum(gb))
    return 2 * inter / total if total > 0 else 0.0


BASELINE = 0.7856  # raw + Triangle, morph=3, 无后处理

# ═══════════════════════════════════════════
# 扫描 1: morph_kernel 大小
# ═══════════════════════════════════════════
print("=" * 65)
print("扫描 1: morph_kernel (raw + Triangle + 后处理)")
print("-" * 65)
for mk in [3, 5, 7, 9, 11]:
    vals = []
    for img_path in image_paths:
        img = cv2.imread(str(img_path))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gt = cv2.imread(str(find_mask(img_path)), cv2.IMREAD_GRAYSCALE)
        sp = SegmentParams(method="otsu_roi", threshold_kind="triangle", morph_kernel=mk)
        mask = segment_otsu_triangle(gray, sp)
        mask = postprocess_mask(mask, 30)
        vals.append(dice(mask, gt))
    print(f"  morph_kernel={mk:2d}:  avg Dice = {np.mean(vals):.4f}  ({np.mean(vals)-BASELINE:+.4f} vs baseline)")

# ═══════════════════════════════════════════
# 扫描 2: CLAHE clip + Triangle (不是 dual!)
# ═══════════════════════════════════════════
print("\n" + "=" * 65)
print("扫描 2: CLAHE预处理 + Triangle (非dual)")
print("-" * 65)
for clip in [0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 0.7, 1.0]:
    vals = []
    for img_path in image_paths:
        img = cv2.imread(str(img_path))
        gt = cv2.imread(str(find_mask(img_path)), cv2.IMREAD_GRAYSCALE)
        pp = PreprocessParams(median_ksize=5, use_bilateral=False, clahe_clip=clip,
                              clahe_tile=8, use_tophat=False, use_blackhat=False)
        enhanced = preprocess_gray(img, pp)
        sp = SegmentParams(method="otsu_roi", threshold_kind="triangle", morph_kernel=3)
        mask = segment_otsu_triangle(enhanced, sp)
        mask = postprocess_mask(mask, 30)
        vals.append(dice(mask, gt))
    best_flag = " ← best" if clip == 0.1 else ""
    print(f"  CLAHE clip={clip:5.2f} + Triangle: avg Dice = {np.mean(vals):.4f}  ({np.mean(vals)-BASELINE:+.4f}){best_flag}")

# ═══════════════════════════════════════════
# 扫描 3: median_ksize (raw, 无CLAHE)
# ═══════════════════════════════════════════
print("\n" + "=" * 65)
print("扫描 3: median_ksize (raw灰度, 仅中值滤波 + Triangle + 后处理)")
print("-" * 65)
for mk in [1, 3, 5, 7, 9]:
    vals = []
    for img_path in image_paths:
        img = cv2.imread(str(img_path))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gt = cv2.imread(str(find_mask(img_path)), cv2.IMREAD_GRAYSCALE)
        if mk > 1:
            gray = cv2.medianBlur(gray, mk)
        sp = SegmentParams(method="otsu_roi", threshold_kind="triangle", morph_kernel=3)
        mask = segment_otsu_triangle(gray, sp)
        mask = postprocess_mask(mask, 30)
        vals.append(dice(mask, gt))
    label = "无" if mk == 1 else f"ksize={mk}"
    print(f"  median {label:>8}:  avg Dice = {np.mean(vals):.4f}  ({np.mean(vals)-BASELINE:+.4f})")

# ═══════════════════════════════════════════
# 扫描 4: min_post_area
# ═══════════════════════════════════════════
print("\n" + "=" * 65)
print("扫描 4: min_post_area (raw + Triangle + 后处理)")
print("-" * 65)
for mpa in [0, 10, 20, 30, 50, 100, 200]:
    vals = []
    for img_path in image_paths:
        img = cv2.imread(str(img_path))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gt = cv2.imread(str(find_mask(img_path)), cv2.IMREAD_GRAYSCALE)
        sp = SegmentParams(method="otsu_roi", threshold_kind="triangle", morph_kernel=3)
        mask = segment_otsu_triangle(gray, sp)
        mask = postprocess_mask(mask, mpa)
        vals.append(dice(mask, gt))
    print(f"  min_post_area={mpa:3d}:  avg Dice = {np.mean(vals):.4f}  ({np.mean(vals)-BASELINE:+.4f})")

# ═══════════════════════════════════════════
# 扫描 5: CLAHE + Triangle + 不同 median
# ═══════════════════════════════════════════
print("\n" + "=" * 65)
print("扫描 5: CLAHE + Triangle — clip × median 交叉")
print("-" * 65)
best_combo = (0, 0, 0.0)
for clip in [0.05, 0.1, 0.15, 0.2]:
    for mk in [1, 3, 5]:
        vals = []
        for img_path in image_paths:
            img = cv2.imread(str(img_path))
            gt = cv2.imread(str(find_mask(img_path)), cv2.IMREAD_GRAYSCALE)
            pp = PreprocessParams(median_ksize=mk, use_bilateral=False, clahe_clip=clip,
                                  clahe_tile=8, use_tophat=False, use_blackhat=False)
            enhanced = preprocess_gray(img, pp)
            sp = SegmentParams(method="otsu_roi", threshold_kind="triangle", morph_kernel=3)
            mask = segment_otsu_triangle(enhanced, sp)
            mask = postprocess_mask(mask, 30)
            vals.append(dice(mask, gt))
        avg = np.mean(vals)
        if avg > best_combo[2]:
            best_combo = (clip, mk, avg)
        print(f"  clip={clip:.2f} median={mk}:  avg Dice = {avg:.4f}  ({avg-BASELINE:+.4f})")
print(f"\n  最佳组合: CLAHE clip={best_combo[0]:.2f}, median={best_combo[1]}, Dice={best_combo[2]:.4f}")

# ═══════════════════════════════════════════
# 扫描 6: "聪明 dual" — raw+Triangle vs CLAHE最佳+Triangle
# ═══════════════════════════════════════════
print("\n" + "=" * 65)
print("扫描 6: 聪明 dual — 每张图自动选 raw+Tri vs CLAHE+Tri (取Dice高的)")
print("-" * 65)
from app.core.segment import score_segmentation

best_clip = best_combo[0]  # 用上面找到的最佳 CLAHE clip
best_median = best_combo[1]

for img_path in image_paths:
    img = cv2.imread(str(img_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gt = cv2.imread(str(find_mask(img_path)), cv2.IMREAD_GRAYSCALE)

    # raw + Triangle
    sp = SegmentParams(method="otsu_roi", threshold_kind="triangle", morph_kernel=3)
    mask_raw = segment_otsu_triangle(gray, sp)

    # CLAHE + Triangle
    pp = PreprocessParams(median_ksize=best_median, use_bilateral=False, clahe_clip=best_clip,
                          clahe_tile=8, use_tophat=False, use_blackhat=False)
    enhanced = preprocess_gray(img, pp)
    mask_clahe = segment_otsu_triangle(enhanced, sp)

    d_raw = dice(mask_raw, gt)
    d_clahe = dice(mask_clahe, gt)
    # 聪明选：用 score_segmentation 来选
    s_raw = score_segmentation(mask_raw, gray)
    s_clahe = score_segmentation(mask_clahe, enhanced)
    pick = "raw" if s_raw >= s_clahe else "clh"
    correct = (d_raw >= d_clahe and pick == "raw") or (d_clahe >= d_raw and pick == "clh")
    # 如果一样，选 raw (更快)
    best_d = max(d_raw, d_clahe)
    print(f"  {img_path.stem}: raw={d_raw:.4f} clahe={d_clahe:.4f}  "
          f"score选{pick} 正确={str(correct):5s}  最好={best_d:.4f}")

# 汇总
oracle_vals = []
smart_vals = []
score_correct = 0
for img_path in image_paths:
    img = cv2.imread(str(img_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gt = cv2.imread(str(find_mask(img_path)), cv2.IMREAD_GRAYSCALE)

    sp = SegmentParams(method="otsu_roi", threshold_kind="triangle", morph_kernel=3)
    mask_raw = segment_otsu_triangle(gray, sp)
    mask_raw = postprocess_mask(mask_raw, 30)

    pp = PreprocessParams(median_ksize=best_median, use_bilateral=False, clahe_clip=best_clip,
                          clahe_tile=8, use_tophat=False, use_blackhat=False)
    enhanced = preprocess_gray(img, pp)
    mask_clahe = segment_otsu_triangle(enhanced, sp)
    mask_clahe = postprocess_mask(mask_clahe, 30)

    d_raw = dice(mask_raw, gt)
    d_clahe = dice(mask_clahe, gt)

    s_raw = score_segmentation(mask_raw, gray)
    s_clahe = score_segmentation(mask_clahe, enhanced)
    if (d_raw >= d_clahe and s_raw >= s_clahe) or (d_clahe >= d_raw and s_clahe >= s_raw):
        score_correct += 1

    oracle_vals.append(max(d_raw, d_clahe))
    smart_vals.append(d_raw if s_raw >= s_clahe else d_clahe)

print(f"\n  Oracle (每次都选对的)        : avg Dice = {np.mean(oracle_vals):.4f}")
print(f"  Score-guided 选择            : avg Dice = {np.mean(smart_vals):.4f}  (正确率 {score_correct}/{N})")
print(f"  固定 raw+Triangle (baseline) : avg Dice = {BASELINE:.4f}")
print(f"  Oracle 提升空间               : {np.mean(oracle_vals)-BASELINE:+.4f}")

# ═══════════════════════════════════════════
# 总结
# ═══════════════════════════════════════════
print("\n" + "=" * 65)
print("总结")
print("-" * 65)
print(f"  baseline (raw+Triangle): {BASELINE:.4f}")
print(f"  pipeline 当前方案       : {np.mean(oracle_vals):.4f} (raw+Triangle+后处理)")
print(f"  理论最优 (Oracle)       : {np.mean(oracle_vals):.4f} (每图取 raw/clahe 高者)")
print(f"  评分引导选择            : {np.mean(smart_vals):.4f}")

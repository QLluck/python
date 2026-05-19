"""
单步调试脚本：只跑你正在改的那一个函数，快速看效果。

用法:
    python debug_step.py <图片路径> <步骤名>

步骤名:
    preprocess  - 测试预处理函数
    detect      - 测试 ROI 检测
    segment     - 测试分割函数
    mask        - 只看最终掩码
    overview    - 所有中间结果并排显示

示例:
    python debug_step.py test.jpg preprocess
    python debug_step.py test.jpg segment
    python debug_step.py test.jpg overview
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.core import decode, preprocess, detect, segment, postprocess, viz
from app.config import settings


def run_preprocess(bgr):
    """测预处理"""
    print("测试: preprocess_gray()")
    # 在这里改参数测试效果
    pp = preprocess.PreprocessParams(
        median_ksize=5,
        clahe_clip=2.0,
        clahe_tile=8,
        use_tophat=True,
        tophat_kernel=15,
    )
    result = preprocess.preprocess_gray(bgr, pp)
    print(f"  输出: shape={result.shape}, range=[{result.min()}, {result.max()}]")
    return result


def run_detect(bgr, enhanced):
    """测 ROI 检测"""
    print("测试: detect_roi()")
    dp = detect.DetectParams(
        mode="gray_medical",
        detect_threshold="otsu",
        min_component_area=50,
        max_component_area_ratio=0.95,
    )
    roi, mask, note = detect.detect_roi(bgr, enhanced, dp)
    print(f"  ROI: {roi}, note: {note}")
    # 返回 ROI 预览
    return viz.draw_roi(bgr, roi)


def run_segment(gray_roi):
    """测分割"""
    print("测试: segment_roi()")
    sp = segment.SegmentParams(
        method="dual",     # 改这里测试不同方法: otsu_roi / region_grow / watershed / dual
        threshold_kind="otsu",
        morph_kernel=3,
        grow_T=15,
        seed_strategy="dark",
    )
    mask, warnings = segment.segment_roi(gray_roi, sp)
    if warnings:
        for w in warnings:
            print(f"  Warning: {w}")
    print(f"  分割像素: {int(np.sum(mask > 0))}")
    return mask


def run_full_mask(bgr, enhanced):
    """测完整掩码生成"""
    dp = detect.DetectParams(mode="gray_medical")
    roi, _, _ = detect.detect_roi(bgr, enhanced, dp)
    x, y, rw, rh = roi
    gray_roi = enhanced[y:y+rh, x:x+rw]

    sp = segment.SegmentParams(method="dual")
    mask_roi, _ = segment.segment_roi(gray_roi, sp)
    mask_roi = postprocess.postprocess_mask(mask_roi, 50)

    full = np.zeros(enhanced.shape, dtype=np.uint8)
    full[y:y+rh, x:x+rw] = mask_roi
    return full


def show_window(title, img):
    """在 OpenCV 窗口中显示图片（按任意键关闭）"""
    if img.ndim == 2:
        display = img
    else:
        display = img
    cv2.imshow(title, display)


def main():
    parser = argparse.ArgumentParser(description="单步调试工具")
    parser.add_argument("image", help="输入图片路径")
    parser.add_argument("step", choices=["preprocess", "detect", "segment", "mask", "overview"],
                        help="要测试的步骤")
    parser.add_argument("--save", action="store_true", help="保存结果图片")
    args = parser.parse_args()

    img_path = Path(args.image)
    if not img_path.exists():
        print(f"错误: 找不到文件 '{args.image}'")
        sys.exit(1)

    # 解码
    data = img_path.read_bytes()
    dec = decode.decode_and_scale(data, img_path.name, max_side=1280)
    bgr = dec.bgr
    print(f"图片: {bgr.shape}")

    # 根据步骤运行
    if args.step == "preprocess":
        result = run_preprocess(bgr)

    elif args.step in ("detect", "segment", "mask", "overview"):
        enhanced = run_preprocess(bgr)

        if args.step == "detect":
            result = run_detect(bgr, enhanced)

        elif args.step in ("segment", "mask", "overview"):
            dp = detect.DetectParams(mode="gray_medical")
            roi, _, _ = detect.detect_roi(bgr, enhanced, dp)
            x, y, rw, rh = roi
            gray_roi = enhanced[y:y+rh, x:x+rw]
            print(f"ROI: ({x}, {y}, {rw}, {rh})")

            if args.step == "segment":
                result = run_segment(gray_roi)

            elif args.step in ("mask", "overview"):
                mask_roi = run_segment(gray_roi)
                mask_roi = postprocess.postprocess_mask(mask_roi, 50)
                full_mask = np.zeros(enhanced.shape, dtype=np.uint8)
                full_mask[y:y+rh, x:x+rw] = mask_roi

                if args.step == "mask":
                    result = full_mask
                else:
                    # overview: 显示所有中间结果
                    overlay = viz.overlay_mask(bgr, full_mask)
                    overlay = viz.draw_contours(overlay, full_mask)
                    overlay = viz.draw_roi(overlay, roi)

                    cv2.imshow("Original", bgr)
                    cv2.imshow("Enhanced Gray", enhanced)
                    cv2.imshow("ROI Gray", gray_roi)
                    cv2.imshow("Mask ROI", mask_roi)
                    cv2.imshow("Full Mask", full_mask)
                    cv2.imshow("Final Overlay", overlay)
                    print("\n显示所有中间结果，按任意键关闭窗口...")
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    return

    # 显示结果
    if result is not None:
        cv2.imshow(f"Result - {args.step}", result)

        if args.save:
            out_name = f"debug_{args.step}_{img_path.stem}.png"
            cv2.imwrite(out_name, result)
            print(f"已保存: {out_name}")

        print("按任意键关闭窗口...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

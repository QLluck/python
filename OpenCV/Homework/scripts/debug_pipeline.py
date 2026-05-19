"""
离线调试脚本：绕过 Web 服务器，直接跑图像处理流水线。
每一步中间结果保存为 PNG，方便对比调参效果。

用法:
    python debug_pipeline.py <图片路径> [--method otsu_roi|region_grow|watershed|dual]

示例:
    python debug_pipeline.py test.jpg
    python debug_pipeline.py test.jpg --method region_grow
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import cv2
import numpy as np

# 确保项目根目录在 sys.path 里
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.core import decode, preprocess, detect, segment, postprocess, viz
from app.config import settings


def save_step(img, output_dir, step_name, prefix="", is_gray=False):
    """保存中间结果图片到 output_dir/prefix_step_name.png"""
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{prefix}_{step_name}.png" if prefix else f"{step_name}.png"
    path = output_dir / filename

    if is_gray:
        cv2.imwrite(str(path), img)
    elif img.ndim == 2:
        cv2.imwrite(str(path), img)
    else:
        # BGR 保存
        cv2.imwrite(str(path), img)

    print(f"  [SAVED] {path}")


def main():
    parser = argparse.ArgumentParser(description="离线图像处理调试工具")
    parser.add_argument("image", help="输入图片路径")
    parser.add_argument("--method", default="dual",
                        choices=["otsu_roi", "region_grow", "watershed", "dual"],
                        help="分割方法 (默认 dual)")
    parser.add_argument("--mode", default="gray_medical",
                        choices=["gray_medical", "dermoscopy"],
                        help="图像模式")
    parser.add_argument("--max-side", type=int, default=1280, help="最大边长")
    parser.add_argument("--out", default=None, help="输出目录 (默认 debug_out/<图片名>/)")
    parser.add_argument("--display", action="store_true",
                        help="除了保存文件，还用OpenCV窗口显示结果")
    args = parser.parse_args()

    img_path = Path(args.image)
    if not img_path.exists() or not img_path.is_file():
        print(f"错误: 找不到文件 '{args.image}'")
        sys.exit(1)

    # 创建输出目录
    if args.out:
        out_dir = Path(args.out)
    else:
        out_dir = PROJECT_ROOT / "debug_out" / img_path.stem
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"输入图片: {img_path}")
    print(f"输出目录: {out_dir}")
    print(f"分割方法: {args.method}")
    print(f"图像模式: {args.mode}")
    print("=" * 60)

    # 读取图片文件
    data = img_path.read_bytes()
    t0 = time.perf_counter()

    # ============================================================
    # 步骤 0: 解码 + 缩放
    # ============================================================
    print("\n[步骤0] 解码图片...")
    t_start = time.perf_counter()
    dec = decode.decode_and_scale(data, img_path.name, args.max_side)
    bgr = dec.bgr
    h, w = bgr.shape[:2]
    print(f"  原始尺寸: {dec.original_shape}")
    print(f"  缩放后:   {bgr.shape}  (scale={dec.scale:.3f})")
    print(f"  耗时:     {(time.perf_counter() - t_start)*1000:.0f}ms")

    save_step(bgr, out_dir, "00_original")

    # ============================================================
    # 步骤 1: 预处理
    # ============================================================
    print("\n[步骤1] 预处理...")
    t_start = time.perf_counter()
    pp = preprocess.PreprocessParams(
        median_ksize=settings.median_ksize,
        use_bilateral=settings.use_bilateral,
        clahe_clip=settings.clahe_clip,
        clahe_tile=settings.clahe_tile,
        use_tophat=settings.use_tophat,
        tophat_kernel=settings.tophat_kernel,
        use_blackhat=settings.use_blackhat,
        blackhat_kernel=settings.blackhat_kernel,
    )
    enhanced = preprocess.preprocess_gray(bgr, pp)
    print(f"  输出尺寸: {enhanced.shape}")
    print(f"  值范围:   [{enhanced.min()}, {enhanced.max()}], mean={enhanced.mean():.1f}")
    print(f"  耗时:     {(time.perf_counter() - t_start)*1000:.0f}ms")

    save_step(enhanced, out_dir, "01_preprocess", is_gray=True)

    # ============================================================
    # 步骤 2: ROI 检测
    # ============================================================
    print("\n[步骤2] ROI检测...")
    t_start = time.perf_counter()
    dp = detect.DetectParams(
        mode=args.mode,  # type: ignore[arg-type]
        detect_threshold=settings.detect_threshold,
        adaptive_block_size=settings.adaptive_block_size,
        adaptive_c=settings.adaptive_c,
        min_component_area=settings.min_component_area,
        max_component_area_ratio=settings.max_component_area_ratio,
        roi_margin_ratio=settings.roi_margin_ratio,
        color_fusion=settings.color_fusion,
    )
    roi, det_bw, note = detect.detect_roi(bgr, enhanced, dp)
    x, y, rw, rh = roi
    print(f"  ROI:      x={x}, y={y}, w={rw}, h={rh}")
    print(f"  ROI占图: {rw*rh/(h*w)*100:.1f}%")
    print(f"  备注:     {note}")

    # 保存检测二值图
    save_step(det_bw, out_dir, "02_detect_binary", is_gray=True)

    # ROI 预览
    roi_preview = viz.draw_roi(bgr, roi)
    save_step(roi_preview, out_dir, "02_roi_preview")

    # ============================================================
    # 步骤 3: 分割
    # ============================================================
    print(f"\n[步骤3] 分割 (method={args.method})...")
    t_start = time.perf_counter()

    gray_roi = enhanced[y:y+rh, x:x+rw]
    if gray_roi.size == 0:
        print("  错误: ROI 为空")
        sys.exit(1)

    sp = segment.SegmentParams(
        method=args.method,  # type: ignore[arg-type]
        threshold_kind="otsu",
        morph_kernel=settings.morph_kernel_segment,
        grow_T=settings.grow_T,
        seed_strategy=settings.seed_strategy,
    )
    mask_roi, seg_warnings = segment.segment_roi(gray_roi, sp)

    if seg_warnings:
        for w in seg_warnings:
            print(f"  警告: {w}")

    # 保存 ROI 内灰度图和分割结果
    save_step(gray_roi, out_dir, "03_gray_roi", is_gray=True)
    save_step(mask_roi, out_dir, "03_mask_roi", is_gray=True)

    # ============================================================
    # 步骤 4: 后处理
    # ============================================================
    print("\n[步骤4] 后处理...")
    t_start = time.perf_counter()
    mask_roi_clean = postprocess.postprocess_mask(mask_roi, settings.min_post_area)
    print(f"  耗时: {(time.perf_counter() - t_start)*1000:.0f}ms")

    save_step(mask_roi_clean, out_dir, "04_mask_postprocessed", is_gray=True)

    # ============================================================
    # 步骤 5: 拼回全图 + 可视化
    # ============================================================
    print("\n[步骤5] 可视化...")
    t_start = time.perf_counter()

    # 全图掩码
    full_mask = np.zeros((h, w), dtype=np.uint8)
    full_mask[y:y+rh, x:x+rw] = mask_roi_clean
    save_step(full_mask, out_dir, "05_full_mask", is_gray=True)

    # 叠红色
    overlay = viz.overlay_mask(bgr, full_mask)
    # 描黄边
    overlay = viz.draw_contours(overlay, full_mask)
    # 画绿框
    overlay = viz.draw_roi(overlay, roi)
    save_step(overlay, out_dir, "05_final_overlay")

    # 保存分割掩码(彩色)
    mask_color = np.zeros_like(bgr)
    mask_color[full_mask > 0] = (0, 0, 255)
    blend = cv2.addWeighted(bgr, 0.7, mask_color, 0.3, 0)
    save_step(blend, out_dir, "05_blend")

    # ============================================================
    # 统计
    # ============================================================
    total_ms = (time.perf_counter() - t0) * 1000
    pixel_count = int(np.sum(full_mask > 0))
    percentage = pixel_count / (h * w) * 100

    print("\n" + "=" * 60)
    print("完成！")
    print(f"  总耗时:       {total_ms:.0f}ms")
    print(f"  分割像素数:   {pixel_count}")
    print(f"  占图比例:     {percentage:.2f}%")
    print(f"  输出目录:     {out_dir}")
    print(f"  生成文件:")
    for f in sorted(out_dir.iterdir()):
        if f.suffix == ".png":
            print(f"    - {f.name}")

    # ============================================================
    # 可选: OpenCV 窗口显示
    # ============================================================
    if args.display:
        cv2.imshow("00 Original", bgr)
        cv2.imshow("01 Preprocess", enhanced)
        cv2.imshow("03 ROI Gray", gray_roi)
        cv2.imshow("03 Mask ROI", mask_roi)
        cv2.imshow("04 Postprocessed", mask_roi_clean)
        cv2.imshow("05 Final", overlay)
        print("\n按任意键关闭窗口...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

"""End-to-end pipeline and stage-specific runs."""

from __future__ import annotations

import contextlib
import csv
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

import cv2
import numpy as np
import structlog

from app.config import settings
from app.core import decode, detect, lbp, metrics, postprocess, preprocess, segment, viz
from app.core.exceptions import AppException, ValidationError
from app.core.validators import validate_odd_kernel_size, validate_positive, validate_range

logger = structlog.get_logger(__name__)

Stage = Literal["meta_only", "preprocess_only", "detect_only", "full"]


@dataclass
class ProcessRequest:
    stage: Stage = "full"
    mode: str = "dermoscopy"                # 皮肤镜模式，利用LAB颜色辅助
    max_side: int = 1280
    median_ksize: int = 9                   # 中值滤波，9经验证最优 (+0.006 vs 5)
    use_bilateral: bool = False             # 消融实验无显著提升，关掉省算力
    bilateral_d: int = 7                    # 稍大空间核
    bilateral_sigma_color: float = 75.0     # 更强颜色平滑
    bilateral_sigma_space: float = 50.0
    clahe_clip: float = 0.5                 # 温和对比度，消融实验验证最优
    clahe_tile: int = 8
    use_tophat: bool = False                # 默认关闭，破坏阈值分割对比度
    tophat_kernel: int = 21                 # 大核，黑素瘤通常较大
    use_blackhat: bool = False
    blackhat_kernel: int = 15
    detect_threshold: str = "adaptive"      # 自适应阈值应对光照不均
    adaptive_block_size: int = 45           # 大块适应光照渐变
    adaptive_c: int = 4                     # 更宽松常数
    min_component_area: int = 30            # 不过滤早期小病灶
    max_component_area_ratio: float = 0.90
    roi_margin_ratio: float = 0.15          # 更大边距：边界不规则
    color_fusion: str = "or"                # OR融合：包含所有颜色线索
    segment_method: str = "otsu_roi"        # 阈值分割，Triangle最优 (dual评分不可靠)
    threshold_in_segment: str = "triangle"  # 15图验证: 0.7856 vs Otsu 0.7604
    morph_kernel_segment: int = 5           # 5经验证最优 (+0.002 vs 3)
    min_post_area: int = 100                # 100经验证最优，过滤更多噪声碎片
    grow_T: int = 20                        # 更大容差：边界渐变模糊
    grow_G: float = 0.0
    use_gradient_gate: bool = False
    seed_strategy: str = "dark"             # 黑素瘤通常暗于周围
    watershed_fg_erosion_iters: int = 2
    watershed_bg_dilation_iters: int = 3
    return_lbp: bool = False

    def __post_init__(self):
        """Validate parameters after initialization."""
        # Validate kernel sizes (must be odd)
        validate_odd_kernel_size("median_ksize", self.median_ksize, min_value=1)
        validate_odd_kernel_size("tophat_kernel", self.tophat_kernel, min_value=3)
        validate_odd_kernel_size("blackhat_kernel", self.blackhat_kernel, min_value=3)
        validate_odd_kernel_size("morph_kernel_segment", self.morph_kernel_segment, min_value=3)
        validate_odd_kernel_size("adaptive_block_size", self.adaptive_block_size, min_value=3)

        # Validate positive values
        validate_positive("max_side", self.max_side)
        validate_positive("bilateral_d", self.bilateral_d)
        validate_positive("clahe_tile", self.clahe_tile)
        validate_positive("min_component_area", self.min_component_area)
        validate_positive("min_post_area", self.min_post_area)

        # Validate ranges
        validate_range("bilateral_sigma_color", self.bilateral_sigma_color, 0.0, 200.0)
        validate_range("bilateral_sigma_space", self.bilateral_sigma_space, 0.0, 200.0)
        validate_range("clahe_clip", self.clahe_clip, 0.0, 100.0)
        validate_range("max_component_area_ratio", self.max_component_area_ratio, 0.0, 1.0)
        validate_range("roi_margin_ratio", self.roi_margin_ratio, 0.0, 1.0)
        validate_range("grow_G", self.grow_G, 0.0, 1.0)

        # Validate enums
        if self.stage not in ("meta_only", "preprocess_only", "detect_only", "full"):
            raise ValidationError(
                f"Invalid stage '{self.stage}'. Must be one of: meta_only, preprocess_only, detect_only, full",
                details={"stage": self.stage, "allowed": ["meta_only", "preprocess_only", "detect_only", "full"]},
            )

        if self.mode not in ("gray_medical", "dermoscopy"):
            raise ValidationError(
                f"Invalid mode '{self.mode}'. Must be one of: gray_medical, dermoscopy",
                details={"mode": self.mode, "allowed": ["gray_medical", "dermoscopy"]},
            )

        if self.detect_threshold not in ("otsu", "adaptive"):
            raise ValidationError(
                f"Invalid detect_threshold '{self.detect_threshold}'. Must be one of: otsu, adaptive",
                details={"detect_threshold": self.detect_threshold, "allowed": ["otsu", "adaptive"]},
            )

        if self.color_fusion not in ("and", "or"):
            raise ValidationError(
                f"Invalid color_fusion '{self.color_fusion}'. Must be one of: and, or",
                details={"color_fusion": self.color_fusion, "allowed": ["and", "or"]},
            )

        if self.segment_method not in ("otsu_roi", "region_grow", "watershed", "dual"):
            raise ValidationError(
                f"Invalid segment_method '{self.segment_method}'. Must be one of: otsu_roi, region_grow, watershed, dual",
                details={"segment_method": self.segment_method, "allowed": ["otsu_roi", "region_grow", "watershed", "dual"]},
            )

        if self.threshold_in_segment not in ("otsu", "triangle", "adaptive"):
            raise ValidationError(
                f"Invalid threshold_in_segment '{self.threshold_in_segment}'. Must be one of: otsu, triangle, adaptive",
                details={"threshold_in_segment": self.threshold_in_segment, "allowed": ["otsu", "triangle", "adaptive"]},
            )

        if self.seed_strategy not in ("dark", "bright", "dt_peak"):
            raise ValidationError(
                f"Invalid seed_strategy '{self.seed_strategy}'. Must be one of: dark, bright, dt_peak",
                details={"seed_strategy": self.seed_strategy, "allowed": ["dark", "bright", "dt_peak"]},
            )


_LOG_FIELDS = [
    "timestamp_ms",
    "ok",
    "elapsed_ms",
    "stage",
    "mode",
    "segment_method",
    "roi",
    "scale",
    "error",
]


def _append_run_log(row: Dict[str, Any], log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = log_path.is_file()
    full = {k: row.get(k, "") for k in _LOG_FIELDS}
    with log_path.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=_LOG_FIELDS, extrasaction="ignore")
        if not file_exists:
            w.writeheader()
        w.writerow(full)


def _normalize_for_display(gray: np.ndarray) -> np.ndarray:
    """Stretch grayscale to full [0,255] range for preview only — does not modify pipeline input."""
    if gray.max() <= gray.min():
        return gray
    return cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)


def run(
    file_bytes: bytes,
    filename: str | None,
    req: ProcessRequest,
    gt_bytes: Optional[bytes] = None,
    log_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    t0 = time.perf_counter()
    timings: Dict[str, int] = {}
    warnings: List[str] = []
    meta: Dict[str, Any] = {
        "w": 0,
        "h": 0,
        "scale": 1.0,
        "original_size": [0, 0, 0],
        "roi": None,
        "elapsed_ms": 0,
        "warnings": [],
        "metrics": None,
    }
    out: Dict[str, Any] = {
        "ok": True,
        "error": None,
        "overlay_png_b64": None,
        "mask_png_b64": None,
        "lbp_png_b64": None,
        "preprocess_png_b64": None,
        "roi_preview_png_b64": None,
        "meta": meta,
    }

    try:
        allowed_stages = {"meta_only", "preprocess_only", "detect_only", "full"}
        if req.stage not in allowed_stages:
            raise ValueError(f"Invalid stage (use one of {sorted(allowed_stages)}).")

        # Decode stage
        t_decode = time.perf_counter()
        dec = decode.decode_and_scale(file_bytes, filename, int(req.max_side))
        timings["decode_ms"] = int((time.perf_counter() - t_decode) * 1000)

        bgr = dec.bgr
        gray_raw = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)  # raw contrast is best for thresholding
        gray_raw = cv2.medianBlur(gray_raw, req.median_ksize)  # denoise: ksize=9 best per scan
        h, w = bgr.shape[:2]
        meta["w"] = w
        meta["h"] = h
        meta["scale"] = dec.scale
        meta["original_size"] = [int(dec.original_shape[0]), int(dec.original_shape[1]), int(dec.original_shape[2])]

        if req.stage == "meta_only":
            meta["elapsed_ms"] = int((time.perf_counter() - t0) * 1000)
            meta["timings"] = timings
            logger.info("processing_completed", stage="meta_only", **timings)
            _maybe_log(req, meta, log_dir, ok=True)
            return out

        # Preprocess stage
        t_preprocess = time.perf_counter()
        pp = preprocess.PreprocessParams(
            median_ksize=req.median_ksize,
            use_bilateral=req.use_bilateral,
            bilateral_d=req.bilateral_d,
            bilateral_sigma_color=req.bilateral_sigma_color,
            bilateral_sigma_space=req.bilateral_sigma_space,
            clahe_clip=req.clahe_clip,
            clahe_tile=req.clahe_tile,
            use_tophat=req.use_tophat,
            tophat_kernel=req.tophat_kernel,
            use_blackhat=req.use_blackhat,
            blackhat_kernel=req.blackhat_kernel,
        )
        enhanced = preprocess.preprocess_gray(bgr, pp)
        timings["preprocess_ms"] = int((time.perf_counter() - t_preprocess) * 1000)

        if req.stage == "preprocess_only":
            enhanced_disp = _normalize_for_display(enhanced)
            pre_bgr = cv2.cvtColor(enhanced_disp, cv2.COLOR_GRAY2BGR)
            out["preprocess_png_b64"] = viz.bgr_to_png_rgb_b64(pre_bgr)
            meta["elapsed_ms"] = int((time.perf_counter() - t0) * 1000)
            meta["timings"] = timings
            logger.info("processing_completed", stage="preprocess_only", **timings)
            _maybe_log(req, meta, log_dir, ok=True)
            return out

        if req.mode not in ("gray_medical", "dermoscopy"):
            raise ValueError("mode must be gray_medical or dermoscopy.")

        # Detect stage
        t_detect = time.perf_counter()
        dp = detect.DetectParams(
            mode=req.mode,  # type: ignore[arg-type]
            detect_threshold=req.detect_threshold,
            adaptive_block_size=req.adaptive_block_size,
            adaptive_c=req.adaptive_c,
            min_component_area=req.min_component_area,
            max_component_area_ratio=req.max_component_area_ratio,
            roi_margin_ratio=req.roi_margin_ratio,
            color_fusion=req.color_fusion,
        )
        roi, det_bw, detect_note = detect.detect_roi(bgr, enhanced, dp)
        timings["detect_ms"] = int((time.perf_counter() - t_detect) * 1000)

        # If detect_roi returned a warning (fallback to full image), propagate it
        if detect_note.startswith("No lesion"):
            warnings.append(detect_note)
            logger.warning("roi_fallback", note=detect_note)

        meta["roi"] = [int(roi[0]), int(roi[1]), int(roi[2]), int(roi[3])]
        roi_preview = viz.draw_roi(bgr, roi)
        out["roi_preview_png_b64"] = viz.bgr_to_png_rgb_b64(roi_preview)

        if req.stage == "detect_only":
            meta["elapsed_ms"] = int((time.perf_counter() - t0) * 1000)
            meta["timings"] = timings
            logger.info("processing_completed", stage="detect_only", **timings)
            _maybe_log(req, meta, log_dir, ok=True)
            return out

        x, y, rw, rh = 0,0,w,h;
        # 用 raw 灰度做分割 — CLAHE 对全局阈值有轻微副作用 (15图验证 raw+Triangle=0.7856 最优)
        gray_roi = gray_raw[y : y + rh, x : x + rw]
        if gray_roi.size == 0:
            raise ValueError("ROI is empty after detection.")

        # Segment stage
        t_segment = time.perf_counter()
        sp = segment.SegmentParams(
            method=req.segment_method,  # type: ignore[arg-type]
            threshold_kind=req.threshold_in_segment,
            morph_kernel=req.morph_kernel_segment,
            grow_T=req.grow_T,
            grow_G=req.grow_G,
            use_gradient_gate=req.use_gradient_gate,
            seed_strategy=req.seed_strategy,
            watershed_fg_erosion_iters=req.watershed_fg_erosion_iters,
            watershed_bg_dilation_iters=req.watershed_bg_dilation_iters,
        )
        mask_roi, seg_warn = segment.segment_roi(gray_roi, sp)
        warnings.extend(seg_warn)
        timings["segment_ms"] = int((time.perf_counter() - t_segment) * 1000)

        # Postprocess stage
        t_postprocess = time.perf_counter()
        mask_roi = postprocess.postprocess_mask(mask_roi, req.min_post_area)
        timings["postprocess_ms"] = int((time.perf_counter() - t_postprocess) * 1000)

        full_mask = np.zeros((h, w), dtype=np.uint8)
        full_mask[y : y + rh, x : x + rw] = mask_roi

        # Visualization stage
        t_viz = time.perf_counter()
        overlay = viz.overlay_mask(bgr, full_mask)
        overlay = viz.draw_contours(overlay, full_mask)
        overlay = viz.draw_roi(overlay, roi)

        out["overlay_png_b64"] = viz.bgr_to_png_rgb_b64(overlay)
        mask_bgr = cv2.cvtColor(full_mask, cv2.COLOR_GRAY2BGR)
        out["mask_png_b64"] = viz.bgr_to_png_rgb_b64(mask_bgr)
        enhanced_disp = _normalize_for_display(enhanced)  # CLAHE-only, good contrast
        pre_bgr = cv2.cvtColor(enhanced_disp, cv2.COLOR_GRAY2BGR)
        out["preprocess_png_b64"] = viz.bgr_to_png_rgb_b64(pre_bgr)
        timings["viz_ms"] = int((time.perf_counter() - t_viz) * 1000)

        if req.return_lbp:
            t_lbp = time.perf_counter()
            # Tophat emphasizes local texture — compute on demand for LBP only
            pp_lbp = preprocess.PreprocessParams(
                median_ksize=req.median_ksize,
                use_bilateral=req.use_bilateral,
                bilateral_d=req.bilateral_d,
                bilateral_sigma_color=req.bilateral_sigma_color,
                bilateral_sigma_space=req.bilateral_sigma_space,
                clahe_clip=req.clahe_clip,
                clahe_tile=req.clahe_tile,
                use_tophat=True,
                tophat_kernel=req.tophat_kernel,
                use_blackhat=False,
            )
            enhanced_lbp = preprocess.preprocess_gray(bgr, pp_lbp)
            lbp_vis = lbp.uniform_lbp_image(enhanced_lbp)
            lbp_bgr = cv2.cvtColor(lbp_vis, cv2.COLOR_GRAY2BGR)
            lbp_bgr = viz.draw_roi(lbp_bgr, roi)
            out["lbp_png_b64"] = viz.bgr_to_png_rgb_b64(lbp_bgr)
            timings["lbp_ms"] = int((time.perf_counter() - t_lbp) * 1000)

        if gt_bytes:
            try:
                gt = metrics.decode_mask_bytes(gt_bytes)
                gt = metrics.resize_mask_to((h, w), gt)
                d, i = metrics.dice_iou(full_mask, gt)
                meta["metrics"] = {
                    "dice": round(d, 4),
                    "iou": round(i, 4),
                    "note": "GT resized to output size if needed.",
                }
            except Exception as ex:  # noqa: BLE001
                meta["metrics"] = {"error": str(ex)}

        meta["warnings"] = warnings
        meta["elapsed_ms"] = int((time.perf_counter() - t0) * 1000)
        meta["timings"] = timings

        logger.info("processing_completed", stage=req.stage, total_ms=meta["elapsed_ms"], **timings)
        _maybe_log(req, meta, log_dir, ok=True)
        return out

    except AppException:
        # Re-raise our custom exceptions to be handled by global exception handler
        raise
    except ValueError as e:
        out["ok"] = False
        out["error"] = str(e)
        meta["elapsed_ms"] = int((time.perf_counter() - t0) * 1000)
        meta["warnings"] = warnings
        meta["timings"] = timings
        _maybe_log(req, meta, log_dir, ok=False, error=str(e))
        return out
    except Exception as e:  # noqa: BLE001
        out["ok"] = False
        out["error"] = f"Unexpected processing error: {e}"
        meta["elapsed_ms"] = int((time.perf_counter() - t0) * 1000)
        meta["warnings"] = warnings
        meta["timings"] = timings
        _maybe_log(req, meta, log_dir, ok=False, error=out["error"])
        return out


def _maybe_log(
    req: ProcessRequest,
    meta: Dict[str, Any],
    log_dir: Optional[Path],
    *,
    ok: bool = True,
    error: str = "",
) -> None:
    base = log_dir if log_dir is not None else Path(__file__).resolve().parent.parent.parent
    log_path = base / settings.runs_log_csv
    row = {
        "timestamp_ms": int(time.time() * 1000),
        "ok": ok,
        "elapsed_ms": meta.get("elapsed_ms"),
        "stage": req.stage,
        "mode": req.mode,
        "segment_method": req.segment_method,
        "roi": meta.get("roi"),
        "scale": meta.get("scale"),
        "error": error,
    }
    with contextlib.suppress(OSError):
        _append_run_log(row, log_path)

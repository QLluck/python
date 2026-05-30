"""HTTP routes."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import JSONResponse

from app.core.pipeline import ProcessRequest, run
from app.core.validators import sanitize_filename, validate_file_extension, validate_file_size

router = APIRouter()


def _parse_bool(v: object, default: bool = False) -> bool:
    if v is None:
        return default
    if isinstance(v, bool):
        return v
    s = str(v).strip().lower()
    if s in ("true", "1", "yes", "on"):
        return True
    if s in ("false", "0", "no", "off", ""):
        return False
    return default


@router.get("/health")
def health() -> dict:
    return {"ok": True}


@router.post("/api/process")
async def api_process(
    file: UploadFile = File(...),
    stage: str = Form("full"),
    mode: str = Form("dermoscopy"),              # 皮肤镜模式
    max_side: int = Form(1280),
    median_ksize: int = Form(9),
    use_bilateral: str = Form("false"),          # 双边滤波关，消融实验无显著提升
    bilateral_d: int = Form(7),
    bilateral_sigma_color: float = Form(75.0),
    bilateral_sigma_space: float = Form(50.0),
    clahe_clip: float = Form(0.5),              # 温和对比度，0.5经15图验证最优
    clahe_tile: int = Form(8),
    use_tophat: str = Form("false"),             # 默认关闭，破坏阈值分割对比度
    tophat_kernel: int = Form(21),              # 大核
    use_blackhat: str = Form("false"),
    blackhat_kernel: int = Form(15),
    detect_threshold: str = Form("adaptive"),    # 自适应阈值
    adaptive_block_size: int = Form(45),
    adaptive_c: int = Form(4),
    min_component_area: int = Form(30),          # 不过滤小病灶
    max_component_area_ratio: float = Form(0.90),
    roi_margin_ratio: float = Form(0.15),        # 更大边距
    color_fusion: str = Form("or"),              # OR融合
    segment_method: str = Form("otsu_roi"),      # 阈值分割，15图验证Triangle最优
    threshold_in_segment: str = Form("triangle"),
    morph_kernel_segment: int = Form(5),         # 形态学核，5经验证最优
    min_post_area: int = Form(100),              # 100经验证最优，过滤噪声碎片
    grow_T: int = Form(20),                      # 更大容差
    grow_G: float = Form(0.0),
    use_gradient_gate: str = Form("false"),
    seed_strategy: str = Form("dark"),
    watershed_fg_erosion_iters: int = Form(2),
    watershed_bg_dilation_iters: int = Form(3),
    return_lbp: str = Form("false"),
    gt_mask: Optional[UploadFile] = File(None),
) -> JSONResponse:
    # Validate and sanitize filename
    safe_filename = sanitize_filename(file.filename or "upload")
    validate_file_extension(safe_filename)
    
    # Read file data
    data = await file.read()
    
    # Validate file size
    validate_file_size(len(data))
    
    gt_bytes: Optional[bytes] = None
    if gt_mask is not None and gt_mask.filename:
        gt_safe_filename = sanitize_filename(gt_mask.filename)
        validate_file_extension(gt_safe_filename)
        gt_bytes = await gt_mask.read()
        validate_file_size(len(gt_bytes))

    req = ProcessRequest(
        stage=stage,  # type: ignore[arg-type]
        mode=mode,
        max_side=max_side,
        median_ksize=median_ksize,
        use_bilateral=_parse_bool(use_bilateral),
        bilateral_d=bilateral_d,
        bilateral_sigma_color=bilateral_sigma_color,
        bilateral_sigma_space=bilateral_sigma_space,
        clahe_clip=clahe_clip,
        clahe_tile=clahe_tile,
        use_tophat=_parse_bool(use_tophat, True),
        tophat_kernel=tophat_kernel,
        use_blackhat=_parse_bool(use_blackhat),
        blackhat_kernel=blackhat_kernel,
        detect_threshold=detect_threshold,
        adaptive_block_size=adaptive_block_size,
        adaptive_c=adaptive_c,
        min_component_area=min_component_area,
        max_component_area_ratio=max_component_area_ratio,
        roi_margin_ratio=roi_margin_ratio,
        color_fusion=color_fusion,
        segment_method=segment_method,  # type: ignore[arg-type]
        threshold_in_segment=threshold_in_segment,
        morph_kernel_segment=morph_kernel_segment,
        min_post_area=min_post_area,
        grow_T=grow_T,
        grow_G=grow_G,
        use_gradient_gate=_parse_bool(use_gradient_gate),
        seed_strategy=seed_strategy,
        watershed_fg_erosion_iters=watershed_fg_erosion_iters,
        watershed_bg_dilation_iters=watershed_bg_dilation_iters,
        return_lbp=_parse_bool(return_lbp),
    )

    log_dir = Path(__file__).resolve().parent.parent.parent
    result = run(data, safe_filename, req, gt_bytes=gt_bytes, log_dir=log_dir)

    return JSONResponse(result)

"""ML API routes for smart segmentation."""

from __future__ import annotations

import base64
from io import BytesIO
from typing import Optional

import cv2
import numpy as np
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from app.core.decode import decode_image_bytes
from app.core.preprocess import preprocess_gray, PreprocessParams
from app.core.segment import segment_region_grow, segment_region_grow_color, analyze_color_variance, SegmentParams, score_segmentation
from app.ml.predictor import Predictor

# Initialize router
ml_router = APIRouter(prefix="/api/ml", tags=["ml"])

# Global predictor instance (lazy loaded)
_predictor: Optional[Predictor] = None


def get_predictor() -> Predictor:
    """Get or create the global predictor instance."""
    global _predictor
    if _predictor is None:
        _predictor = Predictor(version="1.0.0")
        try:
            _predictor.load_models()
        except FileNotFoundError:
            # Models not trained yet - predictor will use heuristics
            pass
    return _predictor


@ml_router.get("/model-info")
async def get_model_info() -> JSONResponse:
    """
    Get information about the loaded ML model.
    
    Returns:
        Model version, training date, accuracy, and feature count
    """
    try:
        predictor = get_predictor()
        info = predictor.get_model_info()
        return JSONResponse({"ok": True, "model_info": info})
    except Exception as e:
        return JSONResponse(
            {"ok": False, "error": str(e)},
            status_code=500
        )


@ml_router.post("/predict-parameters")
async def predict_parameters(
    file: UploadFile = File(...),
    max_side: int = Form(1280),
) -> JSONResponse:
    """
    Predict optimal segmentation parameters from image features.
    
    Args:
        file: Input image file
        max_side: Maximum image dimension for preprocessing
    
    Returns:
        Predicted method, parameters, confidence score, and extracted features
    """
    try:
        # Read and decode image
        data = await file.read()
        img = decode_image_bytes(data, file.filename or "upload")
        
        # Preprocess image to grayscale
        preprocess_params = PreprocessParams()
        gray = preprocess_gray(img, preprocess_params)
        
        # Predict parameters
        predictor = get_predictor()
        result = predictor.predict(gray)
        
        # Format response
        return JSONResponse({
            "ok": True,
            "method": result["method"],
            "parameters": result["parameters"],
            "confidence": result["confidence"],
            "features": {k: float(v) for k, v in result["features"].items()},
        })
        
    except Exception as e:
        return JSONResponse(
            {"ok": False, "error": str(e)},
            status_code=500
        )


@ml_router.post("/click-segment")
async def click_segment(
    file: UploadFile = File(...),
    click_x: int = Form(...),
    click_y: int = Form(...),
    original_width: int = Form(...),
    original_height: int = Form(...),
    max_side: int = Form(1280),
    accumulated_mask_b64: Optional[str] = Form(None),
    roi_x: Optional[int] = Form(None),
    roi_y: Optional[int] = Form(None),
    roi_w: Optional[int] = Form(None),
    roi_h: Optional[int] = Form(None),
) -> JSONResponse:
    """
    Perform click-based interactive segmentation.
    
    Args:
        file: Input image file
        click_x: X coordinate of click point (in original image coordinates)
        click_y: Y coordinate of click point (in original image coordinates)
        original_width: Original image width (before any scaling)
        original_height: Original image height (before any scaling)
        max_side: Maximum image dimension for preprocessing
        roi_x, roi_y, roi_w, roi_h: Optional ROI bounds
    
    Returns:
        Segmentation mask and overlay as base64-encoded images
    """
    try:
        import time
        start_time = time.time()
        
        # Read and decode image
        data = await file.read()
        decode_time = time.time()
        print(f"[PERF] File read: {(decode_time - start_time)*1000:.0f}ms")
        
        img = decode_image_bytes(data, file.filename or "upload")
        img_decode_time = time.time()
        print(f"[PERF] Image decode: {(img_decode_time - decode_time)*1000:.0f}ms, size: {img.shape}")
        
        actual_height, actual_width = img.shape[:2]
        
        print(f"[COORD] Original size: {original_width}x{original_height}")
        print(f"[COORD] Actual size: {actual_width}x{actual_height}")
        print(f"[COORD] Click: ({click_x}, {click_y})")
        
        # 图像未缩放，直接使用原始坐标
        adjusted_click_x = click_x
        adjusted_click_y = click_y
        
        # Validate coordinates are within bounds
        if adjusted_click_x < 0 or adjusted_click_x >= actual_width or \
           adjusted_click_y < 0 or adjusted_click_y >= actual_height:
            return JSONResponse(
                {
                    "ok": False, 
                    "error": f"点击坐标超出图像范围。"
                            f"坐标: ({click_x}, {click_y}), "
                            f"图像尺寸: {actual_width}x{actual_height}"
                },
                status_code=400
            )
        
        # Analyze color variance to decide segmentation mode
        color_mode, color_ratio = analyze_color_variance(img, adjusted_click_x, adjusted_click_y)
        print(f"[COLOR] Mode: {color_mode}, ratio: {color_ratio:.3f}")
        
        # Preprocess grayscale (needed for prediction and grayscale fallback)
        preprocess_params = PreprocessParams(
            use_tophat=False,
            use_blackhat=False,
            median_ksize=3,
            clahe_clip=2.0,
        )
        gray = preprocess_gray(img, preprocess_params)
        preprocess_time = time.time()
        print(f"[PERF] Preprocess: {(preprocess_time - img_decode_time)*1000:.0f}ms")
        
        h, w = gray.shape
        
        # Build ROI if provided
        roi = None
        if all(v is not None for v in [roi_x, roi_y, roi_w, roi_h]):
            roi = (roi_x, roi_y, roi_w, roi_h)
            print(f"[COORD] ROI adjusted: {roi}")
        
        # Predict parameters for click-based segmentation
        predictor = get_predictor()
        prediction = predictor.predict_for_click(gray, adjusted_click_x, adjusted_click_y, roi, bgr_image=img)
        predict_time = time.time()
        print(f"[PERF] ML prediction: {(predict_time - preprocess_time)*1000:.0f}ms")
        
        grow_T = float(prediction["parameters"]["grow_T"])
        chroma_factor = float(prediction["parameters"].get("chroma_factor", 0.6))
        
        # F: Dual-path segmentation — always run grayscale baseline,
        # also run color path when image has color info, pick the better result

        # Path 1: Grayscale region growing (always run as baseline)
        if roi:
            x, y, w_roi, h_roi = roi
            gray_roi = gray[y:y+h_roi, x:x+w_roi]
            seed_x = adjusted_click_x - x
            seed_y = adjusted_click_y - y
        else:
            gray_roi = gray
            seed_x = adjusted_click_x
            seed_y = adjusted_click_y

        params = SegmentParams(
            method="region_grow",
            grow_T=int(grow_T),
            seed_strategy="dark",
        )
        mask_roi_gray = segment_region_grow(gray_roi, params, manual_seed=(seed_x, seed_y))

        if roi:
            mask_gray = np.zeros_like(gray)
            mask_gray[y:y+h_roi, x:x+w_roi] = mask_roi_gray
        else:
            mask_gray = mask_roi_gray

        # Path 2: Color-aware segmentation (run if image has color info)
        mask_color = None
        if color_ratio > 0.2:  # lowered from 0.3 to be more inclusive
            mask_color = segment_region_grow_color(
                img, adjusted_click_x, adjusted_click_y,
                grow_T=grow_T, chroma_factor=chroma_factor,
            )

        # F: Score both paths and pick the better result
        if mask_color is not None:
            score_gray = score_segmentation(mask_gray, gray)
            score_color = score_segmentation(mask_color, gray)
            print(f"[DUAL] gray_score={score_gray:.3f}, color_score={score_color:.3f}")

            if score_color > score_gray:
                mask = mask_color
                chosen_mode = "lab"
            else:
                mask = mask_gray
                chosen_mode = "gray"
        else:
            mask = mask_gray
            chosen_mode = "gray"

        segment_time = time.time()
        print(f"[PERF] Segmentation ({chosen_mode}, color_ratio={color_ratio:.3f}): {(segment_time - predict_time)*1000:.0f}ms")
        
        # Merge with accumulated mask if provided
        if accumulated_mask_b64:
            try:
                acc_data = base64.b64decode(accumulated_mask_b64)
                acc_arr = np.frombuffer(acc_data, dtype=np.uint8)
                acc_mask = cv2.imdecode(acc_arr, cv2.IMREAD_GRAYSCALE)
                if acc_mask is not None and acc_mask.shape == mask.shape:
                    mask = cv2.bitwise_or(mask, acc_mask)
                    print(f"[MERGE] Merged with accumulated mask, total pixels: {int(np.sum(mask > 0))}")
                else:
                    print(f"[MERGE] Accumulated mask shape mismatch or decode failed, ignoring")
            except Exception as e:
                print(f"[MERGE] Failed to decode accumulated mask: {e}")
        
        # Create overlay (blend mask with original image)
        # Keep BGR format throughout; imencode expects BGR
        overlay = img.copy().astype(np.float32)
        red_bgr = np.array([0, 0, 255], dtype=np.float32)  # BGR: B=0,G=0,R=255 = red
        overlay[mask > 0] = overlay[mask > 0] * 0.5 + red_bgr * 0.5
        overlay = np.clip(overlay, 0, 255).astype(np.uint8)

        # Draw yellow contours around segmented region
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(overlay, contours, -1, (0, 255, 255), 2)  # BGR yellow

        overlay_time = time.time()
        print(f"[PERF] Overlay creation: {(overlay_time - segment_time)*1000:.0f}ms")
        
        # Encode mask and overlay as base64
        _, mask_encoded = cv2.imencode('.png', mask)
        mask_b64 = base64.b64encode(mask_encoded.tobytes()).decode('utf-8')
        
        _, overlay_encoded = cv2.imencode('.png', overlay)
        overlay_b64 = base64.b64encode(overlay_encoded.tobytes()).decode('utf-8')
        encode_time = time.time()
        print(f"[PERF] Base64 encoding: {(encode_time - overlay_time)*1000:.0f}ms")
        
        total_time = encode_time - start_time
        print(f"[PERF] TOTAL: {total_time*1000:.0f}ms")
        
        # 计算分割统计信息
        pixel_count = int(np.sum(mask > 0))
        percentage = (pixel_count / (h * w)) * 100
        seed_value = int(gray[adjusted_click_y, adjusted_click_x])
        
        print(f"[DEBUG] Click: ({click_x}, {click_y})")
        print(f"[DEBUG] Image size: {w}x{h}")
        print(f"[DEBUG] Seed value: {seed_value}")
        print(f"[DEBUG] Threshold: {prediction['parameters']['grow_T']:.1f}")
        print(f"[DEBUG] Segmented: {pixel_count} pixels ({percentage:.2f}%)")
        
        return JSONResponse({
            "ok": True,
            "mask_b64": mask_b64,
            "overlay_b64": overlay_b64,
            "parameters_used": prediction["parameters"],
            "confidence": prediction["confidence"],
            "performance": {
                "total_ms": int(total_time * 1000),
                "image_size": f"{w}x{h}"
            },
            "debug_info": {
                "original_click_position": {"x": click_x, "y": click_y},
                "adjusted_click_position": {"x": adjusted_click_x, "y": adjusted_click_y},
                "scale_factor": 1.0,
                "color_mode": chosen_mode,
                "color_ratio": round(color_ratio, 3),
                "original_image_size": {"width": original_width, "height": original_height},
                "processed_image_size": {"width": w, "height": h},
                "seed_value": seed_value,
                "threshold_used": float(prediction["parameters"]["grow_T"]),
                "chroma_factor": chroma_factor,
                "segmented_pixels": pixel_count,
                "segmented_percentage": round(percentage, 2),
                "image_stats": {
                    "mean": float(gray.mean()),
                    "std": float(gray.std()),
                    "min": int(gray.min()),
                    "max": int(gray.max())
                }
            }
        })
        
    except Exception as e:
        return JSONResponse(
            {"ok": False, "error": str(e)},
            status_code=500
        )


@ml_router.post("/save-training-data")
async def save_training_data(
    image_features: str = Form(...),  # JSON string of features
    parameters: str = Form(...),  # JSON string of parameters
    dice_score: Optional[float] = Form(None),
    user_rating: Optional[int] = Form(None),  # 1 = thumbs up, -1 = thumbs down
) -> JSONResponse:
    """
    Save training data from user interactions.
    
    Args:
        image_features: JSON string of extracted image features
        parameters: JSON string of final parameters used
        dice_score: Optional Dice score if ground truth available
        user_rating: Optional user rating (1 or -1)
    
    Returns:
        Success status and sample ID
    """
    try:
        import json
        from datetime import datetime
        from pathlib import Path
        
        # Parse inputs
        features = json.loads(image_features)
        params = json.loads(parameters)
        
        # Create training data directory if needed
        training_dir = Path(__file__).parent.parent / "ml" / "models" / "training_data"
        training_dir.mkdir(parents=True, exist_ok=True)
        
        # Append to real user data CSV
        csv_path = training_dir / "real_user_data.csv"
        
        # Create sample record
        sample = {
            "timestamp": datetime.now().isoformat(),
            "method": params.get("method", "unknown"),
            **features,
            "dice_score": dice_score or 0.0,
            "user_rating": user_rating or 0,
            **params,
        }
        
        # Append to CSV
        import csv
        import os
        
        file_exists = csv_path.exists()
        with open(csv_path, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=sample.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(sample)
        
        # Generate sample ID
        sample_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return JSONResponse({
            "ok": True,
            "saved": True,
            "sample_id": sample_id,
        })
        
    except Exception as e:
        return JSONResponse(
            {"ok": False, "error": str(e)},
            status_code=500
        )

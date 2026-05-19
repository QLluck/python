"""
Click-based interactive segmentation utilities.

Provides functions for interactive segmentation from user click points,
including support for multiple clicks and result merging.
"""

from __future__ import annotations

from typing import List, Optional, Tuple

import cv2
import numpy as np

from app.core.segment import segment_region_grow, SegmentParams
from app.ml.predictor import Predictor


def segment_from_click(
    image: np.ndarray,
    click_x: int,
    click_y: int,
    predictor: Optional[Predictor] = None,
    roi: Optional[Tuple[int, int, int, int]] = None,
    grow_T: Optional[int] = None
) -> np.ndarray:
    """
    Perform segmentation from a single click point.
    
    Args:
        image: Grayscale image
        click_x: X coordinate of click
        click_y: Y coordinate of click
        predictor: Optional ML predictor for parameter prediction
        roi: Optional ROI (x, y, w, h) to constrain segmentation
        grow_T: Optional manual threshold (overrides ML prediction)
    
    Returns:
        Binary segmentation mask
    """
    h, w = image.shape[:2]
    
    # Extract ROI if specified
    if roi:
        x, y, w_roi, h_roi = roi
        gray_roi = image[y:y+h_roi, x:x+w_roi]
        seed_x = click_x - x
        seed_y = click_y - y
    else:
        gray_roi = image
        seed_x = click_x
        seed_y = click_y
    
    # Predict parameters if predictor provided
    if grow_T is None:
        if predictor is not None:
            prediction = predictor.predict_for_click(image, click_x, click_y, roi)
            grow_T = int(prediction["parameters"]["grow_T"])
        else:
            # Default threshold
            grow_T = 15
    
    # Run region growing
    params = SegmentParams(
        method="region_grow",
        grow_T=grow_T,
        seed_strategy="dark",  # Not used with manual seed
    )
    
    mask_roi = segment_region_grow(gray_roi, params, manual_seed=(seed_x, seed_y))
    
    # Create full-size mask
    if roi:
        mask = np.zeros((h, w), dtype=np.uint8)
        x, y, w_roi, h_roi = roi
        mask[y:y+h_roi, x:x+w_roi] = mask_roi
    else:
        mask = mask_roi
    
    return mask


def segment_from_multiple_clicks(
    image: np.ndarray,
    clicks: List[Tuple[int, int]],
    predictor: Optional[Predictor] = None,
    roi: Optional[Tuple[int, int, int, int]] = None,
    merge_strategy: str = "union"
) -> np.ndarray:
    """
    Perform segmentation from multiple click points and merge results.
    
    Args:
        image: Grayscale image
        clicks: List of (x, y) click coordinates
        predictor: Optional ML predictor for parameter prediction
        roi: Optional ROI to constrain segmentation
        merge_strategy: How to merge results ("union" or "intersection")
    
    Returns:
        Binary segmentation mask combining all click results
    """
    if not clicks:
        return np.zeros(image.shape[:2], dtype=np.uint8)
    
    # Segment from first click
    merged_mask = segment_from_click(image, clicks[0][0], clicks[0][1], predictor, roi)
    
    # Merge additional clicks
    for click_x, click_y in clicks[1:]:
        mask = segment_from_click(image, click_x, click_y, predictor, roi)
        
        if merge_strategy == "union":
            merged_mask = cv2.bitwise_or(merged_mask, mask)
        elif merge_strategy == "intersection":
            merged_mask = cv2.bitwise_and(merged_mask, mask)
        else:
            raise ValueError(f"Unknown merge strategy: {merge_strategy}")
    
    return merged_mask


def create_overlay(
    image: np.ndarray,
    mask: np.ndarray,
    color: Tuple[int, int, int] = (255, 0, 0),
    alpha: float = 0.5
) -> np.ndarray:
    """
    Create an overlay visualization of segmentation mask on image.
    
    Args:
        image: Original image (grayscale or RGB)
        mask: Binary segmentation mask
        color: RGB color for overlay (default: red)
        alpha: Transparency (0=transparent, 1=opaque)
    
    Returns:
        RGB image with mask overlay
    """
    # Convert to RGB if grayscale
    if len(image.shape) == 2:
        overlay = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
        overlay = image.copy()
    
    # Apply colored overlay where mask is active
    mask_bool = mask > 0
    overlay[mask_bool] = (
        overlay[mask_bool] * (1 - alpha) + 
        np.array(color, dtype=np.uint8) * alpha
    ).astype(np.uint8)
    
    return overlay


def add_click_markers(
    image: np.ndarray,
    clicks: List[Tuple[int, int]],
    color: Tuple[int, int, int] = (0, 255, 0),
    radius: int = 5,
    thickness: int = 2
) -> np.ndarray:
    """
    Add visual markers for click points on image.
    
    Args:
        image: Image to draw on
        clicks: List of (x, y) click coordinates
        color: RGB color for markers (default: green)
        radius: Marker radius in pixels
        thickness: Marker line thickness
    
    Returns:
        Image with click markers drawn
    """
    result = image.copy()
    
    for i, (x, y) in enumerate(clicks):
        # Draw circle
        cv2.circle(result, (x, y), radius, color, thickness)
        
        # Draw crosshair
        cv2.line(result, (x - radius - 3, y), (x - radius - 1, y), color, thickness)
        cv2.line(result, (x + radius + 1, y), (x + radius + 3, y), color, thickness)
        cv2.line(result, (x, y - radius - 3), (x, y - radius - 1), color, thickness)
        cv2.line(result, (x, y + radius + 1), (x, y + radius + 3), color, thickness)
        
        # Draw number label
        cv2.putText(
            result,
            str(i + 1),
            (x + radius + 5, y - radius - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            1,
            cv2.LINE_AA
        )
    
    return result

"""Image decode, validation, and longest-side scaling."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import cv2
import numpy as np
import structlog

from app.core.exceptions import ImageDecodeError, ValidationError

logger = structlog.get_logger(__name__)

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp"}


@dataclass
class DecodeResult:
    bgr: np.ndarray
    original_shape: Tuple[int, int, int]  # h, w, c
    scale: float  # applied scale (new / original) for longest dimension logic: min(1, max_side/max(h,w))


def validate_extension(filename: str | None) -> None:
    if not filename:
        raise ValidationError("Missing filename.")
    lower = filename.lower()
    if not any(lower.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise ValidationError(
            f"Unsupported file type. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}.",
            details={"filename": filename, "allowed_extensions": list(ALLOWED_EXTENSIONS)},
        )


def decode_image_bytes(data: bytes, filename: str = "unknown") -> np.ndarray:
    if not data:
        raise ImageDecodeError("Empty file body.", details={"filename": filename})

    arr = np.frombuffer(data, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    if img is None:
        raise ImageDecodeError(
            f"Failed to decode image '{filename}'. "
            f"The file may be corrupted or in an unsupported format. "
            f"Supported formats: PNG, JPEG, BMP. "
            f"File size: {len(data) / 1024:.2f}KB. "
            f"Please try: 1) Re-saving the image, 2) Converting to PNG/JPEG, 3) Using a different file.",
            details={
                "filename": filename,
                "file_size_bytes": len(data),
                "file_size_kb": round(len(data) / 1024, 2),
                "supported_formats": ["PNG", "JPEG", "BMP"],
            },
        )

    if img.ndim != 3 or img.shape[2] not in (3, 4):
        raise ImageDecodeError(
            f"Unexpected channel count after decode: shape={img.shape}.",
            details={"shape": img.shape, "filename": filename},
        )
    if img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    return img


def scale_longest_side(bgr: np.ndarray, max_side: int) -> Tuple[np.ndarray, float]:
    if max_side <= 0:
        raise ValidationError("max_side must be a positive integer.", details={"max_side": max_side})
    h, w = bgr.shape[:2]
    m = max(h, w)
    if m <= max_side:
        return bgr, 1.0  # No copy needed if no scaling
    scale = max_side / float(m)
    new_w = max(1, int(round(w * scale)))
    new_h = max(1, int(round(h * scale)))
    resized = cv2.resize(bgr, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return resized, scale


def decode_and_scale(data: bytes, filename: str | None, max_side: int) -> DecodeResult:
    logger.info("decode_started", filename=filename, data_size=len(data), max_side=max_side)

    validate_extension(filename)
    raw = decode_image_bytes(data, filename or "unknown")
    oh, ow, oc = raw.shape

    logger.info("image_decoded", filename=filename, shape=(oh, ow, oc))

    # Auto-scale large images for performance
    max_dimension = max(oh, ow)
    if max_dimension > 2000:
        logger.warning(
            "large_image_auto_scaled",
            original_size=(oh, ow),
            max_dimension=max_dimension,
            recommended_max=2000,
            note="Large images are automatically scaled to improve processing speed",
        )
        # Force smaller max_side for very large images
        max_side = min(max_side, 1280)

    scaled, s = scale_longest_side(raw, max_side)

    logger.info(
        "decode_completed",
        filename=filename,
        original_shape=(oh, ow, oc),
        scaled_shape=scaled.shape,
        scale_factor=round(s, 3),
    )

    return DecodeResult(bgr=scaled, original_shape=(oh, ow, oc), scale=float(s))

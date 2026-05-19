"""Custom validators for input validation."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from app.core.exceptions import ValidationError

# Allowed file extensions
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp"}

# Maximum file size (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024


def validate_file_size(size: int, max_size: int = MAX_FILE_SIZE) -> None:
    """Validate file size is within limits.
    
    Args:
        size: File size in bytes
        max_size: Maximum allowed size in bytes
        
    Raises:
        ValidationError: If file size exceeds limit
    """
    if size > max_size:
        raise ValidationError(
            f"File too large ({size / 1024 / 1024:.2f}MB). Maximum allowed: {max_size / 1024 / 1024:.0f}MB",
            details={"size_bytes": size, "max_bytes": max_size, "size_mb": round(size / 1024 / 1024, 2)},
        )


def validate_file_extension(filename: str) -> None:
    """Validate file has an allowed extension.
    
    Args:
        filename: Name of the file
        
    Raises:
        ValidationError: If extension is not allowed
    """
    if not filename:
        raise ValidationError("Filename is required.", details={"filename": filename})

    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            f"Unsupported file extension '{ext}'. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
            details={"extension": ext, "allowed": sorted(ALLOWED_EXTENSIONS)},
        )


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal attacks.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename (basename only, no path components)
    """
    if not filename:
        return "unnamed"

    # Get basename only (remove any path components)
    safe_name = Path(filename).name

    # Remove any remaining path separators
    safe_name = safe_name.replace("/", "_").replace("\\", "_")

    # Remove any null bytes
    safe_name = safe_name.replace("\x00", "")

    # Limit length
    if len(safe_name) > 255:
        # Keep extension
        stem = Path(safe_name).stem[:240]
        ext = Path(safe_name).suffix
        safe_name = stem + ext

    return safe_name or "unnamed"


def validate_odd_kernel_size(name: str, value: int, min_value: int = 3) -> int:
    """Validate kernel size is odd and >= min_value.
    
    Args:
        name: Parameter name for error messages
        value: Kernel size value
        min_value: Minimum allowed value
        
    Returns:
        Validated kernel size
        
    Raises:
        ValidationError: If validation fails
    """
    if value < min_value:
        raise ValidationError(
            f"{name} must be >= {min_value} (got {value})",
            details={"parameter": name, "value": value, "min_value": min_value},
        )

    if value % 2 == 0:
        raise ValidationError(
            f"{name} must be odd (got {value}). Try {value - 1} or {value + 1}",
            details={"parameter": name, "value": value, "suggestion": [value - 1, value + 1]},
        )

    return value


def validate_range(name: str, value: float, min_val: float, max_val: float) -> float:
    """Validate value is within range [min_val, max_val].
    
    Args:
        name: Parameter name for error messages
        value: Value to validate
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        
    Returns:
        Validated value
        
    Raises:
        ValidationError: If value is out of range
    """
    if not min_val <= value <= max_val:
        raise ValidationError(
            f"{name} must be between {min_val} and {max_val} (got {value})",
            details={"parameter": name, "value": value, "min": min_val, "max": max_val},
        )

    return value


def validate_positive(name: str, value: float) -> float:
    """Validate value is positive (> 0).
    
    Args:
        name: Parameter name for error messages
        value: Value to validate
        
    Returns:
        Validated value
        
    Raises:
        ValidationError: If value is not positive
    """
    if value <= 0:
        raise ValidationError(
            f"{name} must be positive (got {value})", details={"parameter": name, "value": value}
        )

    return value

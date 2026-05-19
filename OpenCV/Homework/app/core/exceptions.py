"""Custom exception classes for the application."""

from __future__ import annotations


class AppException(Exception):
    """Base exception for all application errors.

    Attributes:
        message: Human-readable error message
        code: Machine-readable error code
        status_code: HTTP status code
        details: Optional additional error details
    """

    def __init__(
        self,
        message: str,
        code: str,
        status_code: int = 500,
        details: dict | None = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class ValidationError(AppException):
    """Input validation errors.

    Raised when user input fails validation checks.
    """

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message, "VALIDATION_ERROR", 400, details)


class ImageDecodeError(AppException):
    """Image decoding errors.

    Raised when image file cannot be decoded or is corrupted.
    """

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message, "IMAGE_DECODE_ERROR", 400, details)


class ProcessingError(AppException):
    """Image processing errors.

    Raised when image processing operations fail.
    """

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message, "PROCESSING_ERROR", 500, details)


class ResourceLimitError(AppException):
    """Resource limit exceeded.

    Raised when resource limits (file size, memory, timeout) are exceeded.
    """

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message, "RESOURCE_LIMIT_ERROR", 413, details)

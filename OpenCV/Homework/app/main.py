"""FastAPI entry: health, static UI, /api/process."""

from __future__ import annotations

import os
import time
import uuid
from datetime import datetime
from pathlib import Path

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError as PydanticValidationError
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.routes import router
from app.api.ml_routes import ml_router
from app.core.exceptions import AppException, ResourceLimitError
from app.core.logging import configure_logging

# Configure logging based on environment
is_production = os.getenv("ENV", "development").lower() == "production"
configure_logging(json_logs=is_production)

logger = structlog.get_logger(__name__)

ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / "static"

app = FastAPI(title="Medical lesion segmentation", version="1.0.0")

# Configure CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class FileSizeLimitMiddleware(BaseHTTPMiddleware):
    """Middleware to enforce file upload size limits."""

    async def dispatch(self, request: Request, call_next):
        if request.method == "POST" and request.url.path == "/api/process":
            content_length = request.headers.get("content-length")
            if content_length:
                size = int(content_length)
                max_size = 10 * 1024 * 1024  # 10MB
                if size > max_size:
                    logger.warning("file_too_large", size_mb=round(size / 1024 / 1024, 2), max_mb=10)
                    raise ResourceLimitError(
                        f"File too large ({size / 1024 / 1024:.2f}MB). Maximum allowed: 10MB",
                        details={"size_bytes": size, "size_mb": round(size / 1024 / 1024, 2), "max_mb": 10},
                    )
        return await call_next(request)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers to all responses."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response


app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(FileSizeLimitMiddleware)


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    """Log all requests with timing and request ID."""
    request_id = str(uuid.uuid4())
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=request_id)

    start_time = time.time()

    logger.info(
        "request_started",
        method=request.method,
        path=request.url.path,
        client=request.client.host if request.client else None,
    )

    response = await call_next(request)

    duration = time.time() - start_time

    logger.info(
        "request_completed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration_seconds=round(duration, 3),
    )

    response.headers["X-Request-ID"] = request_id
    return response


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle custom application exceptions."""
    logger.error(
        "application_error",
        error_code=exc.code,
        error_message=exc.message,
        status_code=exc.status_code,
        details=exc.details,
        exc_info=True,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "ok": False,
            "error": {
                "message": exc.message,
                "code": exc.code,
                "details": exc.details,
            },
            "timestamp": datetime.utcnow().isoformat() + "Z",
        },
    )


@app.exception_handler(PydanticValidationError)
async def validation_exception_handler(request: Request, exc: PydanticValidationError) -> JSONResponse:
    """Handle Pydantic validation errors."""
    logger.warning(
        "validation_error",
        errors=exc.errors(),
    )
    return JSONResponse(
        status_code=422,
        content={
            "ok": False,
            "error": {
                "message": "Validation error",
                "code": "VALIDATION_ERROR",
                "details": {"errors": exc.errors()},
            },
            "timestamp": datetime.utcnow().isoformat() + "Z",
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    logger.error(
        "unexpected_error",
        error_type=type(exc).__name__,
        error_message=str(exc),
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={
            "ok": False,
            "error": {
                "message": "Internal server error",
                "code": "INTERNAL_ERROR",
                "details": {},
            },
            "timestamp": datetime.utcnow().isoformat() + "Z",
        },
    )


app.include_router(router)

app.include_router(ml_router)


@app.get("/")
def index_page() -> FileResponse:
    return FileResponse(STATIC / "index.html")


app.mount("/static", StaticFiles(directory=str(STATIC)), name="static")

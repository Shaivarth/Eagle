from __future__ import annotations

# Re-export all schemas from eagle.schemas for full backwards compatibility
from eagle.schemas import (
    AnalyzeResponse,
    AnalyzeResult,
    CameraInfo,
    ExposureInfo,
    GpsMetadata,
    ImageFileInfo,
    LocationInfo,
    RawExifTag,
)

__all__ = [
    "AnalyzeResponse",
    "AnalyzeResult",
    "CameraInfo",
    "ExposureInfo",
    "GpsMetadata",
    "ImageFileInfo",
    "LocationInfo",
    "RawExifTag",
]

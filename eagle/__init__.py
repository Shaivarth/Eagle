"""Eagle — Digital Forensics & EXIF/GPS Metadata Extraction Utility."""

from __future__ import annotations

__version__ = "1.0.0"

from eagle.analyzer import (
    AnalysisError,
    DecompressionBombError,
    InvalidImageError,
    analyze_image,
    analyze_image_bytes,
    analyze_image_file,
)
from eagle.exif_utils import extract_full_metadata
from eagle.geocode import reverse_geocode, reverse_geocode_async
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
    "__version__",
    "analyze_image",
    "analyze_image_file",
    "analyze_image_bytes",
    "extract_full_metadata",
    "reverse_geocode",
    "reverse_geocode_async",
    "AnalyzeResponse",
    "AnalyzeResult",
    "CameraInfo",
    "ExposureInfo",
    "GpsMetadata",
    "ImageFileInfo",
    "LocationInfo",
    "RawExifTag",
    "AnalysisError",
    "InvalidImageError",
    "DecompressionBombError",
]

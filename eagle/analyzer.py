from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional, Union

import httpx
from PIL import Image

from eagle.exif_utils import extract_full_metadata
from eagle.geocode import reverse_geocode
from eagle.schemas import AnalyzeResponse

logger = logging.getLogger("eagle")

# Maximum local file size (100 MB) for CLI safety
MAX_FILE_BYTES = 100 * 1024 * 1024


class AnalysisError(Exception):
    """Base exception for Eagle image analysis errors."""
    pass


class InvalidImageError(AnalysisError):
    """Raised when the input file is not a valid or supported image."""
    pass


class DecompressionBombError(AnalysisError):
    """Raised when an image exceeds safe pixel dimensions."""
    pass


def analyze_image_bytes(
    image_bytes: bytes,
    filename: str = "image",
    geocode: bool = False,
    include_preview: bool = False,
) -> AnalyzeResponse:
    """Analyze raw image bytes and return full metadata and forensics information.

    :param image_bytes: Raw binary content of the image.
    :param filename: Name of the file for reporting and format hints.
    :param geocode: Whether to perform reverse geocoding if GPS coordinates are present.
    :param include_preview: Whether to generate a base64 preview thumbnail.
    :return: AnalyzeResponse object with all structured metadata.
    """
    if not image_bytes:
        raise InvalidImageError("Image data is empty.")

    try:
        full_meta = extract_full_metadata(image_bytes, filename, include_preview=include_preview)
    except Image.DecompressionBombError as e:
        raise DecompressionBombError("Image dimensions exceed safety limits (potential decompression bomb).") from e
    except Exception as e:
        raise InvalidImageError(f"Failed to process image: {e}") from e

    if full_meta["file_info"].format is None:
        raise InvalidImageError(f"The file '{filename}' could not be decoded as a valid image (JPG, PNG, HEIC, etc.).")

    gps_info = full_meta["gps_info"]
    has_gps = bool(gps_info and gps_info.latitude is not None and gps_info.longitude is not None)

    latitude = gps_info.latitude if has_gps else None
    longitude = gps_info.longitude if has_gps else None
    location = None
    geocode_error = None

    if geocode and has_gps and latitude is not None and longitude is not None:
        try:
            location = reverse_geocode(latitude, longitude)
        except (httpx.HTTPError, httpx.TimeoutException, Exception) as exc:
            logger.warning("Reverse geocoding failed: %s", exc)
            geocode_error = f"Reverse geocoding failed: {exc}"

    return AnalyzeResponse(
        filename=filename,
        has_gps=has_gps,
        latitude=latitude,
        longitude=longitude,
        location=location,
        geocode_error=geocode_error,
        preview_url=full_meta.get("preview_url"),
        file_info=full_meta["file_info"],
        camera_info=full_meta["camera_info"],
        exposure_info=full_meta["exposure_info"],
        gps_info=full_meta["gps_info"],
        raw_exif=full_meta["raw_exif"],
    )


def analyze_image_file(
    file_path: Union[str, Path],
    geocode: bool = False,
    include_preview: bool = False,
) -> AnalyzeResponse:
    """Analyze an image file on the local filesystem.

    :param file_path: Local filesystem path to the image.
    :param geocode: Whether to perform reverse geocoding if GPS coordinates are present.
    :param include_preview: Whether to generate a base64 preview thumbnail.
    :return: AnalyzeResponse object with all structured metadata.
    """
    path = Path(file_path).resolve()

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not path.is_file():
        raise InvalidImageError(f"Path is not a regular file: {file_path}")

    file_size = path.stat().st_size
    if file_size > MAX_FILE_BYTES:
        raise InvalidImageError(f"File size exceeds safety limit of {MAX_FILE_BYTES // (1024 * 1024)} MB.")

    try:
        with open(path, "rb") as f:
            image_bytes = f.read()
    except PermissionError as e:
        raise PermissionError(f"Permission denied reading file: {file_path}") from e
    except OSError as e:
        raise InvalidImageError(f"Error reading file '{file_path}': {e}") from e

    return analyze_image_bytes(
        image_bytes=image_bytes,
        filename=path.name,
        geocode=geocode,
        include_preview=include_preview,
    )


def analyze_image(
    source: Union[str, Path, bytes],
    filename: Optional[str] = None,
    geocode: bool = False,
    include_preview: bool = False,
) -> AnalyzeResponse:
    """Unified entry point to analyze an image from either a file path or raw bytes."""
    if isinstance(source, (str, Path)):
        return analyze_image_file(source, geocode=geocode, include_preview=include_preview)
    elif isinstance(source, (bytes, bytearray)):
        return analyze_image_bytes(
            bytes(source),
            filename=filename or "image",
            geocode=geocode,
            include_preview=include_preview,
        )
    else:
        raise TypeError(f"Unsupported source type: {type(source)}")

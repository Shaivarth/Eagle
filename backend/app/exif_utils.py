from __future__ import annotations

# Re-export all EXIF utilities from eagle.exif_utils for full backwards compatibility
from eagle.exif_utils import (
    _clean_val,
    _dms_to_decimal,
    _dms_to_string,
    _format_aperture,
    _format_exposure_bias,
    _format_exposure_program,
    _format_file_size,
    _format_flash,
    _format_focal_length,
    _format_iso,
    _format_metering_mode,
    _format_shutter_speed,
    _generate_preview_base64,
    _ratio_to_float,
    extract_full_metadata,
)

__all__ = [
    "extract_full_metadata",
    "_generate_preview_base64",
    "_ratio_to_float",
    "_dms_to_decimal",
    "_dms_to_string",
    "_format_file_size",
    "_clean_val",
    "_format_shutter_speed",
    "_format_aperture",
    "_format_iso",
    "_format_focal_length",
    "_format_exposure_bias",
    "_format_flash",
    "_format_metering_mode",
    "_format_exposure_program",
]

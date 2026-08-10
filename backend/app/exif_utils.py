from __future__ import annotations

import io

from typing import Any, Dict, List, Optional, Tuple

from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS

from app.schemas import (
    CameraInfo,
    ExposureInfo,
    GpsMetadata,
    ImageFileInfo,
    RawExifTag,
)

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass


def _ratio_to_float(value: Any) -> float:
    if value is None:
        return 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        if isinstance(value, (tuple, list)) and len(value) >= 2:
            num, den = value[0], value[1]
            return float(num) / float(den) if den != 0 else 0.0
        return 0.0


def _dms_to_decimal(dms: Tuple, reference: str) -> float:
    degrees = _ratio_to_float(dms[0])
    minutes = _ratio_to_float(dms[1])
    seconds = _ratio_to_float(dms[2])

    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if reference in ("S", "W"):
        decimal = -decimal
    return decimal


def _dms_to_string(dms: Tuple, reference: str) -> Optional[str]:
    try:
        deg = int(_ratio_to_float(dms[0]))
        min_ = int(_ratio_to_float(dms[1]))
        sec = _ratio_to_float(dms[2])
        return f"{deg}° {min_:02d}' {sec:05.2f}\" {reference}"
    except Exception:
        return None


def _format_file_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"


def _clean_val(val: Any) -> str:
    if val is None:
        return ""
    if isinstance(val, bytes):
        if len(val) > 64:
            return f"[{len(val)} bytes binary data]"
        try:
            return val.decode("utf-8", errors="ignore").strip("\x00").strip()
        except Exception:
            return val.hex()
    if isinstance(val, (tuple, list)):
        return ", ".join(_clean_val(x) for x in val)
    if isinstance(val, dict):
        return str({k: _clean_val(v) for k, v in val.items()})

    s = str(val).strip("\x00").strip()
    return s


def _format_shutter_speed(val: Any) -> Optional[str]:
    sec = _ratio_to_float(val)
    if sec <= 0:
        return None
    if sec >= 1.0:
        return f"{sec:.1f} s" if sec % 1 != 0 else f"{int(sec)} s"
    inv = 1.0 / sec
    return f"1/{round(inv)} s"


def _format_aperture(val: Any) -> Optional[str]:
    f_num = _ratio_to_float(val)
    if f_num <= 0:
        return None
    return f"f/{f_num:.1f}"


def _format_iso(val: Any) -> Optional[str]:
    if val is None:
        return None
    if isinstance(val, (tuple, list)) and len(val) > 0:
        val = val[0]
    try:
        return f"ISO {int(val)}"
    except (ValueError, TypeError):
        return f"ISO {val}"


def _format_focal_length(val: Any) -> Optional[str]:
    fl = _ratio_to_float(val)
    if fl <= 0:
        return None
    return f"{fl:.1f} mm" if fl % 1 != 0 else f"{int(fl)} mm"


def _format_exposure_bias(val: Any) -> Optional[str]:
    bias = _ratio_to_float(val)
    if bias == 0:
        return "0 EV"
    return f"{bias:+.1f} EV"


def _format_flash(val: Any) -> Optional[str]:
    if val is None:
        return None
    try:
        v = int(val)
        fired = bool(v & 1)
        return "Flash fired" if fired else "Flash did not fire"
    except (ValueError, TypeError):
        return _clean_val(val)


def _format_metering_mode(val: Any) -> Optional[str]:
    modes = {
        0: "Unknown",
        1: "Average",
        2: "Center-Weighted Average",
        3: "Spot",
        4: "Multi-Spot",
        5: "Pattern / Multi-Segment",
        6: "Partial",
    }
    try:
        return modes.get(int(val), f"Mode {val}")
    except (ValueError, TypeError):
        return None


def _format_exposure_program(val: Any) -> Optional[str]:
    programs = {
        1: "Manual",
        2: "Normal / Program AE",
        3: "Aperture Priority",
        4: "Shutter Priority",
        5: "Creative Program",
        6: "Action Program",
        7: "Portrait Mode",
        8: "Landscape Mode",
    }
    try:
        return programs.get(int(val), f"Program {val}")
    except (ValueError, TypeError):
        return None


def extract_full_metadata(image_bytes: bytes, filename: str) -> dict[str, Any]:
    size_bytes = len(image_bytes)
    formatted_size = _format_file_size(size_bytes)

    image = None
    exif_obj = None
    fmt = None
    width = None
    height = None
    megapixels = None
    color_mode = None
    mime_type = None

    try:
        image = Image.open(io.BytesIO(image_bytes))
        fmt = image.format
        mime_type = Image.MIME.get(fmt, f"image/{fmt.lower()}" if fmt else None)
        width, height = image.size
        megapixels = round((width * height) / 1_000_000, 2)
        color_mode = image.mode
        exif_obj = image.getexif()
    except Exception:
        image = None

    filename_lower = filename.lower()
    is_heic_file = filename_lower.endswith(".heic") or filename_lower.endswith(".heif")
    try:
        import pillow_heif
        if is_heic_file or image is None:
            heif_file = pillow_heif.open_heif(io.BytesIO(image_bytes))
            if image is None:
                image = heif_file.to_pillow()
                fmt = "HEIC"
                mime_type = "image/heic"
                width, height = image.size
                megapixels = round((width * height) / 1_000_000, 2)
                color_mode = image.mode

            heif_info = getattr(heif_file, "info", {}) or {}
            exif_bytes = heif_info.get("exif")
            if exif_bytes and (not exif_obj or len(exif_obj) == 0):
                try:
                    loaded_exif = Image.Exif()
                    loaded_exif.load(exif_bytes)
                    if len(loaded_exif) > 0:
                        exif_obj = loaded_exif
                except Exception:
                    pass
    except Exception:
        pass

    if image is not None and (not exif_obj or len(exif_obj) == 0):
        raw_info_exif = image.info.get("exif") if hasattr(image, "info") else None
        if raw_info_exif and isinstance(raw_info_exif, bytes):
            try:
                loaded_exif = Image.Exif()
                loaded_exif.load(raw_info_exif)
                if len(loaded_exif) > 0:
                    exif_obj = loaded_exif
            except Exception:
                pass

    file_info = ImageFileInfo(
        file_size_bytes=size_bytes,
        formatted_file_size=formatted_size,
        format=fmt,
        mime_type=mime_type,
        width=width,
        height=height,
        megapixels=megapixels,
        color_mode=color_mode,
    )

    if not exif_obj:
        return {
            "file_info": file_info,
            "camera_info": CameraInfo(),
            "exposure_info": ExposureInfo(),
            "gps_info": GpsMetadata(),
            "raw_exif": [],
        }

    combined_exif: dict[str, Any] = {}
    raw_tags_list: list[RawExifTag] = []

    for tag_id, value in exif_obj.items():
        tag_name = TAGS.get(tag_id, f"Tag_{tag_id}")
        combined_exif[tag_name] = value
        raw_val = _clean_val(value)
        if raw_val and tag_name not in ("MakerNote", "JPEGThumbnail", "TileData"):
            raw_tags_list.append(
                RawExifTag(
                    tag_id=f"0x{tag_id:04X}",
                    tag_name=tag_name,
                    value=raw_val,
                )
            )

    exif_sub_tag = next((tag for tag, name in TAGS.items() if name == "ExifOffset"), 0x8769)
    try:
        exif_ifd = exif_obj.get_ifd(exif_sub_tag)
        if exif_ifd:
            for tag_id, value in exif_ifd.items():
                tag_name = TAGS.get(tag_id, f"Tag_{tag_id}")
                combined_exif[tag_name] = value
                raw_val = _clean_val(value)
                if raw_val and tag_name not in ("MakerNote", "JPEGThumbnail"):
                    raw_tags_list.append(
                        RawExifTag(
                            tag_id=f"0x{tag_id:04X}",
                            tag_name=tag_name,
                            value=raw_val,
                        )
                    )
    except Exception:
        pass

    gps_sub_tag = next((tag for tag, name in TAGS.items() if name == "GPSInfo"), 0x8825)
    gps_dict: dict[str, Any] = {}
    try:
        gps_ifd = exif_obj.get_ifd(gps_sub_tag)
        if gps_ifd:
            for tag_id, value in gps_ifd.items():
                tag_name = GPSTAGS.get(tag_id, f"GPS_{tag_id}")
                gps_dict[tag_name] = value
                raw_val = _clean_val(value)
                if raw_val:
                    raw_tags_list.append(
                        RawExifTag(
                            tag_id=f"GPS_0x{tag_id:02X}",
                            tag_name=f"GPS.{tag_name}",
                            value=raw_val,
                        )
                    )
    except Exception:
        pass

    camera_info = CameraInfo(
        make=_clean_val(combined_exif.get("Make")) or None,
        model=_clean_val(combined_exif.get("Model")) or None,
        lens_model=_clean_val(combined_exif.get("LensModel") or combined_exif.get("LensInfo")) or None,
        software=_clean_val(combined_exif.get("Software")) or None,
    )

    date_orig = (
        _clean_val(combined_exif.get("DateTimeOriginal"))
        or _clean_val(combined_exif.get("DateTimeDigitized"))
        or _clean_val(combined_exif.get("DateTime"))
        or None
    )

    exposure_info = ExposureInfo(
        date_time_original=date_orig,
        exposure_time=_format_shutter_speed(combined_exif.get("ExposureTime")),
        aperture=_format_aperture(combined_exif.get("FNumber") or combined_exif.get("ApertureValue")),
        iso=_format_iso(combined_exif.get("ISOSpeedRatings") or combined_exif.get("PhotographicSensitivity")),
        focal_length=_format_focal_length(combined_exif.get("FocalLength")),
        focal_length_35mm=_format_focal_length(combined_exif.get("FocalLengthIn35mmFilm")),
        exposure_bias=_format_exposure_bias(combined_exif.get("ExposureBiasValue")),
        flash=_format_flash(combined_exif.get("Flash")),
        white_balance="Manual" if combined_exif.get("WhiteBalance") == 1 else ("Auto" if combined_exif.get("WhiteBalance") == 0 else None),
        metering_mode=_format_metering_mode(combined_exif.get("MeteringMode")),
        exposure_program=_format_exposure_program(combined_exif.get("ExposureProgram")),
    )

    lat_dms = gps_dict.get("GPSLatitude")
    lat_ref = gps_dict.get("GPSLatitudeRef")
    lon_dms = gps_dict.get("GPSLongitude")
    lon_ref = gps_dict.get("GPSLongitudeRef")
    alt_val = gps_dict.get("GPSAltitude")
    alt_ref = gps_dict.get("GPSAltitudeRef", 0)

    latitude = None
    longitude = None
    latitude_dms_str = None
    longitude_dms_str = None
    altitude_str = None

    if lat_dms and lat_ref and lon_dms and lon_ref:
        try:
            latitude = _dms_to_decimal(lat_dms, lat_ref)
            longitude = _dms_to_decimal(lon_dms, lon_ref)
            latitude_dms_str = _dms_to_string(lat_dms, lat_ref)
            longitude_dms_str = _dms_to_string(lon_dms, lon_ref)
        except Exception:
            pass

    if alt_val is not None:
        try:
            alt_m = _ratio_to_float(alt_val)
            if alt_ref == 1:
                alt_m = -alt_m
            altitude_str = f"{alt_m:.1f} m ({alt_m * 3.28084:.1f} ft)"
        except Exception:
            pass

    gps_date = _clean_val(gps_dict.get("GPSDateStamp"))
    gps_time = gps_dict.get("GPSTimeStamp")
    gps_ts_str = None
    if gps_date or gps_time:
        if gps_time and isinstance(gps_time, (tuple, list)):
            t_str = ":".join(f"{int(_ratio_to_float(x)):02d}" for x in gps_time[:3])
            gps_ts_str = f"{gps_date} {t_str} UTC".strip()
        else:
            gps_ts_str = gps_date

    gps_info = GpsMetadata(
        latitude=latitude,
        longitude=longitude,
        latitude_dms=latitude_dms_str,
        longitude_dms=longitude_dms_str,
        altitude=altitude_str,
        timestamp=gps_ts_str,
    )

    return {
        "file_info": file_info,
        "camera_info": camera_info,
        "exposure_info": exposure_info,
        "gps_info": gps_info,
        "raw_exif": raw_tags_list,
    }

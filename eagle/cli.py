from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from eagle import __version__
from eagle.analyzer import (
    AnalysisError,
    DecompressionBombError,
    InvalidImageError,
    analyze_image_file,
)
from eagle.schemas import AnalyzeResponse
from eagle.tui import render_analysis_header, render_startup_screen


def _format_val(val: Optional[object], fallback: str = "Not available") -> str:
    if val is None or val == "" or val == []:
        return fallback
    return str(val)


def render_terminal_report(result: AnalyzeResponse) -> str:
    """Render a clean, human-readable terminal report of the analysis result."""
    lines: list[str] = []

    # Header with preserved ASCII Eagle emblem
    lines.append(render_analysis_header())
    lines.append("")

    # File Section
    lines.append("FILE ───────────────────────────────────────────────────────")
    lines.append(f"  Name        : {result.filename}")
    if result.file_info:
        lines.append(f"  Size        : {result.file_info.formatted_file_size} ({result.file_info.file_size_bytes:,} bytes)")
        lines.append(f"  Format      : {_format_val(result.file_info.format)}")
        lines.append(f"  MIME Type   : {_format_val(result.file_info.mime_type)}")
        if result.file_info.width and result.file_info.height:
            lines.append(f"  Dimensions  : {result.file_info.width} × {result.file_info.height} px")
        else:
            lines.append(f"  Dimensions  : Not available")
        lines.append(f"  Megapixels  : {_format_val(f'{result.file_info.megapixels} MP' if result.file_info.megapixels else None)}")
        lines.append(f"  Color Mode  : {_format_val(result.file_info.color_mode)}")
    else:
        lines.append("  Details     : Not available")
    lines.append("")

    # Camera Section
    lines.append("CAMERA ─────────────────────────────────────────────────────")
    if result.camera_info and any([
        result.camera_info.make,
        result.camera_info.model,
        result.camera_info.lens_model,
        result.camera_info.software,
    ]):
        lines.append(f"  Make        : {_format_val(result.camera_info.make)}")
        lines.append(f"  Model       : {_format_val(result.camera_info.model)}")
        lines.append(f"  Lens        : {_format_val(result.camera_info.lens_model)}")
        lines.append(f"  Software    : {_format_val(result.camera_info.software)}")
    else:
        lines.append("  Make        : Not available")
        lines.append("  Model       : Not available")
        lines.append("  Lens        : Not available")
        lines.append("  Software    : Not available")
    lines.append("")

    # Exposure Section
    lines.append("EXPOSURE ───────────────────────────────────────────────────")
    if result.exposure_info and any([
        result.exposure_info.date_time_original,
        result.exposure_info.exposure_time,
        result.exposure_info.aperture,
        result.exposure_info.iso,
        result.exposure_info.focal_length,
    ]):
        lines.append(f"  Date/Time   : {_format_val(result.exposure_info.date_time_original)}")
        lines.append(f"  Shutter     : {_format_val(result.exposure_info.exposure_time)}")
        lines.append(f"  Aperture    : {_format_val(result.exposure_info.aperture)}")
        lines.append(f"  ISO         : {_format_val(result.exposure_info.iso)}")
        lines.append(f"  Focal Length: {_format_val(result.exposure_info.focal_length)}")
        if result.exposure_info.focal_length_35mm:
            lines.append(f"  35mm Equiv  : {result.exposure_info.focal_length_35mm}")
        if result.exposure_info.exposure_bias:
            lines.append(f"  Bias        : {result.exposure_info.exposure_bias}")
        if result.exposure_info.flash:
            lines.append(f"  Flash       : {result.exposure_info.flash}")
        if result.exposure_info.white_balance:
            lines.append(f"  White Bal.  : {result.exposure_info.white_balance}")
        if result.exposure_info.metering_mode:
            lines.append(f"  Metering    : {result.exposure_info.metering_mode}")
        if result.exposure_info.exposure_program:
            lines.append(f"  Program     : {result.exposure_info.exposure_program}")
    else:
        lines.append("  Date/Time   : Not available")
        lines.append("  Shutter     : Not available")
        lines.append("  Aperture    : Not available")
        lines.append("  ISO         : Not available")
        lines.append("  Focal Length: Not available")
    lines.append("")

    # Location Section
    lines.append("LOCATION ───────────────────────────────────────────────────")
    if result.has_gps and result.gps_info:
        lines.append("  GPS Status  : Available")
        lines.append(f"  Latitude    : {result.latitude:.6f}° ({_format_val(result.gps_info.latitude_dms)})")
        lines.append(f"  Longitude   : {result.longitude:.6f}° ({_format_val(result.gps_info.longitude_dms)})")
        lines.append(f"  Altitude    : {_format_val(result.gps_info.altitude)}")
        lines.append(f"  GPS Time    : {_format_val(result.gps_info.timestamp)}")
        if result.location:
            lines.append(f"  Location    : {_format_val(result.location.display_name)}")
            if result.location.city or result.location.state or result.location.country:
                parts = [p for p in [result.location.city, result.location.state, result.location.country] if p]
                lines.append(f"  Address     : {', '.join(parts)}")
        elif result.geocode_error:
            lines.append(f"  Geocoding   : Error ({result.geocode_error})")
        else:
            lines.append("  Geocoding   : Disabled (use --geocode to resolve address)")
    else:
        lines.append("  GPS Status  : Not available")
    lines.append("")

    # EXIF Summary Section
    lines.append("EXIF ───────────────────────────────────────────────────────")
    tag_count = len(result.raw_exif)
    lines.append(f"  Total Tags  : {tag_count} extracted")
    if tag_count > 0:
        lines.append("  Top Tags    :")
        for tag in result.raw_exif[:8]:
            val_display = tag.value if len(tag.value) <= 45 else tag.value[:42] + "..."
            lines.append(f"    - [{tag.tag_id}] {tag.tag_name:<24}: {val_display}")
        if tag_count > 8:
            lines.append(f"    ... and {tag_count - 8} more tags (use --json to view all)")
    lines.append("────────────────────────────────────────────────────────────")
    lines.append("Analysis complete.")

    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="eagle",
        description="Eagle — Digital Forensics & EXIF/GPS Metadata Extraction CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"Eagle v{__version__} (PyPI: eagle-x)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # analyze subcommand
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze a local image file for forensics and EXIF/GPS metadata",
        description="Read a local image and extract hardware, camera, exposure, GPS, and raw EXIF headers.",
    )
    analyze_parser.add_argument(
        "image",
        type=str,
        help="Path to local image file (JPG, PNG, HEIC, TIFF, WebP, etc.)",
    )
    analyze_parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output raw structured analysis data as JSON to stdout",
    )
    analyze_parser.add_argument(
        "--geocode",
        action="store_true",
        dest="geocode",
        help="Perform reverse geocoding via OpenStreetMap Nominatim if GPS coordinates are present",
    )

    return parser


import io


def safe_print(text: str, file: Optional[Any] = None) -> None:
    """Print text safely across different terminal encodings (e.g. Windows cp1252)."""
    target = file if file is not None else sys.stdout
    try:
        print(text, file=target)
    except UnicodeEncodeError:
        encoding = getattr(target, "encoding", None) or "utf-8"
        encoded = text.encode(encoding, errors="replace").decode(encoding)
        print(encoded, file=target)


def main(args: Optional[list[str]] = None) -> int:
    if isinstance(sys.stdout, io.TextIOWrapper) and hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if isinstance(sys.stderr, io.TextIOWrapper) and hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    parser = build_parser()
    parsed_args = parser.parse_args(args)

    if not parsed_args.command:
        safe_print(render_startup_screen())
        return 0

    if parsed_args.command == "analyze":
        image_path = parsed_args.image
        is_json = parsed_args.json_output
        do_geocode = parsed_args.geocode

        try:
            result = analyze_image_file(
                image_path,
                geocode=do_geocode,
                include_preview=False,
            )
        except FileNotFoundError:
            safe_print(f"Error: File not found: '{image_path}'", file=sys.stderr)
            return 1
        except PermissionError:
            safe_print(f"Error: Permission denied reading: '{image_path}'", file=sys.stderr)
            return 1
        except DecompressionBombError as e:
            safe_print(f"Error: Security limit exceeded - {e}", file=sys.stderr)
            return 1
        except InvalidImageError as e:
            safe_print(f"Error: Invalid image - {e}", file=sys.stderr)
            return 1
        except Exception as e:
            safe_print(f"Error: Analysis failed - {e}", file=sys.stderr)
            return 1

        if is_json:
            # Emit valid JSON strictly to stdout
            safe_print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))
        else:
            safe_print(render_terminal_report(result))

        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())

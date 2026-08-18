from __future__ import annotations

import argparse
import io
import json
import os
import sys
from pathlib import Path
from typing import Any, Optional

from eagle import __version__
from eagle.analyzer import (
    AnalysisError,
    DecompressionBombError,
    InvalidImageError,
    analyze_image_file,
)
from eagle.schemas import AnalyzeResponse
from eagle.tui import (
    BOLD,
    BOLD_PURPLE,
    CYAN,
    DIM_GRAY,
    PURPLE,
    RESET,
    _should_colorize,
    render_analysis_header,
    render_startup_screen,
)


def _format_val(val: Optional[object], fallback: str = "Not available") -> str:
    if val is None or val == "" or val == []:
        return fallback
    return str(val)


def render_terminal_report(result: AnalyzeResponse) -> str:
    """Render a clean, human-readable terminal report of the analysis result."""
    color = _should_colorize()
    p = PURPLE if color else ""
    bp = BOLD_PURPLE if color else ""
    g = DIM_GRAY if color else ""
    b = BOLD if color else ""
    r = RESET if color else ""

    lines: list[str] = []

    # Header with preserved purple ASCII Eagle emblem
    lines.append(render_analysis_header())
    lines.append("")

    # File Section
    lines.append(f"{bp}FILE ───────────────────────────────────────────────────────{r}")
    lines.append(f"  {b}Name{r}        : {result.filename}")
    if result.file_info:
        lines.append(f"  {b}Size{r}        : {result.file_info.formatted_file_size} ({result.file_info.file_size_bytes:,} bytes)")
        lines.append(f"  {b}Format{r}      : {_format_val(result.file_info.format)}")
        lines.append(f"  {b}MIME Type{r}   : {_format_val(result.file_info.mime_type)}")
        if result.file_info.width and result.file_info.height:
            lines.append(f"  {b}Dimensions{r}  : {result.file_info.width} × {result.file_info.height} px")
        else:
            lines.append(f"  {b}Dimensions{r}  : Not available")
        lines.append(f"  {b}Megapixels{r}  : {_format_val(f'{result.file_info.megapixels} MP' if result.file_info.megapixels else None)}")
        lines.append(f"  {b}Color Mode{r}  : {_format_val(result.file_info.color_mode)}")
    else:
        lines.append(f"  {b}Details{r}     : Not available")
    lines.append("")

    # Camera Section
    lines.append(f"{bp}CAMERA ─────────────────────────────────────────────────────{r}")
    if result.camera_info and any([
        result.camera_info.make,
        result.camera_info.model,
        result.camera_info.lens_model,
        result.camera_info.software,
    ]):
        lines.append(f"  {b}Make{r}        : {_format_val(result.camera_info.make)}")
        lines.append(f"  {b}Model{r}       : {_format_val(result.camera_info.model)}")
        lines.append(f"  {b}Lens{r}        : {_format_val(result.camera_info.lens_model)}")
        lines.append(f"  {b}Software{r}    : {_format_val(result.camera_info.software)}")
    else:
        lines.append(f"  {b}Make{r}        : Not available")
        lines.append(f"  {b}Model{r}       : Not available")
        lines.append(f"  {b}Lens{r}        : Not available")
        lines.append(f"  {b}Software{r}    : Not available")
    lines.append("")

    # Exposure Section
    lines.append(f"{bp}EXPOSURE ───────────────────────────────────────────────────{r}")
    if result.exposure_info and any([
        result.exposure_info.date_time_original,
        result.exposure_info.exposure_time,
        result.exposure_info.aperture,
        result.exposure_info.iso,
        result.exposure_info.focal_length,
    ]):
        lines.append(f"  {b}Date/Time{r}   : {_format_val(result.exposure_info.date_time_original)}")
        lines.append(f"  {b}Shutter{r}     : {_format_val(result.exposure_info.exposure_time)}")
        lines.append(f"  {b}Aperture{r}    : {_format_val(result.exposure_info.aperture)}")
        lines.append(f"  {b}ISO{r}         : {_format_val(result.exposure_info.iso)}")
        lines.append(f"  {b}Focal Length{r}: {_format_val(result.exposure_info.focal_length)}")
        if result.exposure_info.focal_length_35mm:
            lines.append(f"  {b}35mm Equiv{r}  : {result.exposure_info.focal_length_35mm}")
        if result.exposure_info.exposure_bias:
            lines.append(f"  {b}Bias{r}        : {result.exposure_info.exposure_bias}")
        if result.exposure_info.flash:
            lines.append(f"  {b}Flash{r}       : {result.exposure_info.flash}")
        if result.exposure_info.white_balance:
            lines.append(f"  {b}White Bal.{r}  : {result.exposure_info.white_balance}")
        if result.exposure_info.metering_mode:
            lines.append(f"  {b}Metering{r}    : {result.exposure_info.metering_mode}")
        if result.exposure_info.exposure_program:
            lines.append(f"  {b}Program{r}     : {result.exposure_info.exposure_program}")
    else:
        lines.append(f"  {b}Date/Time{r}   : Not available")
        lines.append(f"  {b}Shutter{r}     : Not available")
        lines.append(f"  {b}Aperture{r}    : Not available")
        lines.append(f"  {b}ISO{r}         : Not available")
        lines.append(f"  {b}Focal Length{r}: Not available")
    lines.append("")

    # Location Section
    lines.append(f"{bp}LOCATION ───────────────────────────────────────────────────{r}")
    if result.has_gps and result.gps_info:
        lines.append(f"  {b}GPS Status{r}  : {p}Available{r}")
        lines.append(f"  {b}Latitude{r}    : {result.latitude:.6f}° ({_format_val(result.gps_info.latitude_dms)})")
        lines.append(f"  {b}Longitude{r}   : {result.longitude:.6f}° ({_format_val(result.gps_info.longitude_dms)})")
        lines.append(f"  {b}Altitude{r}    : {_format_val(result.gps_info.altitude)}")
        lines.append(f"  {b}GPS Time{r}    : {_format_val(result.gps_info.timestamp)}")
        if result.location:
            lines.append(f"  {b}Location{r}    : {_format_val(result.location.display_name)}")
            if result.location.city or result.location.state or result.location.country:
                parts = [part for part in [result.location.city, result.location.state, result.location.country] if part]
                lines.append(f"  {b}Address{r}     : {', '.join(parts)}")
        elif result.geocode_error:
            lines.append(f"  {b}Geocoding{r}   : Error ({result.geocode_error})")
        else:
            lines.append(f"  {b}Geocoding{r}   : Disabled (use --geocode to resolve address)")
    else:
        lines.append(f"  {b}GPS Status{r}  : Not available")
    lines.append("")

    # EXIF Summary Section
    lines.append(f"{bp}EXIF ───────────────────────────────────────────────────────{r}")
    tag_count = len(result.raw_exif)
    lines.append(f"  {b}Total Tags{r}  : {tag_count} extracted")
    if tag_count > 0:
        lines.append(f"  {b}Top Tags{r}    :")
        for tag in result.raw_exif[:8]:
            val_display = tag.value if len(tag.value) <= 45 else tag.value[:42] + "..."
            lines.append(f"    - [{tag.tag_id}] {tag.tag_name:<24}: {val_display}")
        if tag_count > 8:
            lines.append(f"    ... and {tag_count - 8} more tags (use --json to view all)")
    lines.append(f"{bp}────────────────────────────────────────────────────────────{r}")
    lines.append(f"{p}Analysis complete.{r}")

    return "\n".join(lines)


def _configure_hunt_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "image",
        type=str,
        help="Path to local image file (JPG, PNG, HEIC, TIFF, WebP, etc.)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output raw structured telemetry stream as JSON to stdout",
    )
    parser.add_argument(
        "--geocode",
        action="store_true",
        dest="geocode",
        help="Perform reverse geocoding on GPS coordinates via OpenStreetMap Nominatim",
    )


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

    # Primary eagle predator action: hunt
    hunt_parser = subparsers.add_parser(
        "hunt",
        help="Hunt down EXIF/GPS metadata and forensic telemetry from an image",
        description="Lock on a local image and rip hardware, camera, exposure, GPS, and raw EXIF headers.",
    )
    _configure_hunt_args(hunt_parser)

    # Aliases for different predator actions & backward compatibility
    for action in ["strike", "rip", "scan", "talon", "swoop", "analyze"]:
        alias_parser = subparsers.add_parser(
            action,
            help=f"Alias for 'eagle hunt'",
            description=f"Analyze local image (alias for 'eagle hunt').",
        )
        _configure_hunt_args(alias_parser)

    return parser


def safe_print(text: str, file: Optional[Any] = None) -> None:
    """Print text safely across different terminal encodings (e.g. Windows cp1252)."""
    target = file if file is not None else sys.stdout
    try:
        print(text, file=target)
    except UnicodeEncodeError:
        encoding = getattr(target, "encoding", None) or "utf-8"
        encoded = text.encode(encoding, errors="replace").decode(encoding)
        print(encoded, file=target)


HUNT_COMMANDS = {"hunt", "strike", "rip", "scan", "talon", "swoop", "analyze"}


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

    if parsed_args.command in HUNT_COMMANDS:
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

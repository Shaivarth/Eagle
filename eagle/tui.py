from __future__ import annotations

import os
import sys
from typing import Optional

from eagle import __version__
from eagle.schemas import AnalyzeResponse

# Exact website accent purple from index.css (--accent: #b892ff -> rgb(184, 146, 255))
PURPLE = "\033[38;2;184;146;255m"
BOLD_PURPLE = "\033[1;38;2;184;146;255m"
CYAN = "\033[38;2;140;200;255m"
DIM_GRAY = "\033[38;2;128;128;128m"
BOLD = "\033[1m"
RESET = "\033[0m"


def _should_colorize() -> bool:
    """Determine if ANSI color codes should be used."""
    if os.getenv("NO_COLOR"):
        return False
    return True


# Original Eagle ASCII artwork preserved exactly from frontend/src/components/EagleEmblem.tsx
EAGLE_ASCII_ART = """                        z$b
               .e$$$b.  $$$F  .d$$be
           .d$$$$$$$$$$e$$$be$$$$$$$$$$e.
       .e$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$b.
     z$$$$$$$P**""**$$$$$$$$$$$P*\"\"\"\"***$$$$$b.
   z$$$$*"            "$$$$$$"            "*$$$$c
 z$$*"                 ^$$$$                  "*$$.
^"                      $$$F                      ^%
                        $$$b
                        $P*$
                       4P  *r
                       4    %"""


def _box_line(text: str, width: int = 60) -> str:
    """Center text inside box borders with exact width calculation."""
    padding = width - len(text)
    if padding < 0:
        text = text[:width]
        padding = 0
    left = padding // 2
    right = padding - left
    return f"║{' ' * left}{text}{' ' * right}║"


def render_startup_screen() -> str:
    """Render the startup welcome screen featuring the purple Eagle ASCII emblem,

    pixel-perfect box, version metadata, and hunting navigation menu.
    """
    color = _should_colorize()
    p = PURPLE if color else ""
    bp = BOLD_PURPLE if color else ""
    g = DIM_GRAY if color else ""
    r = RESET if color else ""

    lines: list[str] = []
    # Colored ASCII Eagle
    lines.append(f"{p}{EAGLE_ASCII_ART}{r}")
    lines.append("")

    # Perfectly aligned box (Inner width 60 chars)
    lines.append(f"{p}╔{'═' * 60}╗{r}")
    lines.append(f"{p}{_box_line('EAGLE', 60)}{r}")
    lines.append(f"{p}{_box_line(f'IMAGE INTELLIGENCE & FORENSICS (v{__version__})', 60)}{r}")
    lines.append(f"{p}{_box_line('github.com/shaivarth', 60)}{r}")
    lines.append(f"{p}╚{'═' * 60}╝{r}")
    lines.append("")

    # Eagle-themed commands
    lines.append(f"{bp}COMMANDS & HUNTING ACTIONS:{r}")
    lines.append(f"  {p}eagle hunt <image>{r}            Lock on target image & extract deep EXIF/GPS telemetry")
    lines.append(f"  {p}eagle hunt <image> --json{r}     Output raw telemetry stream as JSON to stdout")
    lines.append(f"  {p}eagle hunt <image> --geocode{r}  Track GPS coordinates via reverse geocoding")
    lines.append(f"  {p}eagle --help{r}                  Show flight manual and options")
    lines.append(f"  {p}eagle --version{r}               Show current version")
    lines.append("")
    lines.append(f"{bp}UPGRADE:{r}")
    lines.append(f"  {p}pip install --upgrade eagle-x{r}")
    lines.append("")
    lines.append(f"{g}Aliases: 'eagle strike', 'eagle rip', 'eagle scan', 'eagle analyze'{r}")
    lines.append("")

    return "\n".join(lines)


def render_analysis_header() -> str:
    """Render header before analysis output with the purple Eagle ASCII emblem."""
    color = _should_colorize()
    p = PURPLE if color else ""
    r = RESET if color else ""

    lines: list[str] = []
    lines.append(f"{p}{EAGLE_ASCII_ART}{r}")
    lines.append("")
    lines.append(f"{p}╔{'═' * 60}╗{r}")
    lines.append(f"{p}{_box_line('EAGLE', 60)}{r}")
    lines.append(f"{p}{_box_line('IMAGE INTELLIGENCE & FORENSICS', 60)}{r}")
    lines.append(f"{p}{_box_line('github.com/shaivarth', 60)}{r}")
    lines.append(f"{p}╚{'═' * 60}╝{r}")
    return "\n".join(lines)

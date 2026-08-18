from __future__ import annotations

import sys
from typing import Optional

from eagle import __version__
from eagle.schemas import AnalyzeResponse

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


def render_startup_screen() -> str:
    """Render the startup welcome screen featuring the original Eagle ASCII emblem,

    version metadata, and quick navigation menu.
    """
    lines: list[str] = []
    lines.append(EAGLE_ASCII_ART)
    lines.append("")
    lines.append("╔══════════════════════════════════════════════════════════════╗")
    lines.append("║                           EAGLE                              ║")
    lines.append(f"║        IMAGE INTELLIGENCE & FORENSICS (v{__version__:<18}) ║")
    lines.append("╚══════════════════════════════════════════════════════════════╝")
    lines.append("")
    lines.append("COMMANDS & USAGE:")
    lines.append("  eagle analyze <image>            Run deep forensics & metadata extraction")
    lines.append("  eagle analyze <image> --json     Output structured JSON to stdout")
    lines.append("  eagle analyze <image> --geocode  Perform reverse geocoding on GPS coordinates")
    lines.append("  eagle --help                     Show detailed options and arguments")
    lines.append("  eagle --version                  Show current version")
    lines.append("")
    return "\n".join(lines)


def render_analysis_header() -> str:
    """Render header before analysis output."""
    lines: list[str] = []
    lines.append(EAGLE_ASCII_ART)
    lines.append("")
    lines.append("╔══════════════════════════════════════════════════════════════╗")
    lines.append("║                           EAGLE                              ║")
    lines.append("║              IMAGE INTELLIGENCE & FORENSICS                  ║")
    lines.append("╚══════════════════════════════════════════════════════════════╝")
    return "\n".join(lines)

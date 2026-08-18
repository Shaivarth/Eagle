from __future__ import annotations

import json
from pathlib import Path
import pytest
from PIL import Image

from eagle.cli import main


def test_cli_no_args_shows_startup_screen(capsys):
    ret = main([])
    assert ret == 0
    captured = capsys.readouterr()
    assert "EAGLE" in captured.out
    assert "IMAGE INTELLIGENCE & FORENSICS" in captured.out
    assert "COMMANDS & HUNTING ACTIONS:" in captured.out
    # Verify exact ASCII artwork signature elements
    assert "z$b" in captured.out
    assert ".d$$$$$$$$$$e$$$be$$$$$$$$$$e." in captured.out


def test_cli_help(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["--help"])
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "Eagle" in captured.out
    assert "hunt" in captured.out


def test_cli_version(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["--version"])
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "Eagle v1.0.0" in captured.out


def test_cli_hunt_terminal_output(tmp_path: Path, capsys):
    img_path = tmp_path / "cli_test.jpg"
    img = Image.new("RGB", (100, 100), color=(10, 20, 30))
    img.save(img_path, format="JPEG")

    ret = main(["hunt", str(img_path)])
    assert ret == 0
    captured = capsys.readouterr()
    assert "IMAGE INTELLIGENCE & FORENSICS" in captured.out
    assert "cli_test.jpg" in captured.out
    assert "100 × 100 px" in captured.out
    assert "Analysis complete." in captured.out


def test_cli_aliases(tmp_path: Path, capsys):
    img_path = tmp_path / "alias_test.jpg"
    img = Image.new("RGB", (80, 80), color=(10, 20, 30))
    img.save(img_path, format="JPEG")

    for cmd in ["strike", "rip", "scan", "analyze"]:
        ret = main([cmd, str(img_path)])
        assert ret == 0


def test_cli_hunt_json_output(tmp_path: Path, capsys):
    img_path = tmp_path / "cli_json_test.png"
    img = Image.new("RGB", (150, 75), color=(50, 50, 50))
    img.save(img_path, format="PNG")

    ret = main(["hunt", str(img_path), "--json"])
    assert ret == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["filename"] == "cli_json_test.png"
    assert data["file_info"]["width"] == 150
    assert data["file_info"]["height"] == 75
    assert data["file_info"]["format"] == "PNG"


def test_cli_non_existent_file(capsys):
    ret = main(["hunt", "does_not_exist_file_99.jpg"])
    assert ret == 1
    captured = capsys.readouterr()
    assert "Error: File not found" in captured.err


def test_cli_invalid_image(tmp_path: Path, capsys):
    bad_file = tmp_path / "bad.txt"
    bad_file.write_text("not an image")

    ret = main(["hunt", str(bad_file)])
    assert ret == 1
    captured = capsys.readouterr()
    assert "Error: Invalid image" in captured.err

from __future__ import annotations

import io
from pathlib import Path
import pytest
from PIL import Image
from PIL.TiffImagePlugin import IFDRational

from eagle import (
    AnalysisError,
    DecompressionBombError,
    InvalidImageError,
    analyze_image,
    analyze_image_bytes,
    analyze_image_file,
)


@pytest.fixture
def sample_image_no_exif(tmp_path: Path) -> Path:
    img_path = tmp_path / "plain_image.png"
    img = Image.new("RGB", (200, 100), color=(73, 109, 137))
    img.save(img_path, format="PNG")
    return img_path


@pytest.fixture
def sample_image_with_exif(tmp_path: Path) -> Path:
    img_path = tmp_path / "photo_with_exif.jpg"
    img = Image.new("RGB", (300, 200), color=(255, 128, 0))
    exif = Image.Exif()
    exif[0x010F] = "EagleTestMake"
    exif[0x0110] = "EagleTestModel"
    exif[0x0131] = "EagleOS 1.0"

    # Exif IFD
    exif[0x8769] = {
        0x9003: "2026:01:01 12:00:00",
        0x829A: IFDRational(1, 100),  # 1/100s
        0x829D: IFDRational(28, 10),  # f/2.8
        0x8827: 200,                  # ISO 200
        0x920A: IFDRational(50, 1),   # 50mm
    }

    # GPS IFD
    exif[0x8825] = {
        1: "N",
        2: (IFDRational(37, 1), IFDRational(46, 1), IFDRational(2964, 100)),  # 37° 46' 29.64" N -> 37.7749
        3: "W",
        4: (IFDRational(122, 1), IFDRational(25, 1), IFDRational(984, 100)),  # 122° 25' 09.84" W -> -122.4194
        6: IFDRational(152, 10),                                              # 15.2m altitude
        29: "2026:01:01",
    }

    img.save(img_path, format="JPEG", exif=exif.tobytes())
    return img_path


def test_analyze_image_no_exif(sample_image_no_exif: Path):
    result = analyze_image_file(sample_image_no_exif)
    assert result.filename == "plain_image.png"
    assert result.has_gps is False
    assert result.latitude is None
    assert result.longitude is None
    assert result.file_info is not None
    assert result.file_info.width == 200
    assert result.file_info.height == 100
    assert result.file_info.format == "PNG"
    assert result.camera_info.make is None


def test_analyze_image_with_exif_and_gps(sample_image_with_exif: Path):
    result = analyze_image_file(sample_image_with_exif)
    assert result.filename == "photo_with_exif.jpg"
    assert result.has_gps is True
    assert result.latitude is not None
    assert abs(result.latitude - 37.7749) < 0.001
    assert result.longitude is not None
    assert abs(result.longitude - (-122.4194)) < 0.001

    assert result.camera_info.make == "EagleTestMake"
    assert result.camera_info.model == "EagleTestModel"
    assert result.camera_info.software == "EagleOS 1.0"

    assert result.exposure_info.date_time_original == "2026:01:01 12:00:00"
    assert result.exposure_info.exposure_time == "1/100 s"
    assert result.exposure_info.aperture == "f/2.8"
    assert result.exposure_info.iso == "ISO 200"
    assert result.exposure_info.focal_length == "50 mm"

    assert result.gps_info is not None
    assert "37°" in (result.gps_info.latitude_dms or "")
    assert "15.2 m" in (result.gps_info.altitude or "")


def test_analyze_non_existent_file():
    with pytest.raises(FileNotFoundError):
        analyze_image_file("non_existent_image_12345.jpg")


def test_analyze_invalid_image_file(tmp_path: Path):
    bad_file = tmp_path / "not_an_image.txt"
    bad_file.write_text("Hello, this is just plain text.")
    with pytest.raises(InvalidImageError):
        analyze_image_file(bad_file)


def test_analyze_bytes(sample_image_with_exif: Path):
    data = sample_image_with_exif.read_bytes()
    result = analyze_image_bytes(data, filename="memory_test.jpg")
    assert result.filename == "memory_test.jpg"
    assert result.has_gps is True
    assert result.camera_info.make == "EagleTestMake"


def test_unified_analyze_entrypoint(sample_image_no_exif: Path):
    # Test path string
    r1 = analyze_image(str(sample_image_no_exif))
    assert r1.file_info.format == "PNG"

    # Test Path object
    r2 = analyze_image(sample_image_no_exif)
    assert r2.file_info.format == "PNG"

    # Test bytes
    r3 = analyze_image(sample_image_no_exif.read_bytes(), filename="test.png")
    assert r3.file_info.format == "PNG"

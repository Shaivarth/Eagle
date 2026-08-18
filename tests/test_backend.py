from __future__ import annotations

import io
import sys
from pathlib import Path

# Ensure backend directory is in sys.path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from PIL import Image

from app.main import app

client = TestClient(app)


def test_backend_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_backend_analyze_image(tmp_path: Path):
    # Create an in-memory image
    buf = io.BytesIO()
    img = Image.new("RGB", (120, 80), color=(100, 150, 200))
    img.save(buf, format="JPEG")
    buf.seek(0)

    response = client.post(
        "/api/analyze",
        files={"file": ("test_upload.jpg", buf, "image/jpeg")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test_upload.jpg"
    assert data["has_gps"] is False
    assert data["file_info"]["width"] == 120
    assert data["file_info"]["height"] == 80
    assert data["file_info"]["format"] == "JPEG"


def test_backend_analyze_empty_file():
    response = client.post(
        "/api/analyze",
        files={"file": ("empty.jpg", io.BytesIO(b""), "image/jpeg")},
    )
    assert response.status_code == 400
    assert "Uploaded file is empty" in response.json()["detail"]


def test_backend_analyze_invalid_format():
    response = client.post(
        "/api/analyze",
        files={"file": ("not_image.txt", io.BytesIO(b"hello world"), "text/plain")},
    )
    assert response.status_code == 415

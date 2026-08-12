from __future__ import annotations

import logging

import httpx
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.exif_utils import extract_full_metadata
from app.geocode import reverse_geocode
from app.schemas import AnalyzeResponse

logger = logging.getLogger("eagle")

app = FastAPI(
    title="Eagle API",
    description="Extracts GPS EXIF data and comprehensive metadata from images (JPG, PNG, HEIC).",
    version="1.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_UPLOAD_BYTES = 25 * 1024 * 1024


@app.get("/api/health")
async def health_check() -> dict:
    return {"status": "ok"}


@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_image(file: UploadFile = File(...)) -> AnalyzeResponse:
    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if len(image_bytes) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Image exceeds 25 MB limit.")

    filename = file.filename or "unknown"
    full_meta = extract_full_metadata(image_bytes, filename)

    if full_meta["file_info"].format is None:
        raise HTTPException(
            status_code=415,
            detail=f"The uploaded file '{filename}' could not be decoded as a valid image (JPG, PNG, HEIC).",
        )

    gps_info = full_meta["gps_info"]
    has_gps = bool(gps_info and gps_info.latitude is not None and gps_info.longitude is not None)

    latitude = gps_info.latitude if has_gps else None
    longitude = gps_info.longitude if has_gps else None
    location = None
    geocode_error = None

    if has_gps and latitude is not None and longitude is not None:
        try:
            location = await reverse_geocode(latitude, longitude)
        except (httpx.HTTPError, httpx.TimeoutException) as exc:
            logger.warning("Reverse geocoding failed: %s", exc)
            geocode_error = "Coordinates were found, but reverse geocoding failed."

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

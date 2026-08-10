from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel


class LocationInfo(BaseModel):
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    display_name: Optional[str] = None


class ImageFileInfo(BaseModel):
    file_size_bytes: int
    formatted_file_size: str
    format: Optional[str] = None
    mime_type: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    megapixels: Optional[float] = None
    color_mode: Optional[str] = None


class CameraInfo(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    lens_model: Optional[str] = None
    software: Optional[str] = None


class ExposureInfo(BaseModel):
    date_time_original: Optional[str] = None
    exposure_time: Optional[str] = None
    aperture: Optional[str] = None
    iso: Optional[str] = None
    focal_length: Optional[str] = None
    focal_length_35mm: Optional[str] = None
    exposure_bias: Optional[str] = None
    flash: Optional[str] = None
    white_balance: Optional[str] = None
    metering_mode: Optional[str] = None
    exposure_program: Optional[str] = None


class GpsMetadata(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    latitude_dms: Optional[str] = None
    longitude_dms: Optional[str] = None
    altitude: Optional[str] = None
    timestamp: Optional[str] = None


class RawExifTag(BaseModel):
    tag_id: str
    tag_name: str
    value: str


class AnalyzeResponse(BaseModel):
    filename: str
    has_gps: bool
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location: Optional[LocationInfo] = None
    geocode_error: Optional[str] = None
    file_info: Optional[ImageFileInfo] = None
    camera_info: Optional[CameraInfo] = None
    exposure_info: Optional[ExposureInfo] = None
    gps_info: Optional[GpsMetadata] = None
    raw_exif: List[RawExifTag] = []


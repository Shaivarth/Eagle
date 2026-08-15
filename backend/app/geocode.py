from __future__ import annotations

import asyncio
import os
import time
from typing import Dict, Optional, Tuple

import httpx

from app.schemas import LocationInfo

NOMINATIM_URL = "https://nominatim.openstreetmap.org/reverse"
CONTACT_EMAIL = os.getenv("NOMINATIM_CONTACT_EMAIL", "local-dev@eagle.app")
USER_AGENT = os.getenv("NOMINATIM_USER_AGENT", f"Eagle/1.0 (EXIF location viewer; contact: {CONTACT_EMAIL})")

# Cache reverse geocode results keyed by coordinates rounded to 4 decimal places (~11m accuracy)
_GEOCODE_CACHE: Dict[Tuple[float, float], LocationInfo] = {}
_LAST_REQUEST_TIME: float = 0.0
_RATE_LIMIT_LOCK = asyncio.Lock()
_MIN_REQUEST_INTERVAL: float = 1.0  # Nominatim usage policy requires <= 1 request/sec


async def reverse_geocode(latitude: float, longitude: float) -> LocationInfo:
    # 4 decimal places is ~11 meters resolution, ideal for cache hits on near-identical coordinates
    cache_key = (round(latitude, 4), round(longitude, 4))
    if cache_key in _GEOCODE_CACHE:
        return _GEOCODE_CACHE[cache_key]

    params = {
        "lat": latitude,
        "lon": longitude,
        "format": "jsonv2",
        "zoom": 10,
        "addressdetails": 1,
    }
    headers = {"User-Agent": USER_AGENT}

    # Enforce Nominatim 1 request per second rate limit
    global _LAST_REQUEST_TIME
    async with _RATE_LIMIT_LOCK:
        now = time.monotonic()
        elapsed = now - _LAST_REQUEST_TIME
        if elapsed < _MIN_REQUEST_INTERVAL:
            await asyncio.sleep(_MIN_REQUEST_INTERVAL - elapsed)
        _LAST_REQUEST_TIME = time.monotonic()

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(NOMINATIM_URL, params=params, headers=headers)
            response.raise_for_status()
            payload = response.json()

    address = payload.get("address", {})

    city: Optional[str] = (
        address.get("city")
        or address.get("town")
        or address.get("village")
        or address.get("municipality")
        or address.get("county")
    )
    state: Optional[str] = address.get("state") or address.get("region")
    country: Optional[str] = address.get("country")
    display_name: Optional[str] = payload.get("display_name")

    result = LocationInfo(
        city=city, state=state, country=country, display_name=display_name
    )

    # Store in memory cache (cap size to prevent unbounded memory growth)
    if len(_GEOCODE_CACHE) > 1000:
        _GEOCODE_CACHE.clear()
    _GEOCODE_CACHE[cache_key] = result

    return result


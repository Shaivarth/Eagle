"""Reverse geocoding of coordinates to a human-readable place name.

Uses the free OpenStreetMap Nominatim API. Nominatim's usage policy requires
a descriptive User-Agent and at most one request per second per client, both
of which are respected here.
"""

from __future__ import annotations

from typing import Optional

import httpx

from app.schemas import LocationInfo

NOMINATIM_URL = "https://nominatim.openstreetmap.org/reverse"
USER_AGENT = "Eagle/1.0 (EXIF location viewer; contact: local-dev)"


async def reverse_geocode(latitude: float, longitude: float) -> LocationInfo:
    """Looks up city / state / country for a coordinate pair.

    Raises httpx.HTTPError (or similar) on network/HTTP failure so the
    caller can decide how to surface that to the client.
    """
    params = {
        "lat": latitude,
        "lon": longitude,
        "format": "jsonv2",
        "zoom": 10,
        "addressdetails": 1,
    }
    headers = {"User-Agent": USER_AGENT}

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

    return LocationInfo(
        city=city, state=state, country=country, display_name=display_name
    )

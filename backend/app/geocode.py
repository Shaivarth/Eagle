from __future__ import annotations

# Re-export reverse geocoding from eagle.geocode for full backwards compatibility
from eagle.geocode import (
    CONTACT_EMAIL,
    NOMINATIM_URL,
    USER_AGENT,
    LocationInfo,
    reverse_geocode_async as reverse_geocode,
)

__all__ = [
    "reverse_geocode",
    "LocationInfo",
    "NOMINATIM_URL",
    "USER_AGENT",
    "CONTACT_EMAIL",
]

# Eagle Architecture & CLI Integration Design

## Overview
This document details the architectural audit and decoupling strategy for **Eagle** (Photo EXIF & GPS Location Extraction Utility) to support both the existing web application (FastAPI + React) and a standalone Python command-line interface (`eagle`) packaged as `eagle-x` on PyPI.

---

## 1. Repository Audit Summary

### 1.1 Existing Structure
```
georeveal/
├── assets/
│   └── demo.gif
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── exif_utils.py       # EXIF extraction and formatting logic
│   │   ├── geocode.py          # Nominatim reverse geocoding
│   │   ├── main.py             # FastAPI routes & upload handling
│   │   └── schemas.py          # Pydantic schemas (ImageFileInfo, CameraInfo, etc.)
│   └── requirements.txt        # fastapi, uvicorn, Pillow, httpx, pillow-heif, python-multipart
├── frontend/
│   ├── src/                    # React + Vite frontend
│   └── package.json
├── README.md
└── .gitignore
```

### 1.2 Reusable Core Logic
The following functionality is currently implemented in `backend/app/` and is completely independent of FastAPI/HTTP:
1. **Metadata & EXIF Extraction (`exif_utils.py`)**:
   - PIL and `pillow_heif` initialization.
   - Decompression bomb guard (`100_000_000` pixels limit).
   - Image format detection, resolution, file size formatting, color mode, megapixels calculation.
   - EXIF tag parsing from standard tags, `ExifOffset` IFD, and `GPSInfo` IFD.
   - Hardware extraction (Make, Model, Lens Model, Software).
   - Exposure settings parsing (Shutter Speed formatting, Aperture, ISO, Focal Length, Exposure Bias, Flash, White Balance, Metering Mode, Exposure Program).
   - GPS coordinate extraction (DMS to decimal degrees, DMS formatting, Altitude, Timestamp).
   - Raw EXIF key-value extraction with hex IDs.
2. **Reverse Geocoding (`geocode.py`)**:
   - OpenStreetMap Nominatim reverse geocoding via HTTP (`httpx`).
   - Rate limiting (enforcing $\le 1$ req/sec) and in-memory coordinates caching.
3. **Data Models (`schemas.py`)**:
   - Pydantic models: `ImageFileInfo`, `CameraInfo`, `ExposureInfo`, `GpsMetadata`, `LocationInfo`, `RawExifTag`, `AnalyzeResponse`.

### 1.3 Web-Coupled Logic
1. **FastAPI Endpoints (`backend/app/main.py`)**:
   - Streaming multipart chunk uploads with a 25MB limit.
   - HTTP status code mapping (`400`, `413`, `415`).
   - CORS middleware for React frontend.
   - Base64 preview generation for web rendering.

---

## 2. Target Architecture

The core philosophy is **Single Source of Truth** for image forensics. The core package (`eagle`) contains zero web framework dependencies.

```
                  ┌───────────────────────────────┐
                  │          Eagle Core           │
                  │   (Metadata, GPS, Schemas)    │
                  └───────────────┬───────────────┘
                                  │
                 ┌────────────────┴────────────────┐
                 ▼                                 ▼
    ┌─────────────────────────┐       ┌─────────────────────────┐
    │       Eagle CLI         │       │     FastAPI Backend     │
    │ (Terminal / JSON output)│       │  (HTTP / Multipart API) │
    └─────────────────────────┘       └────────────┬────────────┘
                                                   │
                                                   ▼
                                      ┌─────────────────────────┐
                                      │      React Frontend     │
                                      │   (Web UI & Leaflet Map)│
                                      └─────────────────────────┘
```

### 2.1 File & Module Organization
```
Eagle/
├── eagle/                      # Reusable Python Package (PyPI: eagle-x)
│   ├── __init__.py             # Exposes version, public API
│   ├── __main__.py             # python -m eagle support
│   ├── analyzer.py             # High-level analysis API (file & bytes)
│   ├── exif_utils.py           # Core EXIF & image metadata parser
│   ├── geocode.py              # Nominatim geocoder (sync & async)
│   ├── schemas.py              # Pydantic data models
│   └── cli.py                  # CLI command implementation
├── backend/
│   └── app/                    # FastAPI web app (imports from `eagle`)
│       ├── __init__.py
│       ├── main.py             # API routes
│       ├── schemas.py          # Re-exports from eagle.schemas
│       ├── exif_utils.py       # Re-exports from eagle.exif_utils
│       └── geocode.py          # Re-exports from eagle.geocode
├── frontend/                   # Existing React frontend (untouched)
├── tests/                      # CLI and core test suite
├── docs/
│   └── CLI_ARCHITECTURE.md
├── pyproject.toml              # Modern build config for eagle-x
├── LICENSE                     # MIT License
└── README.md                   # Updated dual-interface documentation
```

---

## 3. Dependency Separation

| Tier | Dependencies | Purpose |
|------|-------------|---------|
| **Eagle Core (`eagle-x`)** | `Pillow>=10.4.0`<br>`pillow-heif>=0.18.0`<br>`pydantic>=2.0.0`<br>`httpx>=0.27.0` | Core image decoding, HEIC support, EXIF parsing, schemas, optional geocoding. |
| **Server Extras (`server`)** | `fastapi>=0.115.0`<br>`uvicorn[standard]>=0.30.6`<br>`python-multipart>=0.0.9` | Running the web backend. |
| **Frontend** | React, Vite, Leaflet | Browser UI. |

---

## 4. CLI Design & Specification

### 4.1 Invocation Syntax
- Direct command: `eagle analyze <IMAGE_PATH> [--json] [--geocode]`
- Python module: `python -m eagle analyze <IMAGE_PATH> [--json] [--geocode]`
- Version check: `eagle --version`
- Help: `eagle --help`

### 4.2 Terminal Output Behavior
- **Default (Interactive / Text)**:
  - Formatted forensics report with banner, file details, camera specs, exposure settings, GPS coordinates, geocoded address (if requested), and raw EXIF summary.
  - Graceful handling of absent metadata (e.g. `Not available`).
- **Machine-Readable (`--json`)**:
  - Valid JSON written strictly to `stdout`.
  - Reuses Pydantic model serialization (`model_dump()`).
  - Diagnostic/error messages routed strictly to `stderr` to avoid breaking JSON pipelines (e.g. `jq`, scripts).

---

## 5. Security & Safety Review
1. **Decompression Bomb Protection**: PIL and HEIF dimensions are verified with a 100 Megapixel limit to prevent memory exhaustion attacks.
2. **Path Traversal & File Safety**: CLI resolves and validates input paths strictly through `pathlib.Path.resolve()`, checking existence and read permissions.
3. **No Unsafe Execution**: No `eval`, `pickle`, or `subprocess` execution.
4. **Privacy First**: By default, image analysis is 100% offline and local. No image bytes or metadata are transmitted externally unless `--geocode` is explicitly supplied to query OpenStreetMap Nominatim.

<h2 align="center">EAGLE</h2>

<div align="center">

<table>
  <tr>
    <td width="70%" valign="top">
      <h3>Photo EXIF & GPS Location Extraction Utility</h3>
      <blockquote>
        An OSINT and digital forensics utility that rips open raw image headers, extracts deep EXIF metadata, camera hardware specs, and precise GPS coordinates, reverse-geocodes the location, and outputs structured intelligence to the terminal, JSON, or an interactive web map.
      </blockquote>
      <p>
        <img src="https://img.shields.io/badge/PyPI-eagle--x-3776AB?style=flat-square&logo=pypi&logoColor=white" alt="PyPI" />
        <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
        <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" />
        <img src="https://img.shields.io/badge/Mapping-Leaflet-199900?style=flat-square&logo=leaflet&logoColor=white" alt="Leaflet" />
        <img src="https://img.shields.io/badge/Parser-Pillow_&_HEIF-E95420?style=flat-square" alt="Pillow HEIF" />
        <img src="https://img.shields.io/badge/License-MIT-blue?style=flat-square" alt="MIT License" />
      </p>
    </td>
    <td width="30%" align="center" valign="middle">
      <img src="frontend/public/Eagle.png" alt="Eagle Logo" width="220" />
    </td>
  </tr>
</table>

</div>

---

<p align="center">
  <img src="assets/demo.gif" alt="Eagle Demo" width="100%" max-width="800px" style="border-radius: 8px;" />
</p>

---

## ⚡ Quick Start: Command-Line Interface (CLI)

Eagle is distributed on PyPI as [`eagle-x`](https://pypi.org/project/eagle-x/) and provides the `eagle` command-line tool.

### Installation

```bash
pip install eagle-x
```

### Basic Analysis

Analyze any local image on your filesystem:

```bash
eagle analyze photo.jpg
```

Example Output:
```text
╔══════════════════════════════════════════════════════════╗
║                          EAGLE                           ║
║              IMAGE INTELLIGENCE & FORENSICS              ║
╚══════════════════════════════════════════════════════════╝

FILE ───────────────────────────────────────────────────────
  Name        : photo.jpg
  Size        : 4.82 MB (5,054,144 bytes)
  Format      : JPEG
  MIME Type   : image/jpeg
  Dimensions  : 4032 × 3024 px
  Megapixels  : 12.19 MP
  Color Mode  : RGB

CAMERA ─────────────────────────────────────────────────────
  Make        : Apple
  Model       : iPhone 15 Pro
  Lens        : iPhone 15 Pro back triple camera 6.76mm f/1.78
  Software    : 17.5.1

EXPOSURE ───────────────────────────────────────────────────
  Date/Time   : 2024:06:15 14:32:08
  Shutter     : 1/120 s
  Aperture    : f/1.8
  ISO         : ISO 64
  Focal Length: 6.8 mm
  35mm Equiv  : 24 mm
  Flash       : Flash did not fire
  White Bal.  : Auto
  Metering    : Pattern / Multi-Segment
  Program     : Normal / Program AE

LOCATION ───────────────────────────────────────────────────
  GPS Status  : Available
  Latitude    : 37.774900° (37° 46' 29.64" N)
  Longitude   : -122.419400° (122° 25' 09.84" W)
  Altitude    : 15.2 m (49.9 ft)
  GPS Time    : 2024:06:15 21:32:08 UTC
  Geocoding   : Disabled (use --geocode to resolve address)

EXIF ───────────────────────────────────────────────────────
  Total Tags  : 42 extracted
  Top Tags    :
    - [0x010F] Make                    : Apple
    - [0x0110] Model                   : iPhone 15 Pro
    - [0x9003] DateTimeOriginal        : 2024:06:15 14:32:08
    ... and 39 more tags (use --json to view all)
────────────────────────────────────────────────────────────
Analysis complete.
```

### Automation & Machine-Readable Output (`--json`)

Output clean, structured JSON to `stdout` for piping into scripts, security workflows, or `jq`:

```bash
eagle analyze photo.jpg --json
```

```json
{
  "filename": "photo.jpg",
  "has_gps": true,
  "latitude": 37.7749,
  "longitude": -122.4194,
  "file_info": {
    "file_size_bytes": 5054144,
    "formatted_file_size": "4.82 MB",
    "format": "JPEG",
    "mime_type": "image/jpeg",
    "width": 4032,
    "height": 3024,
    "megapixels": 12.19,
    "color_mode": "RGB"
  },
  "camera_info": {
    "make": "Apple",
    "model": "iPhone 15 Pro",
    "lens_model": "iPhone 15 Pro back triple camera 6.76mm f/1.78",
    "software": "17.5.1"
  },
  "exposure_info": { ... },
  "gps_info": { ... },
  "raw_exif": [ ... ]
}
```

### Optional Reverse Geocoding (`--geocode`)

Resolve GPS coordinates into a human-readable street/city/country address via OpenStreetMap Nominatim:

```bash
eagle analyze photo.jpg --geocode
```

### Development Invocation (Source Checkout)

Run Eagle directly from the repository without installation:

```bash
python -m eagle analyze path/to/image.jpg
```

---

## 🔒 Privacy & Security

- **100% Local by Default**: `eagle analyze` runs entirely on your local machine. No image data or metadata is ever uploaded or transmitted over the network.
- **Optional Geocoding**: Only when `--geocode` is explicitly passed will Eagle make an HTTPS request to OpenStreetMap Nominatim with the extracted coordinates.
- **Decompression Bomb Protection**: Input images exceeding 100 Megapixels are rejected to prevent memory exhaustion attacks.
- **Safe Parsing**: Binary tags and malformed EXIF data are sanitized to prevent crashes or terminal corruption.

---

## 📸 Supported Formats & Features

| Category | Supported Data |
|----------|----------------|
| **Image Formats** | JPEG / JPG, PNG, HEIC / HEIF, TIFF, WebP, BMP |
| **File Attributes** | Dimensions, File Size, Megapixels, Color Mode, MIME type |
| **Camera Hardware** | Manufacturer / Make, Model, Lens Model, Firmware / Software |
| **Exposure Settings** | Timestamp, Shutter Speed, Aperture, ISO, Focal Length (incl. 35mm), Exposure Bias, Flash, White Balance, Metering Mode, Exposure Program |
| **GPS Coordinates** | Latitude & Longitude (Decimal & DMS), Altitude, GPS Timestamp |
| **Raw EXIF IFDs** | Standard 0th IFD, ExifOffset Sub-IFD, GPS IFD |

---

## 🐍 Python Library Usage

```python
from eagle import analyze_image_file

# Analyze local image
result = analyze_image_file("photo.jpg", geocode=False)

print(f"Camera: {result.camera_info.make} {result.camera_info.model}")
if result.has_gps:
    print(f"Coordinates: {result.latitude}, {result.longitude}")
```

---

## 🌐 Web Application Setup

If you prefer the graphical user interface with the interactive Leaflet map:

### 1. Setup Backend

Pop open a terminal, hop into the `backend` directory, and create an isolated environment:

```bash
cd backend
python -m venv .venv

# Activate environment:
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Install dependencies and start server
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Your backend is listening at `http://localhost:8000` (Swagger docs at `http://localhost:8000/docs`).

### 2. Setup Frontend

In a second terminal window:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser, drag and drop an image, and inspect the forensics and map.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
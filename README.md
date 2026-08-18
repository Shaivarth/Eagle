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
        <img src="https://img.shields.io/badge/Parser-Pillow_&_HEIF-E95420?style=flat-square" alt="Pillow HEIF" />
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

<h3 align="center">Command-Line Interface</h3>

<p align="justify">
Eagle is distributed on PyPI as <code>eagle-x</code> and exposes the terminal command <code>eagle</code>. Install the package directly using pip, then analyze any image on your local filesystem with <code>eagle hunt photo.jpg</code>. For automation and OSINT pipelines, stream pure structured JSON output using <code>eagle hunt photo.jpg --json</code>, or perform reverse geocoding via <code>eagle hunt photo.jpg --geocode</code>.
</p>

#### Windows (PowerShell / Command Prompt)

```powershell
# Install from PyPI
pip install eagle-x

# Launch the purple flight manual
eagle

# Hunt down metadata & GPS telemetry
eagle hunt photo.jpg
eagle hunt "C:\Users\YourName\Pictures\photo.jpg"

# Output clean JSON to stdout
eagle hunt photo.jpg --json

# Upgrade to latest version
pip install --upgrade eagle-x
```

#### macOS / Linux (Terminal)

```bash
# Install from PyPI
pip3 install eagle-x

# Launch the purple flight manual
eagle

# Hunt down metadata & GPS telemetry
eagle hunt photo.jpg
eagle hunt ~/Pictures/photo.jpg

# Output clean JSON to stdout
eagle hunt photo.jpg --json

# Upgrade to latest version
pip3 install --upgrade eagle-x
```

---

<h3 align="center">Terminal Output</h3>

<p align="justify">
When running the hunting command, Eagle extracts hardware specifications, exposure settings, GPS coordinates, and raw EXIF headers directly inside the terminal:
</p>

```text
                        z$b
               .e$$$b.  $$$F  .d$$be
           .d$$$$$$$$$$e$$$be$$$$$$$$$$e.
       .e$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$b.
     z$$$$$$$P**""**$$$$$$$$$$$P*""""***$$$$$b.
   z$$$$*"            "$$$$$$"            "*$$$$c
 z$$*"                 ^$$$$                  "*$$.
^"                      $$$F                      ^%
                        $$$b
                        $P*$
                       4P  *r
                       4    %

╔════════════════════════════════════════════════════════════╗
║                           EAGLE                            ║
║               IMAGE INTELLIGENCE & FORENSICS               ║
║                    github.com/shaivarth                    ║
╚════════════════════════════════════════════════════════════╝

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

---

<h3 align="center">Privacy & Security</h3>

<p align="justify">
Eagle analysis is 100% local by default. No image data or metadata is ever uploaded or transmitted over the network unless <code>--geocode</code> is explicitly passed to query OpenStreetMap Nominatim. Input images exceeding 100 Megapixels are rejected to protect against decompression bomb attacks, and binary tags are sanitized to prevent crashes.
</p>

---

<h3 align="center">Supported Formats & Telemetry</h3>

<p align="justify">
Eagle supports deep header inspection across JPEG, PNG, HEIC/HEIF, TIFF, WebP, and BMP images. Extracted telemetry includes file dimensions, color mode, megapixels, camera hardware, exposure settings, GPS coordinates (Decimal & DMS), altitude, GPS timestamp, and standard raw EXIF IFD structures.
</p>

---

<h3 align="center">Python Library Usage</h3>

<p align="justify">
You can integrate Eagle directly into your Python scripts and forensics pipelines without invoking the CLI:
</p>

```python
from eagle import analyze_image_file

result = analyze_image_file("photo.jpg", geocode=False)

print(f"Camera: {result.camera_info.make} {result.camera_info.model}")
if result.has_gps:
    print(f"Coordinates: {result.latitude}, {result.longitude}")
```

---

<h2 align="center">If you want GUI</h2>

<h3 align="center">Setup Backend</h3>

<p align="justify">
Pop open a terminal, hop into the <code>backend</code> directory with <code>cd backend</code>, and create an isolated virtual environment:
</p>

#### Windows (PowerShell)

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### macOS / Linux (Terminal)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

<p align="justify">
Your backend is now listening at <code>http://localhost:8000</code>, and you can inspect the interactive Swagger docs at <code>http://localhost:8000/docs</code>.
</p>

---

<h3 align="center">Setup Frontend</h3>

<p align="justify">
In a second terminal window, head over to the frontend with <code>cd frontend</code> and install the necessary dependencies using <code>npm install</code>. Once that's done, fire up the Vite dev server with <code>npm run dev</code>, open <code>http://localhost:5173</code> in your browser, drag and drop an image in, and you're good to go.
</p>

#### Windows / macOS / Linux

```bash
cd frontend
npm install
npm run dev
```

---

<p align="center">
This project is open-source and available under the <a href="LICENSE">MIT License</a>.
</p>
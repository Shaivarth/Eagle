<div align="center">

<pre align="center">
  ███████╗  █████╗   ██████╗  ██╗      ███████╗
  ██╔════╝ ██╔══██╗ ██╔════╝  ██║      ██╔════╝
  █████╗   ███████║ ██║  ███╗ ██║      █████╗  
  ██╔══╝   ██╔══██║ ██║   ██║ ██║      ██╔══╝  
  ███████╗ ██║  ██║ ╚██████╔╝ ███████╗ ███████╗
  ╚══════╝ ╚═╝  ╚═╝  ╚═════╝  ╚══════╝ ╚══════╝
</pre>

### Photo EXIF & GPS Location Extraction Utility

---

<p align="center">
You feed Eagle an image, it rips open the raw EXIF header, grabs the exact GPS coordinates, reverse-geocodes the location, and drops a pin on an interactive map. If there's no GPS data in the file, it tells you straight up. Nothing is ever fabricated or guessed.
</p>

---

## Prerequisites

<p align="center">
<strong>Python 3.10+</strong> &nbsp;&bull;&nbsp; <strong>Node.js 18+ &amp; npm</strong>
</p>

---

## Backend Setup (FastAPI)

<p align="center">Open Terminal 1</p>

```bash
cd backend
python -m venv .venv
```

<p align="center"><strong>Activation</strong></p>

<p align="center">
<strong>Windows (PowerShell):</strong> <code>.venv\Scripts\activate</code><br>
<strong>Linux / macOS:</strong> <code>source .venv/bin/activate</code>
</p>

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

<p align="center">
Backend is live at <code>http://localhost:8000</code><br>
Check API docs at <code>http://localhost:8000/docs</code>
</p>

---

## Frontend Setup (React + Vite)

<p align="center">Open Terminal 2</p>

```bash
cd frontend
npm install
npm run dev
```

<p align="center">
Pop open <code>http://localhost:5173</code> in your browser. Boom. You're set.
</p>

---

</div>

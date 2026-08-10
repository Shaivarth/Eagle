<div align="center">

```
  ███████╗  █████╗   ██████╗  ██╗      ███████╗
  ██╔════╝ ██╔══██╗ ██╔════╝  ██║      ██╔════╝
  █████╗   ███████║ ██║  ███╗ ██║      █████╗  
  ██╔══╝   ██╔══██║ ██║   ██║ ██║      ██╔══╝  
  ███████╗ ██║  ██║ ╚██████╔╝ ███████╗ ███████╗
  ╚══════╝ ╚═╝  ╚═╝  ╚═════╝  ╚══════╝ ╚══════╝
```

### *Photo EXIF & GPS Location Extraction Utility*

---

### Prerequisites

Python 3.10+  •  Node.js 18+ & npm

---


#### Backend Setup (FastAPI)

Open Terminal 1:

```bash
cd backend
python -m venv .venv
```

Activation:

**Windows (PowerShell):** `.venv\Scripts\activate`  
**Linux / macOS:** `source .venv/bin/activate`

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

```bash
Backend is live at `http://localhost:8000`  
Check docs at `http://localhost:8000/docs`
```
---

#### Frontend Setup (React + Vite)

Open Terminal 2:

```bash
cd frontend
npm install
npm run dev
```

```bash
Pop open `http://localhost:5173` in your browser. Boom. You're set.
```
---
</div>

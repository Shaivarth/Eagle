<h2 align="center">EAGLE</h2>

<div align="center">

<table>
  <tr>
    <td width="70%" valign="top">
      <h3>Photo EXIF & GPS Location Extraction Utility</h3>
      <blockquote>
        An OSINT and digital forensics utility that rips open raw image headers, extracts deep EXIF metadata, camera hardware specs, and precise GPS coordinates, reverse-geocodes the location, and drops an interactive pin on the map.
      </blockquote>
      <p>
        <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
        <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" />
        <img src="https://img.shields.io/badge/Frontend-React_18-61DAFB?style=flat-square&logo=react&logoColor=black" alt="React" />
        <img src="https://img.shields.io/badge/Language-TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript" />
        <img src="https://img.shields.io/badge/Build-Vite-646CFF?style=flat-square&logo=vite&logoColor=white" alt="Vite" />
        <img src="https://img.shields.io/badge/Mapping-Leaflet-199900?style=flat-square&logo=leaflet&logoColor=white" alt="Leaflet" />
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

<h2 align="center">Backend Setup</h2>

<p align="center">
First, pop open a terminal, hop into the <code>backend</code> directory with <code>cd backend</code>, and create an isolated environment by running <code>python -m venv .venv</code>. Activate it using <code>.venv\Scripts\Activate.ps1</code> on Windows (or <code>source .venv/bin/activate</code> on Linux/macOS). Once active, grab all the required packages via <code>pip install -r requirements.txt</code>, then start the server with <code>uvicorn app.main:app --reload --port 8000</code>. Your backend is now listening at <code>http://localhost:8000</code>, and you can inspect the interactive Swagger docs at <code>http://localhost:8000/docs</code>.
</p>

---

<h2 align="center">Frontend Setup</h2>

<p align="center">
In a second terminal window, head over to the frontend with <code>cd frontend</code> and install the necessary dependencies using <code>npm install</code>. Once that's done, fire up the Vite dev server with <code>npm run dev</code>, open <code>http://localhost:5173</code> in your browser, drag and drop an image in, and you're good to go.
</p>

---

<h2 align="center">License</h2>

<p align="center">
This project is open-source and available under the MIT License.
</p>
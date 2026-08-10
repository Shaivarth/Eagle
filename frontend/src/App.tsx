import { useState } from "react";
import UploadArea from "./components/UploadArea";
import MetadataResult from "./components/MetadataResult";
import MapView from "./components/MapView";
import Footer from "./components/Footer";
import EagleEmblem from "./components/EagleEmblem";
import { analyzeImage } from "./api";
import type { AnalyzeResponse } from "./types";
import "./App.css";

type Status = "idle" | "loading" | "done" | "error";

export default function App() {
  const [status, setStatus] = useState<Status>("idle");
  const [fileName, setFileName] = useState<string | null>(null);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleFileSelected = async (file: File) => {
    setFileName(file.name);
    setResult(null);
    setErrorMessage(null);
    setStatus("loading");

    try {
      const analyzed = await analyzeImage(file);
      setResult(analyzed);
      setStatus("done");
    } catch (error) {
      setErrorMessage(
        error instanceof Error ? error.message : "Something went wrong."
      );
      setStatus("error");
    }
  };

  return (
    <main className="app">
      <div className="app__content">
        <header className="app__header">
          <h1 className="app__title">Eagle</h1>
          <p className="app__description">
            Upload an image to inspect its complete EXIF metadata, camera specs,
            exposure settings, and GPS location.
          </p>
        </header>

        <section className="app__section">
          <UploadArea
            onFileSelected={handleFileSelected}
            selectedFileName={fileName}
            disabled={status === "loading"}
          />
        </section>

        {status === "idle" && <EagleEmblem />}

        {status === "loading" && (
          <section className="app__section">
            <p className="app__status">reading exif data...</p>
          </section>
        )}

        {status === "error" && errorMessage && (
          <section className="app__section">
            <p className="app__status app__status--error">{errorMessage}</p>
          </section>
        )}

        {status === "done" && result && (
          <>
            <section className="app__section">
              <MetadataResult result={result} />
            </section>

            {result.has_gps &&
              result.latitude !== null &&
              result.longitude !== null && (
                <section className="app__section">
                  <MapView
                    latitude={result.latitude}
                    longitude={result.longitude}
                    label={result.location?.display_name ?? undefined}
                  />
                </section>
              )}
          </>
        )}
      </div>

      <Footer />
    </main>
  );
}

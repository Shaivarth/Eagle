import type { AnalyzeResponse } from "./types";

// Configurable at build time via a .env file: VITE_API_BASE_URL=http://localhost:8000
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

/**
 * Uploads an image to the backend and returns its extracted GPS / location data.
 * Throws an Error with a user-facing message on failure.
 */
export async function analyzeImage(file: File): Promise<AnalyzeResponse> {
  const formData = new FormData();
  formData.append("file", file);

  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/api/analyze`, {
      method: "POST",
      body: formData,
    });
  } catch {
    throw new Error(
      "Could not reach the Eagle server. Is the backend running?"
    );
  }

  if (!response.ok) {
    let detail = "Failed to analyze image.";
    try {
      const body = await response.json();
      if (typeof body?.detail === "string") {
        detail = body.detail;
      }
    } catch {
      // response body wasn't JSON; fall back to the default message
    }
    throw new Error(detail);
  }

  return (await response.json()) as AnalyzeResponse;
}

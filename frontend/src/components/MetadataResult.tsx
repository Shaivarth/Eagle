import { useState } from "react";
import type { AnalyzeResponse } from "../types";
import "./MetadataResult.css";

interface MetadataResultProps {
  result: AnalyzeResponse;
}

function formatCoordinate(value: number | null): string {
  if (value === null || value === undefined) return "unavailable";
  return value.toFixed(6);
}

function formatLocationLine(result: AnalyzeResponse): string | null {
  const location = result.location;
  if (!location) return null;

  const parts = [location.city, location.state, location.country].filter(
    (part): part is string => Boolean(part)
  );

  if (parts.length > 0) {
    return parts.join(", ");
  }

  return location.display_name;
}

export default function MetadataResult({ result }: MetadataResultProps) {
  const [rawExifSearch, setRawExifSearch] = useState("");
  const [isRawExpanded, setIsRawExpanded] = useState(false);

  const { file_info, camera_info, exposure_info, gps_info, raw_exif = [] } = result;
  const locationLine = formatLocationLine(result);

  const filteredRawExif = raw_exif.filter(
    (item) =>
      item.tag_name.toLowerCase().includes(rawExifSearch.toLowerCase()) ||
      item.tag_id.toLowerCase().includes(rawExifSearch.toLowerCase()) ||
      item.value.toLowerCase().includes(rawExifSearch.toLowerCase())
  );

  const hasCameraData = Boolean(
    camera_info &&
      (camera_info.make || camera_info.model || camera_info.lens_model || camera_info.software)
  );

  const hasExposureData = Boolean(
    exposure_info &&
      (exposure_info.date_time_original ||
        exposure_info.aperture ||
        exposure_info.exposure_time ||
        exposure_info.iso ||
        exposure_info.focal_length)
  );

  return (
    <div className="metadata-panel">
      {/* Section 1: Image & File Properties (Top Section) */}
      <div className="metadata-section">
        <div className="metadata-section__header">[ file &amp; image properties ]</div>
        <dl className="metadata-list">
          <dt>filename:</dt>
          <dd>{result.filename}</dd>

          <dt>file size:</dt>
          <dd>{file_info?.formatted_file_size ?? "unavailable"}</dd>

          <dt>dimensions:</dt>
          <dd>
            {file_info?.width && file_info?.height
              ? `${file_info.width} x ${file_info.height} px (${file_info.megapixels} MP)`
              : "unavailable"}
          </dd>

          <dt>format:</dt>
          <dd>{file_info?.format ?? "unavailable"}</dd>

          <dt>mime type:</dt>
          <dd>{file_info?.mime_type ?? "unavailable"}</dd>

          <dt>color mode:</dt>
          <dd>{file_info?.color_mode ?? "unavailable"}</dd>
        </dl>
      </div>

      {/* Section 2: Location / GPS Data */}
      <div className="metadata-section">
        <div className="metadata-section__header">[ gps location ]</div>
        {result.has_gps && result.latitude !== null && result.longitude !== null ? (
          <dl className="metadata-list">
            <dt>latitude:</dt>
            <dd>{formatCoordinate(result.latitude)}</dd>

            <dt>longitude:</dt>
            <dd>{formatCoordinate(result.longitude)}</dd>

            {gps_info?.latitude_dms && (
              <>
                <dt>lat (dms):</dt>
                <dd>{gps_info.latitude_dms}</dd>
              </>
            )}

            {gps_info?.longitude_dms && (
              <>
                <dt>lon (dms):</dt>
                <dd>{gps_info.longitude_dms}</dd>
              </>
            )}

            {gps_info?.altitude && (
              <>
                <dt>altitude:</dt>
                <dd>{gps_info.altitude}</dd>
              </>
            )}

            {gps_info?.timestamp && (
              <>
                <dt>gps time:</dt>
                <dd>{gps_info.timestamp}</dd>
              </>
            )}

            <dt>location:</dt>
            <dd>
              {locationLine ?? (
                <span className="metadata-dim">
                  {result.geocode_error ?? "unavailable"}
                </span>
              )}
            </dd>
          </dl>
        ) : (
          <p className="metadata-none">no gps location data found in this image.</p>
        )}
      </div>

      {/* Section 3: Camera & Hardware */}
      <div className="metadata-section">
        <div className="metadata-section__header">[ camera &amp; hardware ]</div>
        {hasCameraData ? (
          <dl className="metadata-list">
            {camera_info?.make && (
              <>
                <dt>make:</dt>
                <dd>{camera_info.make}</dd>
              </>
            )}
            {camera_info?.model && (
              <>
                <dt>model:</dt>
                <dd>{camera_info.model}</dd>
              </>
            )}
            {camera_info?.lens_model && (
              <>
                <dt>lens model:</dt>
                <dd>{camera_info.lens_model}</dd>
              </>
            )}
            {camera_info?.software && (
              <>
                <dt>software:</dt>
                <dd>{camera_info.software}</dd>
              </>
            )}
          </dl>
        ) : (
          <p className="metadata-none">no camera hardware metadata found.</p>
        )}
      </div>

      {/* Section 4: Exposure & Capture Settings */}
      <div className="metadata-section">
        <div className="metadata-section__header">[ exposure &amp; shot settings ]</div>
        {hasExposureData ? (
          <dl className="metadata-list">
            {exposure_info?.date_time_original && (
              <>
                <dt>date/time:</dt>
                <dd>{exposure_info.date_time_original}</dd>
              </>
            )}
            {exposure_info?.aperture && (
              <>
                <dt>aperture:</dt>
                <dd>{exposure_info.aperture}</dd>
              </>
            )}
            {exposure_info?.exposure_time && (
              <>
                <dt>shutter speed:</dt>
                <dd>{exposure_info.exposure_time}</dd>
              </>
            )}
            {exposure_info?.iso && (
              <>
                <dt>iso speed:</dt>
                <dd>{exposure_info.iso}</dd>
              </>
            )}
            {exposure_info?.focal_length && (
              <>
                <dt>focal length:</dt>
                <dd>
                  {exposure_info.focal_length}
                  {exposure_info.focal_length_35mm && ` (${exposure_info.focal_length_35mm} 35mm eq.)`}
                </dd>
              </>
            )}
            {exposure_info?.exposure_bias && (
              <>
                <dt>exposure bias:</dt>
                <dd>{exposure_info.exposure_bias}</dd>
              </>
            )}
            {exposure_info?.flash && (
              <>
                <dt>flash:</dt>
                <dd>{exposure_info.flash}</dd>
              </>
            )}
            {exposure_info?.white_balance && (
              <>
                <dt>white balance:</dt>
                <dd>{exposure_info.white_balance}</dd>
              </>
            )}
            {exposure_info?.metering_mode && (
              <>
                <dt>metering mode:</dt>
                <dd>{exposure_info.metering_mode}</dd>
              </>
            )}
            {exposure_info?.exposure_program && (
              <>
                <dt>program:</dt>
                <dd>{exposure_info.exposure_program}</dd>
              </>
            )}
          </dl>
        ) : (
          <p className="metadata-none">no exposure settings found in metadata.</p>
        )}
      </div>

      {/* Section 5: Raw EXIF Tags Inspector */}
      {raw_exif.length > 0 && (
        <div className="metadata-section">
          <button
            type="button"
            className="raw-exif-toggle"
            onClick={() => setIsRawExpanded(!isRawExpanded)}
          >
            {isRawExpanded
              ? `[-] hide raw exif tags (${raw_exif.length} tags)`
              : `[+] inspect all raw exif tags (${raw_exif.length} tags)`}
          </button>

          {isRawExpanded && (
            <div className="raw-exif-body">
              <div className="raw-exif-filter">
                <span className="raw-exif-prompt">&gt; filter:</span>
                <input
                  type="text"
                  placeholder="type tag name, id, or value..."
                  value={rawExifSearch}
                  onChange={(e) => setRawExifSearch(e.target.value)}
                  className="raw-exif-input"
                />
                <span className="raw-exif-count">
                  ({filteredRawExif.length}/{raw_exif.length})
                </span>
              </div>

              <div className="raw-exif-table-wrapper">
                <table className="raw-exif-table">
                  <thead>
                    <tr>
                      <th>tag id</th>
                      <th>tag name</th>
                      <th>value</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredRawExif.length > 0 ? (
                      filteredRawExif.map((tag, idx) => (
                        <tr key={`${tag.tag_id}-${tag.tag_name}-${idx}`}>
                          <td className="tag-id">{tag.tag_id}</td>
                          <td className="tag-name">{tag.tag_name}</td>
                          <td className="tag-val">{tag.value}</td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan={3} className="table-empty">
                          no matching raw tags found for "{rawExifSearch}"
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export interface LocationInfo {
  city: string | null;
  state: string | null;
  country: string | null;
  display_name: string | null;
}

export interface ImageFileInfo {
  file_size_bytes: number;
  formatted_file_size: string;
  format: string | null;
  mime_type: string | null;
  width: number | null;
  height: number | null;
  megapixels: number | null;
  color_mode: string | null;
}

export interface CameraInfo {
  make: string | null;
  model: string | null;
  lens_model: string | null;
  software: string | null;
}

export interface ExposureInfo {
  date_time_original: string | null;
  exposure_time: string | null;
  aperture: string | null;
  iso: string | null;
  focal_length: string | null;
  focal_length_35mm: string | null;
  exposure_bias: string | null;
  flash: string | null;
  white_balance: string | null;
  metering_mode: string | null;
  exposure_program: string | null;
}

export interface GpsMetadata {
  latitude: number | null;
  longitude: number | null;
  latitude_dms: string | null;
  longitude_dms: string | null;
  altitude: string | null;
  timestamp: string | null;
}

export interface RawExifTag {
  tag_id: string;
  tag_name: string;
  value: string;
}

export interface AnalyzeResponse {
  filename: string;
  has_gps: boolean;
  latitude: number | null;
  longitude: number | null;
  location: LocationInfo | null;
  geocode_error: string | null;
  preview_url?: string | null;
  file_info: ImageFileInfo | null;
  camera_info: CameraInfo | null;
  exposure_info: ExposureInfo | null;
  gps_info: GpsMetadata | null;
  raw_exif: RawExifTag[];
}

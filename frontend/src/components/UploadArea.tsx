import { useRef, useState, type ChangeEvent, type DragEvent } from "react";
import "./UploadArea.css";

interface UploadAreaProps {
  onFileSelected: (file: File) => void;
  selectedFileName: string | null;
  disabled: boolean;
}

const ACCEPTED_EXTENSIONS =
  "image/jpeg,image/jpg,image/png,image/heic,image/heif,image/heic-sequence,image/heif-sequence,.jpg,.jpeg,.png,.heic,.heif,.HEIC,.HEIF";

export default function UploadArea({
  onFileSelected,
  selectedFileName,
  disabled,
}: UploadAreaProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [isDragActive, setIsDragActive] = useState(false);

  const openFilePicker = () => {
    if (!disabled) {
      inputRef.current?.click();
    }
  };

  const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      onFileSelected(file);
    }
    // Reset so selecting the same file again still fires onChange.
    event.target.value = "";
  };

  const handleDrop = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragActive(false);
    if (disabled) return;

    const file = event.dataTransfer.files?.[0];
    if (file) {
      onFileSelected(file);
    }
  };

  const handleDragOver = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    if (!disabled) setIsDragActive(true);
  };

  const handleDragLeave = () => {
    setIsDragActive(false);
  };

  return (
    <div
      className={`upload-area ${isDragActive ? "upload-area--active" : ""} ${
        disabled ? "upload-area--disabled" : ""
      }`}
      onClick={openFilePicker}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      role="button"
      tabIndex={0}
      aria-label="Upload image"
      onKeyDown={(event) => {
        if (event.key === "Enter" || event.key === " ") {
          openFilePicker();
        }
      }}
    >
      <input
        ref={inputRef}
        type="file"
        accept={ACCEPTED_EXTENSIONS}
        onChange={handleInputChange}
        className="upload-area__input"
        disabled={disabled}
      />
      <p className="upload-area__label">
        drop image here, or click to select a file
      </p>
      <p className="upload-area__formats">jpg &middot; png &middot; heic</p>
      {selectedFileName && (
        <p className="upload-area__filename">&gt; {selectedFileName}</p>
      )}
    </div>
  );
}

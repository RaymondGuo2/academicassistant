import React, { useState } from "react";

export default function FileUploadButton({ onFileSelect }) {
    const [fileName, setFileName] = useState("");

    function handleFileChange(event) {
        const file = event.target.files[0];
        if (file) {
            setFileName(file.name);
            if (onFileSelect) onFileSelect(file);
        }
    }

    return (
        <div>
            <label
                htmlFor="file-upload"
                style={{
                    padding: "8px 16px",
                    backgroundColor: "#007bff",
                    color: "white",
                    borderRadius: "4px",
                    cursor: "pointer",
                    display: "inline-block",
                }}
                >
                    Upload File
                </label>
                <input
                    id="file-upload"
                    type="file"
                    style={{ display: "none" }}
                    onChange={handleFileChange}
                />
                {fileName && <p>Selected file: {fileName}</p>}
        </div>
    );
}
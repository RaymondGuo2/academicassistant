import React, { useState } from "react";

export default function FileUploadButton() {
    const [fileName, setFileName] = useState("");
    const [uploadStatus, setUploadStatus] = useState("");

    async function handleFileChange(event) {
        const file = event.target.files[0];
        if (!file) return;

        setFileName(file.name);
        setUploadStatus("Uploading...");

        // Prepare FormData to send file in POST request
        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("http://localhost:8000/upload", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Upload failed: ${response.statusText}`);
            }

            const data = await response.json();
            setUploadStatus(`Upload complete. Doc ID: ${data.doc_id}`);
        } catch (error) {
            console.error("Error uploading file:", error);
            setUploadStatus("Upload failed.");
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
            {uploadStatus && <p>{uploadStatus}</p>}
        </div>
    );
}

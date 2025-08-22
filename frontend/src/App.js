import React from "react";
import FileUploadButton  from "./components/FileUploadButton";
import UploadedDocumentTable from "./components/UploadedDocumentTable";

export default function App() {
  function handleFile(file) {
    console.log("Selected file in App:", file);
  }
  return (
    <>
      <div style={{ padding: "20px" }}>
        <h1>My React App</h1>
        <FileUploadButton onFileSelect={handleFile} />
      </div>
      <div style={{ padding: "20px" }}>
        <h2>Uploaded Documents</h2>
        <UploadedDocumentTable />
      </div>
    </>
  );
}
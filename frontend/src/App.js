import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import FileUploadButton  from "./components/FileUploadButton";
import UploadedDocumentTable from "./components/UploadedDocumentTable";
import "./App.css";
import Database from "./pages/Database";  

function Home({ onFileSelect }) {
  return (
    <div className="content">
      <h2>Welcome to the Academic Assistant 🎓</h2>
      <p>Your one-stop solution for managing academic documents.</p>

      <h3>Please upload your files below: </h3>
      <FileUploadButton onFileSelect={onFileSelect} />

      <br />
      <br />

      <h3>Uploaded Documents</h3>
      <UploadedDocumentTable />
    </div>
  );
}

export default function App() {
  function handleFile(file) {
    console.log("Selected file in App:", file);
  }

  return (
    <Router>
      {/* Navbar */}
      <nav className="navbar">
        <div className="logo">Academic Assistant</div>
        <ul className="nav-links">
          <li><Link to="/">Home</Link></li>
          <li><Link to="/database">Database</Link></li>
        </ul>
      </nav>

      <Routes>
        <Route path="/" element={<Home onFileSelect={handleFile} />} />
        <Route path="/database" element={<Database />} />
      </Routes>
    </Router>
  );
}
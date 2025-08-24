import React, {useEffect, useState} from "react";
import "../App.css";

export default function DatabaseDisplay() {
    const [documents, setDocuments] = useState([]);

    async function fetchDocuments() {
        try {
            const response = await fetch("http://localhost:8000/documents", {
                method: "GET",
            });

            if (!response.ok) {
                throw new Error(`Fetch failed: ${response.statusText}`);
            }

            const data = await response.json();
            console.log("Fetched documents:", data.documents);
            setDocuments(data.documents);
        } catch (error) {
            console.error("Error fetching documents:", error);
        }
    }

    useEffect(() => {
        fetchDocuments();
        const interval = setInterval(fetchDocuments, 500);
        return () => clearInterval(interval);
    }, []);

    return (
        <>
        <div className="content">
            <h1>Database Page</h1>
            <p>This is where your database features will go.</p>
        </div>
        <table>
            <thead>
                <tr>
                    <th>Document ID</th>
                    <th>File Name</th>
                    <th>Status</th>
                    <th>File Path</th>
                </tr>
            </thead>
            <tbody>
                {documents.map((doc) => (
                    <tr key={doc.id}>
                        <td>{doc.doc_id}</td>
                        <td>{doc.file_name}</td>
                        <td>{doc.status}</td>
                        <td>{doc.filepath}</td>
                    </tr>
                ))}
            </tbody>
        </table>
        </>
    );
}
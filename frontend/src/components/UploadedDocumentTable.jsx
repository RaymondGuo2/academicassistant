import React, {useEffect, useState} from "react";

export default function UploadedDocumentTable() {
    const [documents, setDocuments] = useState([]);
    async function fetchDocuments(){

        try{
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
    }, []);

    return(
        <table>
            <thead>
                <tr>
                    <th>Document ID</th>
                    <th>Status</th>
                    <th>File Path</th>
                </tr>
            </thead>
            <tbody>
                {documents.map((doc) => (
                    <tr key={doc.id}>
                        <td>{doc.doc_id}</td>
                        <td>{doc.status}</td>
                        <td>{doc.filepath}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    )
}
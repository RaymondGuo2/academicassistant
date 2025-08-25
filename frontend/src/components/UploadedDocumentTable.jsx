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
        const interval = setInterval(fetchDocuments, 500);
        return () => clearInterval(interval);
    }, []);

    function handleDelete(docId) {
    fetch(`http://localhost:8000/documents/${docId}`, {
        method: "DELETE",
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Delete failed");
            }
            // Refetch or update state
            setDocuments((prevDocs) => prevDocs.filter((doc) => doc.doc_id !== docId));
        })
        .catch((err) => console.error(err));
    }

    function handleProcessed(docId) {
        fetch(`http://localhost:8000/documents/${docId}/processed`, {
            method: "GET",
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Fetch failed");
                }
                return response.json();
            })
            .then((data) => {
                console.log("Processed data:", data);
            })
            .catch((err) => console.error(err));
    }

    return(
        <table>
            <thead>
                <tr>
                    <th>Document ID</th>
                    <th>File Name</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {documents.map((doc) => (
                    <tr key={doc.id}>
                        <td>{doc.doc_id}</td>
                        <td>{doc.file_name}</td>
                        <td>{doc.status}</td>
                        <td>
                            <button onClick={() => handleDelete(doc.doc_id)}>Delete</button>
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    )
}
import React, { useEffect } from 'react';

export default function Query() {
    const [query, setQuery] = React.useState("");
    const [responseText, setResponseText] = React.useState("");
    const textareaRef = React.useRef(null);

    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = "auto"; // Reset height
            textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`; // Set to scroll height
        }
    }, [responseText]);

    async function handleSubmit(event) {
        event.preventDefault();
        try {
            const response = await fetch("http://localhost:8000/query", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ query }),
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            const data = await response.json();
            console.log("Query submitted successfully:", data);
            setResponseText(data.answer || "No answer received.");

        } catch (error) {
            console.error("Error occurred while submitting query:", error);
            setResponseText("Error occurred while submitting query.");
        }
    }

    const handleReset = () => {
        setQuery("");
        setResponseText("");
    };

    return (
        <>
            <form onSubmit={handleSubmit}>
                <label>
                    <input
                        type="text"
                        placeholder="Type your query here..."
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        style={{
                            width: "100%",
                            resize: "none",
                            overflow: "hidden",
                            marginTop: "1em",
                        }}
                    />
                </label>
                <br></br>
                <button type="reset" onClick={handleReset}>Reset Query</button>
                <button type="submit">Submit Query</button>
            </form>
            <textarea
                ref={textareaRef}
                value={responseText}
                readOnly
                style={{
                    width: "100%",
                    resize: "none",
                    overflow: "hidden",
                    marginTop: "1em",
                }}
                placeholder="Response will appear here..."
            />
        </>
    );
}
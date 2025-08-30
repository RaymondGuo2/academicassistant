import React from 'react';

export default function Query() {
    const [query, setQuery] = React.useState("");

    async function handleSubmit(event) {
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

        } catch (error) {
            console.error("Error occurred while submitting query:", error);
        }
    }

    const handleReset = () => {
        setQuery("");
    };

    return (
        <form onSubmit={handleSubmit}>
            <label>
                <input
                    type="text"
                    placeholder="Type your query here..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
            </label>
            <br></br>
            <button type="reset" onClick={handleReset}>Reset Query</button>
            <br></br>
            <button type="submit" onClick={handleSubmit}>Submit Query</button>
        </form>
    );
}
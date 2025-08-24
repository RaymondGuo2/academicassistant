from database import get_db_connection

# Create the table
def create_table():
    with get_db_connection() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS research (
            id SERIAL PRIMARY KEY,
            doc_id UUID UNIQUE NOT NULL,
            file_name TEXT NOT NULL,
            status TEXT NOT NULL,
            filepath TEXT UNIQUE NOT NULL
        );
        """)
        print("Table 'research' created")

def insert_research(doc_id, file_name, status, filepath):
    with get_db_connection() as cur:
        cur.execute(
            "INSERT INTO research (doc_id, file_name, status, filepath) VALUES (%s, %s, %s, %s)",
            (doc_id, file_name, status, filepath)
        )
        print(f"Inserted research record with doc_id: {doc_id}")
    
def get_all_research():
    with get_db_connection() as cur:
        cur.execute("SELECT doc_id, file_name, status, filepath FROM research ORDER BY id DESC;")
        rows = cur.fetchall()
        return [{"doc_id": r[0], "file_name": r[1], "status": r[2], "file_path": r[3]} for r in rows]

def delete_research(doc_id):
    with get_db_connection() as cur:
        cur.execute("DELETE FROM research WHERE doc_id = %s", (doc_id,))
        print(f"Deleted research record with doc_id: {doc_id}")
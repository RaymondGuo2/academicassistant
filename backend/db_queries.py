import json
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

def create_processed_table():
    with get_db_connection() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS processed_data (
            id SERIAL PRIMARY KEY,
            doc_id UUID REFERENCES research(doc_id) ON DELETE CASCADE,
            text_content TEXT NOT NULL,
            metadata JSONB
        );
        """)
        print("Table 'processed_data' created")

def create_vector_table():
    with get_db_connection() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS document_chunks (
            chunk_id SERIAL PRIMARY KEY,
            doc_id UUID REFERENCES research(doc_id) ON DELETE CASCADE,
            chunk_text TEXT,
            embedding VECTOR(1536)
        );
        """)
        print("Table 'document_chunks' created")

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

def get_documents_by_status(status):
    with get_db_connection() as cur:
        cur.execute("SELECT doc_id, file_name, status, filepath FROM research WHERE status = %s;", (status,))
        return cur.fetchall()
    
def save_processed(doc_id, text, metadata):
    with get_db_connection() as cur:
        cur.execute(
            "INSERT INTO processed_data (doc_id, text_content, metadata) VALUES (%s, %s, %s)",
            (doc_id, text, json.dumps(metadata))
        )
        print(f"Saved processed data for doc_id: {doc_id}")

def get_processed_by_doc_id(doc_id):
    with get_db_connection() as cur:
        cur.execute("SELECT doc_id, text_content, metadata FROM processed_data WHERE doc_id = %s;", (doc_id,))
        return cur.fetchall()

def update_status(doc_id, status):
    with get_db_connection() as cur:
        cur.execute("UPDATE research SET status = %s WHERE doc_id = %s;", (status, doc_id))

def insert_chunk(doc_id, chunk_text, vector):
    with get_db_connection() as cur:
        cur.execute(
            "INSERT INTO document_chunks (doc_id, chunk_text, embedding) VALUES (%s, %s, %s)",
            (doc_id, chunk_text, vector)
        )


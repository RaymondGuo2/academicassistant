from database import get_db_connection

# Create the table
def create_table():
    with get_db_connection() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS research (
            id SERIAL PRIMARY KEY,
            doc_id UUID UNIQUE NOT NULL,
            status TEXT NOT NULL,
            filepath TEXT UNIQUE NOT NULL
        );
        """)
        print("Table 'research' created")

def insert_research(doc_id, status, filepath):
    with get_db_connection() as cur:
        cur.execute(
            "INSERT INTO research (doc_id, status, filepath) VALUES (%s, %s, %s)",
            (doc_id, status, filepath)
        )
        print(f"Inserted research record with doc_id: {doc_id}")

def get_research_by_id(doc_id):
    with get_db_connection() as cur:
        cur.execute("SELECT * FROM research WHERE doc_id = %s;", (doc_id,))
        return cur.fetchone()
    
def get_research():
    with get_db_connection() as cur:
        cur.execute("SELECT * FROM research;")
        return cur.fetchall()

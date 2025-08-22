import psycopg2
import os 
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

@contextmanager
def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    print("Database connection established")
    try:
        cur = conn.cursor()
        yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    with get_db_connection() as cur:
        cur.execute("SELECT 1;")
        print("Test query executed successfully")
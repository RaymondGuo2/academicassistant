import time
import db_queries
from processors import extract_text_and_metadata

def worker_loop():
    print("Working script")
    while True:
        docs = db_queries.get_documents_by_status("uploaded")
        for doc in docs:
            print(f"Processing document {doc[0]}...")
            try:
                text, metadata = extract_text_and_metadata(doc[3])
                db_queries.save_processed(doc[0], text, metadata)
                db_queries.update_status(doc[0], "processed")
            except Exception as e:
                print(f"Error processing document {doc[0]}: {e}")
                db_queries.update_status(doc[0], "error")
        time.sleep(5)

if __name__ == "__main__":
    worker_loop()
import time
import db_queries
from processors import extract_text_and_metadata

def worker_loop():
    while True:
        docs = db_queries.get_documents_by_status("uploaded")
        for doc in docs:
            print(f"Processing document {doc['doc_id']}...")
            try:
                text, metadata = extract_text_and_metadata(doc['filepath'])
                db_queries.save_processed(doc['doc_id'], text, metadata)
                db_queries.update_status(doc['doc_id'], "processed")
            except Exception as e:
                print(f"Error processing document {doc['doc_id']}: {e}")
                db_queries.update_status(doc['doc_id'], "error")
        time.sleep(5)

if __name__ == "__main__":
    worker_loop()
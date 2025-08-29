import time
import db_queries
from processors import extract_text_and_metadata
import chunking

def worker_loop():
    print("Working script")
    while True:
        docs = db_queries.get_documents_by_status("uploaded")
        for doc in docs:
            print(f"Processing document {doc[0]}...")
            try:
                # Phase 2: extract text and metadata
                text, metadata = extract_text_and_metadata(doc[3])
                db_queries.save_processed(doc[0], text, metadata)
                db_queries.update_status(doc[0], "processed")

                # Phase 3: chunk + embed
                chunks = chunking.chunk_text(text)
                print("Passed chunking")
                embeddings = chunking.get_embeddings(chunks)
                print("Passed embedding")
                for chunk in embeddings:
                    db_queries.insert_chunk(
                        doc_id=doc[0],
                        chunk_text=chunk["chunk_text"],
                        vector=chunk["vector"]
                    )
                
                db_queries.update_status(doc[0], "indexed")
                print(f"Document {doc[0]} processed and indexed.")
            except Exception as e:
                print(f"Error processing document {doc[0]}: {e}")
                db_queries.update_status(doc[0], "error")
        time.sleep(5)

if __name__ == "__main__":
    worker_loop()
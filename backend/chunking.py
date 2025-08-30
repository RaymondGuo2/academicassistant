import tiktoken
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chunk_text(text, max_tokens=500, overlap=50):
    """
    Splits text into overlapping chunks for embeddings
    """
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)
    
    chunks = []
    start = 0
    while start < len(tokens):
        end = start + max_tokens
        chunk_tokens = tokens[start:end]
        chunk_text = tokenizer.decode(chunk_tokens)
        chunks.append({
            "start": start, 
            "end": min(end, len(tokens)),
            "text": chunk_text
        })
        start += max_tokens - overlap
    return chunks

def get_embeddings(text_chunks):
    embeddings = []
    for chunk in text_chunks:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk["text"]
        )
        embeddings.append({
            "chunk_text": chunk["text"],
            "vector": response.data[0].embedding,
            "start": chunk["start"],
            "end": chunk["end"]
        })
    return embeddings

def process_query(query):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    return response.data[0].embedding if response.data else []
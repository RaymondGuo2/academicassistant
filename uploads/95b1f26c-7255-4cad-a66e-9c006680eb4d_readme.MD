# 🧠 MindMeld — AI-Powered Context-Aware Research Workspace

A workspace where you can dump all your messy notes, PDFs, links, and ideas, and the LLM becomes your research partner — remembering everything, connecting dots, and generating insights automatically.

## Core Concept

You throw in:
- Articles
- Meeting notes
- Screenshots
- Audio transcriptions

The LLM processes & indexes everything in a semantic vector database.

Then you can:
- Ask deep questions across all your materials (“What do these reports say about Q3 customer churn?”)
- Get summaries, timelines, comparisons, and trend analysis.
- Auto-generate presentations or reports from your knowledge dump.

## Backend Stack

### Ingestion Pipeline

- Python / Node microservice to accept text, PDFs, images (OCR with Tesseract or Vision API).
- Audio → Text via Whisper.

### Storage & Retrieval

- PostgreSQL for metadata.
- Vector Database (Pinecone, Weaviate, or open-source like Milvus) for semantic search.

### AI Orchestration
- LLM (OpenAI / Anthropic) for question answering & summarization.
- LangChain / LlamaIndex for retrieval-augmented generation (RAG).

### Background Workers (Celery or Kafka) to:

- Auto-tag and cluster notes.
- Build topic maps.
- Extract entities and relationships.

## Frontend Features

### React / Next.js app
- Drag & drop note upload.
- Search bar that’s “Google + Chat” for your own data.
- Knowledge graph view: see how documents connect.
- Highlight-to-ask: Select any text snippet and ask the LLM for context or deeper explanation.

### Multi-modal search
- Type questions
- Upload an image or chart and ask “Explain this”
- Speak into mic for quick queries

## High-Level Architecture

![Image Failed to Load](images/architecture.png)

## Steps

### Phase 1 — Basic Ingestion Path
**Goal**: User can upload a file, and it’s stored in raw storage with a DB record.

**Tasks**:

1. Frontend upload form → select PDF/image/audio/URL.
2. Backend API endpoint (POST /upload)
    - Accepts file or URL.
    - Generates unique doc ID.
    - Saves file to object storage.
    - Inserts record into Postgres {doc_id, status: "uploaded", metadata...}.
3. Basic document listing API (GET /documents)
    - Returns list of uploaded docs and status.

### Phase 2 — Processing & Text Extraction
**Goal**: Raw files → clean text with metadata.

**Tasks**:

1. Worker job trigger when new doc is uploaded
    - Poll Postgres for status="uploaded" OR use a message queue.
2. Extraction by file type:
    - PDF → pdfplumber / PyMuPDF to extract text.
    - Image → OCR with pytesseract or AWS Textract.
    - Audio → Whisper transcription.
3. Text normalization
    - Remove extra whitespace, normalize quotes, unify encoding.
    - Extract basic metadata (title, author, date).
4. Store cleaned text in Postgres (separate table) or as a text file in object storage.
5. Update doc status to processed.

### Phase 3 — Chunking & Embedding
**Goal**: Turn clean text into vector-searchable chunks.

**Tasks**:

1. Chunking function
    - Split text into ~500 token chunks with ~50 token overlap.
2. Embedding generation
    - Call OpenAI / HuggingFace embeddings model for each chunk.
3. Store embeddings
    - Insert into vector DB (Pinecone, Weaviate, or Postgres+pgvector).
    - Store chunk metadata in Postgres: {chunk_id, doc_id, offsets, text, embedding_id}.
4. Update doc status to indexed.

### Phase 4 — Retrieval & RAG Orchestration
**Goal**: User can ask questions and get context-based answers.

**Tasks**:

1. Query API endpoint (POST /query)
    - Accepts {question, filters}.
2. Vector DB search
    - Retrieve top-k most similar chunks (optionally filtered by doc/date/tag).
3. Prompt construction
    - Combine: retrieved chunk text + user question + system instructions.
4. LLM call
    - Send prompt to LLM API and get answer.
5. Provenance linking
    - Attach chunk IDs and doc IDs to the answer.
6. Return result to frontend.

### Phase 5 — Frontend Integration
**Goal**: Full user flow from upload → indexed → query → answer.

**Tasks**:

1. Document status updates
    - WebSocket or polling to show “Processing / Indexed” in real time.
2. Query interface
    - Text box for questions, result display area.
3. Clickable provenance links
    - Clicking shows the chunk in context.

### Phase 6 — Production Readiness
**Goal**: Scale, secure, and monitor.

**Tasks**:

1. Auth & Permissions
    - Only logged-in users can upload/query.
2. Job queue scaling
    - Multiple workers for heavy OCR/transcription jobs.
3. Caching
    - Store recent Q&A pairs in Redis.
4. Monitoring & logging
    - Track errors, request times, worker queues.
5. Deployment
    - sContainerize with Docker, deploy to AWS/GCP/Azure.
# RAG Ingestion & Retrieval API

A Retrieval-Augmented Generation (RAG) backend built with **FastAPI**. It has two APIs:

- **Ingestion API**: takes a document, parses it, embeds it, and stores it.
- **Retrieval API**: takes a user question, finds the 3 most relevant chunks, and generates an answer with an LLM.

Embeddings are stored in a **FAISS** vector database. Document details (metadata) are stored in **PostgreSQL** using **SQLAlchemy**.

---

## Tech Stack

| Part | Technology |
|---|---|
| API framework | FastAPI |
| Embedding model | `<all-MiniLM-L6-v2>` |
| Vector database | FAISS |
| Relational database | PostgreSQL (SQLAlchemy) |
| LLM | `<openai/gpt-oss-120b>` (via Groq API) |
| Containerization | Docker / Docker Compose |

---

## How It Works

### 1. Ingestion Flow

<img width="356" height="665" alt="image" src="https://github.com/user-attachments/assets/ca2a7184-9467-4aca-bd6a-e3db63d7d5fa" />

```

**Steps**

1. The user sends a document to the Ingestion API.
2. The document is **parsed** to extract its text.
3. The text is **not cleaned**. The same raw parsed data is used as it is.
4. The text is split into chunks.
5. Each chunk is converted to a vector by the **embedding model**.
6. The vectors are saved in the **FAISS** vector database.
7. The details (document info, chunk text, ids) are saved in **PostgreSQL**.

### 2. Retrieval Flow

<img width="356" height="665" alt="image" src="https://github.com/user-attachments/assets/6aac3345-60b5-498f-b1c3-7ca367d8e853" />





## Project Structure
```
RAG/
├── App/
│   └── main.py            # FastAPI app entry point
├── router/
│   ├── ingestion.py       # Ingestion API routes
│   └── retrievel.py       # Retrieval API routes
├── chunking/
│   └── chunks.py          # Splits text into chunks
├── embedding/
│   └── embedding.py       # Embedding model loading and encoding
├── database/
│   └── database.py        # PostgreSQL connection (SQLAlchemy)
├── model/
│   └── model.py           # Database models and schemas
├── context/
│   └── context.py         # Builds context from retrieved chunks
├── prompt/
│   └── prompt.py          # Prompt template
├── llm/
│   └── llm.py             # LLM API call
├── vector_db/             # FAISS index files (not in Git)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env                   # Secrets (not in Git)
```


## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/<ingestion-endpoint>` | Upload a document, parse, embed and store it |
| GET | `/<retrieval-endpoint>` | Ask a question and get an answer |

Check `/docs` for the exact request and response format.

---

## Notes

- **No text cleaning** is done during ingestion. The parsed text is embedded as it is.
- Retrieval returns the **top 3** most similar chunks.
- `vector_db/` and `Rag_chunks.json` are not pushed to Git. Run the ingestion API again to rebuild them.
- Secrets live only in `.env`. Docker Compose reads them from there.

---

## Author

[zcodex8](https://github.com/zcodex8)

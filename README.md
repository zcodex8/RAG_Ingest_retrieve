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
| LLM | `<openai/gpt-oss-120b>` (via groq API) |
| Containerization | Docker / Docker Compose |

---

## How It Works

### 1. Ingestion Flow

![Ingestion Flow](images/ingestion_flow.png)
<img width="648" height="238" alt="image" src="https://github.com/user-attachments/assets/12c9f151-8187-4008-ad14-5b9691cffe0d" />


**Steps**

1. The user sends a document to the Ingestion API.
2. The document is **parsed** to extract its text.
3. The text is **not cleaned**. The same raw parsed data is used as it is.
4. The text is split into chunks.
5. Each chunk is converted to a vector by the **embedding model**.
6. The vectors are saved in the **FAISS** vector database.
7. The details (document info, chunk text, ids) are saved in **PostgreSQL**.

### 2. Retrieval Flow

![Retrieval Flow](images/retrieval_flow.png)
<img width="618" height="168" alt="image" src="https://github.com/user-attachments/assets/16f60d5a-3c8b-480d-a86a-337a12f5528f" />


**Steps**

1. The user sends a question to the Retrieval API.
2. The embedding model and the FAISS index are loaded.
3. The query is converted into an embedding.
4. FAISS runs a **similarity search** and returns the **top 3** closest chunks.
5. The context is built from these chunks.
6. The **prompt**, the **context** and the **user query** are sent to the LLM through its API.
7. The LLM generates the answer, and the API returns it to the user.

---

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

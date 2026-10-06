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
| Embedding model | `<your-embedding-model>` |
| Vector database | FAISS |
| Relational database | PostgreSQL (SQLAlchemy) |
| LLM | `<your-llm-provider>` (via API) |
| Containerization | Docker / Docker Compose |

---

## How It Works

### 1. Ingestion Flow

![Ingestion Flow](images/ingestion_flow.png)

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

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/zcodex8/RAG_Ingest_retrieve.git
cd RAG_Ingest_retrieve
```

### 2. Create the `.env` file

```env
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
DATABASE_URL=postgresql://your_db_user:your_db_password@localhost:5432/your_db_name
LLM_API_KEY=your_llm_api_key
```

> Never commit `.env` to Git. It is already listed in `.gitignore`.

### 3. Run locally

```bash
python -m venv .rag
.rag\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn App.main:app --reload
```

### 4. Run with Docker

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`.
Interactive docs (Swagger): `http://localhost:8000/docs`

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/<ingestion-endpoint>` | Upload a document, parse, embed and store it |
| POST | `/<retrieval-endpoint>` | Ask a question and get an answer |

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

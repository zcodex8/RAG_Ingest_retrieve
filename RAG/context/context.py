from fastapi import FastAPI,HTTPException
from langchain_community.vectorstores import FAISS
from embedding.embedding import embedding

vectorestore = FAISS.load_local(
    "Rag_db",
    embedding,
    allow_dangerous_deserialization=True
)

def retrieve(query:str)->str:
    "Retrieve the relievent document from Faiss db"
    try:
      result = vectorestore.similarity_search(query, k=3)

      final_result = "/n/n".join(
            (f"context:{r.page_content}")
          for r in result
        )
      return final_result
    except:
     raise HTTPException(
        status_code=404,
        detail="No context found"
    )
     

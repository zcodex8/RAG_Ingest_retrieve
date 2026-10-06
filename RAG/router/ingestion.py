from  pypdf import PdfReader
from io import BytesIO
from pypdf.errors import PdfStreamError
from fastapi import FastAPI,HTTPException,APIRouter, UploadFile,File,status,Depends
from chunking import chunks
import json
from embedding import embedding
from langchain_huggingface.embeddings import  HuggingFaceEmbeddings
from fastapi import FastAPI,HTTPException
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from embedding.embedding import embedding
from model import model
from database.database import get_db
from sqlalchemy.orm import session



router = APIRouter(tags=["Ingestion"])


@router.post("/Ingestion")
async def Ingest(file:UploadFile=File(),db: session = Depends(get_db)):

    
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    try:
        read = await file.read()
        pdf = BytesIO(read)
        reader = PdfReader(pdf,strict=False)


        text = ""

        for page in reader.pages:
            data = page.extract_text()

            if data:
                 text += data

        chunk_file = chunks.spliter(text)
        

        items = chunk_file
        docs = [Document(page_content=item)
                for item in chunk_file]
        
        

        vectoredb = FAISS.from_documents(docs,embedding)

        DB= vectoredb.save_local("Rag_db")

        filename = file.filename
        data = model.document(
            filename = filename
        )
        db.add(data)
        db.commit()

        return{"chunks":"success"} 

    
    except PdfStreamError:
        raise HTTPException(status_code=400,detail="The uploaded file is corrupted")
from langchain_text_splitters import RecursiveCharacterTextSplitter
from fastapi import FastAPI,HTTPException
    
    
data =[]
def spliter(text):
    try:  
       text_spliter = RecursiveCharacterTextSplitter(chunk_size=50,chunk_overlap=35)
       chunks = text_spliter.split_text(text)
       for c in chunks:
            data.append(c)
       return data    
    except:
        raise HTTPException(
            status_code=400,
            detail="something wrong in chunking"
        )
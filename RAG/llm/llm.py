from groq import Groq
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os
from fastapi import HTTPException

load_dotenv()

try:
    Api = os.getenv("Api")
    model = os.getenv("model")
    model= ChatGroq(model=model,api_key=Api,temperature=0.5,max_completion_tokens=1024,top_p=1,stream=False,stop=None)
except:
    raise HTTPException(
        status_code=400,
        detail="something is wrong with Api"
    )
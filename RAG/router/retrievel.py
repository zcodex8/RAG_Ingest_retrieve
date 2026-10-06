from fastapi import FastAPI,HTTPException,APIRouter, UploadFile,File,status,Depends
from context.context import retrieve
from llm.llm import model
from prompt.prompt import prompt



router = APIRouter(tags=["response"])


@router.get('/reponse')
async def response(query:str):

    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="This is Not valid")
    try:
        context = retrieve(query)
        chain = prompt | model
        response = chain.invoke({"context":context, "query":query})

        return {"Ai":response.content}
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No response invoked"
        )


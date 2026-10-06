from fastapi import FastAPI
from pydantic import BaseModel
from router import ingestion,retrievel
from database.database import base,get_db,engine


base.metadata.create_all(bind=engine)


app = FastAPI()



app.include_router(ingestion.router)
app.include_router(retrievel.router)
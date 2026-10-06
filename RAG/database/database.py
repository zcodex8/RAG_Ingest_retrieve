from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext import declarative
import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


DB_url = os.getenv("DB")

engine = create_engine(DB_url)

sessionlocal = sessionmaker(autoflush=False,bind=engine) 

base = declarative.declarative_base()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

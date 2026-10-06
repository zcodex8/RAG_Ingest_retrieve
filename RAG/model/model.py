from sqlalchemy.orm import mapped_column,sessionmaker
from database.database import get_db,base
from sqlalchemy import String,Integer





class document(base):
    __tablename__ = "Docs"

    id  = mapped_column(Integer,primary_key=True,index=True)
    filename = mapped_column(String,nullable=False)
    file_ext = mapped_column(String,default=".pdf",nullable=False)
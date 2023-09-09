import os
import sys

project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

    
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from connect_db import create_db_engine
from sqlalchemy.orm import sessionmaker

engine = create_db_engine()  
Session = sessionmaker(bind=engine)

Base = declarative_base()

class SearchResult(Base):
    __tablename__ = 'search_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    query = Column(String(length=255), nullable=True)  
    title = Column(String(length=255), nullable=True)  
    snippet = Column(String(length=1024), nullable=True)  
    url = Column(String(length=512), nullable=True) 
    category = Column(String(length=100), nullable=True)  
    intent_desc = Column(String(length=512), nullable=True) 
    intent_label = Column(String(length=64), nullable=True)  
    query_date = Column(DateTime(timezone=True), nullable=True)  
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # Keep timestamp as non-nullable

    Base.metadata.create_all(engine)

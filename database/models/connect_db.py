from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

def create_db_engine():
    """
    Create and return a SQLAlchemy engine based on the connection string from environment variables.
    """
    CONN_STR = os.getenv('CONN_STR')
    return create_engine(CONN_STR)

from sqlalchemy.orm import declarative_base
from sqlalchemy import BINARY, TIMESTAMP, Column, ForeignKey, Index, Integer, String, DateTime, Text
from sqlalchemy.sql import func


Base = declarative_base()


class QueryIntent(Base):
    __tablename__ = "query_intents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    query = Column(String(length=255), nullable=True)
    intent_desc = Column(String(length=512), nullable=True)
    query_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )


class SearchResult(Base):
    __tablename__ = "search_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text(collation="utf8mb4_unicode_ci"))
    snippet = Column(Text(collation="utf8mb4_unicode_ci"))
    url = Column(String(length=650))
    position = Column(Integer)
    search_engine = Column(String(length=8))
    scraping_id = Column(String(36, collation="utf8mb4_unicode_ci"))
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    query_id_index = Index('query_id_index', QueryIntent.id) 
    query_id = Column(
        Integer, ForeignKey("query_intents.id", ondelete="CASCADE"), nullable=False
    )

    def __init__(self, title: str, snippet: str, url: str, position: int, search_engine: str, query_id: int):
        self.title = title
        self.snippet = snippet
        self.url = url
        self.position = position
        self.search_engine = search_engine.lower()
        self.query_id = query_id

    def as_dict(self):
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "query_id": self.query_id,
            "search_engine": self.search_engine,
        }
        


  



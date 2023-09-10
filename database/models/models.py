from sqlalchemy.orm import declarative_base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.sql import func


Base = declarative_base()


class QueryIntent(Base):
    __tablename__ = "query_intents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    query = Column(String(length=255), nullable=True)
    intent_desc = Column(String(length=512), nullable=True)
    query_date = Column(DateTime(timezone=True), nullable=True)
    category = Column(String(length=128), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )


class SearchResult(Base):
    __tablename__ = "search_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text(collation="utf8mb4_unicode_ci"))
    snippet = Column(Text(collation="utf8mb4_unicode_ci"))
    url = Column(String(length=512))
    position = Column(Integer)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    query_id = Column(
        Integer, ForeignKey("query_intents.id", ondelete="CASCADE"), nullable=False
    )

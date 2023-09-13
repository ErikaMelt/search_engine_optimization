from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from database.models.connect_db import create_db_engine
from database.repository.query_intent_repository import add_query_intent_data_from_csv
from database.models.models import QueryIntent, SearchResult


def setup_database():
    engine = create_db_engine()

    with engine.connect() as connection:
        inspector = inspect(connection)
        if not inspector.has_table(QueryIntent.__table__.name):
            QueryIntent.metadata.create_all(engine)
            add_query_intent_data_from_csv()

        if not inspector.has_table(SearchResult.__table__.name):
            SearchResult.metadata.create_all(engine)

    # Create foreign key constraint after both tables exist
    if inspector.has_table(QueryIntent.__table__.name) and inspector.has_table(
        SearchResult.__table__.name
    ):
        from sqlalchemy import ForeignKeyConstraint

        ForeignKeyConstraint(
            columns=[SearchResult.__table__.c.query_id],
            refcolumns=[QueryIntent.__table__.c.id],
        ).create(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    session.close()

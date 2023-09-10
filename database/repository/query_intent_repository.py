import pandas as pd
from database.models.connect_db import create_db_engine
from database.models.models import QueryIntent
from sqlalchemy.orm import sessionmaker


def add(query_intent):
    """
    Add multiple intents to the database in a single session.

    Args:
        search_results: List of Querys instances to add.
    """
    engine = create_db_engine()
    Session = sessionmaker(bind=engine)

    try:
        session = Session()
        session.bulk_save_objects(query_intent)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_queries(limit=20):
    """
    Get a list of queries from the database with an optional limit.

    Args:
        limit: Maximum number of queries to retrieve (default is 20).

    Returns:
        List of SearchResult instances.
    """
    engine = create_db_engine()
    Session = sessionmaker(bind=engine)

    try:
        session = Session()
        queries = (
            session.query(QueryIntent)
            .order_by(QueryIntent.created_at)
            .limit(limit)
            .all()
        )
        query_data = [(query, query.id) for query in queries]

        return query_data
    except Exception as e:
        raise e
    finally:
        session.close()


def add_query_intent_data_from_csv():
    try:

        df = pd.read_csv("notebooks/cleaned_data/df_clean.csv")

        query_intents = []
        for _, row in df.iterrows():
            query = QueryIntent(
                query=row["query"],
                intent_desc=row["intent"],
                query_date=row["query_date_time"],
            )
            query_intents.append(query)

        add(query_intents)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

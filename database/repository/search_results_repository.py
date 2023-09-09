from database.models.search_result import SearchResult
from sqlalchemy.orm import sessionmaker
from database.models.connect_db import create_db_engine  

def add_search_results(search_results):
    """
    Add multiple search_results to the database in a single session.

    Args:
        search_results: List of SearchResult instances to add.
    """
    engine = create_db_engine()  
    Session = sessionmaker(bind=engine)

    try:
        session = Session()
        session.bulk_save_objects(search_results)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def edit_search_result(search_result_id, new_data):
    """
    Edit a search_result by ID with new data.

    Args:
        search_result_id: ID of the search_result to edit.
        new_data: Dictionary containing new data.
    """
    engine = create_db_engine()  
    Session = sessionmaker(bind=engine)

    try:
        session = Session()
        search_result = session.query(SearchResult).get(search_result_id)
        if search_result:
            for key, value in new_data.items():
                setattr(search_result, key, value)
            session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def delete_search_result(search_result_id):
    """
    Delete a search_result by ID.

    Args:
        search_result_id: ID of the search_result to delete.
    """
    engine = create_db_engine()  
    Session = sessionmaker(bind=engine)

    try:
        session = Session()
        search_result = session.query(SearchResult).get(search_result_id)
        if search_result:
            session.delete(search_result)
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
        queries = session.query(SearchResult).order_by(SearchResult.timestamp).limit(limit).all()
        return queries
    except Exception as e:
        raise e
    finally:
        session.close()
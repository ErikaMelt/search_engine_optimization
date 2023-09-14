import logging
import uuid

from sqlalchemy import desc, select, union
import config
from database.models.evaluation_data import EvaluationData
from database.models.models import QueryIntent, SearchResult
from sqlalchemy.orm import sessionmaker
from database.models.connect_db import create_db_engine


def add(search_results):
    """
    Add multiple search_results to the database in a single session.

    Args:
        search_results: List of SearchResult instances to add.

    Returns:
        str: The generated scraping_id.
    """
    engine = create_db_engine()
    Session = sessionmaker(bind=engine)
    scraping_id = uuid.uuid4().hex

    try:
        session = Session()
        for result in search_results:
            if isinstance(result, SearchResult):
                result.scraping_id = scraping_id

        session.bulk_save_objects(search_results)
        session.commit()

        return scraping_id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def edit(search_result_id, new_data):
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
        logging.error(f"SearchResult repository: {e}")
    finally:
        session.close()


def delete(search_result_id):
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


def retrieve_search_results_by_scraping_id(scraping_id):
    """
    Retrieve a list of search_results

    Args:
        scraping_id: scraping_id of the search_result to retrieve.

    Returns:
        List: The search results retrieved
    """
    engine = create_db_engine()
    Session = sessionmaker(bind=engine)

    try:
        session = Session()
        search_results = (
            session.query(SearchResult).filter_by(scraping_id=scraping_id).all()
        )
        session.expunge_all()
        session.commit()

        return search_results
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def retrieve_search_result_and_query_intent(query_id):
    """
    Retrieve a list of search_results

    Args:
        query_id: query_id of the search_result to retrieve.

    Returns:
        List: The search results and the query intent retrieved
    """
    engine = create_db_engine()
    Session = sessionmaker(bind=engine)

    try:
        session = Session()
        bing_results = (
            session.query(SearchResult, QueryIntent)
            .filter(
                SearchResult.query_id == query_id,
                SearchResult.search_engine == config.CONST_BING,
            )
            .join(QueryIntent, SearchResult.query_id == QueryIntent.id)
            .order_by(desc(SearchResult.created_at))
            .limit(4)
            .all()
        )

        google_results = (
            session.query(SearchResult, QueryIntent)
            .filter(
                SearchResult.query_id == query_id,
                SearchResult.search_engine == config.CONST_GOOGLE,
            )
            .join(QueryIntent, SearchResult.query_id == QueryIntent.id)
            .order_by(desc(SearchResult.created_at))
            .limit(4)
            .all()
        )
        combined_results_query = bing_results + google_results
        print(combined_results_query)

        combined_results = []

        for result, query_intent in combined_results_query:
            combined_result = EvaluationData(
                query_id=result.query_id,
                intent_desc=query_intent.intent_desc,
                title=result.title,
                url=result.url,
                snippet=result.snippet,
                search_engine=result.search_engine,
                scraping_id=result.scraping_id,
                position=result.position,
                id=result.id,
            )

            combined_results.append(combined_result)

        return combined_results
    except Exception as e:
        raise e
    finally:
        session.close()


def retrieve_search_results_by_query_id(query_id):
    """
    Retrieve a list of search_results

    Args:
        query_id: query_id of the search_result to retrieve.

    Returns:
        List: The search results retrieved
    """
    engine = create_db_engine()
    Session = sessionmaker(bind=engine)

    try:
        session = Session()
        search_results = session.query(SearchResult).filter_by(query_id=query_id).all()
        session.expunge_all()
        session.commit()

        return search_results
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

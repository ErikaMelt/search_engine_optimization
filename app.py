import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, project_root)

from database.models.create_tables import setup_database
from database.repository.search_results_repository import add
from database.repository.query_intent_repository import get_queries
from scraper.scraper import scrape_bing


script_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, project_root)


if __name__ == "__main__":

    setup_database()
    queries_data = get_queries(20)

    if queries_data:
        for query, query_id in queries_data:
            print(query.query, query_id)
            search_results = scrape_bing(query.query, query_id)
            if search_results:
               add(search_results) 
import os
import sys
import time

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, project_root)


from database.models.create_tables import setup_database
from database.repository.search_results_repository import add
from database.repository.query_intent_repository import get_queries
from scraper.scraper_bing import scrape_bing
from scraper.scraper_google import scrape_google
from gpt_model.gpt_35_model import generate_evaluation
from multiprocessing import Pool
from functools import partial
import traceback


script_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, project_root)
CONST_BING = "bing"
CONST_GOOGLE = "google"

# Define a function to scrape and add search results
def scrape_and_add(query, query_id, search_engines):
    try:
        search_results = []

        if CONST_BING in search_engines:
            bing_results = scrape_bing(query, query_id)
            if bing_results:
                search_results.extend(bing_results)

        if CONST_GOOGLE in search_engines:
            google_results = scrape_google(query, query_id)
            if google_results:
                search_results.extend(google_results)

        if search_results:
            add(search_results)
    except Exception as e:
        traceback.print_exc()  # Print the exception traceback for debugging


if __name__ == "__main__":

    #setup_database()
    queries_data = get_queries(20)

    if queries_data:
        # Define the number of processes to use (adjust as needed)
        num_processes = 4

        # Specify the search engines to use
        search_engines = [CONST_BING, CONST_GOOGLE]

        # Create a pool of worker processes
        pool = Pool(processes=num_processes)

        scrape_and_add_partial = partial(scrape_and_add, search_engines=search_engines)

        start_time = time.time()
        # Process all queries with Bing and Google
        queries = [(query.query, query_id) for query, query_id in queries_data]
        pool.starmap(scrape_and_add_partial, queries)

        end_time = time.time()

        # Calculate and print the total processing time
        total_processing_time = end_time - start_time
        print(f"Total processing time: {total_processing_time} seconds")

        # Close the pool of worker processes
        pool.close()
        pool.join()

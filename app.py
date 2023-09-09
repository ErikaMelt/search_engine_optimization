import os
import sys
from database.repository.search_results_repository import get_queries
from scraper.scraper import scrape_bing

script_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.insert(0, project_root)


if __name__ == '__main__':
    queries = get_queries(20)  
    
    if queries:
        # Send the first query to the scraper initially
        first_query = queries[0]
        print(f'query:{first_query.query}')
        result = scrape_bing(first_query.query)
        if result:
            print(result)
            # Update the database with the result for the first query
            # edit_search_result(first_query.id, {'result': result})

        # Now, iterate through the remaining queries and scrape them
        """   for query in queries[1:]:
            result = scrape_bing(query.query)
            if result:
                edit_search_result(query.id, {'result': result}) """



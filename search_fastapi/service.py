from database.repository.query_intent_repository import get_queries
from scraper.scraper_bing import scrape_bing
from scraper.scraper_google import scrape_google


def get_query_data():
    queries_data = get_queries(20)
    return queries_data


def scrape_bing_and_google_results(queries_data):
    results = []
    for query_dict in queries_data:
        query_string = query_dict.get("query", "")
        query_id = query_dict.get("query_id", "")
        bing_results = scrape_bing(query_string, query_id)
        google_results = scrape_google(query_string, query_id)
        results.extend(bing_results)
        results.extend(google_results)
    return results

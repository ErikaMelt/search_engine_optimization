from dotenv import load_dotenv
import requests
import os
import sys
import asyncio

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, project_root)

SCRAPER_ENDPOINT = "http://127.0.0.1:8000/api"


async def main():
    load_dotenv()
    scraping_id = "6041d475e6ca4faf9f8b57ccbabf5a7a"

    query_data = requests.get(SCRAPER_ENDPOINT + "/get_queries?" + scraping_id).json()

    response = requests.post(SCRAPER_ENDPOINT + "/scrape", json=query_data)

    if response.status_code != 200:
        print(response.text)
        return

    data = response.json()
    guid = data.get("guid")

    response = requests.get(
        SCRAPER_ENDPOINT + "/get_search_results?scraping_id=" + guid
    ).json()
    if response is None:
        return

    search_results = response.get("search_results")

    results_to_evaluate = {}
    filtered_results = []
    for result in search_results:
        query_id = result.get("query_id")

    filtered_results = [res for res in search_results if res["query_id"] == query_id]

    response = requests.get(
        SCRAPER_ENDPOINT + "/get_combined_query_results?query_id=" + str(query_id)
    ).json()

    results_to_evaluate[query_id] = {
        "query_intent": response["query_intent"],
        "search_results": filtered_results,
    }

    print(f"Results_____{results_to_evaluate}")


if __name__ == "__main__":
    asyncio.run(main())

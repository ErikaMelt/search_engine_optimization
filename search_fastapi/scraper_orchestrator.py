from dotenv import load_dotenv
import requests
import os
import sys
import asyncio

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, project_root)

from search_fastapi.main import get_search_results

SCRAPER_ENDPOINT = 'http://127.0.0.1:8000/api'

async def main():
    load_dotenv()    
    scraping_id='6041d475e6ca4faf9f8b57ccbabf5a7a'
    
    from search_fastapi.main import get_queries
    query_data = requests.get(SCRAPER_ENDPOINT+'/get_queries?'+scraping_id).json()
    
    response = requests.post(SCRAPER_ENDPOINT+'/scrape', json=query_data)

    if response.status_code != 200:
        print(response.text)
        return

    data = response.json()
    guid = data.get("guid")      
            
    response = requests.get(SCRAPER_ENDPOINT+'/get_search_results?scraping_id='+guid).json()
    if response is None:
        return

    for result in response['search_results']:
        print(result)
        

if __name__ == "__main__":
    asyncio.run(main())

import os
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv

from database.models.models import SearchResult

load_dotenv()

BING_SEARCH_URL = os.getenv("BING_SEARCH_URL")


def scrape_bing(query, query_id):
    results = []
    search_url = BING_SEARCH_URL.format(query=query)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            ol_elements = soup.find_all("li", class_="b_algo")

            if ol_elements:
                position = 0
                for li_element in ol_elements:
                    result = SearchResult()
                    result.title = li_element.find("a").text.encode("utf-8")
                    result.url = li_element.find("a").get("href")
                    result.snippet = li_element.find(
                        "div", {"class": "b_caption"}
                    ).text.encode("utf-8")
                    position += 1
                    result.position = position
                    result.query_id = query_id
                    results.append(result)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
    return results

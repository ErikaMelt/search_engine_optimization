import os
import re
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv

from database.models.models import SearchResult

load_dotenv()

BING_SEARCH_URL = os.getenv("BING_SEARCH_URL")


def scrape_bing(query, query_id=1):
    position = 0
    search_results = []
    search_url = BING_SEARCH_URL.format(query=query)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5023.114 Safari/537.36",
    }
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("li", class_="b_algo")

        if response.status_code == 200 and results:
            for result in results:
                h2_element = result.find("h2")
                if h2_element:
                    title_element = h2_element.find("a")
                    if title_element:

                        title = title_element.text
                    else:
                        title = "No title found"
                else:
                    title = "No title found"
                url = result.find("a")["href"]
                snippet = result.find(
                    "div", {"class": "b_caption", "role": "contentinfo"}
                ).text
                position += 1

                pattern = r"Web(?:\w+\s\d{1,2},\s\d{4}\s·\s)?(.+)"
                matches = re.search(pattern, snippet)
                if matches:
                    cleaned_snippet = matches.group(1).strip()

                search_result = SearchResult(
                    title=title,
                    snippet=cleaned_snippet,
                    url=url,
                    position=position,
                    query_id=query_id,
                )
                search_results.append(search_result)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
    return search_results

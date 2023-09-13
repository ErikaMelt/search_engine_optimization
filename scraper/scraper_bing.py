import logging
import os
import re
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
from scraper.data_preprocessing.text_processing import clean_text
from config import *

from database.models.models import SearchResult

load_dotenv()

BING_SEARCH_URL = os.getenv("BING_SEARCH_URL")

def get_source(search_url):
    try:
        response = requests.get(search_url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("li", class_="b_algo")
        return results
    except requests.exceptions.RequestException as e:
        logging.error(f"Scraping Bing error: {e}")
        return None
    except Exception as e:
        logging.error(f"Scraping Bing error: {e}")
        return None


def parse_results(results, query_id):
    position = 0
    search_results = []

    if results:
        for result in results:
            h2_element = result.find("h2")
            if h2_element:
                title_element = h2_element.find("a")
                title = (
                    title_element.text
                    if title_element is not None
                    else "No title found"
                )

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
                    search_engine= CONST_BING,
                    query_id=query_id,
                )
                search_results.append(search_result)
    return search_results


def scrape_bing(query, query_id):
    search_url = BING_SEARCH_URL.format(query=query)
    results = get_source(search_url)
    search_results = parse_results(results, query_id=query_id)
    search_results_clean = clean_text(search_results)
    return search_results_clean

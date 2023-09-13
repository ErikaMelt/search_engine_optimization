import os
import re
import requests
from requests_html import HTMLSession
import logging

from database.models.models import SearchResult
from config import *
from scraper.data_preprocessing.text_processing import clean_text

URL = os.getenv("GOOGLE_SEARCH_URL")

def get_source(url):
    """Return the source code for the provided URL.

    Args:
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html.
    """

    try:
        session = HTMLSession()
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()
        return response

    except requests.exceptions.RequestException as e:
        logging.error(f"Scraping Google error: {e}")
        return None
    except Exception as e:
        logging.error(f"Scraping Google error: {e}")
        return None


def parse_results(response, query_id):

    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".VwiC3b"

    results = response.html.find(css_identifier_result)

    search_results = []
    position = 0

    for result in results:
        title_element = result.find(css_identifier_title, first=True)
        url_element = result.find(css_identifier_link, first=True)
        snippet_element = result.find(css_identifier_text, first=True)

        title = title_element.text if title_element is not None else "No title found"
        url = url_element.attrs["href"] if url_element is not None else "No url found"
        snippet = (
            snippet_element.text if snippet_element is not None else "No snippet found"
        )
        position += 1

        pattern = r"[A-Za-z]{3} \d{1,2},? \d{4} — (.*?)\. (.*)"
        matches = re.search(pattern, snippet)
        if matches:
            snippet = matches.group(1).strip()

        search_result = SearchResult(
            title=title,
            snippet=snippet,
            url=url,
            position=position,
            search_engine= CONST_GOOGLE,
            query_id=query_id
        )
        search_results.append(search_result)

    return search_results


def scrape_google(query, query_id):
    search_url = URL.format(query=query)
    response = get_source(search_url)
    if response is not None:
        output = parse_results(response, query_id)
    else:
        output = []
    search_results_clean = clean_text(output)
    return search_results_clean

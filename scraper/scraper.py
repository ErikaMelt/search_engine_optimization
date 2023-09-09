import os
import sys

database_module_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "database", "repository")
)
sys.path.append(database_module_path)
print(f"PATH:{database_module_path}")

from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests

from database.repository.search_results_repository import get_queries

load_dotenv()

BING_SEARCH_URL = os.getenv("BING_SEARCH_URL")


def scrape_bing(query):
    params = {"q": query}
    headers = {"User-Agent": "MyWebScraper/1.0"}

    try:
        response = requests.get(BING_SEARCH_URL, params=params, headers=headers)
        response.raise_for_status()

        if response.status_code == 200:
            # Parse the HTML content of the search results page
            soup = BeautifulSoup(response.text, "html.parser")

            # Locate the main element that contains search results
            main_element = soup.find("ol", id="b_results")

            if main_element:
                # Find all div elements with class "tpcn"
                tpcn_elements = main_element.find_all("div", class_="tpcn")

                # Find all div elements with class "b_title"
                b_title_elements = main_element.find_all("div", class_="b_title")

                # Find all div elements with class "b_caption"
                b_caption_elements = main_element.find_all("div", class_="b_caption")

                # Find all div elements with class "sis"
                sis_elements = main_element.find_all("div", class_="sis")

                # Find all li elements with class "b_algo" and data attributes
                b_algo_elements = soup.find_all(
                    "li",
                    class_="b_algo",
                    attrs={"data-tag": True, "data-partnertag": True},
                )

                # Create a dictionary to store all the elements
                result = {
                    "tpcn": [elem.prettify() for elem in tpcn_elements],
                    "b_title": [elem.prettify() for elem in b_title_elements]
                }

                return result
            else:
                print("Main element 'b_results' not found in the HTML.")
                return None
        else:
            print(
                f"Error: Request was not successful (status code {response.status_code})."
            )
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

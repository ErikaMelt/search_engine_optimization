import os
import sys
import pandas as pd
from database.models.search_result import SearchResult
from database.repository.search_results_repository import add_search_results

project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)


def insert_data():
    try:

        df = pd.read_csv("notebooks/cleaned_data/df_clean.csv")

        search_results = []
        for _, row in df.iterrows():
            search_result = SearchResult(
                query=row["query"],
                intent_desc=row["intent"],
                query_date=row["query_date_time"],
                category=None,
                intent_label=None,
                title=None,
                snippet=None,
                url=None,
            )
            search_results.append(search_result)

        add_search_results(search_results)
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    insert_data()

import json
import logging
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, project_root)


from database.repository.search_results_repository import (
    add,
    retrieve_search_result_and_query_intent,
    retrieve_search_results_by_scraping_id,
)
from database.repository.query_intent_repository import retrieve_query_by_id
from gpt_model.gpt_35_model import generate_evaluation
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from search_fastapi.service import get_query_data, scrape_bing_and_google_results

app = FastAPI()


@app.get("/api/get_queries")
async def get_queries():
    queries = get_query_data()
    return JSONResponse(content={"queries": queries}, status_code=200)


@app.post("/api/scrape")
async def scrape_results(query_data: dict):
    queries = query_data["queries"]
    search_results = scrape_bing_and_google_results(queries)
    guid = add(search_results)
    return JSONResponse(content={"guid": guid}, status_code=200)


@app.get("/api/get_search_results")
async def get_search_results(
    scraping_id: str = Query(
        ..., description="The scraping ID to retrieve search results"
    )
):
    try:
        search_results = retrieve_search_results_by_scraping_id(scraping_id)
        if not search_results:
            raise HTTPException(status_code=404, detail="Scraping ID not found")

        results_dict = [result.as_dict() for result in search_results]
        return JSONResponse(content={"search_results": results_dict}, status_code=200)
    except HTTPException as e:
        logging.error(e)
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)
    except Exception as e:
        logging.error(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/api/get_query_by_id")
async def get_query_by_id(
    query_id: str = Query(..., description="The query ID to retrieve query intent")
):
    try:
        query_intent = retrieve_query_by_id(query_id)
        if not query_intent:
            raise HTTPException(status_code=404, detail="Query id not found")
        return JSONResponse(content={"query_intent": query_intent}, status_code=200)
    except HTTPException as e:
        logging.error(e)
        return JSONResponse(content={"error": str(e)}, status_code=e.status_code)
    except Exception as e:
        logging.error(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/api/get_combined_query_results")
async def get_combined_query_results(
    query_id: str = Query(
        ..., description="The query ID to retrieve query intent and search results"
    )
):
    try:
        query_intent = retrieve_query_by_id(query_id)
        if not query_intent:
            raise HTTPException(status_code=404, detail="Query id not found")

        combined_results = retrieve_search_result_and_query_intent(query_id)
        result_dicts = [
            combined_result.as_dict() for combined_result in combined_results
        ]
        return JSONResponse(content={"results": result_dicts}, status_code=200)
    except HTTPException as e:
        logging.error(e)
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)
    except Exception as e:
        logging.error(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/api/evaluate")
async def evaluate_search_results(evaluation_data: dict) -> JSONResponse:
    evaluation_data_list = evaluation_data["results"]
    evaluation_results = generate_evaluation(evaluation_data_list)
    return JSONResponse(
        content={"evaluation_results": evaluation_results}, status_code=200
    )

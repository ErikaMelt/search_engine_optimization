import logging
import os
import sys


script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, project_root)


from database.models.connect_db import create_db_engine
from database.repository.search_results_repository import add, retrieve
from gpt_model.gpt_35_model import generate_evaluation
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from search_fastapi.service import get_query_data, scrape_bing_and_google_results
from sqlalchemy.orm import sessionmaker

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
async def get_search_results(scraping_id: str = Query(..., description="The scraping ID to retrieve search results")):
    try:        
        search_results = retrieve(scraping_id)        
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

# @app.post("/evaluate")
# async def scrape_results(search_results: json):
#     evaluation_results = generate_evaluation(search_results)
#     return JSONResponse(
#         content={"evaluation_results": evaluation_results}, status_code=200
#     )

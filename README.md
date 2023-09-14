# Search Optimization Project

## Overview

The Search Optimization project is designed to enhance the relevance and clarity of search engine results for specific user intents. This project involves data scraping, data preprocessing, and utilizing the GPT-3.5 Davinci model from OpenAI to evaluate and improve search results.

### Components

- **Dataset**: The project relies on a dataset containing user queries and associated intents. This dataset serves as the foundation for generating search queries.

- **Web Scraping**: Bing and Google search engines are scraped to retrieve search results for each user intent. These results are stored in a MySQL database for further analysis.

- **Data Preprocessing**: Before sending the search results for evaluation, the project performs data preprocessing. This includes tasks like removing stop words and lemmatization to clean the text data.

- **GPT-3.5 Davinci Model**: The OpenAI GPT-3.5 Davinci model is used via the OpenAI API. It analyzes search results for each intent, assigning relevance scores (1-5), suggesting improvements, and identifying the best search engine (Google or Bing) for that intent.

```bash
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=0.2,
    )


Prompt example: ![image](https://github.com/ErikaMelt/search_engine_optimization/assets/104458004/12ea43c7-6605-4a83-ac05-8d7b0ff7d952)

```
- **API**: The project exposes an API using FastAPI, allowing users to interact with the system. Users can submit intents, retrieve search results, and receive optimized results with relevance scores.

- **Dependencies**: Poetry is used for managing project dependencies, ensuring a clean and reproducible environment.

- **Backend**: The backend of the project is developed in Python, leveraging libraries like SQLAlchemy for database interaction and SpaCy for data preprocessing.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/search-optimization.git
   cd search-optimization
   
2. **Install project dependencies using poetry:**
```bash
poetry install
```

3. **Set up a MySQL database for storing search results and update the database configuration in the project settings.**

4. **Start the FastAPI server:**
```
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

5. Access the FastAPI documentation at http://localhost:8000/docs to explore available API endpoints.

Use the API to submit intents, retrieve search results, and receive optimized results with relevance scores and suggestions:

![image](https://github.com/ErikaMelt/search_engine_optimization/assets/104458004/68ae8ffe-6187-4e3f-8f3a-edceab0a4003)

![image](https://github.com/ErikaMelt/search_engine_optimization/assets/104458004/8ab92249-3c68-4b9e-acb0-7b26eac6df8d)

![image](https://github.com/ErikaMelt/search_engine_optimization/assets/104458004/5448b3dc-ea13-42f5-b223-70cd80277531)

![image](https://github.com/ErikaMelt/search_engine_optimization/assets/104458004/3785ea34-8e97-4ce0-b979-ca031e4a28e9)




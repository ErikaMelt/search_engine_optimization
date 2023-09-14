import os
from dotenv import load_dotenv
import openai

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


def generate_evaluation(evaluation_data_list):
    # Create a list to store the prompts for each search result
    prompts = []

    for evaluation_data in evaluation_data_list:
        intent_desc = evaluation_data["intent_desc"]
        title = evaluation_data["title"]
        url = evaluation_data["url"]
        snippet = evaluation_data["snippet"]
        search_engine = evaluation_data["search_engine"]
        position = evaluation_data["position"]
        result_id = evaluation_data["id"]

        # Create a prompt for each search result
        prompt = f"""
        Evaluate the following search result for the intent: '{intent_desc}'
        Title: '{title}'
        Snippet: '{snippet}'
        URL: '{url}'
        Search engine: '{search_engine}'
        position: '{position}
        result_id: '{result_id}
              
        Provide Relevance score: [1 to 5]
        Improvement Suggestion: [clear and concise suggestion and whether the title, url or snippet should be changed]
        Best Search Engine: [Bing, Google]
        Best Result ID: [result_id]
        """
        prompts.append(prompt)

    # Combine all prompts into one
    combined_prompt = "\n".join(prompts)

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=combined_prompt,
        max_tokens=200,
        temperature=0.2,
    )

    evaluation = response.choices[0].text

    return evaluation

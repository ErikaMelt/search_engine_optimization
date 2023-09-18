import os
from dotenv import load_dotenv
import openai

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


def generate_evaluation(evaluation_data_list):
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
        **Title:** '{title}'
        **Snippet:** '{snippet}'
        **URL:** '{url}'
        **Search Engine:** '{search_engine}'
        **Position:** '{position}'
        **Result ID:** '{result_id}'
              
        Please provide a Relevance score between 1 (not relevant) and 5 (highly relevant) based on the given information.
        If you have any suggestions for improvement, please be clear and concise. Mention whether the title, URL, or snippet should be changed.
        Finally, select the Best Search Engine for this intent: [Bing, Google] and specify the Best Result ID from the provided options.
        """
        prompts.append(prompt)

    combined_prompt = "\n".join(prompts)

    print(combined_prompt)

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=combined_prompt,
        max_tokens=200,
        temperature=0.2,
    )

    evaluation = response.choices[0].text
    return evaluation

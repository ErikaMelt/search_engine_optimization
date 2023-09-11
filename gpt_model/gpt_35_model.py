import json
import os
from dotenv import load_dotenv
import openai

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def generate_evaluation(json_data):
    data = json.loads(json_data)

    intents = data.get("intents", [])

    if not intents or len(intents) == 0:
        return "No search results were found."

    prompt = "Please evaluate the following search results based on the provided intents:\n\n"

    for intent in intents:
        intent_name = intent.get("intent", "")
        results = intent.get("results", [])

        prompt += f"Intent: {intent_name}\n\n"

        for result in results:
            title = result.get("title", "")
            snippet = result.get("snippet", "")
            url = result.get("url", "")

            # Append search result information
            prompt += f"Title: {title}\n"
            prompt += f"Snippet: {snippet}\n"
            prompt += f"URL: {url}\n\n"

            # Request ratings and improvement suggestion
            prompt += "Relevance: [Your Relevance Score, 1 to 5]\n"
            prompt += "Clarity: [Your Clarity Score, 1 to 5]\n"
            prompt += "Improvement Suggestion: [clear and consise suggestion and whether the title should be changed]\n\n"
       
    response = openai.Completion.create(
        engine="text-davinci-003", 
        prompt=prompt, 
        max_tokens=200,  
        temperature=0.2
    )

    evaluation = response.choices[0].text

    return evaluation

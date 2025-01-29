
import requests
import json
from ChatPathways.python_scripts.core.llm_models.chatgpt_models import LLMInferenceEngine as LIE
from ChatPathways.python_scripts.utils import prompt_templates

import time

##### #gpt-3.5-turbo-0125
system_prompt="You are a useful assistant. Please provide related citations and include detailed summaries for each."

user_prompt="what were the early observations that spurred interest in the idea of repurposing existing drugs? Give me relevant references"

# user_prompt="""can you provide me with relevant references for the below paragraphs\n \n

# The history of drug repurposing traces its origins to the early 20th century, when scientists began to 
# notice unintended side effects of drugs that suggested potential therapeutic uses beyond their initial indications. 
# A key example of this is Thalidomide, which was originally developed in the 1950s as a sedative and treatment for 
# insomnia, particularly in pregnant women. However, it was later found to cause severe birth defects. Despite this 
# tragic outcome, further research revealed that thalidomide had other beneficial effects, including its use in treating 
# multiple myeloma and leprosy-related complications. This observation led researchers to consider that many drugs might 
# have untapped potential in treating other diseases, setting the foundation for the concept of drug repurposing."""

start= time.time()
LIE.execute_prompt(system_prompt=system_prompt,
                   user_prompt=user_prompt)
end= time.time()
print(f"Running time: {end-start}")





##### #other LLMs
# Open terminal to pull LLMs of interest
# docker exec -it ollama ollama run phi3.5
# docker exec -it ollama ollama run mistral
# docker exec -it ollama ollama run llama3.1:8b

from ollama import Client 
from ollama import chat
from ollama import ChatResponse

system_prompt=system_prompt
user_prompt=user_prompt


start= time.time()
print("================================================")
print(system_prompt)
print(user_prompt)
print("================================================")
client = Client(host="ollama")
response: ChatResponse = client.chat(
    model='phi3.5', #phi3.5, mistral, llama3.1:8b
    messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ]
)
print(response['message']['content'])
end= time.time()
print(f"Running time: {end-start}")






##### #ChatPathways

from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import DuckDuckGoSearchException
import pandas as pd
import time

if len(user_prompt) > 20:
    user_prompt_kw=LIE.execute_prompt(system_prompt=prompt_templates.MAKE_KEYWORDS,
                                        user_prompt=user_prompt)
    search_query = user_prompt_kw + " ncbi"
else:
    search_query = f"{user_prompt} ncbi"

def search_with_retry():
    try:
        results = DDGS().text(keywords=search_query, safesearch="off", timelimit="5y", max_results=5)
        return results
    except DuckDuckGoSearchException as e:
        print(f"Text search failed: {e}")
        # If text search also fails, apply a wait time before retrying
        print("Waiting for 1 second before retrying...")
        time.sleep(1.5)  # Wait before retrying the text search
        # Retry the text search method after delay
        results = DDGS().text(keywords=search_query, safesearch="off", timelimit="5y", max_results=5)
        return results

# Run the function
results = search_with_retry()
results_pd = pd.DataFrame(results)

system_prompt="""
You are an expert scientific writer. Based on the five provided citations below (Citation 1, Citation 2,..., Citation 5), please write a long, detailed summary of them to respond to the user's request.\n 
Citation 1:\n 
title: {} \n 
href: {} \n 
Content: {} \n 

Citation 2:\n 
title: {} \n 
href: {} \n 
Content: {} \n 

Citation 3:\n 
title: {} \n 
href: {} \n 
Content: {} \n 

Citation 4:\n 
title: {} \n 
href: {} \n 
Content: {} \n 

Citation 5:\n 
title: {} \n 
href: {} \n 
Content: {} \n 
Please ensure that you incorporate the provided citations at the relevant points in your text, using sequential markers [1], [2], and so on. 
Additionally, include a References section at the end of your response, listing the citations with their title and href.

Example: Some studies have examined the clinical overlap between the two diseases [1]...

References:
1. {}. ({}).
"""

system_prompt=system_prompt.format(results_pd.iloc[0,0], results_pd.iloc[0,1], results_pd.iloc[0,2], 
                                                                       results_pd.iloc[1,0], results_pd.iloc[1,1], results_pd.iloc[1,2], 
                                                                       results_pd.iloc[2,0], results_pd.iloc[2,1], results_pd.iloc[2,2], 
                                                                       results_pd.iloc[3,0], results_pd.iloc[3,1], results_pd.iloc[3,2], 
                                                                       results_pd.iloc[4,0], results_pd.iloc[4,1], results_pd.iloc[4,2], 
                                                                       results_pd.iloc[0,0], results_pd.iloc[0,1])

start= time.time()
LIE.execute_prompt(system_prompt=system_prompt,
                   user_prompt=user_prompt)
end= time.time()
print(f"Running time: {end-start}")








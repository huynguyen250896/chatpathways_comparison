import os
import uuid
import json 
import requests
import dotenv
from dotenv import load_dotenv
load_dotenv( dotenv.find_dotenv() )

class LLMInferenceEngine:
    
    timeout = 2.5
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.environ.get("OPENAI_API_KEY")}',
    }
    model = {
        'v1': "gpt-3.5-turbo-0125",
        'v2': "gpt-4o-mini"
    }
    api_url = 'https://api.openai.com/v1/chat/completions'

    @staticmethod
    def execute_prompt(system_prompt:str = None, user_prompt:str = "", temperature = 0.7):
        try:
            print("================================================")
            print("Model:", LLMInferenceEngine.model['v1'])
            print("System_prompt:", system_prompt)
            print("User_prompt:", user_prompt)
            print("================================================")
            payload = {
                "model": LLMInferenceEngine.model['v1'],
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                "temperature": temperature
            }
            
            payload_json = json.dumps(payload)   #convert payload in the Python dict into a JSON-formatted string
            response_json = requests.request(method="POST", 
                                        url=LLMInferenceEngine.api_url, 
                                        headers=LLMInferenceEngine.headers,
                                        data=payload_json)
            response_dict = json.loads(response_json.text) #parse the response in a JSON-formatted string into a Python dictionary
            answer = response_dict['choices'][0]['message']['content']
            print("Response from ChatPathways:  ", answer)
            return answer
        except Exception as e:
            return None
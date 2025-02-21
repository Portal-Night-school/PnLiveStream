import requests
from dotenv import load_dotenv
import json
import time
import os

load_dotenv()


API_KANDINSKY = os.getenv("API_KANDINSKY")
SECRET_KEY = os.getenv("SECRET_KEY")

url = "https://api-key.fusionbrain.ai/"

class Kandinsky:
    def __init__(self):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f"Key {API_KANDINSKY}",
            'X-Secret': f"Secret {SECRET_KEY}"
        }
        
    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']
    
    def generate(self, prompt, images=1, width=1024, height=1024):
        model = self.get_model()
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams":{
                "query": f"{prompt}"
            }
        }
        
        data = {
            "model_id": (None, model),
            "params": (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']
    
    def check_generation(self, request_id, attempts=15, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            print(attempts, data)
            if data['status'] == 'DONE':
                return data['images']
            attempts -= 1
            time.sleep(delay)
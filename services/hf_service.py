import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('HF_API_URL')

HEADERS = {
    'Authorization': f'Bearer {os.getenv("HF_TOKEN")}',
}

def call_hf_api(payload):
    response = requests.post(
        API_URL,
        headers=HEADERS,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    return response.json()
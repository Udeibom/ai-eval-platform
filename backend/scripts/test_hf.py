# quick_test.py
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

api_key = os.getenv("HF_API_KEY")
print(f"API Key (first 5 chars): {api_key[:5]}...")

headers = {"Authorization": f"Bearer {api_key}"}
response = requests.post(
    "https://api-inference.huggingface.co/models/gpt2",
    headers=headers,
    json={"inputs": "Hello"}
)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:200]}")
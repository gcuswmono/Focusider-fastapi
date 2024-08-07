# services/gpt_service.py
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GPT_API_KEY")
BASE_URL = os.getenv("GPT_API_BASE_URL")

async def call_gpt_api(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": messages
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        return response.json()

from pydantic_ai import Agent

model = "google-gla:gemini-2.5-flash"
agent = Agent(
    model,
    system_prompt='You are a helpful assistant that can convert currencies.',  
)

import json
import requests
from datetime import datetime

@agent.tool_plain
def convert_currency(from_currency: str, to_currency: str, amount: float, date: str = None) -> str:
    """Convert amount from one currency to another on a specific date (optional)

    Args:
        from_currency (str): The base currency (e.g., 'USD').
        to_currency (str): The target currency (e.g., 'EUR').
        amount (float): The amount to convert.
        date (str, optional): Format 'YYYY-MM-DD'. If None, gets latest rate.

    Returns:
        A JSON string with conversion result.
    """
    base_url = "https://api.exchangerate.host/convert"
    params = {
        "from": from_currency.upper(),
        "to": to_currency.upper(),
        "amount": amount
    }

    if date:
        try:
            datetime.strptime(date, "%Y-%m-%d")
            params["date"] = date
        except ValueError:
            return "Invalid date format. Use YYYY-MM-DD."
    
    print(f"Requesting conversion from {from_currency} to {to_currency} on {date or 'latest'}")
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return json.dumps(data, indent=4)
    else:
        return "Could not retrieve currency data."

from google import genai
from google.genai import types
from IPython.display import Markdown

genai.configure(api_key="AIzaSyDhRYMuQtvKMgcy0Aau7yR_-SjnJipVBVk")
MODEL_ID = "gemini-2.5-flash"

response = genai.GenerativeModel(model_name=MODEL_ID).generate_content(
    contents="What's 100 USD in EUR?",
    generation_config=types.GenerationConfig(),
    tools=[convert_currency]
)

Markdown(response.text)

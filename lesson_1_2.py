import os
from pprint import pprint

import requests
from dotenv import load_dotenv

load_dotenv("./.env")

key = "API_KEY"
open_key = os.getenv(key, None)


def get_response(city, api_key):
    try:
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": api_key}
        response = requests.get(url, params=params)
        json_response = response.json()
        return json_response
    except Exception:
        return None


def print_weather(json_response):
    pprint(json_response)


def pipeline():
    city = "Moscow"
    try:
        response = get_response(city, open_key)
        return print_weather(response)
    except Exception:
        return None


if __name__ == "__main__":
    pipeline()

import requests
import os

def get_route(coordinates):
    API_KEY = os.getenv("ORS_API_KEY")
    url = "https://api.openrouteservice.org/v2/directions/driving-car"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": coordinates
    }
    print(API_KEY)

    response = requests.post(url, json=body, headers=headers)

    if response.status_code != 200:
        raise Exception(response.text)

    return response.json()
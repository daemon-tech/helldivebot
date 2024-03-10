import json
import requests

def fetch_data_from_api(endpoint):
    try:
        response = requests.get(f'https://helldivers-2.fly.dev/api/801/status{endpoint}')
        response.raise_for_status()  
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None
    
    
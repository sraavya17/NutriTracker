import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
usda_api_key = os.getenv("USDA_API_KEY")
search_url = "https://api.nal.usda.gov/fdc/v1/foods/search"

def fetch_data(food_items):
    """Fetch food data from USDA API"""
    food_data = {}
    for item in food_items:
        try:
            params = {"query": item, "api_key": usda_api_key}
            response = requests.get(search_url, params=params)

            if response.status_code == 200:
                foods = response.json().get('foods', [])
                name = response.json()['foods'][0]['description']
                if item.lower() == name.lower():
                    status = "exact_match"
                    nutrients = [
                        {
                            "nutrient": nutrient['nutrientName'],
                            "amount": nutrient['value'],
                            "unit": nutrient['unitName']
                        }
                        for nutrient in response.json()['foods'][0]['foodNutrients']
                    ]
                    food_data[name] = {
                        "status": status,
                        "nutrients": nutrients
                    }
                else:
                    alternatives = [food['description'] for food in foods[:3]]
                    food_data[item] = {
                        "status": "alternatives",
                        "alternatives": alternatives
                    }
            else:
                food_data[item] = {"status": "error", "message": f"Error {response.status_code}"}
        except Exception as e:
            food_data[item] = {"status": "error", "message": str(e)}
    return food_data

def get_nutrient_goals(food_items, user_preferences):
    """Get nutrient goals based on user preferences and fetch food data"""
    with open('nutritional_goals.json', 'r') as file:
        nutrient_goals = json.load(file)

    food_data = fetch_data(food_items)

    user_gender = user_preferences["gender"]
    age = user_preferences["age"]

    user_age = None
    for group in nutrient_goals['data'][user_gender].keys():
        if '-' in group:
            start, end = map(int, group.split('-'))
            if start <= age <= end:
                user_age = group
                break
        elif '+' in group:
            start = int(group.replace('+', ''))
            if age >= start:
                user_age = group
                break
    
    nutrient_data = nutrient_goals["data"][user_gender][user_age]
    return food_data, nutrient_data
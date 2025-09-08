import requests
from dotenv import load_dotenv
import os
from groq import Groq
import json

load_dotenv()

usda_api_key = os.getenv("USDA_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

search_url = "https://api.nal.usda.gov/fdc/v1/foods/search"

def fetch_data(food_items):
    food_data = {}
    for item in food_items:
        print(f"Fetching data for: {item}")
        try:
            params = {
                "query": item,
                "api_key": usda_api_key
            }
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
                print(f"Error fetching data for {item}: {response.status_code}")

        except Exception as e:
            print(f"Error occured fetching data for {item}: {e}")

    return food_data

def user_input():
    food_items = ["apple", "banana", "orange", "honey", "chips"]
    user_preferences = {
        "age": 20,
        "gender": "female",
        "goal": "weight_loss",
        "diet_preference": "vegetarian",
        "allergies": ["peanuts"],
        "calorie_target": 1800
    }
    return food_items, user_preferences

def get_nutrient_goals(food_items, user_preferences):
    with open('nutritional_goals.json', 'r') as file:
        nutrient_goals = json.load(file)

    food_data = fetch_data(food_items)

    categories = ["child", "female"]
    user_gender = user_preferences.get("gender")
    age = user_preferences.get("age")
    age_groups = []
    for category in categories:
        age_groups.extend(age for age in nutrient_goals['data'][category].keys())
    
    for group in age_groups:
        if '-' in group:
            start, end = group.split('-')
            if age >= int(start) and age <= int(end):
                user_age = group
                break
        elif '+' in group:
            start = group.replace('+', '')
            if age >= int(start):
                user_age = group
                break
    nutrient_data = nutrient_goals['data'][user_gender][user_age]
    
    return food_data, nutrient_data
def main():
    food_items, user_preferences = user_input()
    food_data, nutrient_data = get_nutrient_goals(food_items, user_preferences)

    client = Groq(api_key = groq_api_key)
    completion = client.chat.completions.create(
        model = "llama-3.3-70B-Versatile",
        messages = [
            {
                "role": "system",
                "content": "You are a helpful nutrition assistant. You help users understand their dietary intake and make them understand if it aligns with their nutritional goals and preferences."
            },
            {
                "role": "user",
                "content": f"Here is my food intake data for today: {food_data}. My preferences are: {user_preferences}. And the required amount of nutrients required based on gender and age are {nutrient_data} Based on this, provide me with a summary of my nutrient intake and suggest dietary recommendations to help me achieve my health goals."
            }
        ]
    )
    print(completion.choices[0].message.content)


if __name__ == "__main__":
    main()
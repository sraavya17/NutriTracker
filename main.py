import requests
from dotenv import load_dotenv
import os
from llama_cpp import Llama

load_dotenv()

usda_api_key = os.getenv("USDA_API_KEY")

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


def main():
    age = 20
    gender = "female"
    goal = "weight_loss"
    diet_preference = "vegetarian"
    allergies = ["peanuts"]
    calorie_target = 1800

    user_preference = {
        "age": age,
        "gender": gender,
        "goal": goal,
        "diet_preference": diet_preference,
        "allergies": allergies,
        "calorie_target": calorie_target
    }

    user_input = input("Enter comma separated food items to track your nutrients intake: ")
    food_items = [input.strip() for input in user_input.split(',')]
    print(food_items)
    food_data = fetch_data(food_items)
    print(food_data)
    print(user_preference)

    prompt = f"""
    Here are the list of food items:
    {food_items}
    and here are the user preferences:
    {user_preference}
    Now analyze these inputs and check for any dietary restrictions or suggestions.
    """

    llm = Llama.from_pretrained(
	repo_id="sfardin/diet_AI_model_gguf",
	filename="unsloth.Q4_K_M.gguf",
    verbose=False
    )

    output = llm(prompt)
    print(output["choices"][0]["text"])

if __name__ == "__main__":
    main()
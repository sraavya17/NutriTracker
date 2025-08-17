import os
import requests
from dotenv import load_dotenv
load_dotenv()

# get the api key for USDA api
api_key = os.getenv("USDA_API_KEY")

search_url = "https://api.nal.usda.gov/fdc/v1/foods/search"
params = {
    "query":"apple",
    "api_key":api_key
}

# make the request to the API
response = requests.get(search_url, params=params)

print(response.status_code)
# print(response.json()["foods"][0])
print(f"Food Name: {response.json()['foods'][0]['description']}") # fetching the name of the food
print("Nutrients:")
for nutrient in response.json()['foods'][0]['foodNutrients']:
    print(f"{nutrient['nutrientName']} : {nutrient['nutrientNumber']}{nutrient['unitName']}") # fetching the nutrients, their values and their units

# testing on multiple items
items = ['apple', 'banana', 'orange', 'honey', 'chips']

for item in items:
    params = {
        "query": item,
        "api_key": api_key
    }

    response = requests.get(search_url, params=params)

    print(response.status_code)
    print(f"Food Name: {response.json()['foods'][0]['description']}")
    print("Nutrients:")
    for nutrient in response.json()['foods'][0]['foodNutrients']:
        print(f"{nutrient['nutrientName']} : {nutrient['nutrientNumber']}{nutrient['unitName']}")
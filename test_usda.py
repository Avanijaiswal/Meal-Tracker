import os

import requests
from dotenv import load_dotenv

load_dotenv()  # reads the .env file in this folder
api_key = os.getenv("FDC_API_KEY")

print("Key found:", bool(api_key))  # prints True/False, never the key itself
if not api_key:
    raise SystemExit("No key found. Check that .env exists and has FDC_API_KEY=...")

response = requests.get(
    "https://api.nal.usda.gov/fdc/v1/foods/search",
    headers={"X-Api-Key": api_key},
    params={
        "query": "pizza",
        "dataType": "Foundation,SR Legacy",
        "pageSize": 3,
    },
    timeout=15,
)
print("Status:", response.status_code)
response.raise_for_status()

for food in response.json().get("foods", []):
    print("\n" + food["description"])
    for nutrient in food.get("foodNutrients", []):
        if nutrient.get("nutrientNumber") in ("208", "203", "204", "205", "307"):
            print(
                f"  {nutrient['nutrientName']}: "
                f"{nutrient['value']} {nutrient['unitName']}"
            )
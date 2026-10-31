import os
from functools import lru_cache

import requests
from dotenv import load_dotenv

load_dotenv()  # reads FDC_API_KEY from the .env file

SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

# USDA nutrient number -> the short code our report.py already uses
NUTRIENT_CODES = {
    "203": "PROCNT",  # protein (g)
    "204": "FAT",     # fat (g)
    "205": "CHOCDF",  # carbohydrate (g)
    "307": "NA",      # sodium (mg)
    "291": "FIBTG",   # fibre (g)
    "269": "SUGAR",   # sugars (g)
}
LABELS = {
    "PROCNT": "Protein",
    "FAT": "Fat",
    "CHOCDF": "Carbs",
    "NA": "Sodium",
    "FIBTG": "Fiber",
    "SUGAR": "Sugar",
}
ENERGY_NUMBERS = ("208", "957", "958")  # kcal; different data types use different numbers


@lru_cache(maxsize=256)
def _search_usda(food_name):
    # Returns (matched food description, {nutrient number: value per 100 g, ...})
    api_key = os.getenv("FDC_API_KEY")
    if not api_key:
        raise Exception("FDC_API_KEY not found. Check your .env file.")

    response = requests.get(
        SEARCH_URL,
        headers={"X-Api-Key": api_key},
        params={
            "query": food_name,
            "dataType": "Foundation,SR Legacy",
            "pageSize": 1,
        },
        timeout=15,
    )
    response.raise_for_status()

    foods = response.json().get("foods", [])
    if not foods:
        return None, {}

    best = foods[0]
    values = {}
    for n in best.get("foodNutrients", []):
        values[n.get("nutrientNumber")] = n.get("value", 0)
    return best["description"], values


def get_nutrition_for_food(food_name, grams=100):
    # Returns nutrition for `grams` of the food, in the shape report.py expects.
    description, values = _search_usda(food_name)
    if not values:
        return {}

    scale = grams / 100  # USDA gives values per 100 g

    calories = None
    for number in ENERGY_NUMBERS:
        if number in values:
            calories = round(values[number] * scale, 1)
            break

    nutrients = {}
    for number, code in NUTRIENT_CODES.items():
        nutrients[code] = {
            "label": LABELS[code],
            "quantity": round(values.get(number, 0) * scale, 2),
            "unit": "mg" if code == "NA" else "g",
        }

    return {
        "matched_food": description,
        "grams": grams,
        "nutritional_info": {"calories": calories, "totalNutrients": nutrients},
    }
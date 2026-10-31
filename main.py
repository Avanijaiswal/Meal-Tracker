import sys

from camera.camera import capture_from_camera
from food_api import recognize_food
from nutrition import get_nutrition_for_food
from report import print_report
from database.database import log_meal


def ask_grams(default=100):
    # Ask how much was eaten. A photo cannot tell us the weight.
    text = input(f"How many grams did you eat? (Enter = {default}): ").strip()
    if not text:
        return default
    try:
        grams = float(text)
        if grams <= 0:
            raise ValueError
        return grams
    except ValueError:
        print(f"That is not a valid number. Using {default} g.")
        return default


def main():
    # If you pass an image path (python main.py photo.jpg), use it.
    # Otherwise, open the camera.
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = capture_from_camera()

    if not image_path:
        print("No image captured. Exiting.")
        return

    print(f"Analyzing {image_path}...")

    recognition = recognize_food(image_path)
    dish_name = recognition["dish_name"]
    print(f"Recognized: {dish_name} ({recognition['confidence']}% confident)")

    grams = ask_grams()

    nutrition = get_nutrition_for_food(dish_name, grams)
    if not nutrition:
        print(f"No USDA nutrition data found for '{dish_name}'. Nothing saved.")
        return

    print(f"Matched USDA food: {nutrition['matched_food']} ({grams:g} g)")

    result = print_report(dish_name, nutrition)

    if result:
        nutrients, calories, flags = result
        log_meal(dish_name, nutrients, calories, flags)
        print("\nMeal saved to database.")


if __name__ == "__main__":
    main()
import sys

from camera.camera import capture_from_camera
from food_api import recognize_food, get_nutrition
from report import print_report
from database.database import log_meal


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

    nutrition = get_nutrition(recognition["image_id"])

    result = print_report(dish_name, nutrition)

    if result:
        nutrients, calories, flags = result
        log_meal(dish_name, nutrients, calories, flags)
        print("\nMeal saved to database.")


if __name__ == "__main__":
    main()
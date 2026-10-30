def check_health_flags(nutrients, calories):
    flags = []

    def get_value(key):
        # returns the amount of a nutrient, or 0 if it's missing
        return nutrients.get(key, {}).get("quantity",0)
    sodium = get_value("NA")
    sugar = get_value("SUGAR")
    protein = get_value("PROCNT")
    fiber = get_value("FIBTG")

    if calories is not None and calories >= 700:
        flags.append(f"High Calorie : {int(calories)} kcal")

    if sodium >= 800:
        flags.append(f"High Sodium : {int(sodium)} mg")
    if sugar >= 25:
        flags.append("High sugar : {int(sugars)} g")

    if protein >= 25:
        flags.append(f"Good Protein : {int(protein)} g")
    elif protein <= 10:
        flags.append(f"Low Protein : {int(protein)} g")

    if fiber >= 6:
        flags.append(f"Good fiber : {int(fiber)} g")
    elif fiber <= 2 :
        flags.append(f"Low fiber : {int(fiber)} g")

    if len(flags) == 0:
        return ["Balanced meal!"]
    return flags

def print_report(dish_name, nutrition_data):
    print(f"\n--- FOOD REPORT : {dish_name.upper()} ---")

    info = nutrition_data.get("nutritional_info", {})
    if not info:
        print("No nutritional data found.")
        return None

    calories = info.get("calories")
    if calories:
        print(f"Calories : {calories} kcal")

    print("Nutrients : ")
    nutrients = info.get("totalNutrients", {})
    for key, details in nutrients.items():
        name = details.get("label")
        amount = details.get("quantity",0)
        unit = details.get("unit")
        print(f"   - {name}: {amount :.2f} {unit}")

    flags = check_health_flags(nutrients, calories)
    print("\nHealth Notes: ")
    for flag in flags:
        print(f"   * {flag}")

    return nutrients, calories, flags
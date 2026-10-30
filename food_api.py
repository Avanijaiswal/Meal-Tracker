#




def recognize_food(image_path):
    return{"image_id": "fake-123", "dish_name": "Test Pizza"}

def get_nutrition(image_id):
    return{
        "nutritional_info": {
            "calories": 750,
            "totalNutrients": {
                "PROCNT": {"label": "Protein", "quantity": 8, "unit": "g"},
                "CHOCDF": {"label": "Carbs", "quantity": 80, "unit": "g"},
                "FAT": {"label": "Fat", "quantity": 30, "unit": "g"},
                "NA": {"label": "Sodium", "quantity": 900, "unit": "mg"},
                "FIBTG": {"label": "Fiber", "quantity": 1, "unit": "g"}  
            },
        }
    }
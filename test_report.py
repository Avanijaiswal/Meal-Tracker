from report import print_report

fake_data = {
    "nutritional_info": {
        "calories": 750,
        "totalNutrients": {
            "PROCNT": {"label": "Protein", "quantity": 8, "unit": "g"},
            "NA": {"label": "Sodium", "quantity": 900, "unit": "mg"},
            "FIBTG": {"label": "Fiber", "quantity": 1, "unit": "g"}            
        }
    }
}
print_report("test pizza", fake_data)
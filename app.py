import io

import pandas as pd
import requests
import streamlit as st
from PIL import Image

from food_api import recognize_image
from nutrition import get_nutrition_for_food
from report import check_health_flags

st.set_page_config(page_title="MealTrack", page_icon="🍽️")
st.title("MealTrack")
st.caption("Photo → food recognition → USDA nutrition data")

# Meal log lives in this visitor's session only (nothing is stored on the server)
if "history" not in st.session_state:
    st.session_state.history = []


@st.cache_data(show_spinner="Recognizing food...")
def recognize_cached(image_bytes):
    # Cached so the model does not rerun every time a widget changes
    image = Image.open(io.BytesIO(image_bytes))
    return recognize_image(image)


source = st.radio("Photo source", ["Upload a photo", "Use camera"], horizontal=True)
if source == "Upload a photo":
    file = st.file_uploader("Choose a food photo", type=["jpg", "jpeg", "png"])
else:
    file = st.camera_input("Take a photo of your food")

if file is not None:
    image_bytes = file.getvalue()
    st.image(Image.open(io.BytesIO(image_bytes)), width=350)

    guesses = recognize_cached(image_bytes)

    options = [f"{g['label']} ({g['confidence']}%)" for g in guesses]
    choice = st.selectbox("What the model thinks this is:", options)
    food_name = guesses[options.index(choice)]["label"]

    custom = st.text_input("Wrong? Type the food name yourself (optional):")
    if custom.strip():
        food_name = custom.strip()

    grams = st.number_input(
        "How many grams did you eat?", min_value=10, max_value=2000, value=100, step=10
    )

    try:
        nutrition = get_nutrition_for_food(food_name, grams)
    except requests.RequestException:
        st.error("Could not reach the nutrition database. Please try again in a moment.")
        st.stop()
    except Exception as error:
        st.error(f"Nutrition lookup failed: {error}")
        st.stop()

    if not nutrition:
        st.warning(f"No USDA nutrition data found for '{food_name}'. Try typing a simpler name.")
        st.stop()

    info = nutrition["nutritional_info"]
    nutrients = info["totalNutrients"]
    calories = info["calories"]

    st.subheader(f"{food_name} - {grams:g} g")
    st.caption(f"Based on USDA entry: {nutrition['matched_food']}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Calories", f"{calories:g} kcal")
    col2.metric("Protein", f"{nutrients['PROCNT']['quantity']:g} g")
    col3.metric("Carbs", f"{nutrients['CHOCDF']['quantity']:g} g")
    col4.metric("Fat", f"{nutrients['FAT']['quantity']:g} g")
    st.write(
        f"Sodium: {nutrients['NA']['quantity']:g} mg | "
        f"Fiber: {nutrients['FIBTG']['quantity']:g} g | "
        f"Sugar: {nutrients['SUGAR']['quantity']:g} g"
    )

    st.markdown("**Health notes**")
    flags = check_health_flags(nutrients, calories)
    for flag in flags:
        st.write(f"- {flag}")

    if st.button("Add to my log"):
        st.session_state.history.append(
            {
                "Food": food_name,
                "Grams": grams,
                "Calories": calories,
                "Protein (g)": nutrients["PROCNT"]["quantity"],
                "Carbs (g)": nutrients["CHOCDF"]["quantity"],
                "Fat (g)": nutrients["FAT"]["quantity"],
                "Sodium (mg)": nutrients["NA"]["quantity"],
            }
        )
        st.success("Added!")

st.divider()
st.subheader("My meal log (this session)")
if st.session_state.history:
    table = pd.DataFrame(st.session_state.history)
    st.dataframe(table)
    st.download_button(
        "Download as CSV", table.to_csv(index=False), "meals.csv", "text/csv"
    )
else:
    st.write("Nothing logged yet.")

st.caption(
    "Food recognition: nateraw/food (Apache-2.0). "
    "Nutrition data: U.S. Department of Agriculture, FoodData Central. "
    "Estimates only, not medical advice."
)
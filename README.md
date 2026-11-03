# MealTrack

Upload or photograph a meal, and MealTrack identifies the food, looks up nutrition
data, and gives health notes for the portion you ate.

**Live demo:** https://meal-tracker-525.streamlit.app/

## How it works

1. **Image input:** the browser sends a photo (Pillow decodes and prepares it).
2. **Recognition:** a Vision Transformer fine-tuned on Food-101 (`nateraw/food`),
   run with PyTorch and Hugging Face Transformers on CPU, returns the top 3 guesses.
3. **Confirmation:** the user can pick another guess or type the food name.
4. **Nutrition:** USDA FoodData Central is searched and values are scaled to the
   portion size the user enters (USDA data is per 100 g).
5. **Report:** calories, macros and simple health notes, plus a session meal log
   with CSV download.

## Limitations

- Recognizes only the 101 dishes in Food-101 (mostly Western food, few Indian dishes).
- A photo cannot reveal portion size, so the user enters grams.
- The USDA match is a text search and can pick a restaurant or branded item rather
  than a generic one. The matched entry is always shown.
- Nutrition values are estimates, not medical advice.
- The meal log lives only in the visitor's browser session. Nothing is stored on the server.

## Run locally

    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    streamlit run app.py

Create a `.env` file containing `FDC_API_KEY=your_key`. A free key is available at
https://fdc.nal.usda.gov/api-key-signup. Never commit this file.

The command-line version (`main.py`) also uses the webcam through OpenCV (`pip install opencv-python`).

## Credits

- Food recognition model: [nateraw/food](https://huggingface.co/nateraw/food), Apache-2.0.
- Nutrition data: U.S. Department of Agriculture, FoodData Central.
import os

# Hide the harmless Windows symlink warning (must be set before importing transformers)
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification

# Food recognition model: nateraw/food (Apache-2.0)
MODEL_NAME = "nateraw/food"

_processor = None
_model = None


def _load_model():
    # Load the model the first time it is needed, then reuse it
    global _processor, _model
    if _model is None:
        _processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
        _model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)
        _model.eval()
    return _processor, _model


def recognize_image(image, top_k=3):
    # image: a PIL image. Returns the top_k guesses with confidence %.
    processor, model = _load_model()

    inputs = processor(images=image.convert("RGB"), return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = torch.softmax(outputs.logits, dim=-1)[0]
    top = torch.topk(probabilities, top_k)

    results = []
    for score, index in zip(top.values, top.indices):
        label = model.config.id2label[index.item()]
        results.append(
            {
                "label": label.replace("_", " ").title(),
                "confidence": round(score.item() * 100, 1),
            }
        )
    return results


def recognize_food(image_path):
    # Same name and output shape as the old LogMeal function
    image = Image.open(image_path)
    guesses = recognize_image(image)
    return {
        "image_id": "local",
        "dish_name": guesses[0]["label"],
        "confidence": guesses[0]["confidence"],
        "top3": guesses,
    }



import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification

MODEL_NAME = "nateraw/food"

print("Loading model (the first run downloads about 344 MB)...")
processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)
model.eval()  # tells the model we are predicting, not training

# Open the photo and make sure it has 3 colour channels (RGB)
image = Image.open("captured_food.jpg").convert("RGB")

# The processor resizes to 224x224 and normalizes the pixels,
# then returns them as PyTorch tensors
inputs = processor(images=image, return_tensors="pt")

# no_grad: we are not training, so skip the extra bookkeeping
with torch.no_grad():
    outputs = model(**inputs)

# Turn raw scores into percentages that add up to 100
probabilities = torch.softmax(outputs.logits, dim=-1)[0]

# Take the 3 highest and print their names
top3 = torch.topk(probabilities, 3)
for score, index in zip(top3.values, top3.indices):
    label = model.config.id2label[index.item()]
    print(f"{label}: {score.item() * 100:.1f}%")
import json
import requests
from io import BytesIO
from PIL import Image

# Load URLs
with open("urls.json", "r", encoding="utf-8") as f:
    urls = json.load(f)

images = []

for i, url in enumerate(urls, start=1):
    print(f"Downloading page {i}/{len(urls)}")

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    img = Image.open(BytesIO(response.content))

    if img.mode != "RGB":
        img = img.convert("RGB")

    images.append(img)

print("Creating PDF...")

images[0].save(
    "answer_sheet.pdf",
    save_all=True,
    append_images=images[1:]
)

print("Done! Saved as answer_sheet.pdf")
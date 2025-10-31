import os
import random
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# --------------------------
# 1️⃣  QUOTES LIST
# --------------------------
quotes = [
    "You have the right to work, but never to the fruit of work. – Bhagavad Gita 2.47",
    "The soul is neither born, nor does it die. – Bhagavad Gita 2.20",
    "Change is the law of the universe. – Bhagavad Gita 2.14",
    "Man is made by his belief. As he believes, so he is. – Bhagavad Gita 17.3",
    "Set your heart upon your work, but never on its reward. – Bhagavad Gita 2.47",
]

# Pick random quote
quote = random.choice(quotes)
print(f"Selected quote:\n{quote}")

# Create unique file name based on date
today = datetime.now().strftime("%Y-%m-%d")
filename = f"post_{today}.jpg"

# --------------------------
# 2️⃣  GENERATE IMAGE
# --------------------------
img = Image.new("RGB", (1080, 1080), color=(255, 250, 240))
draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype("DejaVuSans.ttf", 40)
except:
    font = ImageFont.load_default()

def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines, current = [], ""
    for w in words:
        test = current + w + " "
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            lines.append(current)
            current = w + " "
    lines.append(current)
    return lines

lines = wrap_text(quote, font, 900)
total_height = sum(draw.textbbox((0, 0), l, font=font)[3] - draw.textbbox((0, 0), l, font=font)[1] for l in lines)
y = (1080 - total_height) / 2

for line in lines:
    bbox = draw.textbbox((0, 0), line, font=font)
    w = bbox[2] - bbox[0]
    draw.text(((1080 - w) / 2, y), line, fill="black", font=font)
    y += bbox[3] - bbox[1] + 10

# Save image with date
img.save(filename)
print(f"✅ Image generated successfully: {filename}")

# --------------------------
# 3️⃣  BUILD RAW GITHUB URL
# --------------------------
GITHUB_USER = "tawadeR"
REPO_NAME = "bhagavad-gita-daily-poster"
BRANCH = "main"

image_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/{filename}"
print(f"Using image URL: {image_url}")

# --------------------------
# 4️⃣  POST TO INSTAGRAM
# --------------------------
ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN")
IG_USER_ID = os.getenv("IG_USER_ID")

if not ACCESS_TOKEN or not IG_USER_ID:
    raise ValueError("❌ Missing environment variables: IG_ACCESS_TOKEN or IG_USER_ID.")

upload_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
payload = {"image_url": image_url, "caption": quote, "access_token": ACCESS_TOKEN}

upload_response = requests.post(upload_url, data=payload)
upload_result = upload_response.json()
print("Upload response:", upload_result)

if "id" not in upload_result:
    raise Exception(f"❌ Failed to upload image: {upload_result}")

creation_id = upload_result["id"]

publish_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
publish_response = requests.post(publish_url, data={"creation_id": creation_id, "access_token": ACCESS_TOKEN})
publish_result = publish_response.json()
print("Publish response:", publish_result)

if "id" in publish_result:
    print("🎉 Successfully posted to Instagram!")
else:
    print("⚠️ Post failed:", publish_result)

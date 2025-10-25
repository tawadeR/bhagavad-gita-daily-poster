import os
import random
import requests
from PIL import Image, ImageDraw, ImageFont

# Quotes list
quotes = [
    "You have the right to work, but never to the fruit of work. – Bhagavad Gita 2.47",
    "The soul is neither born, and nor does it die. – Bhagavad Gita 2.20",
    "Change is the law of the universe. – Bhagavad Gita 2.14",
    "Man is made by his belief. As he believes, so he is. – Bhagavad Gita 17.3",
]

# Pick random quote
quote = random.choice(quotes)

# Create image
img = Image.new('RGB', (1080, 1080), color=(255, 250, 240))
draw = ImageDraw.Draw(img)

# Add text
font = ImageFont.load_default()
text_w, text_h = draw.textsize(quote, font=font)
draw.text(((1080-text_w)/2, (1080-text_h)/2), quote, fill="black", font=font)

# Save image
img.save("post.jpg")

# Instagram API
ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN")
IG_USER_ID = os.getenv("IG_USER_ID")

# Upload image
url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
payload = {
    'image_url': 'https://raw.githubusercontent.com/yourusername/bhagavad-gita-daily-poster/main/post.jpg',  # later we replace this with hosted image
    'caption': quote,
    'access_token': ACCESS_TOKEN
}
r = requests.post(url, data=payload)
print(r.text)

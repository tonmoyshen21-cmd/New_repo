import requests
from openai import OpenAI
import os
from dotenv import load_dotenv
# Load env variables
load_dotenv()
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
FB_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME =os.getenv("CHANNEL_USERNAME")  
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


Base_URL = "https://openrouter.ai/api/v1"
client = OpenAI(
  base_url= Base_URL,
  api_key = OPENAI_API_KEY
) 
def generate_post():
    prompt = """তুমি একজন “Quote Collector”। তোমার কাজ হলো বিখ্যাত ব্যক্তিদের প্রেরণাদায়ক, জীবনের শিক্ষা, সাফল্য বা ইতিবাচক চিন্তার উপর ভিত্তি করে বলা উক্তি সংগ্রহ করা।

শর্তগুলো:

প্রতিবার 1 টি উক্তি দেবে।

প্রতিটি উক্তির শেষে উক্তিটি কার বলা তা উল্লেখ করতে হবে।

উক্তি হবে সংক্ষিপ্ত, প্রভাবশালী এবং সহজে মনে রাখার মতো।

বাংলা উক্তি দেবে।

কোনো উক্তি বানানো যাবে না, অবশ্যই বাস্তব বিখ্যাত ব্যক্তিদের উক্তি হতে হবে।

শেষে ৩–৫টি হ্যাশট্যাগ দেবে (যেমন #Motivation #hyeyou)।
"""
    completion = client.chat.completions.create(
    extra_headers={
        "HTTP-Referer": "<YOUR_SITE_URL>",
        "X-Title": "<YOUR_SITE_NAME>",
    },
    extra_body={},
    model="openai/gpt-oss-20b:free",
    messages=[
        {
        "role": "user",
        "content": prompt
        }
    ]
    )
    message = completion.choices[0].message.content
    return message

def post_to_facebook(message):
    url = f"https://graph.facebook.com/{FB_PAGE_ID}/feed"
    payload = {"message": message, "access_token": FB_ACCESS_TOKEN}
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    try:
        print("🚀 Generating new SQA post...")
        message = generate_post()
        print("✅ Post generated successfully!")
        result = post_to_facebook(message)
        print(f"✅ Post published! Post ID: {result.get('id')}")

    except Exception as e:
        print(f"❌ Error: {e}")
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHANNEL_USERNAME,
            "text": message
        }
        response = requests.post(url, data=payload)

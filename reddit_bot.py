# v7
import requests
import asyncio
import schedule
import time
import os
from telegram import Bot

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

SUBREDDITS = ["EngineeringPorn"]
POST_LIMIT = 3

bot = Bot(token=TELEGRAM_TOKEN)

def get_reddit_posts(subreddit):
    url = f"https://www.reddit.com/r/{subreddit}/top.json?t=day&limit={POST_LIMIT}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Cookie": "over18=1"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Hata: {subreddit} için {response.status_code}")
        return []
    return response.json()["data"]["children"]

def get_image_url(post):
    data = post["data"]
    if "preview" in data and data["preview"]["images"]:
        return data["preview"]["images"][0]["source"]["url"].replace("&amp;", "&")
    return None

async def send_posts():
    for subreddit in SUBREDDITS:
        posts = get_reddit_posts(subreddit)
        for post in posts:
            data = post["data"]
            title = data["title"]
            url = f"https://reddit.com{data['permalink']}"
            caption = f"🔥 {title}\n\n🔗 {url}"
            image_url = get_image_url(post)
            try:
                if image_url:
                    await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=image_url, caption=caption)
                else:
                    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=caption)
            except Exception as e:
                print(f"Hata: {e}")
                await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=caption)
            await asyncio.sleep(3)
    print("Gönderiler tamamlandı!")

def run_bot():
    asyncio.run(send_posts())

schedule.every().monday.at("08:30").do(run_bot)
schedule.every().monday.at("17:00").do(run_bot)
schedule.every().tuesday.at("08:30").do(run_bot)
schedule.every().tuesday.at("17:00").do(run_bot)
schedule.every().wednesday.at("08:30").do(run_bot)
schedule.every().wednesday.at("17:00").do(run_bot)
schedule.every().thursday.at("08:30").do(run_bot)
schedule.every().thursday.at("17:00").do(run_bot)
schedule.every().friday.at("08:30").do(run_bot)
schedule.every().friday.at("17:00").do(run_bot)

print("Bot başladı! Hafta içi 08:30 ve 17:00'da çalışacak.")

while True:
    schedule.run_pending()
    time.sleep(60)

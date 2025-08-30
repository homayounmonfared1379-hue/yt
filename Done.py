import requests
import feedparser
import time
import random
import os

# === SETTINGS ===
BOT_TOKEN = "7971301998:AAG4T-wUt869q46AS6mLIfe0kw3sPAtxHIo"
CHAT_ID = "@sensotestbot0"
YOUTUBE_FEED_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCqutrz21jV8FStzLmqyvnHg"

EMOJIS = ["🔥", "📽", "🔴"]
LAST_VIDEO_FILE = "last_video.txt"  # فایل برای ذخیره آخرین ویدیو

# === HELPER FUNCTIONS ===
def random_emoji(n=1):
    return "".join(random.choices(EMOJIS, k=n))

def read_last_video_id():
    if os.path.exists(LAST_VIDEO_FILE):
        with open(LAST_VIDEO_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

def save_last_video_id(video_id):
    with open(LAST_VIDEO_FILE, "w", encoding="utf-8") as f:
        f.write(video_id)

# === SEND VIDEO ===
def send_video_message(title, video_link, thumbnail_url):
    emoji_title = random_emoji(1)
    emoji_button = random_emoji(1)
    caption_text = f"{emoji_title} {title} {emoji_title}"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    payload = {
        "chat_id": CHAT_ID,
        "photo": thumbnail_url,
        "caption": caption_text,
        "parse_mode": "HTML",
        "reply_markup": {
            "inline_keyboard": [[
                {"text": f"{emoji_button} ویدیو رو ببین {emoji_button}", "url": video_link}
            ]]
        }
    }
    r = requests.post(url, json=payload)
    if r.status_code == 200:
        print("✅ ارسال شد:", title)
    else:
        print("❌ ارسال نشد:", r.text)

# === CHECK FEED ===
def check_youtube_feed():
    last_video_id = read_last_video_id()

    feed = feedparser.parse(YOUTUBE_FEED_URL)
    if feed.bozo:
        print("❌ خطا در خواندن فید:", feed.bozo_exception)
        return

    if not feed.entries:
        print("هیچ ویدیویی پیدا نشد.")
        return

    newest_entry = feed.entries[0]  # فقط آخرین ویدیو
    video_id = newest_entry.yt_videoid
    video_title = newest_entry.title
    video_link = newest_entry.link
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

    if video_id != last_video_id:
        send_video_message(video_title, video_link, thumbnail_url)
        save_last_video_id(video_id)  # ذخیره روی فایل
    else:
        print("ویدیوی جدیدی پیدا نشد.")

# === MAIN LOOP ===
def main():
    while True:
        try:
            check_youtube_feed()
        except Exception as e:
            print("خطا:", e)
        time.sleep(300)  # هر 5 دقیقه بررسی می‌کنه

if __name__ == "__main__":
    main()

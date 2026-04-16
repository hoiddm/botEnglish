import asyncio
import os
from datetime import datetime, time, timedelta
from telegram import Bot
from flask import Flask
import threading

# ===== ENV =====
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TOKEN or not CHAT_ID:
    raise ValueError("Missing TELEGRAM_TOKEN or CHAT_ID")

# ===== LOAD WORDS =====
with open("words.txt", "r", encoding="utf-8") as f:
    words = f.read().splitlines()

bot = Bot(token=TOKEN)

# ===== TIME CONFIG (VN TIME) =====
START_TIME = time(9, 0)
END_TIME = time(18, 0)

def get_vn_time():
    return datetime.utcnow() + timedelta(hours=7)

# ===== BOT LOOP =====
async def send_flashcard():
    index = 0
    print("Bot started...")

    while True:
        try:
            now = get_vn_time()
            current_time = now.time()

            print("Current VN time:", current_time)

            if START_TIME <= current_time <= END_TIME:
                word = words[index]
                parts = word.split("|")

                if len(parts) < 3:
                    print("Sai format:", word)
                    index = (index + 1) % len(words)
                    continue

                vocab, ipa, meaning = [p.strip() for p in parts]

                print(f"Sending: {vocab}")

                await bot.send_message(
                    chat_id=CHAT_ID,
                    text=f"{vocab} | {ipa}"
                )

                await asyncio.sleep(5)

                await bot.send_message(
                    chat_id=CHAT_ID,
                    text=f"→ {meaning}"
                )

                # đảm bảo đúng chu kỳ 15 phút
                await asyncio.sleep(895)

                index = (index + 1) % len(words)

            else:
                print("Ngoài giờ, ngủ...")
                await asyncio.sleep(60)

        except Exception as e:
            print("ERROR:", e)
            await asyncio.sleep(30)

# ===== KEEP ALIVE (CHO RAILWAY) =====
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run_web():
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# ===== MAIN =====
if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    asyncio.run(send_flashcard())

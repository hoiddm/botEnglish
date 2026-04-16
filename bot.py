import asyncio
import os
from datetime import datetime, time
from telegram import Bot

TOKEN = "8641487834:AAGG79GrPhd2ctEMPzu8yeg-zU2NMM2g5u8"
CHAT_ID = "7197704150"

with open("words.txt", "r", encoding="utf-8") as f:
    words = f.read().splitlines()

bot = Bot(token=TOKEN)

START_TIME = time(9, 0)
END_TIME = time(18, 0)

async def send_flashcard():
    index = 0

    while True:
        now = datetime.now().time()

        if START_TIME <= now <= END_TIME:
            word = words[index]
            parts = word.split("|")

            if len(parts) < 3:
                print(f"⚠️ Sai format: {word}")
                index = (index + 1) % len(words)
                continue

            vocab, ipa, meaning = [p.strip() for p in parts]

            try:
                await bot.send_message(chat_id=CHAT_ID, text=f"{vocab} | {ipa}")
                await asyncio.sleep(5)
                await bot.send_message(chat_id=CHAT_ID, text=f"→ {meaning}")
            except Exception as e:
                print("Lỗi gửi:", e)
                await asyncio.sleep(30)
                continue

            await asyncio.sleep(895)
            index = (index + 1) % len(words)

        else:
            await asyncio.sleep(60)

asyncio.run(send_flashcard())

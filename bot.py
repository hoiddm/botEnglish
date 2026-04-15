import random
import asyncio
import os
from telegram import Bot

# 👉 lấy từ Railway ENV
TOKEN = "8641487834:AAGG79GrPhd2ctEMPzu8yeg-zU2NMM2g5u8"
CHAT_ID = "7197704150"

# đọc file từ vựng
with open("words.txt", "r", encoding="utf-8") as f:
    words = f.read().splitlines()

random.shuffle(words)

bot = Bot(token=TOKEN)

async def send_flashcard():
    index = 0
    while True:
        word = words[index]
        parts = word.split("|")

        vocab = parts[0].strip()
        ipa = parts[1].strip()
        meaning = parts[2].strip()

        # gửi full 1 lần
        message = f"{vocab} | {ipa}\n→ {meaning}"
        await bot.send_message(chat_id=CHAT_ID, text=message)

        # ⏱️ 5 phút = 300 giây
        await asyncio.sleep(300)

        index = (index + 1) % len(words)

asyncio.run(send_flashcard())

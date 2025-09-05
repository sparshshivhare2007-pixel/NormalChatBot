import random
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from pyrogram.types import Message

from config import MONGO_URL
from NoxxNetwork import NoxxBot

@NoxxBot.on_message(
    (filters.text | filters.sticker) & ~filters.private & ~filters.bot,
    group=4
)
async def chatbot_universal(client: Client, message: Message):
    try:
        # Ignore commands
        if message.text and (
            message.text.startswith(("!", "/", "?", "@", "#"))
        ):
            return
    except Exception:
        pass

    chatdb = MongoClient(MONGO_URL)
    chatai = chatdb["Word"]["WordDb"]

    search_word = None
    if message.text:
        search_word = message.text
    elif message.sticker:
        search_word = message.sticker.file_unique_id

    await client.send_chat_action(message.chat.id, ChatAction.TYPING)

    responses = []
    if search_word:
        responses = list(chatai.find({"word": search_word}))

    if responses:
        # Exact match se reply
        reply_data = random.choice(responses)
    else:
        # Agar exact match nahi mila to pure DB se random
        all_responses = list(chatai.find())
        if not all_responses:
            return  # agar DB bilkul hi empty hai
        reply_data = random.choice(all_responses)

    try:
        if reply_data.get("check") == "sticker":
            await message.reply_sticker(reply_data["text"])
        else:
            await message.reply_text(reply_data["text"])
    except Exception:
        await message.reply_text(reply_data["text"])


@NoxxBot.on_message(
    filters.private & (filters.text | filters.sticker) & ~filters.bot,
    group=5
)
async def chatbot_private(client: Client, message: Message):
    try:
        if message.text and (
            message.text.startswith(("!", "/", "?", "@", "#"))
        ):
            return
    except Exception:
        pass

    chatdb = MongoClient(MONGO_URL)
    chatai = chatdb["Word"]["WordDb"]

    search_word = None
    if message.text:
        search_word = message.text
    elif message.sticker:
        search_word = message.sticker.file_unique_id

    await client.send_chat_action(message.chat.id, ChatAction.TYPING)

    responses = []
    if search_word:
        responses = list(chatai.find({"word": search_word}))

    if responses:
        reply_data = random.choice(responses)
    else:
        all_responses = list(chatai.find())
        if not all_responses:
            return
        reply_data = random.choice(all_responses)

    try:
        if reply_data.get("check") == "sticker":
            await message.reply_sticker(reply_data["text"])
        else:
            await message.reply_text(reply_data["text"])
    except Exception:
        await message.reply_text(reply_data["text"])

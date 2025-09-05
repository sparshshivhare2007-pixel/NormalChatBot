import random
from Abg.chat_status import adminsOnly

from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from pyrogram.types import InlineKeyboardMarkup, Message

from config import MONGO_URL
from NoxxNetwork import NoxxNetwork
from NoxxNetwork.modules.helpers import CHATBOT_ON, is_admins


@NoxxNetwork.on_cmd("chatbot", group_only=True)
@adminsOnly("can_delete_messages")
async def chaton_(_, m: Message):
    await m.reply_text(
        f"ᴄʜᴀᴛ: {m.chat.title}\n**ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴩᴛɪᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ ᴄʜᴀᴛʙᴏᴛ.**",
        reply_markup=InlineKeyboardMarkup(CHATBOT_ON),
    )
    return


# Global variable to store previous message for each chat
chat_previous_messages = {}


@NoxxNetwork.on_message(
    (filters.text | filters.sticker | filters.group) & ~filters.private & ~filters.bot, group=4
)
async def chatbot_universal(client: Client, message: Message):
    global chat_previous_messages
    
    try:
        # Skip commands
        if message.text and (
            message.text.startswith("!")
            or message.text.startswith("/")
            or message.text.startswith("?")
            or message.text.startswith("@")
            or message.text.startswith("#")
        ):
            return
    except Exception:
        pass

    chatdb = MongoClient(MONGO_URL)
    chatai = chatdb["Word"]["WordDb"]
    
    # Check if chatbot is enabled
    vickdb = MongoClient(MONGO_URL)
    vick = vickdb["VickDb"]["Vick"]
    is_vick = vick.find_one({"chat_id": message.chat.id})
    
    chat_id = message.chat.id
    
    # LEARNING PHASE - Save word-reply pairs
    if message.reply_to_message:
        # Reply to a message - save word-reply pair
        word = None
        reply_text = None
        reply_check = "none"
        
        # Get the word (what was replied to)
        if message.reply_to_message.text:
            word = message.reply_to_message.text
        elif message.reply_to_message.sticker:
            word = message.reply_to_message.sticker.file_unique_id
            
        # Get the reply
        if message.text:
            reply_text = message.text
            reply_check = "none"
        elif message.sticker:
            reply_text = message.sticker.file_id
            reply_check = "sticker"
            
        # Save to database
        if word and reply_text:
            try:
                existing = chatai.find_one({"word": word, "text": reply_text})
                if not existing:
                    chatai.insert_one({
                        "word": word,
                        "text": reply_text,
                        "check": reply_check
                    })
            except Exception as e:
                print(f"Database error: {e}")
                
    else:
        # Direct message - check if previous message exists and save pair
        if chat_id in chat_previous_messages:
            prev_msg = chat_previous_messages[chat_id]
            
            word = None
            reply_text = None
            reply_check = "none"
            
            # Get previous word
            if prev_msg.get("type") == "text":
                word = prev_msg.get("content")
            elif prev_msg.get("type") == "sticker":
                word = prev_msg.get("content")
                
            # Get current reply
            if message.text:
                reply_text = message.text
                reply_check = "none"
            elif message.sticker:
                reply_text = message.sticker.file_id
                reply_check = "sticker"
                
            # Save word-reply pair
            if word and reply_text:
                try:
                    existing = chatai.find_one({"word": word, "text": reply_text})
                    if not existing:
                        chatai.insert_one({
                            "word": word,
                            "text": reply_text,
                            "check": reply_check
                        })
                except Exception as e:
                    print(f"Database error: {e}")
    
    # Store current message as previous for next iteration
    if message.text:
        chat_previous_messages[chat_id] = {
            "type": "text",
            "content": message.text,
            "user_id": message.from_user.id
        }
    elif message.sticker:
        chat_previous_messages[chat_id] = {
            "type": "sticker", 
            "content": message.sticker.file_unique_id,
            "user_id": message.from_user.id
        }
    
    # RESPONSE PHASE - Only if chatbot is enabled
    if not is_vick:
        should_respond = False
        search_word = None
        
        if message.reply_to_message and message.reply_to_message.from_user.id == client.id:
            # Reply to bot
            should_respond = True
            if message.text:
                search_word = message.text
            elif message.sticker:
                search_word = message.sticker.file_unique_id
                
        elif not message.reply_to_message:
            # Direct message - respond randomly or if bot mentioned
            if message.text:
                if f"@{client.me.username}" in message.text.lower() or "bot" in message.text.lower():
                    should_respond = True
                    search_word = message.text.replace(f"@{client.me.username}", "").strip()
                else:
                    # Random response (10% chance)
                    if random.randint(1, 10) == 1:
                        should_respond = True
                        search_word = message.text
            elif message.sticker:
                # Random response to stickers (5% chance)
                if random.randint(1, 20) == 1:
                    should_respond = True
                    search_word = message.sticker.file_unique_id
        
        if should_respond and search_word:
            await client.send_chat_action(message.chat.id, ChatAction.TYPING)
            
            # Find responses
            responses = []
            matches = list(chatai.find({"word": search_word}))
            
            for match in matches:
                responses.append(match["text"])
            
            if responses:
                reply = random.choice(responses)
                # Find the check type for this reply
                reply_data = chatai.find_one({"word": search_word, "text": reply})
                
                try:
                    if reply_data and reply_data.get("check") == "sticker":
                        await message.reply_sticker(reply)
                    else:
                        await message.reply_text(reply)
                except Exception:
                    # Fallback to text if sticker fails
                    try:
                        await message.reply_text(reply)
                    except:
                        pass


@NoxxNetwork.on_message(
    filters.private & (filters.text | filters.sticker) & ~filters.bot, group=5
)
async def chatbot_private(client: Client, message: Message):
    """Handle private messages - always respond"""
    try:
        if message.text and (
            message.text.startswith("!")
            or message.text.startswith("/")
            or message.text.startswith("?")
            or message.text.startswith("@")
            or message.text.startswith("#")
        ):
            return
    except Exception:
        pass

    chatdb = MongoClient(MONGO_URL)
    chatai = chatdb["Word"]["WordDb"]
    
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    
    search_word = None
    if message.text:
        search_word = message.text
    elif message.sticker:
        search_word = message.sticker.file_unique_id
    
    if search_word:
        responses = list(chatai.find({"word": search_word}))
        
        if responses:
            chosen = random.choice(responses)
            try:
                if chosen.get("check") == "sticker":
                    await message.reply_sticker(chosen["text"])
                else:
                    await message.reply_text(chosen["text"])
            except Exception:
                await message.reply_text(chosen["text"])
        else:
            # Default responses
            default_responses = [
                "मुझे समझ नहीं आया 🤔",
                "क्या कह रहे हो? 😅", 
                "और बताओ",
                "हम्म... 🤨",
                "अच्छा! 😊"
            ]
            await message.reply_text(random.choice(default_responses))


@NoxxNetwork.on_cmd("chatstats")
async def chatbot_stats(_, message: Message):
    """Show total learned words"""
    try:
        chatdb = MongoClient(MONGO_URL)
        chatai = chatdb["Word"]["WordDb"]
        
        total_words = chatai.count_documents({})
        text_replies = chatai.count_documents({"check": "none"})
        sticker_replies = chatai.count_documents({"check": "sticker"})
        
        stats_text = f"""
📊 **Universal Chatbot Stats**

🧠 Total Learned Words: `{total_words}`
💬 Text Responses: `{text_replies}`
🎭 Sticker Responses: `{sticker_replies}`

✨ **Learning:** Active everywhere
🌍 **Scope:** Universal (all chats)
        """
        
        await message.reply_text(stats_text)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")


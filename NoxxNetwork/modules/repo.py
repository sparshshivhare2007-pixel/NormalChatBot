import asyncio
import random
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import IMG
from NoxxNetwork import NoxxBot


start_txt = """**
✪ 𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐍𝐘 𝐂𝐫𝐞𝐚𝐭𝐢𝐨𝐧'𝐬 ✪

➲ ᴇᴀsʏ ᴅᴇᴘʟᴏʏᴍᴇɴᴛ ✰  
➲ ɴᴏ ʙᴀɴ ɪssᴜᴇs ✰  
➲ ᴜɴʟɪᴍɪᴛᴇᴅ ᴅʏɴᴏs ✰  
➲ 𝟸𝟺/𝟽 ʟᴀɢ-ғʀᴇᴇ ✰

► sᴇɴᴅ ᴀ sᴄʀᴇᴇɴsʜᴏᴛ ɪғ ʏᴏᴜ ғᴀᴄᴇ ᴀɴʏ ᴘʀᴏʙʟᴇᴍs!
**"""




@NoxxBot.on_cmd("repo")
async def repo(_, m: Message):
    buttons = [
        [ 
          InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ", url=f"https://t.me/{NoxxBot.username}?startgroup=true")
        ],
        [
          InlineKeyboardButton("Nᴀɴᴅ", url="https://t.me/TMZEROO"),
          InlineKeyboardButton("Cʜᴀᴛᴢᴏɴᴇ", url="https://t.me/NYCreation_Chatzone"),
          ],
               [
                InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/TMZEROO"),

],
[
              InlineKeyboardButton("ᴍᴜsɪᴄ", url=f"https://t.me/Music4vcbot"),
              InlineKeyboardButton("Chatabot", url=f"https://t.me/Mahiraxrobot")
              ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await m.reply_photo(
        photo=random.choice(IMG),
        caption=start_txt,
        reply_markup=reply_markup
    )

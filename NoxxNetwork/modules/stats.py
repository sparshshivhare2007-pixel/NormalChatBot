from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from NoxxNetwork import OWNER, NoxxBot
from NoxxNetwork.database.chats import get_served_chats
from NoxxNetwork.database.users import get_served_users


@NoxxBot.on_message(filters.command("stats") & filters.user(OWNER))
async def stats_cmd(cli: Client, message: Message):
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("📊 Show Stats", callback_data="show_stats")]]
    )
    await message.reply_text(
        "ʜᴇʏ ᴍᴀsᴛᴇʀ ✨\nᴛᴀᴘ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ᴠɪᴇᴡ ʟɪᴠᴇ sᴛᴀᴛs 📊",
        reply_markup=keyboard,
    )


@NoxxBot.on_callback_query(filters.regex("show_stats"))
async def show_stats(cli: Client, query: CallbackQuery):
    users = len(await get_served_users())
    chats = len(await get_served_chats())
    bot = await cli.get_me()

    text = f"""📊 ʙᴏᴛ sᴛᴀᴛs ᴏғ {NoxxBot.username}

➻ ᴄʜᴀᴛs : {chats}
➻ ᴜsᴇʀs : {users}"""

    await query.answer(text, show_alert=True)

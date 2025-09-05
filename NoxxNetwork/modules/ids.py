from pyrogram import filters
from pyrogram.enums import ParseMode
from NoxxNetwork import NoxxBot


@NoxxBot.on_cmd("id")
async def getid(client, message):
    chat = message.chat
    your_id = message.from_user.id
    message_id = message.id
    reply = message.reply_to_message

    text = "✨ <b><u>ID ɪɴғᴏʀᴍᴀᴛɪᴏɴ</u></b> ✨\n\n"
    text += f"📩 <b>Message ID:</b> <code>{message_id}</code>\n"
    text += f"🙋 <b>Your ID:</b> <code>{your_id}</code>\n"

    if not message.command:
        message.command = message.text.split()

    if len(message.command) == 2:
        try:
            split = message.text.split(None, 1)[1].strip()
            user_id = (await client.get_users(split)).id
            text += f"👤 <b>User ID:</b> <code>{user_id}</code>\n"
        except Exception:
            return await message.reply_text("❌ This user doesn’t exist.", quote=True)

    text += f"💬 <b>Chat ID:</b> <code>{chat.id}</code>\n\n"

    if (
        not getattr(reply, "empty", True)
        and not message.forward_from_chat
        and not reply.sender_chat
    ):
        text += "🔁 <b>Reply Info:</b>\n"
        text += f"   ┗ 📩 <b>Replied Msg ID:</b> <code>{reply.id}</code>\n"
        text += f"   ┗ 👤 <b>Replied User ID:</b> <code>{reply.from_user.id}</code>\n\n"

    if reply and reply.forward_from_chat:
        text += f"📢 Forwarded Channel: <b>{reply.forward_from_chat.title}</b>\n"
        text += f"🆔 Channel ID: <code>{reply.forward_from_chat.id}</code>\n\n"

    if reply and reply.sender_chat:
        text += f"🏷️ Replied Chat/Channel ID: <code>{reply.sender_chat.id}</code>"

    await message.reply_text(
        text,
        disable_web_page_preview=True,
        parse_mode=ParseMode.HTML,
    )

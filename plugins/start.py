from TechVJ.bot import TechVJBot
from pyrogram import filters
from urllib.parse import quote_plus
from info import URL, LOG_CHANNEL, SHORTLINK
from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size
from TechVJ.util.human_readable import humanbytes
from utils import get_shortlink

@TechVJBot.on_message(filters.private & (filters.video | filters.document))
async def stream_start(client, message):

    file = message.video or message.document
    if not file:
        return

    status = await message.reply_text("⏳ Processing your file...")

    log_msg = await client.send_cached_media(
        chat_id=LOG_CHANNEL,
        file_id=file.file_id
    )

    file_name = get_name(log_msg)
    size = humanbytes(get_media_file_size(message))

    secure_hash = get_hash(log_msg)
    msg_id = log_msg.id

    if not SHORTLINK:
        stream = f"{URL}watch/{secure_hash}{msg_id}"
        download = f"{URL}{secure_hash}{msg_id}"
    else:
        stream = await get_shortlink(f"{URL}watch/{secure_hash}{msg_id}")
        download = await get_shortlink(f"{URL}{secure_hash}{msg_id}")

    buttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("🖥 Watch Online", url=stream),
            InlineKeyboardButton("📥 Download", url=download)
        ]]
    )

    text = (
        f"<b>✅ Your Link Generated!</b>\n\n"
        f"<b>📂 File:</b> <i>{file_name}</i>\n"
        f"<b>📦 Size:</b> <i>{size}</i>\n\n"
        f"<b>🖥 Stream:</b> {stream}\n"
        f"<b>📥 Download:</b> {download}"
    )

    await status.edit_text(text, reply_markup=buttons, disable_web_page_preview=True)

import random
import humanize
from Script import script
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import URL, LOG_CHANNEL, SHORTLINK
from urllib.parse import quote_plus
from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size
from TechVJ.util.human_readable import humanbytes
from database.users_chats_db import db
from utils import temp, get_shortlink
from TechVJ.bot import TechVJBot


# ================= START =================

@TechVJBot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(
            LOG_CHANNEL,
            script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention)
        )

    rm = InlineKeyboardMarkup(
        [[InlineKeyboardButton("✨ Update Channel", url="https://t.me/CARTOONFUNNY03")]]
    )

    await client.send_message(
        chat_id=message.from_user.id,
        text=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
        reply_markup=rm,
        parse_mode=enums.ParseMode.HTML
    )


# ================= STREAM =================

@TechVJBot.on_message(filters.private & (filters.document | filters.video))
async def stream_start(client, message):

    try:
        # ✅ FIX: correct media access
        file = message.video or message.document
        if not file:
            return

        filename = file.file_name
        filesize = humanize.naturalsize(file.file_size)
        fileid = file.file_id
        user_id = message.from_user.id
        username = message.from_user.mention

        # send to log channel
        log_msg = await client.send_cached_media(
            chat_id=LOG_CHANNEL,
            file_id=fileid
        )

        # ✅ FIX: string, not set
        fileName = quote_plus(get_name(log_msg))

        # generate links
        if not SHORTLINK:
            stream = f"{URL}watch/{str(log_msg.id)}/{fileName}?hash={get_hash(log_msg)}"
            download = f"{URL}{str(log_msg.id)}/{fileName}?hash={get_hash(log_msg)}"
        else:
            stream = await get_shortlink(
                f"{URL}watch/{str(log_msg.id)}/{fileName}?hash={get_hash(log_msg)}"
            )
            download = await get_shortlink(
                f"{URL}{str(log_msg.id)}/{fileName}?hash={get_hash(log_msg)}"
            )

        # reply in log channel
        await log_msg.reply_text(
            text=(
                f"•• ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ ꜰᴏʀ ɪᴅ #{user_id}\n"
                f"•• ᴜꜱᴇʀɴᴀᴍᴇ : {username}\n\n"
                f"•• ᖴᎥᒪᗴ Nᗩᗰᗴ : {fileName}"
            ),
            quote=True,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("🚀 Fast Download 🚀", url=download),
                    InlineKeyboardButton("🖥️ Watch Online 🖥️", url=stream)
                ]]
            )
        )

        # user buttons
        rm = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("sᴛʀᴇᴀᴍ 🖥", url=stream),
                InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ 📥", url=download)
            ]]
        )

        msg_text = (
            "<i><u>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !</u></i>\n\n"
            "<b>📂 Fɪʟᴇ ɴᴀᴍᴇ :</b> <i>{}</i>\n\n"
            "<b>📦 Fɪʟᴇ ꜱɪᴢᴇ :</b> <i>{}</i>\n\n"
            "<b>📥 Dᴏᴡɴʟᴏᴀᴅ :</b> <i>{}</i>\n\n"
            "<b>🖥 ᴡᴀᴛᴄʜ :</b> <i>{}</i>\n\n"
            "<b>🚸 Nᴏᴛᴇ : ʟɪɴᴋ ᴡᴏɴ'ᴛ ᴇxᴘɪʀᴇ ᴛɪʟʟ ɪ ᴅᴇʟᴇᴛᴇ</b>"
        )

        await message.reply_text(
            text=msg_text.format(
                get_name(log_msg),
                humanbytes(get_media_file_size(message)),
                download,
                stream
            ),
            quote=True,
            disable_web_page_preview=True,
            reply_markup=rm
        )

    except Exception as e:
        # 🔥 DEBUG (future problem catch)
        await message.reply_text(f"❌ ERROR:\n{e}")
        print(e)

from pyrogram import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, WebAppInfo
from urllib.parse import quote_plus
import os, asyncio
from database.users_chats_db import db 
from utils import temp
from typing import Any
from urllib.parse import quote_plus


BIN_CHANNEL = int(os.environ.get("BIN_CHANNEL", "-1002071839580")) 
GEN_URL = os.environ.get("GEN_URL", "https://filetolink2-filetolinkbot2.koyeb.app/") # https://example.com/

def get_media_from_message(message: "Message") -> Any:
    media_types = (
        "audio",
        "document",
        "photo",
        "sticker",
        "animation",
        "video",
        "voice",
        "video_note",
    )
    for attr in media_types:
        media = getattr(message, attr, None)
        if media:
            return media


def get_hash(media_msg: Message) -> str:
    media = get_media_from_message(media_msg)
    return getattr(media, "file_unique_id", "")[:6]

def get_name(media_msg: Message) -> str:
    media = get_media_from_message(media_msg)
    return getattr(media, 'file_name', "")


@Client.on_callback_query(filters.regex(r"^stream_link"))
async def stream_link(client, query):
     _, file_id, user_id = query.data.split(":")
     msg = await client.send_cached_media(chat_id=int(BIN_CHANNEL),file_id=file_id,) 
     stream = f"{GEN_URL}watch/{str(msg.id)}/{quote_plus(get_name(msg))}?hash={get_hash(msg)}"
     download = f"{GEN_URL}{str(msg.id)}/{quote_plus(get_name(msg))}?hash={get_hash(msg)}"
     if await db.has_premium_access(int(user_id)): 
         btn = [InlineKeyboardButton("⚡️ғᴀꜱᴛ ᴅᴏᴡɴʟᴏᴀᴅ ⚡️", url=download,), InlineKeyboardButton("🖥 ᴡᴀᴛᴄʜ ᴏɴʟɪɴᴇ 🖥", url=stream,),
         ],[InlineKeyboardButton("ᴡᴀᴛᴄʜ ɪɴ ᴡᴇʙ ᴀᴘᴘ", web_app=WebAppInfo(url=stream))]
         return await query.edit_message_reply_markup(InlineKeyboardMarkup(btn))
     else:
         await query.answer("processing...") 
         msg = await query.message.reply(f"Hay bro this features only available in Premium user\n\nYou can go premium if you want access to it.\n\nClick on the /plan to know the premium price")
         await asyncio.sleep(120)
         await msg.delete()
         return

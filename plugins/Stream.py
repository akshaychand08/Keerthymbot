from pyrogram import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, WebAppInfo
from urllib.parse import quote_plus
import os, asyncio
from database.users_chats_db import db 
from utils import temp, get_shortlinks
from typing import Any
from info import BIN_CHANNEL, GEN_URL
from urllib.parse import quote_plus


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
     stream = f"{GEN_URL}watch/{get_hash(msg)}{msg.id}"
     download = f"{GEN_URL}{str(msg.id)}/{quote_plus(get_name(msg))}?hash={get_hash(msg)}"
     if await db.has_premium_access(int(user_id)): 
       download = download
       stream = stream
     else:
       stream = await get_shortlinks(stream, stream_url=True)
       download = await get_shortlinks(download, stream_url=True) 
     btn = [InlineKeyboardButton("🖥 ᴡᴀᴛᴄʜ ᴏɴʟɪɴᴇ 🖥", url=stream,)
     ],[InlineKeyboardButton("⏮️ How to open ⏭️", url="https://t.me/HoW_ToOpEn/42")]
     return await query.edit_message_reply_markup(InlineKeyboardMarkup(btn))

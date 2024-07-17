from utils import get_size, temp
from database.users_chats_db import db 
from info import CUSTOM_FILE_CAPTION
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def send_all_files(client, message, files, chat_id, grp_id):
    for file in files: 
        title = file.file_name
        size=get_size(file.file_size)
        f_caption=file.caption 
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
            except:
                f_caption=f_caption
        if f_caption is None:
            f_caption = f"{files.file_name}"      
        
        await client.send_cached_media(
            chat_id=message.from_user.id,
            file_id=file.file_id,
            caption=f_caption,   
            protect_content=False,
	        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⚡️ fast 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 watch online ⚡️", callback_data=f"stream_link:{file.file_id}:{message.from_user.id}")],]),)
        

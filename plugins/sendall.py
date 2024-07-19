from utils import get_size, temp, replace_username
from database.users_chats_db import db 
from info import CUSTOM_FILE_CAPTION
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Script import FILE_CAP

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
            caption=replace_username(FILE_CAP.format(title, size, message.from_user.mention, temp.U_NAME, temp.B_NAME)),   
            protect_content=False,
	        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⚡️ 𝙁𝙖𝙨𝙩 𝘿𝙤𝙬𝙣𝙡𝙤𝙖𝙙 / 𝙒𝙖𝙩𝙘𝙝 𝙊𝙣𝙡𝙞𝙣𝙚 ⚡️", callback_data=f"stream_link:{files.file_id}:{message.from_user.id}"
                    )
                ],
                [            
                   InlineKeyboardButton( 
                       "🔸Movies Update Channel🔸", url="https://t.me/+DkozCPNwxxJmMjFl"
                   )
                ],
                [
                    InlineKeyboardButton(
                        "🔹𝗙𝗼𝗹𝗹𝗼𝘄 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺🔹", url="https://www.instagram.com/akshaychand10?igsh=OGQ5ZDc2ODk2ZA=="
                    )
                ],
            ]
        ),
    )        

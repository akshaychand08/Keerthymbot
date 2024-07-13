import os
import string
import pytz
from database.reffer import referdb
from datetime import datetime
import logging
from database.verify_db import vr_db
from .pm_filter import auto_filter 
import random
import contextlib
import asyncio
from .Premium import add_premium
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.ia_filterdb import Media, get_file_details, unpack_new_file_id
from database.users_chats_db import db
from info import TUTORIAL_LINK, VR_COM_photo, VR_LOG, CHANNELS, ADMINS, AUTH_CHANNEL, LOG_CHANNEL, PICS, BATCH_FILE_CAPTION, CUSTOM_FILE_CAPTION, PROTECT_CONTENT
from utils import get_shortlinks, get_settings, get_size, is_subscribed, save_group_settings, temp
from database.connections_mdb import active_connection
import re
import json
import base64
logger = logging.getLogger(__name__)

BATCH_FILES = {}

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client:Client, message):
    m = message
    user_id = m.from_user.id
    if len(m.command) == 2 and m.command[1].startswith('notcopy'):
        user_id = int(m.command[1].split("_")[1])
        verify_id = m.command[1].split("_")[2]
        file_id = m.command[1].split("_")[3] if len(m.command[1].split("_")) > 3 else None
        ist_timezone = pytz.timezone('Asia/Kolkata')
        verify_id_info = await db.get_verify_id_info(user_id, verify_id)
        if not verify_id_info or verify_id_info["verified"]:
            await message.reply("Invalid link. Link has already verified or has wrong hash. Try Again")
            return
        await db.update_notcopy_user(user_id, {"last_verified":datetime.now(tz=ist_timezone)})
        await db.update_verify_id_info(user_id, verify_id, {"verified":True})     
        url = temp.VR_ID.get(user_id)
        buttons = [[InlineKeyboardButton("🚶 ʙᴀᴄᴋ ᴛᴏ ɢʀᴏᴜᴘ 🚶",url="https://t.me/+9G1Tx8tQ05pkNjU1"),]]
        if file_id:
            buttons.insert(0, [InlineKeyboardButton("♻️ ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ɢᴇᴛ ғɪʟᴇ ♻️", url=url)])
        time_zone = datetime.now(pytz.timezone("Asia/Kolkata")) 
        current_date = time_zone.strftime("%d-%m-%Y") 
        current_time = time_zone.strftime("%I:%M:%S %p")     
        await client.send_message(VR_LOG, script.VR_LOG_COM_TXT.format(m.from_user.mention, user_id, current_time, current_date)) 

        dmm = await m.reply_photo(
        photo=(VR_COM_photo), 
        caption=(script.COM_TXT.format(message.from_user.mention)), 
        reply_markup=InlineKeyboardMarkup(buttons),parse_mode=enums.ParseMode.HTML)
        await vr_db.save_verification(message.from_user.id)	    
        return
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        buttons = [
            [
                InlineKeyboardButton('🤖 Updates', url='https://t.me/TeamEvamaria')
            ],
            [
                InlineKeyboardButton('ℹ️ Help', url=f"https://t.me/{temp.U_NAME}?start=help"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply(script.START_TXT.format(message.from_user.mention if message.from_user else message.chat.title, temp.U_NAME, temp.B_NAME), reply_markup=reply_markup)
        await asyncio.sleep(2) # 😢 https://github.com/EvamariaTG/EvaMaria/blob/master/plugins/p_ttishow.py#L17 😬 wait a bit, before checking.
        if not await db.get_chat(message.chat.id):
            total=await client.get_chat_members_count(message.chat.id)
            await client.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, "Unknown"))       
            await db.add_chat(message.chat.id, message.chat.title)
        return 
    if len(message.command) == 2 and message.command[1].startswith("reff_"):
        try:
            user_id = int(message.command[1].split("_")[1])
        except ValueError:
            await message.reply_text("𝘐𝘯𝘷𝘢𝘭𝘪𝘥 𝘙𝘦𝘧𝘦𝘳...")
            return
        if user_id == message.from_user.id:
            await message.reply_text("𝘠𝘰𝘶 𝘊𝘰𝘯𝘯𝘰𝘵 𝘙𝘦𝘧𝘦𝘳 𝘠𝘰𝘶𝘳𝘚𝘦𝘭𝘧...")
            return
        if referdb.is_user_in_list(message.from_user.id):
            await message.reply_text("𝘠𝘰𝘶 𝘏𝘢𝘷𝘦 𝘉𝘦𝘦𝘯 𝘈𝘭𝘳𝘦𝘢𝘥𝘺 𝘐𝘯𝘷𝘪𝘵𝘦𝘥...")
            return
        if await db.is_user_exist(message.from_user.id): 
            await message.reply_text("𝘠𝘰𝘶 𝘏𝘢𝘷𝘦 𝘉𝘦𝘦𝘯 𝘈𝘭𝘳𝘦𝘢𝘥𝘺 𝘐𝘯𝘷𝘪𝘵𝘦𝘥...")
            return            
        try:
            uss = await client.get_users(user_id)
        except Exception:
            return
        referdb.add_user(message.from_user.id)
        fromuse = referdb.get_refer_points(user_id) + 10
        if fromuse == 100:
            referdb.add_refer_points(user_id, 0) 
            await message.reply_text(f"𝘠𝘰𝘶 𝘏𝘢𝘷𝘦 𝘉𝘦𝘦𝘯 𝘚𝘶𝘤𝘤𝘦𝘴𝘴𝘧𝘶𝘭𝘭𝘺 𝘐𝘯𝘷𝘪𝘵𝘦𝘥 𝘉𝘺 {uss.mention}!") 
            await client.send_message(user_id, text=f"𝘠𝘰𝘶 𝘏𝘢𝘷𝘦 𝘉𝘦𝘦𝘯 𝘚𝘶𝘤𝘤𝘦𝘴𝘴𝘧𝘶𝘭𝘭𝘺 𝘐𝘯𝘷𝘪𝘵𝘦𝘥 𝘉𝘺 {message.from_user.mention}!") 
            await add_premium(client, user_id, uss)
        else:
            referdb.add_refer_points(user_id, fromuse)
            await message.reply_text(f"𝘠𝘰𝘶 𝘏𝘢𝘷𝘦 𝘚𝘶𝘤𝘤𝘦𝘴𝘴𝘧𝘶𝘭𝘭𝘺 𝘐𝘯𝘷𝘪𝘵𝘦𝘥 𝘉𝘺 {uss.mention}!")
            await client.send_message(user_id, f"𝘠𝘰𝘶 𝘏𝘢𝘷𝘦 𝘚𝘶𝘤𝘤𝘦𝘴𝘴𝘧𝘶𝘭𝘭𝘺 𝘐𝘯𝘷𝘪𝘵𝘦𝘥 𝘉𝘺 {message.from_user.mention}!")
        return
    
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))
    if len(message.command) != 2:
        buttons = [[
            InlineKeyboardButton('➕ Add Me To Your Groups ➕', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
            ],[
            InlineKeyboardButton('🔍 Search', switch_inline_query_current_chat=''),
            InlineKeyboardButton('🤖 Updates', url='https://t.me/TeamEvamaria')
            ],[
            InlineKeyboardButton('ℹ️ Help', callback_data='help'),
            InlineKeyboardButton('😊 About', callback_data='about')
            ],[
            InlineKeyboardButton('= 🌘 ᴀᴅs ꜰʀᴇᴇ sᴜʙsᴄʀɪᴘᴛɪᴏɴ 🌘 =', callback_data='buy_premium'),
            ], [
            InlineKeyboardButton('✨ ʀᴇꜰᴇʀ ᴘʀᴇᴍɪᴜᴍ ✨', callback_data='reffff'),  
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
    if len(message.command) == 2 and message.command[1].startswith('getfile'):
        movies = message.command[1].split("-", 1)[1] 
        movie = movies.replace('-',' ')
        message.text = movie 
        sts = await message.reply_text("searching...")
        await auto_filter(client, message, sts) 
        return

    if AUTH_CHANNEL and not await is_subscribed(client, message):
        try:
            invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        except ChatAdminRequired:
            logger.error("Make sure Bot is admin in Forcesub channel")
            return
        btn = [
            [
                InlineKeyboardButton(
                    "🤖 Join Updates Channel", url=invite_link.invite_link
                )
            ]
        ]

        if message.command[1] != "subscribe":
            try:
                kk, file_id = message.command[1].split("_", 1)
                pre = 'checksubp' if kk == 'filep' else 'checksub' 
                btn.append([InlineKeyboardButton(" 🔄 Try Again", callback_data=f"{pre}#{file_id}")])
            except (IndexError, ValueError):
                btn.append([InlineKeyboardButton(" 🔄 Try Again", url=f"https://t.me/{temp.U_NAME}?start={message.command[1]}")])
        await client.send_message(
            chat_id=message.from_user.id,
            text="**Please Join My Updates Channel to use this Bot!**",
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode=enums.ParseMode.MARKDOWN
            )
        return
    if len(message.command) == 2 and message.command[1] in ["subscribe", "error", "okay", "help"]:
        buttons = [[
            InlineKeyboardButton('➕ Add Me To Your Groups ➕', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
            ],[
            InlineKeyboardButton('🔍 Search', switch_inline_query_current_chat=''),
            InlineKeyboardButton('🤖 Updates', url='https://t.me/TeamEvamaria')
            ],[
            InlineKeyboardButton('ℹ️ Help', callback_data='help'),
            InlineKeyboardButton('😊 About', callback_data='about')
            ],[
            InlineKeyboardButton('= 🌘 ᴀᴅs ꜰʀᴇᴇ sᴜʙsᴄʀɪᴘᴛɪᴏɴ 🌘 =', callback_data='buy_premium')
            ], [
            InlineKeyboardButton('✨ ʀᴇꜰᴇʀ ᴘʀᴇᴍɪᴜᴍ ✨', callback_data='reffff')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
    data = message.command[1]
    try:
        pre, grp_id, file_id = data.split('_', 2)
    except:
        file_id = data
        pre = ""
    settings = await get_settings(int(grp_id))
    user_id = m.from_user.id
    if await db.has_premium_access(user_id):
        pass 
    elif not settings.get("Short_mode") not settings.get("is_short"): 
        pass
    else:
        verify_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
        await db.create_verify_id(user_id, verify_id)
        url = await get_shortlinks(f"https://telegram.me/{temp.U_NAME}?start=notcopy_{user_id}_{verify_id}_{file_id}")
        buttons = [[InlineKeyboardButton(text="🔹 Click hare to Verify 🔹", url=url),], [InlineKeyboardButton(text="🌀 How to verify 🌀", url=TUTORIAL_LINK)]]
        reply_markup=InlineKeyboardMarkup(buttons)
        if not await db.is_user_verified(user_id): 
            temp.VR_ID[message.from_user.id] = f"https://t.me/{temp.U_NAME}?start={message.command[1]}"
            time_zone = datetime.now(pytz.timezone("Asia/Kolkata")) 
            current_date = time_zone.strftime("%d-%m-%Y")  
            current_time = time_zone.strftime("%I:%M:%S %p")      
            await client.send_message(VR_LOG, script.VR_LOG_TXT.format(m.from_user.mention, user_id, current_time, current_date)) 		
            dmb = await m.reply_text(
                text=(script.VR_TXT.format(message.from_user.mention)),
                protect_content = False,
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
            await asyncio.sleep(120) 
            await dmb.delete()	
            return 
    settings = await get_settings(int(grp_id))
    premium = await db.has_premium_access(m.from_user.id)
    type_, grp_id, file_id = data.split("_", 2)
    if type_ != 'shortlink' and not settings.get("Short_mode") not settings.get("is_short") and not premium:
        tz = pytz.timezone('Asia/Colombo')
        time = datetime.now(tz)
        now = time.strftime("%H")    
        if now < "12":
            status = "ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ 🌞"
        elif now < "18":
            status = "ɢᴏᴏᴅ ᴀꜰᴛᴇʀɴᴏᴏɴ 🌗"
        else:
            status = "ɢᴏᴏᴅ ᴇᴠᴇɴɪɴɢ 🌘"        
        user_name = message.from_user.mention 
        user = message.from_user.id
        files_ = await get_file_details(file_id)
        files = files_[0]
        how_to_download = TUTORIAL_LINK       
        g = await get_shortlinks(f"https://telegram.me/{temp.U_NAME}?start=shortlink_{user}_{file_id}")
        am = await client.send_message(chat_id=user,text=f"Hay {user_name}. {status}\n\n<b>▶️ File Name: <code>{files.file_name}</code> \n\n⌛️ Size: {get_size(files.file_size)}\n\n📂 File Link: {g}\n\n<i>Note: This message is deleted in 3 mins to avoid copyrights. Save the link to Somewhere else</i></b>", protect_content=True, reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('📂 Dᴏᴡɴʟᴏᴀᴅ Nᴏᴡ 📂', url=g)
                    ], [
                        InlineKeyboardButton("🔸 ʜᴏᴡ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ 🔸", url=how_to_download),
        
                    ]
                ]
            )
        )
        async def del_func():
            await asyncio.sleep(180)
            await am.delete()
        await asyncio.create_task(del_func())
        return
    
    files_ = await get_file_details(file_id)           
    if not files_:
        return await message.reply('No such file exist.')
    files = files_[0]
    title = files.file_name
    size=get_size(files.file_size)
    f_caption=files.caption
    if CUSTOM_FILE_CAPTION:
        try:
            f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
        except Exception as e:
            logger.exception(e)
            f_caption=f_caption
    if f_caption is None:
        f_caption = f"{files.file_name}"
    await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=file_id,
        caption=f_caption,
        protect_content=True if pre == 'filep' else False,
	    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⚡️ fast 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 watch online ⚡️", callback_data=f"stream_link:{files.file_id}:{message.from_user.id}")],]),)
                    

@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(bot, message):
           
    """Send basic information of channel"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Unexpected type of CHANNELS")

    text = '📑 **Indexed channels/groups**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n**Total:** {len(CHANNELS)}'

    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)


@Client.on_message(filters.command('logs') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))

@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("Processing...⏳", quote=True)
    else:
        await message.reply('Reply to file with /delete which you want to delete', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('This is not supported file format')
        return
    
    file_id, file_ref = unpack_new_file_id(media.file_id)

    result = await Media.collection.delete_one({
        '_id': file_id,
    })
    if result.deleted_count:
        await msg.edit('File is successfully deleted from database')
    else:
        file_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
        result = await Media.collection.delete_many({
            'file_name': file_name,
            'file_size': media.file_size,
            'mime_type': media.mime_type
            })
        if result.deleted_count:
            await msg.edit('File is successfully deleted from database')
        else:
            # files indexed before https://github.com/EvamariaTG/EvaMaria/commit/f3d2a1bcb155faf44178e5d7a685a1b533e714bf#diff-86b613edf1748372103e94cacff3b578b36b698ef9c16817bb98fe9ef22fb669R39 
            # have original file name.
            result = await Media.collection.delete_many({
                'file_name': media.file_name,
                'file_size': media.file_size,
                'mime_type': media.mime_type
            })
            if result.deleted_count:
                await msg.edit('File is successfully deleted from database')
            else:
                await msg.edit('File not found in database')


@Client.on_message(filters.command('deleteall') & filters.user(ADMINS))
async def delete_all_index(bot, message):
    await message.reply_text(
        'This will delete all indexed files.\nDo you want to continue??',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="YES", callback_data="autofilter_delete"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="CANCEL", callback_data="close_data"
                    )
                ],
            ]
        ),
        quote=True,
    )


@Client.on_callback_query(filters.regex(r'^autofilter_delete'))
async def delete_all_index_confirm(bot, message):
    await Media.collection.drop()
    await message.answer('Piracy Is Crime')
    await message.message.edit('Succesfully Deleted All The Indexed Files.')


@Client.on_message(filters.command('settings'))
async def settings(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    settings = await get_settings(grp_id)

    if settings is not None:
        buttons = [
            [
                InlineKeyboardButton(
                    'Shortlink',
                    callback_data=f'setgs#is_short#{settings.get("is_short")}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'enable' if settings.get("is_short") else 'disable',
                    callback_data=f'setgs#is_short#{settings.get("is_short")}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Shortlink mode',
                    callback_data=f'setgs#Short_mode#{settings.get("Short_mode")}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'verification' if settings.get("Short_mode") else 'Shortlink',
                    callback_data=f'setgs#Short_mode#{settings.get("Short_mode")}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'File Secure',
                    callback_data=f'setgs#file_secure#{settings.get("file_secure")}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ Yes' if settings.get("file_secure") else '❌ No',
                    callback_data=f'setgs#file_secure#{settings.get("file_secure")}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Spell Check',
                    callback_data=f'setgs#spell_check#{settings.get("spell_check")}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ Yes' if settings.get("spell_check") else '❌ No',
                    callback_data=f'setgs#spell_check#{settings.get("spell_check")}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Welcome',
                    callback_data=f'setgs#welcome#{settings.get("welcome")}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ Yes' if settings.get("welcome") else '❌ No',
                    callback_data=f'setgs#welcome#{settings.get("welcome")}#{grp_id}',
                ),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(buttons)

        await message.reply_text(
            text=f"<b>Change Your Settings for {title} As Your Wish ⚙</b>",
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.HTML,
            reply_to_message_id=message.id
        )



@Client.on_message(filters.command('set_template'))
async def save_template(client, message):
    sts = await message.reply("Checking template")
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    if len(message.command) < 2:
        return await sts.edit("No Input!!")
    template = message.text.split(" ", 1)[1]
    await save_group_settings(grp_id, 'template', template)
    await sts.edit(f"Successfully changed template for {title} to\n\n{template}")

# Kanged From @TroJanZheX
import asyncio
import re
import ast
import math
from database.reffer import referdb
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script, AK_AKSHAY
import pyrogram
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, \
    make_inactive
from info import PREMIUM_PIC, USERNAME, ADMINS, AUTH_CHANNEL, RQST_CHANNEL, REQ_GRP, AK_AKSHAY1, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_GROUPS, P_TTI_SHOW_OFF, IMDB, \
    SINGLE_BUTTON, SPELL_CHECK_REPLY, IMDB_TEMPLATE
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto, Message
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import get_size, is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings
from database.users_chats_db import db
from database.ia_filterdb import remove_username, Media, get_file_details, get_search_results
from database.filters_mdb import (
    del_all,
    find_filter,
    get_filters,
)
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

BUTTONS = {}
SPELL_CHECK = {}


@Client.on_message(filters.group | filters.private & filters.text & filters.incoming)
async def give_filter(client, message):
    k = await manual_filters(client, message)
    if k == False: 
        if message.text.startswith("/"): return
        if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text): 
            await message.delete()
            return 
        sts = await message.reply_text("searching...")
        await auto_filter(client, message, sts)



@Client.on_message(filters.text & filters.incoming &~ filters.chat(REQ_GRP))
async def give_filter(client, message):
    k = await manual_filters(client, message)
    if k == False:
        await auto_filter(client, message)

@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(REQ_GRP))
async def req_grp_results(bot, msg: Message):
    if msg.text.startswith("/"): return
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", msg.text):
        return
    files = None
    if 2 < len(msg.text) < 100:
        search = msg.text.replace('movie', '').replace('gujarati', '').replace('gujrati', '').replace('punjabi', '').replace('marathi', '').replace('season', '').replace('web', '').replace('series', '').replace('movies', '').replace('episode', '').replace('Episods', '').replace('dubbed', '').replace('dubb', '').replace('!', '').replace('(', '').replace(')', '').replace(':', '').replace(',', '').replace('dabbed', '') 
        files, offset, total_results = await get_search_results(search.lower(), offset=0, filter=True)

    if not files:

        # request movie from admin
        msg_id = msg.id
        user_id = msg.from_user.id
        user_name = msg.from_user.mention
        user_query = msg.text
        reply = search.replace('hindi', '').replace(" ", '+')
        reply_markup1 = [
            [
                InlineKeyboardButton("🔍 Click here to Check Spilling ✅", url=f"https://www.google.com/search?q={reply}+movie"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Updated  ✅",
                    callback_data=f'rq2#up#{msg_id}#{user_query}',
                ),
                InlineKeyboardButton(
                    text="Check Google ✅",
                    callback_data=f'rq1#au#{msg_id}#{user_query}',
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Not released in OTT yet",
                    callback_data=f'rq#nr#{msg_id}#{user_query}',
                ),            
                InlineKeyboardButton(
                    text="Not Available in hindi",
                    callback_data=f'rq#ntaih#{msg_id}#{user_query}',
                ),    
            ],
            [
                InlineKeyboardButton(
                    text="Not Dubb in hindi",
                    callback_data=f'rq#ntdih#{msg_id}#{user_query}',
                ), 
                InlineKeyboardButton(
                    text="original audio",
                    callback_data=f'rq#ntaik#{msg_id}#{user_query}',
                ),                       

            ],
            [
                InlineKeyboardButton(
                    text="Already uploaded ✅",
                    callback_data=f'rq#alupd#{msg_id}#{user_query}',
                ),
                InlineKeyboardButton(
                    text="Go to Google check your spelling",
                    callback_data=f'rq#cysp#{msg_id}#{user_query}',
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Not released yet",
                    callback_data=f'rq3#nry#{msg_id}#{user_query}',
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Send imdb Link",
                    callback_data=f'rq4#simd#{msg_id}#{user_query}',
                ),
                InlineKeyboardButton(
                    text="Not available",
                    callback_data=f'rq#na#{msg_id}#{user_query}',
                ),
            ],
             [
                InlineKeyboardButton(
                    text="Close",
                    callback_data="close_data"          
                ),
            ],
        ]
        await bot.send_message(RQST_CHANNEL, text=f"#MW_Request #MovieRequest\n\nGroup 1 👉 <a href=https://t.me/+kXz6EM6q9tMwZjA1>Click Here</a>\n\nGroup 2 👉 <a href=https://t.me/+NuVCnwIihDc5NzY1>Click Here</a>\n\nUser <b>{user_name}</b>\n\nrequested for <code>{user_query}</code>\n\nReply to <code>/pm {user_id} {msg_id} message</code>`\n\nView message 👉 <a href=https://t.me/iPapdiscussion/{msg_id}>Click Here</a>\n😎", reply_markup=InlineKeyboardMarkup(reply_markup1))
        user_info = USER_SPELL_CHECK.get(msg.from_user.id)
        if not user_info or time.time() - user_info >= 60:
            USER_SPELL_CHECK[msg.from_user.id] = time.time()
            reply = search.replace('hindi', '').replace(" ", '+')
            reply_markup = InlineKeyboardMarkup([[
            InlineKeyboardButton("ɪɴsᴛʀᴜᴄᴛɪᴏɴs", callback_data='inst'),
            InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ", url="https://t.me/+VSL-2W-eQFJlNGJl")
            ],[
            InlineKeyboardButton("🔍 ᴄʟɪᴄᴋ ᴛᴏ ᴄʜᴇᴄᴋ sᴘɪʟʟɪɴɢ ✅", url=f"https://www.google.com/search?q={reply}+movie")
            ]]  
            )
            a = await msg.reply_photo(
                photo=(AK_AKSHAY1),
                caption=(AK_AKSHAY.format(msg.from_user.mention, search)),
                reply_markup=reply_markup                 
            )
            await asyncio.sleep(30)
            await a.delete()
        return

    await msg.reply(f'<b>Dear.</b> {msg.from_user.mention}  \n\n👉 <code>{total_results}</code> 👈 <b>results are already available for your request</b> 👉 <code>{search}</code> 👈 <b>in our bot..\n\n plz Go back our bot and type movie name</b> 👇',  reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔹 Movies Bot 🔹",url="https://t.me/iPapcornPrimeBot"),]]),parse_mode=enums.ParseMode.HTML),

@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):
    ident, req, key, offset = query.data.split("_")
    if int(req) not in [query.from_user.id, 0]:
        return await query.answer("oKda", show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 0
    search = BUTTONS.get(key)
    if not search:
        await query.answer("You are using one of my old messages, please send the request again.", show_alert=True)
        return

    files, n_offset, total = await get_search_results(search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    grp_id = query.message.chat.id
    batch_ids = files
    temp.GETALL[f"{query.message.chat.id}-{query.message.id}"] = batch_ids
    batch_link = f"batchfiles#{query.message.chat.id}#{query.message.id}#{query.from_user.id}"          
    
    btn = []
    for file in files:        
        btn.append([
            InlineKeyboardButton(text=f"⚡️ {get_size(file.file_size)}» {remove_username(file.file_name)}", url=f'https://telegram.dog/{temp.U_NAME}?start=files_{grp_id}_{file.file_id}')
        ])

    if 0 < offset <= 10:
        off_set = 0
    elif offset == 0:
        off_set = None
    else:
        off_set = offset - 10
    if n_offset == 0:
        btn.append(
            [InlineKeyboardButton("⏪ BACK", callback_data=f"next_{req}_{key}_{off_set}"),
             InlineKeyboardButton(f"📃 Pages {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}",
                                  callback_data="pages")]
        )
    elif off_set is None:
        btn.append(
            [InlineKeyboardButton(f"🗓 {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}", callback_data="pages"),
             InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{req}_{key}_{n_offset}")])
    else:
        btn.append(
            [
                InlineKeyboardButton("⏪ BACK", callback_data=f"next_{req}_{key}_{off_set}"),
                InlineKeyboardButton(f"🗓 {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}", callback_data="pages"),
                InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{req}_{key}_{n_offset}")
            ],
        )
    btn.insert(0,
        [InlineKeyboardButton("📰 ʟᴀɴɢᴜᴀɢᴇs", callback_data=f"languages#{key}#{req}#{offset}"),InlineKeyboardButton("send all", callback_data=batch_link)])        
    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    await query.answer()


@Client.on_callback_query(filters.regex(r"^spolling"))
async def advantage_spoll_choker(bot, query):
    _, user, movie_ = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer("okDa", show_alert=True)
    if movie_ == "close_spellcheck":
        return await query.message.delete()
    movies = SPELL_CHECK.get(query.message.reply_to_message.id)
    if not movies:
        return await query.answer("You are clicking on an old button which is expired.", show_alert=True)
    movie = movies[(int(movie_))]
    await query.answer('Checking for Movie in database...')
    k = await manual_filters(bot, query.message, text=movie)
    if k == False:
        files, offset, total_results = await get_search_results(movie, offset=0, filter=True)
        if files:
            k = (movie, files, offset, total_results)
            await auto_filter(bot, query, k)
        else:                
            btn = [[
            InlineKeyboardButton('⌬ ʀᴇQᴜᴇꜱᴛ ᴀᴅᴍɪɴ ⌬', url="https://t.me/+sJaVzpXTaExhMGNl")
        ]]        
            k=await query.message.edit('<b>✯ sᴏʀʀʏ ɴᴏ ꜰɪʟᴇs 📂 ᴡᴇʀᴇ ꜰᴏᴜɴᴅ\n\nʏᴏᴜʀ ᴍᴏᴠɪᴇ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ 📊\n\nɴᴏᴛ ʀᴇʟᴇᴀsᴇ ᴏᴛᴛ ʏᴇᴛ ⚠️\n\nɪꜰ ʏᴏᴜʀ ᴍᴏᴠɪᴇ ɪs ʀᴇʟᴇᴀsᴇᴅ ᴏɴ ᴏᴛᴛ ᴛʜᴇɴ ɴᴏᴛ ᴀᴅᴅ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ 🙁 sᴇɴᴅ ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴀᴅᴍɪɴ ᴛᴏ ᴀᴅᴅ ʏᴏᴜʀ ᴍᴏᴠɪᴇ..\n\n👇 sᴇɴᴅ ʀᴇǫᴜᴇsᴛ 📩</b>', reply_markup=InlineKeyboardMarkup(btn))    
            await asyncio.sleep(60)
            await k.delete()

@Client.on_callback_query(filters.regex(r"^reffff"))
async def refercall(bot, query):
    btn = [[
        InlineKeyboardButton(f'Refer Point {referdb.get_refer_points(query.from_user.id)}📍', callback_data='ref_point'),
        InlineKeyboardButton('Share Link', url=f'https://telegram.me/share/url?url=https://t.me/{bot.me.username}?start=reff_{query.from_user.id}&text=Hello%21%20Experience%20a%20bot%20that%20offers%20a%20vast%20library%20of%20unlimited%20movies%20and%20series.%20%F0%9F%98%83'),
    ],[
        InlineKeyboardButton('⇋ ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ ⇋', callback_data='rf_start')
    ]]
    reply_markup = InlineKeyboardMarkup(btn)
    await bot.edit_message_media(
        query.message.chat.id,
        query.message.id,
        InputMediaPhoto("https://graph.org/file/372c98c53839539955d4d.jpg"))	    
    await query.message.edit_text(
        text=f'<b>𝘏𝘦𝘭𝘭𝘰 {query.from_user.mention} 𝘠𝘰𝘶𝘳 𝘙𝘦𝘧𝘦𝘳 𝘓𝘪𝘯𝘬 :\n\nhttps://t.me/{bot.me.username}?start=reff_{query.from_user.id}\n\n🔋 ꜰᴏʀ ᴇᴠᴇʀʏ ɴᴇᴡ ᴜsᴇʀ ᴡʜᴏ sᴛᴀʀᴛs ᴛʜᴇ ʙᴏᴛ ᴜsɪɴɢ ᴛʜɪs ʟɪɴᴋ, ʏᴏᴜ ᴡɪʟʟ ʀᴇᴄᴇɪᴠᴇ 10 ᴘᴏɪɴᴛs...\n\n‼️ ᴏɴᴄᴇ ʏᴏᴜ ʀᴇᴀᴄʜ 100 ᴘᴏɪɴᴛs, ʏᴏᴜ ᴡɪʟʟ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ɢᴇᴛ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss. ꜰᴏʀ 𝟷𝟻 ᴅᴀʏs</b>',
        reply_markup=reply_markup,
        parse_mode=enums.ParseMode.HTML
    )    
    await query.answer()

@Client.on_callback_query(filters.regex(r"^languages"))
async def languages_(client: Client, query: CallbackQuery):
    _, key, req, offset = query.data.split("#")
    if int(req) != query.from_user.id:
        return await query.answer(f"Hello {query.from_user.first_name},\nDon't Click Other Results!", show_alert=True)
    btn = [[
        InlineKeyboardButton("ʜɪɴᴅɪ", callback_data=f"fl#hindi#{key}#{offset}#{req}"),
        InlineKeyboardButton("ᴇɴɢʟɪꜱʜ", callback_data=f"fl#english#{key}#{offset}#{req}")
        ],[
        InlineKeyboardButton("ᴛᴀᴍɪʟ", callback_data=f"fl#tamil#{key}#{offset}#{req}"),
        InlineKeyboardButton("ᴛᴇʟᴜɢᴜ", callback_data=f"fl#telugu#{key}#{offset}#{req}")
        ],[
        InlineKeyboardButton("ᴍᴀʟᴀʏᴀʟᴀᴍ", callback_data=f"fl#malayalam#{key}#{offset}#{req}"),
        InlineKeyboardButton("ᴋᴀɴɴᴀᴅᴀ", callback_data=f"fl#kannada#{key}#{offset}#{req}")
        ],[
        InlineKeyboardButton("ᴘᴜɴɪᴀʙɪ", callback_data=f"fl#punjabi#{key}#{offset}#{req}"),
        InlineKeyboardButton("ᴍᴀʀᴀᴛʜɪ", callback_data=f"fl#marathi#{key}#{offset}#{req}")
        ],[
        InlineKeyboardButton("ʙᴇɴɢᴏʟɪ", callback_data=f"fl#bengoli#{key}#{offset}#{req}"),
        InlineKeyboardButton("ɢᴜɪʀᴀᴛɪ", callback_data=f"fl#gujrati#{key}#{offset}#{req}")
        ],[
        InlineKeyboardButton("ᴅᴜᴀʟ", callback_data=f"fl#dual#{key}#{offset}#{req}"),
        InlineKeyboardButton("ᴍᴜʟᴛɪ", callback_data=f"fl#multi#{key}#{offset}#{req}")
    ]] 
    btn.append([InlineKeyboardButton(text="⪻ ʙᴀᴄᴋ ᴛᴏ ᴍᴀɪɴ ᴘᴀɢᴇ", callback_data=f"next_{req}_{key}_{offset}")])  
    await query.message.edit_text("<b>ɪɴ ᴡʜɪᴄʜ ʟᴀɴɢᴜᴀɢᴇ ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ, sᴇʟᴇᴄᴛ ʜᴇʀᴇ 👇</b>", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(btn))

@Client.on_callback_query(filters.regex(r"^fl"))
async def filter_languages_cb_handler(client: Client, query: CallbackQuery):
    _, lang, key, offset, req = query.data.split("#")
    if int(req) != query.from_user.id:
        return await query.answer(f"Hello {query.from_user.first_name},\nDon't Click Other Results!", show_alert=True)

    search = BUTTONS.get(key)
    if not search:
        await query.answer(f"Hello {query.from_user.first_name},\nSend New Request Again!", show_alert=True)
        return 

    files, l_offset, total_results = await get_search_results(search, lang=lang)
    if not files:
        await query.answer(f"sᴏʀʀʏ '{lang.title()}' ʟᴀɴɢᴜᴀɢᴇ ꜰɪʟᴇs ɴᴏᴛ ꜰᴏᴜɴᴅ 😕", show_alert=1)
        return
    grp_id = query.message.chat.id 
    batch_ids = files
    temp.GETALL[f"{query.message.chat.id}-{query.message.id}"] = batch_ids
    batch_link = f"batchfiles#{query.message.chat.id}#{query.message.id}#{query.from_user.id}"          
    btn = []
    for file in files:        
        btn.append([
            InlineKeyboardButton(text=f"⚡️ {get_size(file.file_size)}» {remove_username(file.file_name)}", url=f'https://telegram.dog/{temp.U_NAME}?start=files_{grp_id}_{file.file_id}')
        ])    
    if l_offset != "":
        btn.append(
            [InlineKeyboardButton(text=f"1/{math.ceil(int(total_results) / 10)}", callback_data="buttons"),
             InlineKeyboardButton(text="ɴᴇxᴛ »", callback_data=f"lang_next#{req}#{key}#{lang}#{l_offset}#{offset}")]
        )
    btn.insert(0,
        [InlineKeyboardButton("📰 ʟᴀɴɢᴜᴀɢᴇs", callback_data=f"languages#{key}#{req}#{offset}"),InlineKeyboardButton("send all", callback_data=batch_link)])  
    
    btn.append([InlineKeyboardButton(text="⪻ ʙᴀᴄᴋ ᴛᴏ ᴍᴀɪɴ ᴘᴀɢᴇ", callback_data=f"next_{req}_{key}_{offset}")])
    
    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btn))

@Client.on_callback_query(filters.regex(r"^lang_next"))
async def lang_next_page(bot, query):
    ident, req, key, lang, l_offset, offset = query.data.split("#")
    if int(req) != query.from_user.id:
        return await query.answer(f"Hello {query.from_user.first_name},\nDon't Click Other Results!", show_alert=True)
    try:
        l_offset = int(l_offset)
    except:
        l_offset = 0
    search = BUTTONS.get(key)
    if not search:
        await query.answer(f"Hello {query.from_user.first_name},\nSend New Request Again!", show_alert=True)
        return
    files, n_offset, total = await get_search_results(search, offset=l_offset, lang=lang)
    if not files:
        return
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0
    grp_id = query.message.chat.id 
    batch_ids = files
    temp.GETALL[f"{query.message.chat.id}-{query.message.id}"] = batch_ids
    batch_link = f"batchfiles#{query.message.chat.id}#{query.message.id}#{query.from_user.id}"              
    btn = []
    for file in files:        
        btn.append([
            InlineKeyboardButton(text=f"⚡️ {get_size(file.file_size)}» {remove_username(file.file_name)}", url=f'https://telegram.dog/{temp.U_NAME}?start=files_{grp_id}_{file.file_id}')
        ])
    
    if 0 < l_offset <= 10:
        b_offset = 0
    elif l_offset == 0:
        b_offset = None
    else:
        b_offset = l_offset - 10
    if n_offset == 0:
        btn.append(
            [InlineKeyboardButton("« ʙᴀᴄᴋ", callback_data=f"lang_next#{req}#{key}#{lang}#{b_offset}#{offset}"),
             InlineKeyboardButton(f"{math.ceil(int(l_offset) / 10) + 1}/{math.ceil(total / 10)}", callback_data="buttons")]
        )
    elif b_offset is None:
        btn.append(
            [InlineKeyboardButton(f"{math.ceil(int(l_offset) / 10) + 1}/{math.ceil(total / 10)}", callback_data="buttons"),
             InlineKeyboardButton("ɴᴇxᴛ »", callback_data=f"lang_next#{req}#{key}#{lang}#{n_offset}#{offset}")]
        )
    else:
        btn.append(
            [InlineKeyboardButton("« ʙᴀᴄᴋ", callback_data=f"lang_next#{req}#{key}#{lang}#{b_offset}#{offset}"),
             InlineKeyboardButton(f"{math.ceil(int(l_offset) / 10) + 1}/{math.ceil(total / 10)}", callback_data="buttons"),
             InlineKeyboardButton("ɴᴇxᴛ »", callback_data=f"lang_next#{req}#{key}#{lang}#{n_offset}#{offset}")]
        ) 
    btn.append([InlineKeyboardButton(text="⪻ ʙᴀᴄᴋ ᴛᴏ ᴍᴀɪɴ ᴘᴀɢᴇ", callback_data=f"next_{req}_{key}_{offset}")])
    btn.insert(0,
        [InlineKeyboardButton("📰 ʟᴀɴɢᴜᴀɢᴇs", callback_data=f"languages#{key}#{req}#{offset}"),InlineKeyboardButton("send all", callback_data=batch_link)])      
    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btn))
                                          
@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        await query.message.delete()
    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            grpid = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.message.edit_text("Make sure I'm present in your group!!", quote=True)
                    return await query.answer('Piracy Is Crime')
            else:
                await query.message.edit_text(
                    "I'm not connected to any groups!\nCheck /connections or connect to any groups",
                    quote=True
                )
                return await query.answer('Piracy Is Crime')

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            title = query.message.chat.title

        else:
            return await query.answer('Piracy Is Crime')

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("You need to be Group Owner or an Auth User to do that!", show_alert=True)
    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer("That's not for you!!", show_alert=True)
    elif "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        act = query.data.split(":")[2]
        hr = await client.get_chat(int(group_id))
        title = hr.title
        user_id = query.from_user.id

        if act == "":
            stat = "CONNECT"
            cb = "connectcb"
        else:
            stat = "DISCONNECT"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}"),
             InlineKeyboardButton("DELETE", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("BACK", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"Group Name : **{title}**\nGroup ID : `{group_id}`",
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return await query.answer('Piracy Is Crime')
    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title

        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"Connected to **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text('Some error occurred!!', parse_mode=enums.ParseMode.MARKDOWN)
        return await query.answer('Piracy Is Crime')
    elif "disconnect" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"Disconnected from **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return await query.answer('Piracy Is Crime')
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "Successfully deleted connection"
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return await query.answer('Piracy Is Crime')
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "There are no active connections!! Connect to some groups first.",
            )
            return await query.answer('Piracy Is Crime')
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                act = " - ACTIVE" if active else ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "Your connected group details ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    elif "alertmessage" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_filter(grp_id, keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert, show_alert=True)
    if query.data.startswith("file"):
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        settings = await get_settings(query.message.chat.id)
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
            f_caption = f_caption
        if f_caption is None:
            f_caption = f"{files.file_name}"

        try:
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            elif settings['botpm']:
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            else:
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    protect_content=True if ident == "filep" else False 
                )
                await query.answer('Check PM, I have sent files in pm', show_alert=True)
        except UserIsBlocked:
            await query.answer('Unblock the bot mahn !', show_alert=True)
        except PeerIdInvalid:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
        except Exception as e:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
    elif query.data.startswith("checksub"):
        if AUTH_CHANNEL and not await is_subscribed(client, query):
            await query.answer("I Like Your Smartness, But Don't Be Oversmart 😒", show_alert=True)
            return
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
                f_caption = f_caption
        if f_caption is None:
            f_caption = f"{title}"
        await query.answer()
        await client.send_cached_media(
            chat_id=query.from_user.id,
            file_id=file_id,
            caption=f_caption,
            protect_content=True if ident == 'checksubp' else False
        )

    elif query.data == "buy_premium":
        btn = [[
            InlineKeyboardButton('☎ sᴇɴᴅ ᴘᴀʏᴍᴇɴᴛ ᴘʀᴏᴏꜰ ☎', url=USERNAME)
        ],[
            InlineKeyboardButton('⇋ ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ ⇋', callback_data='rf_start')            
        ]]
        reply_markup = InlineKeyboardMarkup(btn)
        await client.edit_message_media(
            query.message.chat.id,
            query.message.id,
            InputMediaPhoto(PREMIUM_PIC))	    
        await query.message.edit_text(
            text=script.PREMIUM_TEXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "rf_premium":
        btn = [[
            InlineKeyboardButton('☎ sᴇɴᴅ ᴘᴀʏᴍᴇɴᴛ ᴘʀᴏᴏꜰ ☎', url=USERNAME)
        ],[
            InlineKeyboardButton('✂️ ᴄʟᴏsᴇ ᴛʜɪs ᴘᴀɢᴇ ✂️', callback_data='close_data')            
        ]]
        reply_markup = InlineKeyboardMarkup(btn)
        await query.message.reply_photo(
            photo=(PREMIUM_PIC),
            caption=script.PREMIUM_TEXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )    
    
    elif query.data == "pages":
        await query.answer()
    elif query.data == "start":
        buttons = [[
            InlineKeyboardButton('➕ Add Me To Your Groups ➕', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
        ], [
            InlineKeyboardButton('ᴄʜᴀɴɴᴇʟ', url='https://t.me/+VSL-2W-eQFJlNGJl'),
            InlineKeyboardButton('ɢʀᴏᴜᴘ', url='https://t.me/+7p7DwzUq5WdmYWU1')
        ], [
            InlineKeyboardButton('ℹ️ ʜᴇʟᴘ', callback_data='help'),
            InlineKeyboardButton('😊 ᴀʙᴏᴜᴛ', callback_data='about')
        ], [
            InlineKeyboardButton('🏅 ᴘʀᴇᴍɪᴜᴍ 🏅', callback_data='buy_premium')        
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        await query.answer('Piracy Is Crime')
    elif query.data == "rf_start":
        buttons = [[
            InlineKeyboardButton('➕ Add Me To Your Groups ➕', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
        ], [
            InlineKeyboardButton('ᴄʜᴀɴɴᴇʟ', url='https://t.me/+VSL-2W-eQFJlNGJl'),
            InlineKeyboardButton('ɢʀᴏᴜᴘ', url='https://t.me/+7p7DwzUq5WdmYWU1')
        ], [
            InlineKeyboardButton('ℹ️ ʜᴇʟᴘ', callback_data='help'),
            InlineKeyboardButton('😊 ᴀʙᴏᴜᴛ', callback_data='about')
        ], [
            InlineKeyboardButton('🏅 ᴘʀᴇᴍɪᴜᴍ 🏅', callback_data='buy_premium')        
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
          query.message.chat.id,
          query.message.id,
          InputMediaPhoto("https://telegra.ph/file/68feb51ce9c55c31d3265.png"))        
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )     
    elif query.data == "ref_point":
        await query.answer(f'You Have: {referdb.get_refer_points(query.from_user.id)} Refferal points.', show_alert=True)

    
    elif query.data == "help":
        buttons = [[
            InlineKeyboardButton('ᴍᴀɴᴜᴀʟ ꜰɪʟᴛᴇʀ', callback_data='manuelfilter'),
            InlineKeyboardButton('ᴀᴜᴛᴏ ꜰɪʟᴛᴇʀ', callback_data='autofilter')
        ], [
            InlineKeyboardButton('ᴄᴏɴɴᴇᴄᴛɪᴏɴ', callback_data='coct'),
            InlineKeyboardButton('ᴇxᴛʀᴀ ᴍᴏᴅꜱ', callback_data='extra')
        ], [
            InlineKeyboardButton('🏠 ʜᴏᴍᴇ', callback_data='start'),
            InlineKeyboardButton('🔮 ꜱᴛᴀᴛᴜꜱ', callback_data='stats')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.HELP_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "about":
        buttons = [[
            InlineKeyboardButton('🤖 ᴜᴘᴅᴀᴛᴇꜱ', url='https://t.me/cinemica'),
            InlineKeyboardButton('♥️ ꜱᴏᴜʀᴄᴇ', callback_data='source')
        ], [
            InlineKeyboardButton('🏠 ʜᴏᴍᴇ', callback_data='start'),
            InlineKeyboardButton('🔐 ᴄʟᴏꜱᴇ', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ABOUT_TXT.format(temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "source":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.SOURCE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "manuelfilter":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help'),
            InlineKeyboardButton('⏹️ Buttons', callback_data='button')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.MANUELFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "button":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='manuelfilter')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.BUTTON_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "autofilter":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.AUTOFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "coct":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CONNECTION_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "extra":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help'),
            InlineKeyboardButton('👮‍♂️ Admin', callback_data='admin')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.EXTRAMOD_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "admin":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='extra')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ADMIN_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "stats":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help'),
            InlineKeyboardButton('♻️', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "rfrsh":
        await query.answer("Fetching MongoDb DataBase")
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help'),
            InlineKeyboardButton('♻️', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data.startswith("setgs"):
        ident, set_type, status, grp_id = query.data.split("#")
        grpid = await active_connection(str(query.from_user.id))

        if str(grp_id) != str(grpid):
            await query.message.edit("Your Active Connection Has Been Changed. Go To /settings.")
            return await query.answer('Piracy Is Crime')
        if set_type == 'is_short' and query.from_user.id not in ADMINS:
            return await query.answer(text=f"ʜᴇʏ, {query.from_user.first_name}\n\nʏᴏᴜ ᴄᴀɴ'ᴛ ᴛᴜʀɴ ᴏғғ ᴛʜɪꜱ ꜱʜᴏʀᴛʟɪɴᴋ", show_alert=True)
            
        if status == "True":
            await save_group_settings(grpid, set_type, False)
        else:
            await save_group_settings(grpid, set_type, True)

        settings = await get_settings(grpid)

        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('Shortlink',
                                         callback_data=f'setgs#is_short#{settings.get("is_short")}#{str(grp_id)}'),
                    InlineKeyboardButton('eneble' if settings.get("is_short") else 'diseble',
                                         callback_data=f'setgs#is_short#{settings.get("is_short")}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Shortlink mode',
                                         callback_data=f'setgs#Short_mode#{settings.get("Short_mode")}#{str(grp_id)}'),
                    InlineKeyboardButton('verification' if settings.get("Short_mode") else 'Shortlink',
                                         callback_data=f'setgs#Short_mode#{settings.get("Short_mode")}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('File Secure',
                                         callback_data=f'setgs#file_secure#{settings.get("file_secure")}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["file_secure"] else '❌ No',
                                         callback_data=f'setgs#file_secure#{settings.get("file_secure")}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Spell Check',
                                         callback_data=f'setgs#spell_check#{settings.get("spell_check")}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings.get("spell_check") else '❌ No',
                                         callback_data=f'setgs#spell_check#{settings.get("spell_check")}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Welcome', callback_data=f'setgs#welcome#{settings.get("welcome")}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings.get("welcome") else '❌ No',
                                         callback_data=f'setgs#welcome#{settings.get("welcome")}#{str(grp_id)}')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_reply_markup(reply_markup)

    elif query.data.startswith("batchfiles"):
        ident, group_id, message_id, user = query.data.split("#")
        chat_id = query.message.chat.id
        group_id = int(group_id)
        message_id = int(message_id)
        user = int(user)
        if user != query.from_user.id:
            return await query.answer("🥷 ᴛʜᴀᴛ ɪꜱ ɴᴏᴛ ғᴏʀ ʏᴏᴜʀ ᴘʟᴢ ꜱᴇᴀʀᴄʜ ʏᴏᴜʀ",show_alert=True)
        link = f"https://telegram.me/{temp.U_NAME}?start=sendallfiles_{query.message.chat.id}_{group_id}-{message_id}"
        return await query.answer(url=link)
        return

    elif query.data.startswith("rq#"):
        _, status, message_id, user_query = query.data.split("#", maxsplit=3)
        dict_info = {"alupd":"Already uploaded ✅\n\nplease Bro Search Only movie/Web series Name 🙏\n\nEx. Jawan\nJawan 2023\nLeo 2023\nLeo 2023 Hindi,Tamil\n\nweb series\nLoki S02\nLoki S02E02\nLoki S02 complete,Combined\n\nNot Search 🙏\nin Hindi language\nMovie,season,All Season, web series", "nry":"Not released yet\n\n🙄release hone se pahle dekhega ke chhore🤨", "ntaik":"Hi BRO, I could not find the dubbed file of the language you told me, but we have found its original audio file, we have updated it.", "ntaih":"Not available in Hindi", "ntdih":"Not Dubb in Hindi", "cysp":"Go to Google and check your spelling  <b><a href=https://www.google.com>𝐆𝐨𝐨𝐠𝐥𝐞</a></b>", "simd":"Send imdb link", "au":"Already uploaded ✅ \n\n Go to Google and check your spelling  <b><a href=https://www.google.com>𝐆𝐨𝐨𝐠𝐥𝐞</a></b>", "up":"Updated  ✅", "nr":"Not released OTT yet", "na":"Not available"}

        user_message = await client.get_messages(REQ_GRP, int(message_id))
        user_id = user_message.from_user.id
        user_mention = (await client.get_users(user_message.from_user.id)).mention
        search = user_query
        text = f"Hey {user_mention}... \n\nYour movie 👉 {dict_info[status]}"
        #reply = search.replace("Kannada", " ").replace("hindi", " ").replace("Malayalam", " ").replace("dubbed", " ").replace("telugu", " ").replace("tamil", " ").replace(" ", "+")
        #btn = [[
            #InlineKeyboardButton('testing', url=f'https://www.google.com/search?q={reply}')
        #]]
        await client.send_message(REQ_GRP, text, reply_to_message_id=int(message_id))  #, reply_markup=InlineKeyboardMarkup(btn))
        bbb = await query.edit_message_text("Request has been updated")
        await asyncio.sleep(20)
        await bbb.delete()    

    elif query.data.startswith("rq1#"):
        _, status, message_id, user_query = query.data.split("#", maxsplit=3)
        dict_info = {"au":"Already uploaded ✅\n\nHey bro your movie Already uploaded go to Google check spelling 🔻\n\nCopy the name from Google and paste it in the group"}

        user_message = await client.get_messages(REQ_GRP, int(message_id))
        user_id = user_message.from_user.id
        user_mention = (await client.get_users(user_message.from_user.id)).mention
        search = user_query
        text = f"Hey {user_mention}... \n\nYour movie 👉 {dict_info[status]}"
        reply = search.replace("Kannada", " ").replace("hindi", " ").replace("Malayalam", " ").replace("dubbed", " ").replace("telugu", " ").replace("tamil", " ").replace(" ", "+")
        btn = [[
            InlineKeyboardButton('🔸 Google 🔸', url=f'https://www.google.com/search?q={reply}+movie')
        ]]
        await client.send_message(REQ_GRP, text, reply_to_message_id=int(message_id), reply_markup=InlineKeyboardMarkup(btn))
        bbb = await query.edit_message_text("Request has been updated")
        await asyncio.sleep(20)
        await bbb.delete()      

    elif query.data.startswith("rq2#"):
        _, status, message_id, user_query = query.data.split("#", maxsplit=3)
        dict_info = {"alupd":"Already uploaded ✅", "nry":"Not released yet", "ntaik":"Not available in kannada", "ntaih":"Not available in Hindi", "ntdih":"Not Dubb in Hindi", "cysp":"Go to Google and check your spelling  <b><a href=https://www.google.com>𝐆𝐨𝐨𝐠𝐥𝐞</a></b>", "simd":"Send imdb link", "au":"Already uploaded ✅ \n\n Go to Google and check your spelling  <b><a href=https://www.google.com>𝐆𝐨𝐨𝐠𝐥𝐞</a></b>", "up":"Updated  ✅\n\nHey bro your movie uploaded go to Group and type movie name 🔻", "nr":"Not released OTT yet", "na":"Not available"}

        user_message = await client.get_messages(REQ_GRP, int(message_id))
        user_id = user_message.from_user.id
        user_mention = (await client.get_users(user_message.from_user.id)).mention
        search = user_query
        text = f"Hey {user_mention}... \n\nYour movie 👉 {dict_info[status]}"
        
        btn = [[
            InlineKeyboardButton('🔹 Group 🔹', url='https://t.me/iPapcornPrimeGroup')
        ]]
        await client.send_message(REQ_GRP, text, reply_to_message_id=int(message_id), reply_markup=InlineKeyboardMarkup(btn))
        bbb = await query.edit_message_text("Request has been updated")
        await asyncio.sleep(20)
        await bbb.delete()

    elif query.data.startswith("rq3#"):
        _, status, message_id, user_query = query.data.split("#", maxsplit=3)
        dict_info = {"alupd":"Already uploaded ✅", "nry":"Not released yet\n\n🙄 Release hone se pahle dekhega ke Chhore 🤨\n\nClick here to Check Release Date 🔻", "ntaik":"Not available in kannada", "ntaih":"Not available in Hindi", "ntdih":"Not Dubb in Hindi", "cysp":"Go to Google and check your spelling  <b><a href=https://www.google.com>𝐆𝐨𝐨𝐠𝐥𝐞</a></b>", "simd":"Send imdb link", "au":"Already uploaded ✅ \n\n Go to Google and check your spelling  <b><a href=https://www.google.com>𝐆𝐨𝐨𝐠𝐥𝐞</a></b>", "up":"Updated  ✅", "nr":"Not released OTT yet", "na":"Not available"}

        user_message = await client.get_messages(REQ_GRP, int(message_id))
        user_id = user_message.from_user.id
        user_mention = (await client.get_users(user_message.from_user.id)).mention
        search = user_query
        text = f"Hey {user_mention}... \n\nYour movie 👉 {dict_info[status]}"
        reply = search.replace("Kannada", " ").replace("hindi", " ").replace("Malayalam", " ").replace("dubbed", " ").replace("telugu", " ").replace("tamil", " ").replace(" ", "+")
        btn = [[
            InlineKeyboardButton('🔸 Check Release Date 🔸', url=f'https://www.google.com/search?q={reply}+movie+release+date')
        ]]
        await client.send_message(REQ_GRP, text, reply_to_message_id=int(message_id), reply_markup=InlineKeyboardMarkup(btn))
        bbb = await query.edit_message_text("Request has been updated")
        await asyncio.sleep(20)
        await bbb.delete()    
        
    elif query.data.startswith("rq4#"):
        _, status, message_id, user_query = query.data.split("#", maxsplit=3)
        dict_info = {"alupd":"Already uploaded ✅", "nry":"Not released yet", "ntaik":"Not available in kannada", "ntaih":"Not available in Hindi", "ntdih":"Not Dubb in Hindi", "cysp":"Go to Google and check your spelling  <b><a href=https://www.google.com>𝐆𝐨𝐨𝐠𝐥𝐞</a></b>", "simd":"Send imdb link\n\nClick here to generate  imdb link 🔻", "au":"Already uploaded ✅ \n\n Go to Google and check your spelling  <b><a href=https://www.google.com>𝐆𝐨𝐨𝐠𝐥𝐞</a></b>", "up":"Updated  ✅", "nr":"Not released OTT yet", "na":"Not available"}

        user_message = await client.get_messages(REQ_GRP, int(message_id))
        user_id = user_message.from_user.id
        user_mention = (await client.get_users(user_message.from_user.id)).mention
        search = user_query
        text = f"Hey {user_mention}... \n\nYour movie 👉 {dict_info[status]}"
        reply = search.replace("Kannada", " ").replace("hindi", " ").replace("Malayalam", " ").replace("dubbed", " ").replace("telugu", " ").replace("tamil", " ").replace(" ", "+")
        btn = [[
            InlineKeyboardButton('▪️ generate imdb link ▪️', url=f'https://m.imdb.com/find/?q={reply}')
        ]]
        await client.send_message(REQ_GRP, text, reply_to_message_id=int(message_id), reply_markup=InlineKeyboardMarkup(btn))
        bbb = await query.edit_message_text("Request has been updated")
        await asyncio.sleep(20)
        await bbb.delete()    

    elif query.data.startswith("direct_gen"):
        stream, download = await direct_gen_handler(query.message)
        if download and stream:
            buttons = [
                    InlineKeyboardButton(
                        "➕ ᴏᴘᴇɴ ꜱᴛʀᴇᴀᴍ & ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ ➕",
                        url=stream,
                    )
                  ]  

            query.message.reply_markup = query.message.reply_markup or []
            # remove the first row
            query.message.reply_markup.inline_keyboard.pop(0)
            query.message.reply_markup.inline_keyboard.insert(0, buttons)
            await query.message.edit_reply_markup(InlineKeyboardMarkup(query.message.reply_markup.inline_keyboard))
                    
    await query.answer("Piracy Is Crime")


async def auto_filter(client, msg, sts, spoll=False):
    if not spoll:
        message = msg
        settings = await get_settings(message.chat.id)
        if message.text.startswith("/"): return  # ignore commands
        if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
            return
        if 2 < len(message.text) < 100:
            search = message.text
            files, offset, total_results = await get_search_results(search.lower(), offset=0, filter=True)
            if not files:
                if settings.get("spell_check"):
                    return await advantage_spell_chok(msg, sts)
                else:
                    return
        else:
            return
    else:
        settings = await get_settings(msg.message.chat.id)
        message = msg.message.reply_to_message  # msg will be callback query
        await msg.message.delete()
        search, files, offset, total_results = spoll
    pre = 'filep' if settings['file_secure'] else 'file'
    grp_id = message.chat.id 
    batch_ids = files
    temp.GETALL[f"{message.chat.id}-{message.id}"] = batch_ids
    batch_link = f"batchfiles#{message.chat.id}#{message.id}#{message.from_user.id}"  
    
    btn = []
    for file in files:        
        btn.append([
            InlineKeyboardButton(text=f"⚡️ {get_size(file.file_size)}» {remove_username(file.file_name)}", url=f'https://telegram.dog/{temp.U_NAME}?start=files_{grp_id}_{file.file_id}')
        ])
    if offset != "":
        key = f"{message.chat.id}-{message.id}"
        BUTTONS[key] = search
        req = message.from_user.id if message.from_user else 0
        btn.append(
            [InlineKeyboardButton(text=f"🗓 1/{math.ceil(int(total_results) / 10)}", callback_data="pages"),
             InlineKeyboardButton(text="NEXT ⏩", callback_data=f"next_{req}_{key}_{offset}")]
        )
    else:
        btn.append(
            [InlineKeyboardButton(text="🗓 1/1", callback_data="pages")]
        )
    key = f"{message.chat.id}-{message.id}"
    req = message.from_user.id if message.from_user else 0 
    BUTTONS[key] = search   
    btn.insert(0,
        [InlineKeyboardButton("📰 ʟᴀɴɢᴜᴀɢᴇs", callback_data=f"languages#{key}#{req}#{offset}"),InlineKeyboardButton("send all", callback_data=batch_link)])        

    cap = f"<b>📕 ᴛɪᴛʟᴇ: {search}\n⚡️ ᴘᴏᴡᴇʀᴇᴅ: <a href=https://t.me/{temp.U_NAME}>{temp.B_NAME}</a>\n🤦 ʀᴇǫᴜᴇꜱᴛ: {message.from_user.mention}</b>"
    dl = await sts.edit(cap, reply_markup=InlineKeyboardMarkup(btn))
    await asyncio.sleep(300)
    await dl.delete()  


async def advantage_spell_chok(msg, sts):
    user = msg.from_user.id if msg.from_user else 0
    query = re.sub(
        r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)",
        "", msg.text, flags=re.IGNORECASE)  # plis contribute some common words
    malik = query.strip()
    try:
        movies = await get_poster(query, bulk=True)
    except Exception as e:
        logger.exception(e)
        await sts.delete()
        reply = malik.replace(" ", '+')  
        reply_markup = InlineKeyboardMarkup([[
        InlineKeyboardButton("🔍 𝗖𝗹𝗶𝗰𝗸 𝗧𝗼 𝗖𝗵𝗲𝗰𝗸 𝗦𝗽𝗶𝗹𝗹𝗶𝗻𝗴 ✅", url=f"https://www.google.com/search?q={reply}+movie")
        ],[
        InlineKeyboardButton("🔍 𝗖𝗹𝗶𝗰𝗸 𝗧𝗼 𝗖𝗵𝗲𝗰𝗸 𝗥𝗲𝗹𝗲𝗮𝘀𝗲 𝗗𝗮𝘁𝗲 📅", url=f"https://www.google.com/search?q={reply}+release+date")
        ]]  
        )    
        a = await msg.reply_text("I couldn't find anything related to that. Check your spelling", reply_markup=reply_markup)
        await asyncio.sleep(12) 
        await a.delete()
        return
    
    if not movies:
        await sts.delete()
        reply = malik.replace(" ", '+')  
        reply_markup = InlineKeyboardMarkup([[
        InlineKeyboardButton("🔍 Click To Check Spilling ✅", url=f"https://www.google.com/search?q={reply}+movie")
        ],[
        InlineKeyboardButton("🔍 Click To Check Release Date 📅", url=f"https://www.google.com/search?q={reply}+release+date")
        ]]  
        )    
        a = await msg.reply_text("I couldn't find anything related to that. Check your spelling", reply_markup=reply_markup)
        await asyncio.sleep(12) 
        await a.delete()
        return
        
    movielist = [movie.get('title') for movie in movies]
    movielist = movielist[:5]

    await sts.delete()
    SPELL_CHECK[msg.id] = movielist
    btn = [[
        InlineKeyboardButton(
            text=movie.strip(),
            callback_data=f"spolling#{user}#{k}",
        )
    ] for k, movie in enumerate(movielist)]
    btn.append([InlineKeyboardButton(text="Close", callback_data=f'spolling#{user}#close_spellcheck')])
    dll = await msg.reply_text(text=f"<b>Hey, {msg.from_user.mention}...😎\n\nᴄʜᴇᴄᴋ ᴀɴᴅ sᴇʟᴇᴄᴛ ᴛʜᴇ ᴍᴏᴠɪᴇ ғʀᴏᴍ ᴛʜᴇ ɢɪᴠᴇɴ ʟɪsᴛ.. \n\n दी गई सूची में अपनी फिल्म देखें और अपनी फिल्म चुनें 👇👇👇</b>",
                    reply_markup=InlineKeyboardMarkup(btn), reply_to_message_id=msg.id)
    await asyncio.sleep(180)
    await dll.delete()   

async def manual_filters(client, message, text=False):
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            await client.send_message(group_id, reply_text, disable_web_page_preview=True)
                        else:
                            button = eval(btn)
                            await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id=reply_id
                            )
                    elif btn == "[]":
                        await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            reply_to_message_id=reply_id
                        )
                    else:
                        button = eval(btn)
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False

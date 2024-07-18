from info import * 
from utils import temp, get_poster, replace_words
from pyrogram import Client, filters, enums
from database.ia_filterdb import Media, get_file_details, get_search_results
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import logging, asyncio

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


REQ_SPELL_CHECK = {}


@Client.on_message(filters.command('pm') & filters.channel)
async def message_cmd_handler(client: Client, m: Message):
    try:
        if len(m.command) < 4:
            wrong_input_txt = "Use this format to send message: `/pm user_id msg_id message`"
            return await m.reply(wrong_input_txt)

        user_id = int(m.command[1])
        reply_msg_id = int(m.command[2])

        try:
            user_mention = (await client.get_users(user_id)).mention
        except Exception as e:
            await m.reply("Some error occurred while fetching user information. Maybe user didn't start the bot yet")
            return 
            
        text = f'Dear {user_mention}, You have a message from admin\n\n{m.text.replace(f"/pm {user_id} {reply_msg_id} ", "")}'
        await client.send_message(REQ_GRP, text, reply_to_message_id=reply_msg_id)
        b =  await m.reply_text("Message sent successfully")
        await asyncio.sleep(10)
        await b.delete()
        await m.delete()
    except Exception as e:
        print(e)


async def usreqst(msg, search, client, release_date, org_name):
        # request movie from admin
        msg_id = msg.id
        user_id = msg.from_user.id
        user_name = msg.from_user.mention
        user_query = msg.text
        reply = search.replace('hindi', '').replace('telugu', '').replace('Kannada', '').replace("tamil", '').replace(" ", '+')
        reply_markup1 = [[
                InlineKeyboardButton("🔔 Movies Cheking Group 🌀", url=f"https://t.me/+2xBSNHJ8h4xjZmM1"),],[
                InlineKeyboardButton("🔍 Check sapling", url=f"https://www.google.com/search?q={reply}+movie"),
                InlineKeyboardButton("🔍 Release date", url=f"https://www.google.com/search?q={reply}+release+date"),],[
                InlineKeyboardButton("Updated  ✅",callback_data=f'rq#up#{msg_id}#{user_query}',),
                InlineKeyboardButton("Already uploaded ✅",callback_data=f'rq#au#{msg_id}#{user_query}',),],[
                InlineKeyboardButton("Not hindi",callback_data=f'rq#nah#{msg_id}#{user_query}',),
                InlineKeyboardButton("Not kan",callback_data=f'rq#nak#{msg_id}#{user_query}',),
                InlineKeyboardButton("Typ oly mov",callback_data=f'rq#tomn#{msg_id}#{user_query}',),],[
                InlineKeyboardButton("Not rel yet",callback_data=f'rq#nry#{msg_id}#{user_query}',),
                InlineKeyboardButton("Not Tam",callback_data=f'rq#natm#{msg_id}#{user_query}',),
                InlineKeyboardButton("Not mal",callback_data=f'rq#nam#{msg_id}#{user_query}',),],[
                InlineKeyboardButton("Not OTT yet",callback_data=f'rq#not#{msg_id}#{user_query}',),                        
                InlineKeyboardButton("Not Tel",callback_data=f'rq#nat#{msg_id}#{user_query}',),
                InlineKeyboardButton("typ oly web",callback_data=f'rq#town#{msg_id}#{user_query}',),],[ 
                InlineKeyboardButton("Send imdb",callback_data=f'rq#simd#{msg_id}#{user_query}',),            
                InlineKeyboardButton("Not available",callback_data=f'rq#na#{msg_id}#{user_query}',),],[
                InlineKeyboardButton("Close",callback_data="close_data"),],] 
        try:
            await client.send_message(RQST_CHANNEL, text=f"my bot 👉 <a href=https://t.me/iPapcornPrimeBot>Click Here</a>\n\nGroup 👉 <a href=https://t.me/+2xBSNHJ8h4xjZmM1>Click Here</a>\n\nUser <b>{user_name}</b>\n\nGoogle: <code>{org_name}</code>\n\nRelease: `{release_date}`\n\nrequested for <code>{user_query}</code>\n\nReply to <code>/pm {user_id} {msg_id} message</code>`\n\nView message 👉 <a href=https://t.me/iPapdiscussion/{msg_id}>Click Here</a>\n😎", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(reply_markup1)) 
        except: 
            await client.send_message(RQST_CHANNEL, text=f"my bot 👉 <a href=https://t.me/iPapcornPrimeBot>Click Here</a>\n\nGroup 👉 <a href=https://t.me/+2xBSNHJ8h4xjZmM1>Click Here</a>\n\nUser <b>{user_name}</b>\n\nGoogle: <code>{org_name}</code>\n\nrequested for <code>{user_query}</code>\n\nReply to <code>/pm {user_id} {msg_id} message</code>`\n\nView message 👉 <a href=https://t.me/iPapdiscussion/{msg_id}>Click Here</a>\n😎", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(reply_markup1)) 
            return await req_spell_chok(msg)
        await req_spell_chok(msg) # req_grp spell check 
        return




async def badreqst(msg, search, client):
        msg_id = msg.id
        user_id = msg.from_user.id
        user_name = msg.from_user.mention
        user_query = msg.text
        reply = search.replace('hindi', '').replace(" ", '+')
        reply_markup1 = [[
                InlineKeyboardButton("🔔 Movies Cheking Group 🌀", url=f"https://t.me/+2xBSNHJ8h4xjZmM1"),],[
                InlineKeyboardButton("🔍 Check sapling", url=f"https://www.google.com/search?q={reply}+movie"),
                InlineKeyboardButton("🔍 Release date", url=f"https://www.google.com/search?q={reply}+release+date"),],[
                InlineKeyboardButton("Updated  ✅",callback_data=f'rq#up#{msg_id}#{user_query}',),
                InlineKeyboardButton("Already uploaded ✅",callback_data=f'rq#au#{msg_id}#{user_query}',),],[
                InlineKeyboardButton("Not hindi",callback_data=f'rq#nah#{msg_id}#{user_query}',),
                InlineKeyboardButton("Not kan",callback_data=f'rq#nak#{msg_id}#{user_query}',),
                InlineKeyboardButton("Typ oly mov",callback_data=f'rq#tomn#{msg_id}#{user_query}',),],[
                InlineKeyboardButton("Not rel yet",callback_data=f'rq#nry#{msg_id}#{user_query}',),
                InlineKeyboardButton("Not Tam",callback_data=f'rq#natm#{msg_id}#{user_query}',),
                InlineKeyboardButton("Not mal",callback_data=f'rq#nam#{msg_id}#{user_query}',),],[
                InlineKeyboardButton("Not OTT yet",callback_data=f'rq#not#{msg_id}#{user_query}',),                        
                InlineKeyboardButton("Not Tel",callback_data=f'rq#nat#{msg_id}#{user_query}',),
                InlineKeyboardButton("typ oly web",callback_data=f'rq#town#{msg_id}#{user_query}',),],[ 
                InlineKeyboardButton("Send imdb",callback_data=f'rq#simd#{msg_id}#{user_query}',),            
                InlineKeyboardButton("Not available",callback_data=f'rq#na#{msg_id}#{user_query}',),],[
                InlineKeyboardButton("Close",callback_data="close_data"),],] 

        await client.send_message(RQST_CHANNEL, text=f"my bot 👉 <a href=https://t.me/iPapcornPrimeBot>Click Here</a>\n\nGroup 👉 <a href=https://t.me/+2xBSNHJ8h4xjZmM1>Click Here</a>\n\nUser <b>{user_name}</b>\n\nrequested for <code>{user_query}</code>\n\nReply to <code>/pm {user_id} {msg_id} message</code>`\n\nView message 👉 <a href=https://t.me/iPapdiscussion/{msg_id}>Click Here</a>\n😎", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(reply_markup1))


#req_grp spell_check 

@Client.on_callback_query(filters.regex(r"^reqspolling"))
async def reqspolling(bot, query):
    _, user, movie_ = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer(f"𝙏𝙝𝙞𝙨 𝙞𝙨 𝙣𝙤𝙩 𝙛𝙤𝙧 𝙮𝙤𝙪 😢", show_alert=True)

    if movie_ == "close_spellcheck":
        return await query.message.delete()
    movies = REQ_SPELL_CHECK.get(query.message.reply_to_message.id)
    if not movies:
        return await query.answer("You are clicking on an old button which is expired.", show_alert=True)
    movie = movies[(int(movie_))]
    movies = await replace_words(movie)

    await query.answer('Checking for Movie in database...')
    files, offset, total_results = await get_search_results(movies)
    if files:
        k = (movies, files, offset, total_results)
        await req_grp_results(bot, query, k) 

    else:
        btn = [[
            InlineKeyboardButton('𝙟𝙤𝙞𝙣 𝙗𝙖𝙘𝙠𝙪𝙥 𝙘𝙝𝙖𝙣𝙣𝙚𝙡', url="https://t.me/arsOfficial10")
        ]]
        await query.message.edit(f"ʜᴇʏ. {query.from_user.mention}\n\nᴛʜɪꜱ ᴍᴏᴠɪᴇ ɴᴏᴛ ғᴏᴜɴᴅ ᴍʏ ᴅᴀᴛᴀʙᴀꜱᴇ..\n\nʏᴏᴜʀ #ʀᴇǫᴜᴇꜱᴛ ʜᴀꜱ ʙᴇᴇɴ ᴀᴄᴄᴇᴘᴛᴇᴅ! ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ ғᴏʀ ᴏᴜʀ ᴀᴅᴍɪɴꜱ ᴛᴏ ʀᴇꜱᴘᴏɴᴅ..", reply_markup=InlineKeyboardMarkup(btn))  
        sts = temp.STS.get(query.from_user.id) 
        await sts.delete()                                                               
                                    

#req_grp results

async def req_grp_results(client, msg, reqspoll=False):
    user_name = msg.from_user.mention
    message = msg
    if not reqspoll:
        return
    else:
        message = msg.message.reply_to_message  # msg will be callback query
        search, files, offset, total_results = reqspoll
        msg_id = message.id
        btn = [[
        InlineKeyboardButton('Close', callback_data="close_data")
    ]]
        sts = temp.STS.get(message.from_user.id)        
        await sts.edit_text(f"#MovieRequest{msg_id}\n\n{user_name}\n\nincorrect name: {message.text}\n\nOrginal name: <code>{search}</code>\n\n⚠️", reply_markup=InlineKeyboardMarkup(btn))
        search = search.replace(" ", '-')
        await message.reply(f'<b>Dear.</b> {msg.from_user.mention}  \n\n👉 <code>{total_results}</code> 👈 <b>results are already available for your request</b> 👉 <code>{search}</code> 👈 <b>in our bot..\n\n plz Go back our bot and type movie name</b> 👇',  reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔹 Get movie 🔹",url=f"https://t.me/{temp.U_NAME}?start=getfile-{search}"),]]),parse_mode=enums.ParseMode.HTML),

        if reqspoll:
            await msg.message.delete()



async def req_spell_chok(msg):
    user = msg.from_user.id if msg.from_user else 0
    query = re.sub(
        r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)",
        "", msg.text, flags=re.IGNORECASE)  # plis contribute some common words

    query = query.strip()    
    try:
        movies = await get_poster(query, bulk=True)
    except Exception as e:
        logger.exception(e)
        reply = query.replace(" ", '+')  
        reply_markup = InlineKeyboardMarkup([[
        InlineKeyboardButton("🔍 𝗖𝗹𝗶𝗰𝗸 𝗧𝗼 𝗖𝗵𝗲𝗰𝗸 𝗦𝗽𝗶𝗹𝗹𝗶𝗻𝗴 ✅", url=f"https://www.google.com/search?q={reply}+movie")
        ],[
        InlineKeyboardButton("🔍 𝗖𝗹𝗶𝗰𝗸 𝗧𝗼 𝗖𝗵𝗲𝗰𝗸 𝗥𝗲𝗹𝗲𝗮𝘀𝗲 𝗗𝗮𝘁𝗲 📅", url=f"https://www.google.com/search?q={reply}+release+date")
        ]]  
        )    
        a = await msg.reply_text(
            text=(script.CUDNT_FND.format(query)),
            reply_markup=reply_markup                 
        )
        await asyncio.sleep(10) 
        await a.delete()
        return
    #movielist = [] 
    if not movies:
        reply = query.replace(" ", '+')  
        reply_markup = InlineKeyboardMarkup([[
        InlineKeyboardButton("🔍 Click To Check Spilling ✅", url=f"https://www.google.com/search?q={reply}+movie")
        ],[
        InlineKeyboardButton("🔍 Click To Check Release Date 📅", url=f"https://www.google.com/search?q={reply}+release+date")
        ]]  
        )    
        a = await msg.reply_text(
            text=(script.CUDNT_FND.format(query)),
            reply_markup=reply_markup                 
        )
        await asyncio.sleep(10) 
        await a.delete()
        return
    movielist = [movie.get('title') for movie in movies]
    #movielist += [f"{movie.get('title')} {movie.get('year')}" for movie in movies]
    movielist = movielist[:5]

    REQ_SPELL_CHECK[msg.id] = movielist
    btn = [[
            InlineKeyboardButton(
            text=movie.strip(),
            callback_data=f"reqspolling#{user}#{k}",
        )
    ] for k, movie in enumerate(movielist)]
    btn.append([InlineKeyboardButton(text="Close", callback_data=f'reqspolling#{user}#close_spellcheck')])
    m = await msg.reply(f"<b>Hey, {msg.from_user.mention}...😎\n\nᴄʜᴇᴄᴋ ᴀɴᴅ sᴇʟᴇᴄᴛ ᴛʜᴇ ᴍᴏᴠɪᴇ ғʀᴏᴍ ᴛʜᴇ ɢɪᴠᴇɴ ʟɪsᴛ.. \n\n दी गई सूची में अपनी फिल्म देखें और अपनी फिल्म चुनें 👇👇👇</b>", reply_markup=InlineKeyboardMarkup(btn))
    await asyncio.sleep(60)
    await m.delete()

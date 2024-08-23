from pyrogram import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from database.verify_db import vr_db 
from info import ADMINS
from database.users_chats_db import db
import info

@Client.on_message(filters.command("verification") & filters.private & filters.user(ADMINS))
async def vrfs(client, message):
    today = await vr_db.get_vr_count("today")
    yesterday = await vr_db.get_vr_count("yesterday")
    this_month = await vr_db.get_vr_count("this_month")
    this_week = await vr_db.get_vr_count("this_week")
    last_month = await vr_db.get_vr_count("last_month")

    btn = [[
        InlineKeyboardButton("today", callback_data=f'vrrfrs#tud'), 
        InlineKeyboardButton(f"{today}", callback_data=f'vrrfrs#tud')
        ],[
        InlineKeyboardButton("yesterday", callback_data=f'vrrfrs#yes'), 
        InlineKeyboardButton(f"{yesterday}", callback_data=f'vrrfrs#yes')
        ],[
        InlineKeyboardButton("this week", callback_data=f'vrrfrs#week'), 
        InlineKeyboardButton(f"{this_week}", callback_data=f'vrrfrs#week')     
        ],[
        InlineKeyboardButton("month", callback_data=f'vrrfrs#mont'), 
        InlineKeyboardButton(f"{this_month}", callback_data=f'vrrfrs#mont')
        ],[
        InlineKeyboardButton("last month", callback_data=f'vrrfrs#lmont'), 
        InlineKeyboardButton(f"{last_month}", callback_data=f'vrrfrs#lmont')        
        ],[
        InlineKeyboardButton("refresh", callback_data=f'vrrfrs#vrrfrs'), 
    ]]
    await message.reply_text("Total verified users", reply_markup=InlineKeyboardMarkup(btn))

@Client.on_callback_query(filters.regex(r"^vrrfrs"))
async def vr_ref(client, query): 
    ident, set_type = query.data.split("#")

    if set_type == "tud":
        return await query.answer('verified users from today', show_alert=True)
    elif set_type == "yes":
        return await query.answer('verified users from yesterday', show_alert=True)
    elif set_type == "week":
        return await query.answer('verified users from this week', show_alert=True)
    elif set_type == "mont":
        return await query.answer('verified users from this month', show_alert=True)
    elif set_type == "lmont":
        return await query.answer('verified users from last month', show_alert=True)
    elif set_type == "vrrfrs":   
        await query.answer("updated data")
        
    today = await vr_db.get_vr_count("today")
    yesterday = await vr_db.get_vr_count("yesterday")
    this_month = await vr_db.get_vr_count("this_month")
    this_week = await vr_db.get_vr_count("this_week")
    last_month = await vr_db.get_vr_count("last_month")
    
    btn = [[
        InlineKeyboardButton("today", callback_data=f'vrrfrs#tud'), 
        InlineKeyboardButton(f"{today}", callback_data=f'vrrfrs#tud')
        ],[
        InlineKeyboardButton("yesterday", callback_data=f'vrrfrs#yes'), 
        InlineKeyboardButton(f"{yesterday}", callback_data=f'vrrfrs#yes')
        ],[
        InlineKeyboardButton("this week", callback_data=f'vrrfrs#week'), 
        InlineKeyboardButton(f"{this_week}", callback_data=f'vrrfrs#week')     
        ],[
        InlineKeyboardButton("month", callback_data=f'vrrfrs#mont'), 
        InlineKeyboardButton(f"{this_month}", callback_data=f'vrrfrs#mont')
        ],[
        InlineKeyboardButton("last month", callback_data=f'vrrfrs#lmont'), 
        InlineKeyboardButton(f"{last_month}", callback_data=f'vrrfrs#lmont')        
        ],[
        InlineKeyboardButton("refresh", callback_data=f'vrrfrs#vrrfrs'), 
    ]]
    await query.message.edit("Total verified users", reply_markup=InlineKeyboardMarkup(btn))
    

@Client.on_message(filters.command("set_shortlink") & filters.user(ADMINS))
async def set_shortlink_data(client, message):
    if len(message.command) < 3:
        await message.reply("Usage: /set_shortlink API SITE")
        return
    
    site = message.command[1]
    api = message.command[2]
    
    await db.save_shortlink_data(api, site)
    await message.reply("Shortlink data saved successfully.")



@Client.on_message(filters.command("set_streamlink") & filters.user(ADMINS))
async def set_streamlink_data(client, message):
    if len(message.command) < 3:
        await message.reply("Usage: /set_streamlink STREAM_API STREAM_SITE")
        return
    
    stream_site = message.command[1]
    stream_api = message.command[2]
    
    await db.save_stream_data(stream_api, stream_site)
    await message.reply("Stream link data saved successfully.")

@Client.on_message(filters.command("add_url") & filters.user(ADMINS))
async def changeauth(_: Client, m):
    args = m.command[1:]
    
    if not args:
        await m.reply_text("You need to provide a url link ")
        return
    info.GEN_URL = " ".join(args)
    await m.reply_text("Changed!")
    return


@Client.on_message(filters.command("get_url") & filters.user(ADMINS))
async def geturl(c, m):
    url = info.GEN_URL
    await m.reply_text(f"your url {url}")
    return

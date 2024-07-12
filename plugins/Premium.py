from datetime import timedelta
import pytz
from Script import script
import datetime, time
from info import ADMINS, PREMIUM_PIC
from utils import get_seconds
from database.users_chats_db import db, delete_all_msg
from pyrogram import Client, filters 
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong

@Client.on_message(filters.command("del_msg") & filters.user(ADMINS))
async def del_msg(client, message):
    user_id = message.from_user.id
    await delete_all_msg(user_id)
    await message.reply_text('deleted')

@Client.on_message(filters.command("remove_premium") & filters.user(ADMINS))
async def remove_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])  # Convert the user_id to integer
        user = await client.get_users(user_id)
        if await db.remove_premium_access(user_id):
            await message.reply_text("Removed!")
            await client.send_message(
                chat_id=user_id,
                text=f"<b>Hay {user.mention}\n\nʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss ʜᴀs Been Removed :\nᴛʜᴀɴᴋ ʏᴏᴜ ꜰᴏʀ ᴜsɪɴɢ ᴏᴜʀ sᴇʀᴠɪᴄᴇ 😊</b>"
            )
        else:
            await message.reply_text("Unable to remove, are you sure it was a premium user id?")
    else:
        await message.reply_text("Usage: /remove_premium user_id")

#testing 

@Client.on_message(filters.command("myplan"))
async def myplan(client, message):
    user = message.from_user.mention 
    user_id = message.from_user.id
    data = await db.get_user(message.from_user.id)  # Convert the user_id to integer
    if data and data.get("expiry_time"):
        #expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=data)
        expiry = data.get("expiry_time") 
        expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
        expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y  ⏰: %I:%M:%S %p")            
        # Calculate time difference
        current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        time_left = expiry_ist - current_time
            
        # Calculate days, hours, and minutes
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
            
        # Format time left as a string
        time_left_str = f"{days} days, {hours} hours, {minutes} minutes"
        await message.reply_text(f"#Premium_user_data:\n\n👤 User: {user}\n\n🪙 User Id: <code>{user_id}</code>\n\n⏰ Time Left: {time_left_str}\n\n⌛️ Expiry: {expiry_str_in_ist}.")   
    else:
        await message.reply_text(f"Hey {user}..\n\nYou do not have any active premium plans, if you want to take premium then\nclick on /plan to know about the plan")
        






@Client.on_message(filters.command("get_premium") & filters.user(ADMINS))
async def get_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        data = await db.get_user(user_id)  # Convert the user_id to integer
        if data and data.get("expiry_time"):
            #expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=data)
            expiry = data.get("expiry_time") 
            expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y %I:%M:%S %p")            
            # Calculate time difference
            current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            time_left = expiry_ist - current_time
            
            # Calculate days, hours, and minutes
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            # Format time left as a string
            time_left_str = f"{days} days, {hours} hours, {minutes} minutes"
            await message.reply_text(f"#Premium_user_data:\n\n👤 User: {user.mention}\n\n🪙 User Id: <code>{user_id}</code>\n\n⏰ Time Left: {time_left_str}\n\n⌛️ Expiry: {expiry_str_in_ist}.")
        else:
            await message.reply_text("No premium data of the user was found in the database!")
    else:
        await message.reply_text("Usage: /get_premium user_id")




@Client.on_message(filters.command("add_premium") & filters.user(ADMINS))
async def give_premium_cmd_handler(client, message):
    if len(message.command) == 4:
        time_zone = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        current_time = time_zone.strftime("%d-%m-%Y  ⏰: %I:%M:%S %p") 
        user_id = int(message.command[1])  # Convert the user_id to integer
        user = await client.get_users(user_id)
        time = message.command[2]+" "+message.command[3]
        seconds = await get_seconds(time)
        if seconds > 0:
            expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
            user_data = {"id": user_id, "expiry_time": expiry_time}  # Using "id" instead of "user_id"  
            await db.update_user(user_data)  # Use the update_user method to update or insert user data
            data = await db.get_user(user_id)
            expiry = data.get("expiry_time")   
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y  ⏰: %I:%M:%S %p")         
            await message.reply_text(f"Premium access added to the user\n\n👤 User: {user.mention}\n\n🪙 user id: <code>{user_id}</code>\n\n⏰ premium access: {time}\n\n🎩 Joining : {current_time}\n\n⌛️ Expiry: {expiry_str_in_ist}.", disable_web_page_preview=True)
            await client.send_photo(
                photo="https://telegra.ph/file/6fedfbed0d268ae3dc427.jpg",            
                chat_id=user_id,
                caption=f"<b>Hay {user.mention}\n\nᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ᴇɴᴊᴏʏ 😀..\n\n⏰ premium access: {time}\n\n🎩 Joining : {current_time}\n\n⌛️ Expiry: {expiry_str_in_ist}</b>"              
            )    

        else:
            await message.reply_text("Invalid time format. Please use '1day for days', '1hour for hours', or '1min for minutes', or '1month for months' or '1year for year'")
    else:
        await message.reply_text("Usage: /add_premium user_id time (e.g., '1 day for days', '1 hour for hours', or '1 min for minutes', or '1 month for months' or '1 year for year')")

@Client.on_message(filters.command("premium_users") & filters.user(ADMINS))
async def premium_user(client, message):
    aa = await message.reply_text("Fetching ...")  
    users = await db.get_all_users()
    users_list = []
    async for user in users:
        users_list.append(user)    
    user_data = {user['id']: await db.get_user(user['id']) for user in users_list}    
    new_users = []
    for user in users_list:
        user_id = user['id']
        data = user_data.get(user_id)
        expiry = data.get("expiry_time") if data else None        
        if expiry:
            expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
            expiry_str_in_ist = expiry_ist.strftime("%d-%m-%Y %I:%M:%S %p")          
            current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            time_left = expiry_ist - current_time
            days, remainder = divmod(time_left.total_seconds(), 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, _ = divmod(remainder, 60)            
            time_left_str = f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes"            
            user_info = await client.get_users(user_id)
            user_str = (
                f"{len(new_users) + 1}. User ID: {user_id}\n"
                f"Name: {user_info.mention}\n"
                f"Expiry Date: {expiry_str_in_ist}\n"
                f"Expiry Time: {time_left_str}\n\n"
            )
            new_users.append(user_str)
    new = "Paid Users - \n\n" + "\n".join(new_users)   
    try:
        await aa.edit_text(new)
    except MessageTooLong:
        with open('usersplan.txt', 'w+') as outfile:
            outfile.write(new)
        await message.reply_document('usersplan.txt', caption="Paid Users:")

@Client.on_message(filters.command('plan') & filters.incoming)
async def plan(client, message):
    user_id = message.from_user.id
    if message.from_user.username:
        user_info = f"@{message.from_user.username}"
    else:
        user_info = f"{message.from_user.mention}"
    btn = [[
            InlineKeyboardButton('☎ sᴇɴᴅ ᴘᴀʏᴍᴇɴᴛ ᴘʀᴏᴏꜰ ☎', url="https//")
            ],[
            InlineKeyboardButton('✂️ ᴄʟᴏsᴇ ᴛʜɪs ᴘᴀɢᴇ ✂️', callback_data='close_data')            
     ]]
    await message.reply_photo(
        photo=(PREMIUM_PIC),
        caption=script.PREMIUM_TEXT, 
        reply_markup=InlineKeyboardMarkup(btn))


async def add_premium(client, user_id, uss):
    seconds = 2592000
    if seconds > 0:
        expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        user_data = {"id": user_id, "expiry_time": expiry_time}  # Using "id" instead of "user_id"  
        await db.update_user(user_data)  # Use the update_user method to update or insert user data                    
        await client.send_message(
        chat_id=user_id,
        text=f"🙋‍♂ <b>Hey {uss.mention}\n\nCongratulations you have received 1 month premium subscription for referring 20 users", disable_web_page_preview=True,              
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔰 ᴍᴏᴠɪᴇ ꜱᴇᴀʀᴄʜ ʜᴇʀᴇ 🔰", url=f"https://t.me/+KP3OcudPwQczZDBl")]]))
        for admin in ADMINS:
            await client.send_message(chat_id=admin, text=f"Successfully completed task by this:\n\nuser: {uss.mention}\n\nuser id: {uss.id}!")




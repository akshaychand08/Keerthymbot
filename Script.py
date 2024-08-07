class script(object):
    START_TXT = """<b>ʜᴇʏ {}..💝

ɪᴍ ⚡️ ᴘᴏᴡᴇʀғᴜʟ ᴀᴜᴛᴏ-ғɪʟᴛᴇʀ ʙᴏᴛ...
😎 ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴍᴇ ᴀs ᴀ ᴀᴜᴛᴏ-ғɪʟᴛᴇʀ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ....
ɪᴛs ᴇᴀsʏ ᴛᴏ ᴜsᴇ ᴍᴇ: ᴊᴜsᴛ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀs ᴀᴅᴍɪɴ, ᴛʜᴀᴛs ᴀʟʟ, ɪ ᴡɪʟʟ ᴘʀᴏᴠɪᴅᴇ ᴍᴏᴠɪᴇs ᴛʜᴇʀᴇ...😎

⚠️ ᴍᴏʀᴇ ʜᴇʟᴘ ᴄʜᴇᴄᴋ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ..

©ᴍᴀɴᴛᴀɪɴᴇᴅ ʙʏ: ᴀᴋꜱʜᴀʏ ᴄʜᴀɴᴅ ✌️</b>"""
    
    HELP_TXT = """𝙷𝙴𝚈 {}
𝙷𝙴𝚁𝙴 𝙸𝚂 𝚃𝙷𝙴 𝙷𝙴𝙻𝙿 𝙵𝙾𝚁 𝙼𝚈 𝙲𝙾𝙼𝙼𝙰𝙽𝙳𝚂."""
    ABOUT_TXT = """🌟 <b>𝙼𝚈 𝙽𝙰𝙼𝙴:</b> {}
👥 <b>𝙲𝚁𝙴𝙰𝚃𝙾𝚁:</b> <a href="https://t.me/Akshaychand08">Akshay Chand</a>
📘 <b>𝙻𝙸𝙱𝚁𝙰𝚁𝚈:</b> 𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼
🌍 <b>𝙻𝙰𝙽𝙶𝚄𝙰𝙶𝙴:</b> 𝙿𝚈𝚃𝙷𝙾𝙽 𝟹
📅 <b>𝙳𝙰𝚃𝙰 𝙱𝙰𝚂𝙴:</b> 𝙼𝙾𝙽𝙶𝙾 𝙳𝙱
🛠️ <b>𝙱𝙾𝚃 𝚂𝙴𝚁𝚅𝙴𝚁:</b> 𝙷𝙴𝚁𝙾𝙺𝚄
ℹ️ <b>𝙱𝚄𝙸𝙻𝙳 𝚂𝚃𝙰𝚃𝚄𝚂:</b> v1.0.1 [ 𝙱𝙴𝚃𝙰 ]
"""
    SOURCE_TXT = """<b>NOTE:</b>
- Lazy Princess is a open source project. 
- Source - https://github.com/LazyDeveloperr/LazyPrincess  

<b>DEVS:</b>
- <a href=https://t.me/Akshaychand08>Akshay Chand</a>"""
    MANUELFILTER_TXT = """Help: <b>Filters</b>

- Filter is the feature were users can set automated replies for a particular keyword and EvaMaria will respond whenever a keyword is found the message

<b>NOTE:</b>
1. eva maria should have admin privillage.
2. only admins can add filters in a chat.
3. alert buttons have a limit of 64 characters.

<b>Commands and Usage:</b>
• /filter - <code>add a filter in chat</code>
• /filters - <code>list all the filters of a chat</code>
• /del - <code>delete a specific filter in chat</code>
• /delall - <code>delete the whole filters in a chat (chat owner only)</code>"""
    BUTTON_TXT = """Help: <b>Buttons</b>

- Eva Maria Supports both url and alert inline buttons.

<b>NOTE:</b>
1. Telegram will not allows you to send buttons without any content, so content is mandatory.
2. Eva Maria supports buttons with any telegram media type.
3. Buttons should be properly parsed as markdown format

<b>URL buttons:</b>
<code>[Button Text](buttonurl:https://t.me/EvaMariaBot)</code>

<b>Alert buttons:</b>
<code>[Button Text](buttonalert:This is an alert message)</code>"""
    AUTOFILTER_TXT = """Help: <b>Auto Filter</b>

<b>NOTE:</b>
1. Make me the admin of your channel if it's private.
2. make sure that your channel does not contains camrips, porn and fake files.
3. Forward the last message to me with quotes.
 I'll add all the files in that channel to my db."""
    CONNECTION_TXT = """Help: <b>Connections</b>

- Used to connect bot to PM for managing filters 
- it helps to avoid spamming in groups.

<b>NOTE:</b>
1. Only admins can add a connection.
2. Send <code>/connect</code> for connecting me to ur PM

<b>Commands and Usage:</b>
• /connect  - <code>connect a particular chat to your PM</code>
• /disconnect  - <code>disconnect from a chat</code>
• /connections - <code>list all your connections</code>"""
    EXTRAMOD_TXT = """Help: <b>Extra Modules</b>

<b>NOTE:</b>
these are the extra features of Eva Maria

<b>Commands and Usage:</b>
• /id - <code>get id of a specified user.</code>
• /info  - <code>get information about a user.</code>
• /imdb  - <code>get the film information from IMDb source.</code>
• /search  - <code>get the film information from various sources.</code>"""
    ADMIN_TXT = """Help: <b>Admin mods</b>

<b>NOTE:</b>
This module only works for my admins

<b>Commands and Usage:</b>
• /logs - <code>to get the rescent errors</code>
• /stats - <code>to get status of files in db.</code>
• /delete - <code>to delete a specific file from db.</code>
• /users - <code>to get list of my users and ids.</code>
• /chats - <code>to get list of the my chats and ids </code>
• /leave  - <code>to leave from a chat.</code>
• /disable  -  <code>do disable a chat.</code>
• /ban  - <code>to ban a user.</code>
• /unban  - <code>to unban a user.</code>
• /channel - <code>to get list of total connected channels</code>
• /broadcast - <code>to broadcast a message to all users</code>"""
    STATUS_TXT = """🎥 TOTAL FILES: <code>{}</code>
👥 TOTAL USERS: <code>{}</code>
💬 TOTAL CHATS: <code>{}</code>
📦 USED STORAGE: <code>{}</code> MiB
🗃️ FREE STORAGE: <code>{}</code> MiB"""
    LOG_TEXT_G = """#NewGroup
Group = {}(<code>{}</code>)
Total Members = <code>{}</code>
Added By - {}
"""
    LOG_TEXT_P = """#NewUser
ID - <code>{}</code>
Name - {}
"""


    
    VR_LOG_COM_TXT = """
<b><u>ᴜsᴇʀ ᴠᴇʀɪꜰɪᴇᴅ sᴜᴄᴄᴇssꜰᴜʟʟʏ ✅</u>

👮‍♀ ɴᴀᴍᴇ:- {}  
✏️ ɪᴅ: <code>{}</code> 
🕜 ᴛɪᴍᴇ: <code>{}</code>
📆 ᴅᴀᴛᴇ:- <code>{} </code></b>

#verified_completed"""

    VR_LOG_TXT = """
<b><u>ᴜsᴇʀ new verifiction</u>

👮‍♀ ɴᴀᴍᴇ:- {}  
✏️ ɪᴅ: <code>{}</code> 
🕜 ᴛɪᴍᴇ: <code>{}</code>
📆 ᴅᴀᴛᴇ:- <code>{} </code></b>

#new_verifiction"""

    
    VR_TXT = """
🚫 You are not verified today.

🔑 Please verify to get unlimited access for one day.

🆘 If you are having any problem with verification, send a screenshot or screen recording showing the problem to @ARS_official10 and ask for help.

🌟 If you don't want to verify daily, you can subscribe to our premium plan to enjoy unlimited movies without the need for daily verification. 

🔔 Click for plan details: /plan

"""

    COM_TXT = """Hey {},

You are now verified until tonight at 12:00 AM. Enjoy your unlimited access for your entertainment! 🎉🍿

#Completed
"""



    PREMIUM_TEXT = """<b><i><u> 🌟 ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʟᴀɴs 🌟</u></i></b>

* At Rs.9    -  1 day
* At Rs.25   -  15 day
* At Rs.49   -  1 month 
* At Rs.99   -  2 months
* At Rs.149  -  3 months
* At Rs.199  -  4 months
* At Rs.239  -  5 months
* At Rs.299  -  6 months


* Premium Plan Benefits:

*  No need verify
*  fast download 
*  watch online
*  Movies (Original Prints And Theatre Prints)
*  unlimited request for movies no limit 
*  all Tv shows 
*  direct files no links

click to check your activ plan- /myplan

* Payment methods:

* UPI ID :  <code>akshaychand10@ybl</code>

* (Tap to Copy) [Supports All Apps Like Google pay, Phone pay, Paytm]

* Must Take a Screenshot after Payment and Send it to @akshaychand08 To Activate Your Subscription

* Contact: @akshaychand08 for Any Doubts and Clarification
"""

FILE_CAP = """
ғɪʟᴇ ɴᴀᴍᴇ:- <code>{}</code>

ғɪʟᴇ ꜱɪᴢᴇ:- {}.

┏━━━━•❅•°•❈•°•❅••━━━━┓\n✰👑 <b>𝐉𝐨𝐢𝐧 <a href=https://t.me/iPapcornPrimeGroup>𝙈𝙤𝙫𝙞𝙚𝙨 𝙂𝙧𝙤𝙪𝙥</a></b>  👑✰\n┗━━━━•❅•°•❈•°•❅•━━━━┛

ʀᴇǫᴜᴇꜱᴛᴇᴅ ʙʏ:- {}

ᴘᴏᴡᴇʀᴇᴅ ʙʏ: <spoiler><a href=https://t.me/{}>{}</a></spoiler>

🔔 Click for plan details: <b>/plan</b> To direct downloading link without ads.
"""

ADMIN_STATUS_TXT = """
➢ {}
➢ {}
➢ {}
➢ {}
➢ {}
➢ {}"""

UNBANP_LOG_TXT = """<b>⍟ UɴBᴀɴɴᴇᴅ Usᴇʀ Lᴏɢs ⍟</b>

<b>Aᴅᴍɪɴ :</b> </b> <b>{}</b>

<b>Nᴀᴍᴇ :</b> <b>{}</b>

<b>⍟ #UnBannedUser ⍟</b>
"""

BANG_LOG_TXT = """<b>⍟ Bᴀɴɴᴇᴅ Gʀᴏᴜᴘ Lᴏɢs ⍟</b>

<b>Cʜᴀᴛ ID :</b> <code>{}</code>

<b>Rᴇᴀsᴏɴ :</b> <code>{}</code>

<b>Aᴅᴍɪɴ :</b> </b> <b>{}</b>

<b>⍟ #BannedGroup ⍟</b>
"""

import re, os
from os import environ

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

# Bot information
PORT = environ.get("PORT", "8080")
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ.get('API_ID', '22301351'))
API_HASH = environ.get('API_HASH', '3035f2bbd92a9c5174d174d92b52b25b')
BOT_TOKEN = environ.get('BOT_TOKEN', '5790067344:AAFcjnHm8eI6SNabEAS8ap2sYp8sKOp35h8')

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = is_enabled((environ.get('USE_CAPTION_FILTER', 'True')), True)
PICS = (environ.get('PICS', 'https://te.legra.ph/file/f772c17d89ab263940aa9.jpg https://te.legra.ph/file/f7f89f94312f465bc1619.jpg https://te.legra.ph/file/bca46ec3f862653984ac3.jpg https://te.legra.ph/file/51df2197b3c81fb5c74bb.jpg https://te.legra.ph/file/e0204c7c62be495bd3757.jpg https://te.legra.ph/file/7e4fb5aaebcfbb491d94b.jpg https://te.legra.ph/file/cac00041d6815ae72c636.jpg https://te.legra.ph/file/aa11112a7008f0c2cfa86.jpg https://te.legra.ph/file/964aadd2b69cbfdbc747b.jpg https://te.legra.ph/file/e20f06f2db0a5cdbadc6b.jpg https://te.legra.ph/file/dfb17b7113756689d1157.jpg https://te.legra.ph/file/e2c6398a9405104ee54a2.jpg https://te.legra.ph/file/8fb297d8d87113955e13a.jpg https://te.legra.ph/file/9305b907779de8d073ac2.jpg https://te.legra.ph/file/8934a9e779a7f21e44290.jpg')).split()

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '5721673207').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '-1001859046902 -1002108230565 -1002222788520').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL', '')
auth_grp = environ.get('AUTH_GROUP')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None

# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://akshay:chand@cluster0.fbevi6n.mongodb.net/?retryWrites=true&w=majority")
DATABASE_NAME = environ.get('DATABASE_NAME', "mongodb")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')
# Others
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1001942599034'))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'iPapdiscussion')
P_TTI_SHOW_OFF = is_enabled((environ.get('P_TTI_SHOW_OFF', "False")), False)
IMDB = is_enabled((environ.get('IMDB', "True")), True)
SINGLE_BUTTON = is_enabled((environ.get('SINGLE_BUTTON', "False")), False)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", None)
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", CUSTOM_FILE_CAPTION)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "<b>Query: {query}</b> \n‌‌‌‌IMDb Data:\n\n🏷 Title: <a href={url}>{title}</a>\n🎭 Genres: {genres}\n📆 Year: <a href={url}/releaseinfo>{year}</a>\n🌟 Rating: <a href={url}/ratings>{rating}</a> / 10")
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), True)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '')).split()]
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "True")), True)
PROTECT_CONTENT = is_enabled((environ.get('PROTECT_CONTENT', "False")), False)
PUBLIC_FILE_STORE = is_enabled((environ.get('PUBLIC_FILE_STORE', "True")), True)

LOG_STR = "Current Cusomized Configurations are:-\n"
LOG_STR += ("IMDB Results are enabled, Bot will be showing imdb details for you queries.\n" if IMDB else "IMBD Results are disabled.\n")
LOG_STR += ("P_TTI_SHOW_OFF found , Users will be redirected to send /start to Bot PM instead of sending file file directly\n" if P_TTI_SHOW_OFF else "P_TTI_SHOW_OFF is disabled files will be send in PM, instead of sending start.\n")
LOG_STR += ("SINGLE_BUTTON is Found, filename and files size will be shown in a single button instead of two separate buttons\n" if SINGLE_BUTTON else "SINGLE_BUTTON is disabled , filename and file_sixe will be shown as different buttons\n")
LOG_STR += (f"CUSTOM_FILE_CAPTION enabled with value {CUSTOM_FILE_CAPTION}, your files will be send along with this customized caption.\n" if CUSTOM_FILE_CAPTION else "No CUSTOM_FILE_CAPTION Found, Default captions of file will be used.\n")
LOG_STR += ("Long IMDB storyline enabled." if LONG_IMDB_DESCRIPTION else "LONG_IMDB_DESCRIPTION is disabled , Plot will be shorter.\n")
LOG_STR += ("Spell Check Mode Is Enabled, bot will be suggesting related movies if movie not found\n" if SPELL_CHECK_REPLY else "SPELL_CHECK_REPLY Mode disabled\n")
LOG_STR += (f"MAX_LIST_ELM Found, long list will be shortened to first {MAX_LIST_ELM} elements\n" if MAX_LIST_ELM else "Full List of casts and crew will be shown in imdb template, restrict them by adding a value to MAX_LIST_ELM\n")
LOG_STR += f"Your current IMDB template is {IMDB_TEMPLATE}"

PREMIUM_PIC = "https://te.legra.ph/file/cce073dc85850f2c63bfa.jpg"

# add your username 
USERNAME = "https://t.me/akshaychand08"

VR_COM_photo = "https://telegra.ph/file/a00c405a374d21ea7cfb7.jpg"

VR_LOG = int(environ.get('VR_LOG', '-1002199851318'))

TUTORIAL_LINK = "https://t.me/HoW_ToOpEn/42"

API = "16fe63613f0c168ed1cd899307368200c968b963"
SITE = "publicearn.com"

STREAM_API = "570bcebdb0b2b6080fc5b71f2e6cd1f68bf5494a"
STREAM_SITE = "publicearn.com"

IS_SHORTLINK = is_enabled((environ.get('IS_SHORTLINK', "True")), True)

SHORT_MODE = is_enabled((environ.get('SHORT_MODE', "True")), True)

# Add the ID of the update channel where new file updates will be sent
update_channel = "-1002148324943"

BIN_CHANNEL = int(os.environ.get("BIN_CHANNEL", "-1001815998255")) 
GEN_URL = os.environ.get("GEN_URL", "https://manojthe.github.io/?PIN=https://stream-manojthe.koyeb.app/") # https://example.com/



# If you want to send messages to the update channel, keep it as True
SEND_MSG = True

CAPTION_LANGUAGES = {
    "Eng": "English", "Hin": "Hindi", "Tam": "Tamil", "Tel": "Telugu", 
    "Mal": "Malayalam", "Kan": "Kannada", "Ben": "Bengali", 
    "Bho": "Bhojpuri", "Ban": "Bangla", "Mar": "Marathi", 
    "Pun": "Punjabi", "Guj": "Gujarati", "Kor": "Korean", 
    "Spa": "Spanish", "Fre": "French", "Ger": "German", 
    "Chi": "Chinese", "Ara": "Arabic", "Por": "Portuguese", 
    "Rus": "Russian", "Jap": "Japanese", "Odi": "Odia", 
    "Ass": "Assamese", "Urd": "Urdu"
}

# movie request 
REQ_GRP = int(environ.get('REQ_GRP', '-1001878519368'))
RQST_CHANNEL = int(environ.get('RQST_CHANNEL', '-1001682547846'))

# Welcome area
NEWGRP = environ.get('NEWGRP',"https://telegra.ph/file/80dc73a6d73bed659cda5.jpg")
GRP_LNK = environ.get('GRP_LNK',"https://t.me/iPapcornPrimeGroup")
CHNL_LNK = environ.get('CHNL_LNK',"https://t.me/arsOfficial10")

REPLACE_WORDS = (
    list(os.environ.get("REPLACE_WORDS").split(","))
    if os.environ.get("REPLACE_WORDS")
    else []
)

REPLACE_WORDS=["movies", "Movies", ",", "episode", "Episode", "episodes", "Episodes", "south indian", "South Indian", "web-series", "punjabi", "marathi", "gujrati", "combined", "!", "kro", "jaldi", "bhai", "Audio", "audio", "movi", "language", "Language", "Hollywood", "All", "all", "bollywood", "Bollywood", "South", "south", "hd", "karo", "Karo", "fullepisode", "please", "plz", "Please", "Plz", "send", "link", "Link", "#request", ":", "'", "full", "Full", "movie", "Movie", "dubb", "dabbed", "dubbed", "gujarati", "season", "Season", "web", "series", "Web", "Series", "webseries", "WebSeries", "upload", "HD", "Hd", "bhejo", "ful", "Send", "Bhejo"]

BLACKLIST_WORDS = (
    list(os.environ.get("BLACKLIST_WORDS").split(","))
    if os.environ.get("BLACKLIST_WORDS")
    else []
)
BLACKLIST_WORDS = ["[D&O]", "Telegram @  Studios", "[MM]", "[]", "[FC]", "[CF]", "LinkZz", "[DFBC]", "@malangmovie", "@AkPictureOfficial", "@mxplayer", "@New_Movie", "@Infinite_Movies2", "MM", "@R A R B G", "[F&T]", "[KMH]", "[DnO]", "[F&T]", "MLM", "@TM_LMO", "@x265_E4E", "@HEVC MoviesZ", "SSDMovies", "@MM Linkz", "[CC]", "@Mallu_Movies", "@DK Drama", "@luxmv_Linkz", "@Akw_links", "CK HEVC", "@Team_HDT", "[CP]", "www 1TamilMV men", "www TamilRockers", "@MM", "@mm", "[MW]", "@TN68 Linkzz", "@Clipmate_Movie", "[MASHOBUC]", "Official TheMoviesBoss", "www CineVez one", "www 7MovieRulz lv", "DCENIMAS", "Eliteflix Official", "@desimovies", "movieworldkdy", "www 1TamilMV vip"]

NEWGRP = environ.get('NEWGRP',"https://telegra.ph/file/80dc73a6d73bed659cda5.jpg")
CHNL_LNK = environ.get('CHNL_LNK',"https://t.me/arsOfficial10")


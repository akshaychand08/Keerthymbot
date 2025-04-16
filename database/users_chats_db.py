# https://github.com/odysseusmax/animated-lamp/blob/master/bot/database/database.py
import motor.motor_asyncio
from info import IS_SHORTLINK, SHORT_MODE, DATABASE_NAME, DATABASE_URI, IMDB, IMDB_TEMPLATE, MELCOW_NEW_USERS, P_TTI_SHOW_OFF, SINGLE_BUTTON, SPELL_CHECK_REPLY, PROTECT_CONTENT
import datetime
import pytz
from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient

my_client = MongoClient(DATABASE_URI)
mydb = my_client["filenames"]

async def add_name(user_id, filename):
    user_db = mydb[str(user_id)]
    user = {'_id': filename}
    
    # Check if the document already exists
    existing_user = user_db.find_one({'_id': filename})
    if existing_user is not None:
        return False
    
    # Attempt to insert the document
    try:
        user_db.insert_one(user)
        return True
    except DuplicateKeyError:
        return False
    
async def delete_all_msg(user_id):
    user_db = mydb[str(user_id)]
    user_db.delete_many({})
    


class Database:
    
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.grp = self.db.groups
        self.misc = self.db.misc
        self.verify_id = self.db.verify_id
        self.users = self.db.uersz
        self.shortlink_col = self.db.shortlinks
        self.collection = self.db["channel_messages"]  # Collection define kar diya

    async def save_channel_id(self, chat_id: int, msg_id: int):
        """Chat ID aur Message ID ko save karega, purana replace hoke naya add hoga."""
        await self.collection.update_one(
            {"chat_id": chat_id},  
            {"$set": {"msg_id": msg_id}},  
            upsert=True  
        )

    async def get_channel_id(self):
        """Latest Chat ID aur Message ID retrieve karega."""
        data = await self.collection.find_one({}, sort=[("_id", -1)])  # Latest entry fetch karega
        if data:
            return data["chat_id"], data["msg_id"]
        return None, None  


    
    async def save_tutorial_link(self, link):
        # Agar pehle se link exist nahi karta, toh save karega
        if not await self.shortlink_col.find_one({"type": "tutorial"}):
            await self.shortlink_col.insert_one({"type": "tutorial", "link": link})
        else:
            # Agar pehle se hai, toh link update karega
            await self.shortlink_col.update_one({"type": "tutorial"}, {"$set": {"link": link}})


    async def get_tutorial_link(self):
        # Link ko database se retrieve karta hai
        data = await self.shortlink_col.find_one({"type": "tutorial"})
        return data["link"] if data else None

    
    async def save_shortlink_data(self, api, site):
        data = {
            'api': api,
            'site': site
        }
        await self.shortlink_col.update_one(
            {'_id': 'shortlink_data'},
            {'$set': data},
            upsert=True
        )

    async def save_stream_data(self, stream_api, stream_site):
        data = {
            'stream_api': stream_api,
            'stream_site': stream_site
        }
        await self.shortlink_col.update_one(
            {'_id': 'stream_data'},
            {'$set': data},
            upsert=True
        )

    async def get_shortlink_data(self):
        return await self.shortlink_col.find_one({'_id': 'shortlink_data'})

    async def get_stream_data(self):
        return await self.shortlink_col.find_one({'_id': 'stream_data'})
        

    def new_user(self, id, name):
        return dict(
            id = id,
            name = name,
            ban_status=dict(
                is_banned=False,
                ban_reason="",
            ),
        )


    def new_group(self, id, title):
        return dict(
            id = id,
            title = title,
            chat_status=dict(
                is_disabled=False,
                reason="",
            ),
        )
    
    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)
    
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id':int(id)})
        return bool(user)
    
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count
    
    async def remove_ban(self, id):
        ban_status = dict(
            is_banned=False,
            ban_reason=''
        )
        await self.col.update_one({'id': id}, {'$set': {'ban_status': ban_status}})
    
    async def ban_user(self, user_id, ban_reason="No Reason"):
        ban_status = dict(
            is_banned=True,
            ban_reason=ban_reason
        )
        await self.col.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})

    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_reason=''
        )
        user = await self.col.find_one({'id':int(id)})
        if not user:
            return default
        return user.get('ban_status', default)

    async def get_all_users(self):
        return self.col.find({})
    

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})


    async def get_banned(self):
        users = self.col.find({'ban_status.is_banned': True})
        chats = self.grp.find({'chat_status.is_disabled': True})
        b_chats = [chat['id'] async for chat in chats]
        b_users = [user['id'] async for user in users]
        return b_users, b_chats
    


    async def add_chat(self, chat, title):
        chat = self.new_group(chat, title)
        await self.grp.insert_one(chat)
    

    async def get_chat(self, chat):
        chat = await self.grp.find_one({'id':int(chat)})
        return False if not chat else chat.get('chat_status')
    

    async def re_enable_chat(self, id):
        chat_status=dict(
            is_disabled=False,
            reason="",
            )
        await self.grp.update_one({'id': int(id)}, {'$set': {'chat_status': chat_status}})
        
    async def update_settings(self, id, settings):
        await self.grp.update_one({'id': int(id)}, {'$set': {'settings': settings}})
        
    
    async def get_settings(self, id):
        default = {
            'is_short': IS_SHORTLINK,
            'Short_mode': SHORT_MODE,
            'botpm': P_TTI_SHOW_OFF,
            'file_secure': PROTECT_CONTENT,
            'imdb': IMDB,
            'spell_check': SPELL_CHECK_REPLY,
            'welcome': MELCOW_NEW_USERS,
            'template': IMDB_TEMPLATE
        }
        chat = await self.grp.find_one({'id':int(id)})
        if chat:
            return chat.get('settings', default)
        return default
    

    async def disable_chat(self, chat, reason="No Reason"):
        chat_status=dict(
            is_disabled=True,
            reason=reason,
            )
        await self.grp.update_one({'id': int(chat)}, {'$set': {'chat_status': chat_status}})
    

    async def total_chat_count(self):
        count = await self.grp.count_documents({})
        return count
    

    async def get_all_chats(self):
        return self.grp.find({})


    async def get_db_size(self):
        return (await self.db.command("dbstats"))['dataSize']

#added single verify 

    async def get_notcopy_user(self, user_id):
        user_id = int(user_id)

        user = await self.misc.find_one({"user_id": user_id})
        ist_timezone = pytz.timezone('Asia/Kolkata')

        if not user:
            res = {
                "user_id": user_id,
                "last_verified": datetime.datetime(2020, 5, 17, 0, 0, 0, tzinfo=ist_timezone),
            } 
            user = await self.misc.insert_one(res) 
            user = await self.misc.find_one({"user_id": user_id}) 
        return user

    async def update_notcopy_user(self, user_id, value:dict):
        user_id = int(user_id)
        myquery = {"user_id": user_id}
        newvalues = { "$set": value }
        await self.misc.update_one(myquery, newvalues)

    async def is_user_verified(self, user_id):
        user = await self.get_notcopy_user(user_id)

        try:
            pastDate = user["last_verified"]
        except Exception:
            user = await self.get_notcopy_user(user_id)
            pastDate = user["last_verified"]

        ist_timezone = pytz.timezone('Asia/Kolkata')
        pastDate = pastDate.astimezone(ist_timezone)
        current_time = datetime.datetime.now(tz=ist_timezone)

        seconds_since_midnight = (current_time - datetime.datetime(current_time.year, current_time.month, current_time.day, 0, 0, 0, tzinfo=ist_timezone)).total_seconds()

        # Calculate the difference between the two times
        time_diff = current_time - pastDate

        # Get the total number of seconds between the two times
        total_seconds = time_diff.total_seconds()
        return total_seconds <= seconds_since_midnight

    
    async def create_verify_id(self, user_id: int, hash):
        res = {"user_id": user_id, "hash":hash, "verified":False}
        return await self.verify_id.insert_one(res)

    async def get_verify_id_info(self, user_id: int, hash):
        return await self.verify_id.find_one({"user_id": user_id, "hash": hash})

    async def dl_verify_id_info(self):
        await self.verify_id.drop()        
    
    
    async def update_verify_id_info(self, user_id, hash, value: dict):
        myquery = {"user_id": user_id, "hash": hash}
        newvalues = { "$set": value }
        return await self.verify_id.update_one(myquery, newvalues)

# premium    
    async def get_user(self, user_id):
        user_data = await self.users.find_one({"id": user_id})
        return user_data
    async def update_user(self, user_data):
        await self.users.update_one({"id": user_data["id"]}, {"$set": user_data}, upsert=True)

    async def has_premium_access(self, user_id):
        user_data = await self.get_user(user_id)
        if user_data:
            expiry_time = user_data.get("expiry_time")
            if expiry_time is None:
                # User previously used the free trial, but it has ended.
                return False
            elif isinstance(expiry_time, datetime.datetime) and datetime.datetime.now() <= expiry_time:
                return True
            else:
                await self.users.update_one({"id": user_id}, {"$set": {"expiry_time": None}})
        return False
    async def update_user(self, user_data):
        await self.users.update_one({"id": user_data["id"]}, {"$set": user_data}, upsert=True)

    async def update_one(self, filter_query, update_data):
        try:
            # Assuming self.client and self.users are set up properly
            result = await self.users.update_one(filter_query, update_data)
            return result.matched_count == 1
        except Exception as e:
            print(f"Error updating document: {e}")
            return False

    async def get_expired(self, current_time):
        expired_users = []
        if data := self.users.find({"expiry_time": {"$lt": current_time}}):
            async for user in data:
                expired_users.append(user)
        return expired_users


    async def remove_premium_access(self, user_id):
        return await self.update_one(
            {"id": user_id}, {"$set": {"expiry_time": None}}
        ) 

    async def get_premium_users(self):
        current_time = datetime.datetime.now()
        premium_users = []
        async for user in self.users.find({"expiry_time": {"$gt": current_time}}):
            premium_users.append(user)
        return premium_users

db = Database(DATABASE_URI, DATABASE_NAME)

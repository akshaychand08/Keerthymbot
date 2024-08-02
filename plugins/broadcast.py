from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid
import datetime
import time, os, asyncio, logging
from database.users_chats_db import db
from info import ADMINS
from utils import broadcast_messages
from contextlib import suppress

logging.basicConfig(level=logging.INFO)

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
async def verupikkals(bot, message):
    cursor = await db.get_all_users()  # Await the coroutine to get the cursor
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text='Broadcasting your messages...'
    )

    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    blocked = 0
    deleted = 0
    failed = 0
    success = 0

    sem = asyncio.Semaphore(25)  # limit the number of concurrent tasks to 25

    async def run_task(user):
        async with sem:
            return await broadcast_func(user, b_msg)

    users = await cursor.to_list(length=None)  # Convert the cursor to a list of users

    tasks = [asyncio.create_task(run_task(user)) for user in users]

    async def update_status():
        nonlocal done, blocked, deleted, failed, success
        while not all(task.done() for task in tasks):
            with suppress(Exception):
                await sts.edit(f"Broadcast in progress:\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")
            await asyncio.sleep(30)  # Update status every 30 seconds

    # Run the update_status coroutine concurrently with the broadcasting
    update_task = asyncio.create_task(update_status())

    try:
        for res in await asyncio.gather(*tasks, return_exceptions=True):
            if isinstance(res, Exception):
                logging.error(f"Error in task: {res}")
                continue
            success1, blocked1, deleted1, failed1, done1 = res
            done += done1
            blocked += blocked1
            deleted += deleted1
            failed += failed1
            success += success1
    finally:
        # Ensure the update_status task finishes
        await update_task

    time_taken = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts.edit(f"Broadcast Completed:\nCompleted in {time_taken} seconds.\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")

async def broadcast_func(user, b_msg):
    success, blocked, deleted, failed, done = 0, 0, 0, 0, 0
    try:
        pti, sh = await broadcast_messages(int(user['id']), b_msg)
        if pti:
            success = 1
        elif pti == False:
            if sh == "Blocked":
                blocked = 1
            elif sh == "Deleted":
                deleted = 1
            elif sh == "Error":
                failed = 1
        done = 1
    except FloodWait as e:
        logging.warning(f"FloodWait: Sleeping for {e.x} seconds")
        await asyncio.sleep(e.x)
    except InputUserDeactivated:
        deleted = 1
    except UserIsBlocked:
        blocked = 1
    except PeerIdInvalid:
        failed = 1
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        failed = 1
    return success, blocked, deleted, failed, done

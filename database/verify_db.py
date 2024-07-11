from datetime import timedelta, datetime
from pymongo import MongoClient
import os
from info import DATABASE_NAME, DATABASE_URI
from os import environ
import pytz

client = MongoClient(DATABASE_URI)
datab = client[f"{DATABASE_NAME}"]
db = datab.verifications
kolkata_timezone = pytz.timezone('Asia/Kolkata')

def save_verification(user_id):
    now = datetime.now(pytz.timezone('Asia/Kolkata'))
    verification = {"user_id": user_id, "verified_at": now}
    collection = db["verifications"]
    collection.insert_one(verification)

def get_verifications_count(time_period):
    collection = db[f"verifications"]
    if time_period == 'today':
        start_datetime = datetime.now(kolkata_timezone).replace(hour=0, minute=0, second=0, microsecond=0)
        end_datetime = datetime.now(kolkata_timezone)
    elif time_period == 'yesterday':
        start_datetime = datetime.now(kolkata_timezone).replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        end_datetime = start_datetime + timedelta(days=1)
    elif time_period == 'this_week':
        start_datetime = datetime.now(kolkata_timezone).replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=datetime.now(kolkata_timezone).weekday())
        end_datetime = datetime.now(kolkata_timezone)
    elif time_period == 'this_month':
        start_datetime = datetime.now(kolkata_timezone).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_datetime = datetime.now(kolkata_timezone)
    else:
        raise ValueError("Invalid time period")
    count = collection.count_documents({'verified_at': {'$gt': start_datetime, '$lt': end_datetime}})
    return count

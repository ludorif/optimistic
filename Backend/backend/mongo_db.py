#  Copyright (c) 2025 Ludovic Riffiod
import json
import os
import uuid

from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure
from starlette import status

from . import model

uri = os.environ["MONGO_DB_URI"]

mongo_client = MongoClient(uri)
optimistic_db = mongo_client["optimistic"]
events_column = optimistic_db["memory"]
winners_column = optimistic_db["winners"]
summary_column = optimistic_db["summary"]
planets_column = optimistic_db["planets"]


def get_all_events_story():
    return events_column.find({}, {"content": 1})


def get_health():
    try:
        # The ismaster command is cheap and does not require auth.
        mongo_client.admin.command('ismaster')
    except ConnectionFailure:
        print("Server not available")

def update_summary(planet, summary_content):
    try:
        summary_column.update_one({"planet": planet}, {"$set": {"content": summary_content}},  upsert=True)
    except Exception as e:
        print(e)

def get_summary(planet):
    summary_content = summary_column.find_one({"planet": planet})['content']
    summary_content = summary_content.replace("\\", "")
    summary_content = summary_content.replace("\"\"\"", "")
    return json.dumps(summary_content)



#  Copyright (c) 2025 Ludovic Riffiod
import json
import os

from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure

uri = os.environ["MONGO_DB_URI"]

mongo_client = MongoClient(uri)
optimistic_db = mongo_client["optimistic"]
events_column = optimistic_db["memory"]
winners_column = optimistic_db["winners"]




def get_events(date):
    if date == "":
        result = list(events_column.find())
    else:
        result = list(events_column.find({"date": date}).sort('votes', DESCENDING))

    return json.dumps(result)




def get_dates():
    events = events_column.find({}, {"date": 1, "_id":1}).distinct("date")
    return json.dumps(list(events))

async def add_event_to_world(json_to_add):
    try:
        events_column.insert_one(json_to_add)
    except Exception as e:
        print(e)

def increase_vote(event_id):
    try:
        result = events_column.update_one({"_id": event_id}, {"$inc": {"votes": 1}})
        print(result.modified_count)
    except Exception as e:
        print(e)

def get_winners():
    result = list(winners_column.find())
    return json.dumps(result)

def define_winner(date):
    events_of_date = events_column.find({"date": date})

    winner = events_of_date[0]

    for event in events_of_date:
        if event["votes"] > winner["votes"]:
            winner = event

    winners_column.insert_one(winner)

def get_health():
    try:
        # The ismaster command is cheap and does not require auth.
        mongo_client.admin.command('ismaster')
    except ConnectionFailure:
        print("Server not available")
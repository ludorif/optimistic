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


def check_current_events(date, client_ip):
    number_of_events = len(list(events_column.find({"date": date})))
    user_already_participated = len(list(events_column.find({"date": date, "client_ip":client_ip}))) > 0
    return number_of_events, user_already_participated

def get_events(date):
    if date == "":
        result = list(events_column.find())
    else:
        pipeline = [
            {"$match": {"date": date}},  # filter by date
            {"$addFields": {"array_size": {"$size": "$votes"}}},  # compute length
            {"$sort": {"array_size": DESCENDING}}  # sort by that length
        ]
        result = list(events_column.aggregate(pipeline))

    return json.dumps(result)




def get_dates():
    events = events_column.find({}, {"date": 1, "_id":1}).distinct("date")
    return json.dumps(list(events))

async def add_event_to_world(json_to_add):
    try:
        events_column.insert_one(json_to_add)
    except Exception as e:
        print(e)

def increase_vote(event_id, client_ip):
    votes_ip_list = events_column.find_one({"_id": event_id})["votes"]
    if client_ip in votes_ip_list:
        return False

    try:
        events_column.update_one({"_id": event_id}, { "$push": { "votes": client_ip } })
        return True
    except Exception as e:
        print(e)
        return False

def get_winners():
    result = list(winners_column.find())
    return json.dumps(result)

def define_winner(date):
    events_of_date = events_column.find({"date": date})

    winner = events_of_date[0]

    for event in events_of_date:
        if len(event["votes"]) > len(winner["votes"]):
            winner = event

    winners_column.insert_one(winner)

def get_health():
    try:
        # The ismaster command is cheap and does not require auth.
        mongo_client.admin.command('ismaster')
    except ConnectionFailure:
        print("Server not available")
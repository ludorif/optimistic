#  Copyright (c) 2025 Ludovic Riffiod
import json
import os

from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure
from starlette import status

uri = os.environ["MONGO_DB_URI"]

mongo_client = MongoClient(uri)
optimistic_db = mongo_client["optimistic"]
events_column = optimistic_db["memory"]
winners_column = optimistic_db["winners"]
summary_column = optimistic_db["summary"]

def check_current_events(date, client_uuid):
    number_of_events = len(list(events_column.find({"date": date})))
    user_already_participated = len(list(events_column.find({"date": date, "client_uuid":client_uuid}))) > 0
    return number_of_events, user_already_participated

def get_all_events_story():
    return events_column.find({}, {"content": 1})

def get_events(date):
    if date == "":
        result = list(events_column.find())
    else:
        pipeline = [
            {"$match": {"date": date}},  # filter by date
            {"$addFields": {"array_size": {"$size": "$votes"}}},  # compute length
            {"$sort": {"array_size": ASCENDING}}  # sort by that length
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

def increase_vote(event_id, client_uuid):
    event = events_column.find_one({"_id": event_id})
    if client_uuid == event["client_uuid"]:
        return status.HTTP_403_FORBIDDEN, "You can't vote for your own event"

    votes_ip_list = event["votes"]
    if client_uuid in votes_ip_list:
        return status.HTTP_403_FORBIDDEN, "You already voted for this event"

    try:
        events_column.update_one({"_id": event_id}, { "$push": { "votes": client_uuid } })
        return status.HTTP_200_OK, "Vote added"
    except Exception as e:
        print(e)
        return status.HTTP_403_FORBIDDEN,e

def get_winners():
    result = list(winners_column.find())
    return json.dumps(result)

def define_winner(date):
    events_of_date = list(events_column.find({"date": date}))

    if len(events_of_date) == 0:
        print("no events")
        return False

    winner = events_of_date[0]

    for event in events_of_date:
        if len(event["votes"]) > len(winner["votes"]):
            winner = event

    winners_column.insert_one(winner)
    return True

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


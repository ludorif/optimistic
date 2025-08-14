import json
from datetime import datetime, timezone
from helper import get_utc_day

from pymongo import MongoClient

uri = "mongodb+srv://testuser:hgGWCIOcm1z7X9zM@cluster0.zrojvuw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

my_client = MongoClient(uri)
mydb = my_client["optimistic"]
my_col = mydb["memory"]


def db_define_winner(date):
    events_of_date = my_col.find({"date": date})

    winner = events_of_date[0]

    for event in events_of_date:
        if event["votes"] > winner["votes"]:
            winner = event

    mydb["winners"].insert_one(winner)
    print("winner: ", winner)


def get_all_events(date):
    if date == "all_dates":
        result = {"events": list(my_col.find()),
                  "winners": list(mydb["winners"].find())}
        print(result)

    else:
        result = my_col.find({"date": date})

    return result

def get_events_to_vote():
    events = my_col.find({"date": get_utc_day()})
    return list(events)

def db_get_dates():
    events = my_col.find({}, {"date": 1, "_id":1}).distinct("date")
    return list(events)

async def add_event_to_world(jsonToAdd):
    try:
        my_col.insert_one(jsonToAdd)
    except Exception as e:
        print(e)

def increase_vote_db(event_id):
    try:
        result = my_col.update_one({"_id": event_id}, {"$inc": {"votes": 1}})
        print(result.modified_count)
    except Exception as e:
        print(e)
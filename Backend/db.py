import json
from os.path import devnull

from pymongo import MongoClient

uri = "mongodb+srv://testuser:hgGWCIOcm1z7X9zM@cluster0.zrojvuw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

my_client = MongoClient(uri)
mydb = my_client["optimistic"]
my_col = mydb["memory"]

def get_all_events():
    events = my_col.find()
    return list(events)

async def add_event_to_world(jsonToAdd):
    try:
        my_col.insert_one(jsonToAdd)
    except Exception as e:
        print(e)
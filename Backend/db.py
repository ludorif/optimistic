from flask import Flask
from pymongo import MongoClient

uri = "mongodb+srv://testuser:hgGWCIOcm1z7X9zM@cluster0.zrojvuw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
myclient = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    mydb = myclient["optimistic"]

    mycol = mydb["test"]

    mydict = {"name": "John2", "address2": "Highway 372"}

    x = mycol.insert_one(mydict)

    print(mycol.find_one())

    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
import os

from app import app
from pymongo import MongoClient
from flask import Flask, jsonify, request
# from flask_pymongo import PyMongo
import pprint
from bson.objectid import ObjectId

# pymongo
client = MongoClient("mongodb+srv://dbUser:user000@cluster0.1t5ad.mongodb.net/ourDb?retryWrites=true&w=majority")
db = client.ourDb
notifies = db["notifies"]

# flask-_pymongo
# app.config["MONGO_URI"] = "mongodb+srv://dbUser:user000@cluster0.1t5ad.mongodb.net/ourDb?retryWrites=true&w=majority"
# mongo = PyMongo(app)


@app.route("/")
def hello_world(): 
    db.list_collection_names()
    print(notifies)
    return "<p>Hello, baruch!</p>"

@app.route("/notify", methods=['GET', 'POST'])
def notify():
    # count = notifies.count_documents({})
    # print(count)
    # note = notifies.find_one({"title":"Moon running"})
    # note["_id"] = str(note["_id"])
    # # all_notes = notifies.find()
    # # print (list(all_notes))
    # print(note)
    # return jsonify(note["title"])
    if request.method == 'POST':
        request_data = request.get_json()
        title = request_data['title']
        running = request_data['running']
        note = {
            "title": title,
            "running": running
        }
        created_note_id = notifies.insert_one(note).inserted_id
        print(ObjectId(created_note_id))
        this_note = notifies.find_one({"_id": ObjectId(created_note_id)})
        print(this_note)
        this_note["_id"] = str(this_note["_id"])
        return this_note








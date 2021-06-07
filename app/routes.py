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
users = db["users"]


# flask-_pymongo
# app.config["MONGO_URI"] = "mongodb+srv://dbUser:user000@cluster0.1t5ad.mongodb.net/ourDb?retryWrites=true&w=majority"
# mongo = PyMongo(app)


@app.route("/")
def hello_world(): 
    db.list_collection_names()
    print(notifies)
    return "<p>Hello, baruch!</p>"

@app.route("/notify", methods=['GET'])
def notify():
    count = notifies.count_documents({})
    print(count)
    note = notifies.find_one({"title":"Moon running"})
    note["_id"] = str(note["_id"])
    # all_notes = notifies.find()
    # print (list(all_notes))
    print(note)
    return jsonify(note["title"])



@app.route("/users", methods=['GET', 'POST'])
def get_users():
    if request.method == 'POST':
        request_data = request.get_json()
        email = request_data['email']
        first_name = request_data['first_name']
        last_name = request_data['last_name']
        picture = request_data['picture']
        sports = request_data['sports']
        telephone = request_data['telephone']

        user = {
            'email': email,
            "first_name": first_name,
            "last_name": last_name,
            'picture': picture,
            "sports": sports,
            'telephone': telephone
        }
        print(request_data)
        # user = {"first_name": request.form.}
        users.insert_one(user)
        return 'post'
    else:
        count = users.count_documents({})
        print(count)
        user = users.find_one({"email":"nastia@abc.com"})
        user["_id"] = str(user["_id"])
        for sport in user["sports"]:
            sport["_id"] = str(sport["_id"])
            sport["running"]["distance"] = str(sport["running"]["distance"])
            print(sport["running"])
    
        print(user)
        return jsonify(user)
import os
from app import app
from pymongo import MongoClient
from flask import Flask, jsonify, request, Response, json
import pprint
from bson.objectid import ObjectId
from bson.json_util import dumps
from passlib.hash import pbkdf2_sha256
import jwt

client = MongoClient("mongodb+srv://dbUser:user000@cluster0.1t5ad.mongodb.net/ourDb?retryWrites=true&w=majority")
db = client.ourDb
users = db["users"]

@app.route("/users", methods=['GET', 'POST'])
def get_users():
    # create a user
    if request.method == 'POST':
        request_data = request.get_json()
        email = request_data['email']
        first_name = request_data['first_name']
        last_name = request_data['last_name']
        picture = request_data['picture']
        sports = request_data['sports']
        telephone = request_data['telephone']
        password = request_data['password']

        hash = pbkdf2_sha256.hash(password)

        user = {
            'email': email,
            "first_name": first_name,
            "last_name": last_name,
            'picture': picture,
            "sports": sports,
            'telephone': telephone,
            'password_hash': hash
        }
        users.insert_one(user)
        
        return Response(
        response=hash,
        status=200,
        mimetype='application/json')

    # get all users
    else:
        cur_users = users.find()
        list_cur = list(cur_users)
        json_data = dumps(list_cur)

        return Response(
        response=json_data,
        status=200,
        mimetype='application/json')

#get user by id
@app.route("/users/<string:userid>", methods=['GET'])
def get_user_by_id(userid):
    objInstance = ObjectId(userid)
    this_user = users.find_one({"_id": objInstance})
    this_user["_id"] = str(this_user["_id"])
    return Response(
        response=json.dumps(this_user),
        status=200,
        mimetype='application/json')

#login user
def create_token(user_id):
    encoded_jwt = jwt.encode({"user_id": user_id}, "secret", algorithm="HS256")
    return encoded_jwt

@app.route("/users/login", methods=['POST'])
def login():
    request_data = request.get_json()
    email = request_data['email']
    password = request_data['password']
    
    user = users.find_one({'email': email})
    if user == None:
        return Response(response='User not found with this email', status=404)
    else:
        user_id = (str(user["_id"]))
        if pbkdf2_sha256.verify(password, user["password_hash"]) == True:
            encoded_jwt = create_token(user_id)
            return Response(response=encoded_jwt, status=200)
        else: 
            return Response(response='Inserted password does not match this E-mail account', status=404)
 

    

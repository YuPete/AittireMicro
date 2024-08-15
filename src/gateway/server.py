#gateway service's server.py


import os, gridfs, pika, json #grid fs allow larger files in mongodb 
#pika allows us to interface with queue (rabbitmq to store messages)
from flask import Flask, request
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util

server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"

mongo = PyMongo(server) #manages MongoDB connections for flask app

fs = gridfs.GridFS(mongo.db) 
#GridfFS allow us to store/transmit files larger than 16mb by breaking them up into shards 
#Grid FS is composed of two parts: 1. Chunks 2. Metadata(for how to reconstruct)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq")) #makes connection with rabbitmq synchronous ; rabbitmq references rabbitmq host
channel = connection.channel()

@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token 
    else:
        return err
    
@server.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)

    access = json.loads(access) #converts json string to python object so we can work with it 

    if access["admin"]:
        if len(request.files) > 1 or len(request.files) < 1:
            return "exactly 1 file required",400
        
        for _, f in request.files.items():
            err = util.upload(f,fs,channel, access)

            if err:
                return err
            
        return "success!", 200
    else:
        return "not authorized", 401
    
@server.route("/download", methods=["GET"])
def download():
    pass

if __name__=="__main__":
    server.run(host="0.0.0.0", port=8080)
    
    
        

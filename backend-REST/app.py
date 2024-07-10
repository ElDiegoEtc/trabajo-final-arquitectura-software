import os
import json

from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)
# os.environ['MONGODB_HOSTNAME'] es el container_name del container MongoDB, entregado al REST-server mediante la variable de entorno definida en ./backend-REST/Dockerfile
client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'] + ':27017')
db = client['ads_db']
collection = db['ads_collection']

@app.route('/', methods=['GET'])
def hello():
    return 'getttt'

@app.route('/', methods=['POST'])
def hello_post():
    req_json = request.get_json()
    # print(req_json + '\n')
    # print("Printed out POST request's JSON data")
    collection.insert_one(json.loads(req_json))
    return "postttt"

if __name__ == "__main__":
    app.run()
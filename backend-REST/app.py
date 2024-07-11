import os
import json
import websockets
import asyncio

from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)
# os.environ['MONGODB_HOSTNAME'] es el container_name del container MongoDB, entregado al REST-server mediante la variable de entorno definida en ./backend-REST/Dockerfile
client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'] + ':27017')
db = client['ads_db']
collection = db['ads_collection']

messages = 0 
connected = []

@app.route('/', methods=['GET'])
def hello():
    return 'getttt'

@app.route('/', methods=['POST'])
def hello_post():
    global messages
    messages += 1
    req_json = request.get_json()
    # print(req_json + '\n')
    # print("Printed out POST request's JSON data")
    websockets.broadcast(connected, f"Se ingresó un registro mediante API REST, con el mensaje {req_json}, total de mensajes {messages}") 
    collection.insert_one(json.loads(req_json))
    return "postttt"

async def handler(websocket: websockets.WebSocketServerProtocol):
    connected.append(websocket)
    await websocket.wait_closed()
    connected.remove(websocket)

async def ws_main():
    async with websockets.serve(handler, "", 8068):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(ws_main())
    app.run()

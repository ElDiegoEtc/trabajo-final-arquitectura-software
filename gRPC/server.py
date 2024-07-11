from concurrent import futures
import grpc
import protofile_pb2
import os
import protofile_pb2_grpc
from pymongo import MongoClient
from google.protobuf.timestamp_pb2 import Timestamp
import datetime

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'] + ':27017')
db = client['grpc_db']
collection = db['grpc_coleccion']

class MessageService(protofile_pb2_grpc.MessageServiceServicer):
    def __init__(self):
        self.messages = []

    def StoreMessage(self, request, context):
        # Guarda mensaje en MongoDB con sus claves
        message_doc = {
            'any_string': request.any_string,
            'datetime': request.datetime.ToDatetime(),
            'system': request.system,
            'status': request.status
        }
        result = collection.insert_one(message_doc)
        print(f"Mensaje ID: {result.inserted_id}")
        return protofile_pb2.MessageResponse(status="Message stored")

    def GetMessages(self, request, context):
        # Obtener mensajes de MongoDB 
        messages = collection.find({})
        message_list = []
        for msg in messages:
            timestamp = Timestamp()
            timestamp.FromDatetime(msg['datetime'])
            message_list.append(protofile_pb2.MessageRequest(
                any_string=msg['any_string'],
                datetime=timestamp,
                system=msg['system'],
                status=msg['status']
            ))
        return protofile_pb2.MessageList(messages=message_list)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    protofile_pb2_grpc.add_MessageServiceServicer_to_server(MessageService(), server)
    server.add_insecure_port('[::]:50051')
    print("Server listening on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

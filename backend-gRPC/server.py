from concurrent import futures
import grpc
import protofile_pb2
import protofile_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp
import datetime

class MessageService(protofile_pb2_grpc.MessageServiceServicer):
    def __init__(self):
        self.messages = []

    def StoreMessage(self, request, context):
        self.messages.append(request)
        return protofile_pb2.MessageResponse(status="Message stored")

    def GetMessages(self, request, context):
        return protofile_pb2.MessageList(messages=self.messages)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    protofile_pb2_grpc.add_MessageServiceServicer_to_server(MessageService(), server)
    server.add_insecure_port('[::]:50051')
    print("Server listening on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

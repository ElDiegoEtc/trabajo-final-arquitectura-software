import grpc
import protofile_pb2
import protofile_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp
import datetime

def format_datetime(dt):
    # Formatear datetime en el formato deseado
    return dt.strftime("%Y-%m-%d %H:%M:%S.%f")

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = protofile_pb2_grpc.MessageServiceStub(channel)
        
        # Crear un objeto Timestamp desde current_time
        current_time = datetime.datetime.now()
        timestamp = Timestamp()
        timestamp.FromDatetime(current_time)
        
        request = protofile_pb2.MessageRequest(
            any_string="Hola gRPC",
            datetime=timestamp,  # Pasar el objeto Timestamp aquí
            grpc_string="gRPC",
            status="Active"
        )
        
        response = stub.StoreMessage(request)
        print("StoreMessage response:", response.status)

        response = stub.GetMessages(protofile_pb2.Empty())
        for msg in response.messages:
            formatted_datetime = format_datetime(msg.datetime.ToDatetime())
            print(f"texto={msg.any_string}, fecha-hora={formatted_datetime}, sistema={msg.grpc_string}, estado={msg.status}")

if __name__ == '__main__':
    run()

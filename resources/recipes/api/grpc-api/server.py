"""gRPC server and client for the Greeter service.

Generate stubs first:
    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto
"""

import grpc
from concurrent import futures

import service_pb2
import service_pb2_grpc


class GreeterServicer(service_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return service_pb2.HelloResponse(message=f"Hello, {request.name}!")

    def StreamGreetings(self, request_iterator, context):
        for req in request_iterator:
            yield service_pb2.HelloResponse(message=f"Streamed: {req.name}")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server listening on :50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()

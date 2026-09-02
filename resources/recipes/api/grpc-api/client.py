"""gRPC client for the Greeter service.

Generate stubs first:
    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto
"""

import grpc

import service_pb2
import service_pb2_grpc


def main():
    channel = grpc.insecure_channel("localhost:50051")
    stub = service_pb2_grpc.GreeterStub(channel)

    # Unary call
    response = stub.SayHello(service_pb2.HelloRequest(name="World"))
    print(f"Unary: {response.message}")

    # Streaming call
    def request_generator():
        yield service_pb2.HelloRequest(name="Alice")
        yield service_pb2.HelloRequest(name="Bob")
        yield service_pb2.HelloRequest(name="Charlie")

    print("Streaming responses:")
    for response in stub.StreamGreetings(request_generator()):
        print(f"  {response.message}")


if __name__ == "__main__":
    main()

"""gRPC UserService client — companion to
https://stackpractices.com/guides/grpc-microservices-guide/

Requires: pip install grpcio
Run while server.py is up:  python client.py
"""
import grpc

import user_service_pb2
import user_service_pb2_grpc


def main():
    channel = grpc.insecure_channel("localhost:50051")  # dev only — TLS in prod
    stub = user_service_pb2_grpc.UserServiceStub(channel)

    # Unary call with a 5s deadline — always set one
    response = stub.GetUser(
        user_service_pb2.GetUserRequest(user_id="1"), timeout=5
    )
    print(f"GetUser: {response.name} <{response.email}>")

    # Server streaming
    for user in stub.ListUsers(user_service_pb2.ListUsersRequest(page_size=10)):
        print(f"ListUsers: {user.name}")

    # TLS production variant:
    # credentials = grpc.ssl_channel_credentials()
    # channel = grpc.secure_channel('user-service:50051', credentials)


if __name__ == "__main__":
    main()

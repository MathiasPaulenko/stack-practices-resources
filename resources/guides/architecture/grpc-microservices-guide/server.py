"""gRPC UserService server with health check — companion to
https://stackpractices.com/guides/grpc-microservices-guide/

Requires: pip install grpcio grpcio-tools grpcio-health-checking
Run after generating stubs:  python server.py
"""
from concurrent import futures
import grpc
from grpc_health.v1 import health, health_pb2_grpc, health_pb2

import user_service_pb2
import user_service_pb2_grpc

USERS = {
    "1": {"name": "Ada Lovelace", "email": "ada@example.com"},
    "2": {"name": "Grace Hopper", "email": "grace@example.com"},
}


class UserServiceServicer(user_service_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        user = USERS.get(request.user_id)
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return user_service_pb2.User()
        return user_service_pb2.User(
            user_id=request.user_id, name=user["name"], email=user["email"]
        )

    def ListUsers(self, request, context):
        for uid, user in list(USERS.items())[: request.page_size or 10]:
            yield user_service_pb2.User(
                user_id=uid, name=user["name"], email=user["email"]
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_service_pb2_grpc.add_UserServiceServicer_to_server(
        UserServiceServicer(), server
    )
    health_pb2_grpc.add_HealthServicer_to_server(health.HealthServicer(), server)
    server.add_insecure_port("[::]:50051")  # dev only — TLS in production
    server.start()
    print("UserService listening on :50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()

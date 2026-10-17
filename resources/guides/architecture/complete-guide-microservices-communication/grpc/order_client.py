import grpc
import order_pb2
import order_pb2_grpc

def get_order(order_id: str) -> order_pb2.OrderResponse:
    with grpc.insecure_channel("order-service:50051") as channel:
        stub = order_pb2_grpc.OrderServiceStub(channel)
        return stub.GetOrder(order_pb2.OrderRequest(order_id=order_id))

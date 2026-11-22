// gRPC service-to-service client for the orders service.
// Companion to https://stackpractices.com/recipes/microservices-communication/
// Requires: @grpc/grpc-js, @grpc/proto-loader, tsx (see package.json).
// Needs an OrderService gRPC server at ORDERS_GRPC_ADDR (default orders-service:50051).

import { credentials, makeClientConstructor } from '@grpc/grpc-js';
import { loadPackageDefinition } from '@grpc/grpc-js';
import { loadSync } from '@grpc/proto-loader';

interface OrderItem {
  sku: string;
  qty: number;
}

interface Order {
  id: string;
  items: OrderItem[];
  status: string;
}

const packageDefinition = loadSync('proto/orders.proto', {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});

const protoDescriptor = loadPackageDefinition(packageDefinition);
const OrderServiceClient = makeClientConstructor(
  (protoDescriptor as any).orders.OrderService.service,
  'OrderService'
);

export class OrderGrpcClient {
  private client: any;

  constructor(address: string = 'orders-service:50051') {
    this.client = new OrderServiceClient(address, credentials.createInsecure());
  }

  getOrder(orderId: string): Promise<Order> {
    return new Promise((resolve, reject) => {
      this.client.getOrder({ id: orderId }, (err: Error | null, response: Order) => {
        if (err) reject(err);
        else resolve(response);
      });
    });
  }

  createOrder(items: OrderItem[]): Promise<Order> {
    return new Promise((resolve, reject) => {
      this.client.createOrder({ items }, (err: Error | null, response: Order) => {
        if (err) reject(err);
        else resolve(response);
      });
    });
  }
}

// Example invocation:
//   const client = new OrderGrpcClient(process.env.ORDERS_GRPC_ADDR);
//   console.log(await client.getOrder('ord_123'));

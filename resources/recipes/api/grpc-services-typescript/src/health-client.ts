import * as grpc from '@grpc/grpc-js';
import { service as healthServiceDefinition } from 'grpc-health-check';

const HealthClient = grpc.makeClientConstructor(
  healthServiceDefinition as any,
  'grpc.health.v1.Health'
);

const client = new (HealthClient as any)('localhost:50051', grpc.credentials.createInsecure());

client.check({ service: 'users.UserService' }, (err: any, response: any) => {
  if (err) {
    console.error('Health check failed:', err.message);
    process.exit(1);
  }
  console.log('Health status:', response.status);
});

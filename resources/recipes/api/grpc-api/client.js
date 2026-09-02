// gRPC client (Node.js with @grpc/grpc-js)
// Run: node client.js

const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

const packageDefinition = protoLoader.loadSync('service.proto', {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});
const proto = grpc.loadPackageDefinition(packageDefinition).greeter;

const client = new proto.Greeter('localhost:50051', grpc.credentials.createInsecure());

// Unary call
client.sayHello({ name: 'World' }, (err, response) => {
  if (err) {
    console.error('Unary error:', err);
    return;
  }
  console.log('Unary:', response.message);

  // Streaming call
  const stream = client.streamGreetings();
  ['Alice', 'Bob', 'Charlie'].forEach((name) => stream.write({ name }));
  stream.end();

  stream.on('data', (response) => {
    console.log('Streaming:', response.message);
  });
  stream.on('end', () => {
    console.log('Stream complete');
  });
});

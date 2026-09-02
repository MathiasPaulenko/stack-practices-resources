// gRPC server (Node.js with @grpc/grpc-js)
// Run: node server.js

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

function sayHello(call, callback) {
  callback(null, { message: `Hello, ${call.request.name}!` });
}

function streamGreetings(call) {
  call.on('data', (req) => {
    call.write({ message: `Streamed: ${req.name}` });
  });
  call.on('end', () => call.end());
}

const server = new grpc.Server();
server.addService(proto.Greeter.service, { sayHello, streamGreetings });
server.bindAsync('0.0.0.0:50051', grpc.ServerCredentials.createInsecure(), (err) => {
  if (err) {
    console.error(err);
    return;
  }
  console.log('Server listening on :50051');
});

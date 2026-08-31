import * as fs from 'fs';
import * as path from 'path';
import * as grpc from '@grpc/grpc-js';
import { UserServiceClient } from './generated/user_grpc_pb';
import { GetUserRequest, ListUsersRequest, CreateUserRequest, ChatMessage } from './generated/user_pb';

function authInterceptor(options: grpc.InterceptorOptions, nextCall: grpc.NextCall): grpc.InterceptingCall {
  const requester = new grpc.RequesterBuilder()
    .withStart((metadata, _listener, next) => {
      metadata.add('authorization', `Bearer ${process.env.API_TOKEN || 'dev-token-123'}`);
      next(metadata, _listener);
    })
    .build();
  return new grpc.InterceptingCall(nextCall(options), requester);
}

const useTls = process.env.GRPC_TLS === 'true';
const clientCredentials = useTls
  ? grpc.credentials.createSsl(fs.readFileSync(path.join(__dirname, '../certs/ca-cert.pem')))
  : grpc.credentials.createInsecure();

const client = new UserServiceClient('localhost:50051', clientCredentials, {
  interceptors: [authInterceptor],
});

const deadline = Date.now() + 5000;

function getUser(id: string): Promise<unknown> {
  const request = new GetUserRequest();
  request.setId(id);
  return new Promise((resolve, reject) => {
    client.getUser(request, { deadline }, (err, response) => {
      if (err) reject(err);
      else resolve(response);
    });
  });
}

function listUsers(): Promise<unknown[]> {
  return new Promise((resolve) => {
    const users: unknown[] = [];
    const stream = client.listUsers(new ListUsersRequest(), { deadline });
    stream.on('data', (user) => users.push(user));
    stream.on('end', () => resolve(users));
  });
}

function createUsers(names: string[]): Promise<unknown> {
  return new Promise((resolve, reject) => {
    const stream = client.createUsers((err, list) => {
      if (err) reject(err);
      else resolve(list);
    });
    names.forEach((name) => {
      const req = new CreateUserRequest();
      req.setName(name);
      stream.write(req);
    });
    stream.end();
  });
}

function chat() {
  const stream = client.chat();
  stream.on('data', (msg: ChatMessage) => console.log(msg.getContent()));
  const message = new ChatMessage();
  message.setUserId('client');
  message.setContent('Hello');
  message.setTimestamp(Date.now());
  stream.write(message);
}

(async () => {
  console.log(await getUser('1'));
  console.log(await listUsers());
  console.log(await createUsers(['Bob', 'Carol']));
  chat();
})();

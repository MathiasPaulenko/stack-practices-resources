import * as fs from 'fs';
import * as path from 'path';
import * as grpc from '@grpc/grpc-js';
import { HealthImplementation } from 'grpc-health-check';
import { UserServiceService, IUserServiceServer } from './generated/user_grpc_pb';
import { GetUserRequest, User, ListUsersRequest, CreateUserRequest, UserList, ChatMessage } from './generated/user_pb';

const server = new grpc.Server();

const userService: IUserServiceServer = {
  getUser: (call, callback) => {
    const user = new User();
    user.setId(call.request.getId());
    user.setName('Alice');
    user.setEmail('alice@stackpractices.local');
    callback(null, user);
  },

  listUsers: (call) => {
    for (let i = 1; i <= 3; i++) {
      const user = new User();
      user.setId(String(i));
      user.setName(`User ${i}`);
      call.write(user);
    }
    call.end();
  },

  createUsers: (call, callback) => {
    const users: User[] = [];
    call.on('data', (req: CreateUserRequest) => {
      const user = new User();
      user.setId(String(users.length + 1));
      user.setName(req.getName());
      user.setEmail(req.getEmail());
      users.push(user);
    });
    call.on('end', () => {
      const list = new UserList();
      list.setUsersList(users);
      callback(null, list);
    });
  },

  chat: (call) => {
    call.on('data', (msg: ChatMessage) => {
      const reply = new ChatMessage();
      reply.setUserId('server');
      reply.setContent(`Echo: ${msg.getContent()}`);
      reply.setTimestamp(Date.now());
      call.write(reply);
    });
    call.on('end', () => call.end());
  },
};

server.addService(UserServiceService, userService);

const healthImpl = new HealthImplementation({
  'users.UserService': grpc.status.SERVING,
  '': grpc.status.SERVING,
});
healthImpl.addToServer(server);

const useTls = process.env.GRPC_TLS === 'true';
const bindAddress = '0.0.0.0:50051';

const credentials = useTls
  ? grpc.ServerCredentials.createSsl(
      fs.readFileSync(path.join(__dirname, '../certs/ca-cert.pem')),
      [{
        private_key: fs.readFileSync(path.join(__dirname, '../certs/server-key.pem')),
        cert_chain: fs.readFileSync(path.join(__dirname, '../certs/server-cert.pem')),
      }],
      false
    )
  : grpc.ServerCredentials.createInsecure();

server.bindAsync(bindAddress, credentials, (err) => {
  if (err) throw err;
  server.start();
  console.log(`gRPC server running on ${bindAddress} (${useTls ? 'TLS' : 'insecure'})`);
});

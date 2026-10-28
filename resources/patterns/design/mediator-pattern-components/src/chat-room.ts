// Mediator pattern: centralize communication between components
interface ChatMediator {
  sendMessage(msg: string, user: User): void;
  registerUser(user: User): void;
}

abstract class User {
  constructor(protected mediator: ChatMediator, public name: string) {}
  abstract send(msg: string): void;
  abstract receive(msg: string): void;
}

class ChatUser extends User {
  send(msg: string) { this.mediator.sendMessage(msg, this); }
  receive(msg: string) { console.log(`[${this.name}] received: ${msg}`); }
}

class ChatRoom implements ChatMediator {
  private users: User[] = [];

  registerUser(user: User) { this.users.push(user); }

  sendMessage(msg: string, sender: User) {
    // Broadcast to all except sender
    this.users.filter(u => u !== sender).forEach(u => u.receive(msg));
  }
}

const chat = new ChatRoom();
const alice = new ChatUser(chat, "Alice");
const bob = new ChatUser(chat, "Bob");
chat.registerUser(alice);
chat.registerUser(bob);

alice.send("Hello everyone");
// [Bob] received: Hello everyone

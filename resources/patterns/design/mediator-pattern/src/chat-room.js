// Mediator pattern: chat room. Run: node chat-room.js
class ChatRoom {
  constructor() {
    this.users = [];
  }

  addUser(user) {
    this.users.push(user);
  }

  sendMessage(message, sender) {
    for (const user of this.users) {
      if (user !== sender) {
        user.receive(message, sender.name);
      }
    }
  }
}

class User {
  constructor(name, mediator) {
    this.name = name;
    this.mediator = mediator;
    mediator.addUser(this);
  }

  send(message) {
    console.log(`${this.name} sends: ${message}`);
    this.mediator.sendMessage(message, this);
  }

  receive(message, fromName) {
    console.log(`${this.name} receives from ${fromName}: ${message}`);
  }
}

const room = new ChatRoom();
const alice = new User("Alice", room);
new User("Bob", room);
alice.send("Hello everyone!");

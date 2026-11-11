// Factory Pattern: canonical notification example with a registry.
class EmailNotification {
  send(message) {
    return `Sending email: ${message}`;
  }
}

class SmsNotification {
  send(message) {
    return `Sending SMS: ${message}`;
  }
}

class PushNotification {
  send(message) {
    return `Sending push: ${message}`;
  }
}

class NotificationFactory {
  static registry = new Map([
    ["email", () => new EmailNotification()],
    ["sms", () => new SmsNotification()],
  ]);

  static register(channel, creator) {
    this.registry.set(channel, creator);
  }

  static create(channel) {
    const creator = this.registry.get(channel);
    if (!creator) throw new Error(`Unknown channel: ${channel}`);
    return creator();
  }
}

const notifier = NotificationFactory.create("email");
console.log(notifier.send("Hello!"));

NotificationFactory.register("push", () => new PushNotification());
console.log(NotificationFactory.create("push").send("Hello!"));

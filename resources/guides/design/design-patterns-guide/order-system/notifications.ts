// Factory Method pattern: the order needs a notifier whose concrete type
// depends on the channel chosen at runtime.

export interface Notifier {
  send(recipient: string, message: string): void;
}

export class EmailNotifier implements Notifier {
  send(recipient: string, message: string): void {
    console.log(`[email -> ${recipient}] ${message}`);
  }
}

export class SMSNotifier implements Notifier {
  send(recipient: string, message: string): void {
    console.log(`[sms -> ${recipient}] ${message}`);
  }
}

export class PushNotifier implements Notifier {
  send(recipient: string, message: string): void {
    console.log(`[push -> ${recipient}] ${message}`);
  }
}

export class NotificationFactory {
  static create(kind: string): Notifier {
    switch (kind) {
      case "email":
        return new EmailNotifier();
      case "sms":
        return new SMSNotifier();
      case "push":
        return new PushNotifier();
      default:
        throw new Error(`Unsupported channel: ${kind}`);
    }
  }
}

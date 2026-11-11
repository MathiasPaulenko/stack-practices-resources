// Factory Method — notification channels decided at runtime (TypeScript)
interface Notifier {
  send(message: string, recipient: string): Promise<void>;
}

class EmailNotifier implements Notifier {
  constructor(private smtpHost: string, private from: string) {}
  async send(message: string, recipient: string): Promise<void> {
    console.log(`Email to ${recipient}: ${message}`);
  }
}

class SmsNotifier implements Notifier {
  constructor(private twilioSid: string) {}
  async send(message: string, recipient: string): Promise<void> {
    console.log(`SMS to ${recipient}: ${message}`);
  }
}

abstract class NotificationFactory {
  abstract createNotifier(): Notifier;

  async notifyUser(message: string, recipient: string): Promise<void> {
    const notifier = this.createNotifier();
    await notifier.send(message, recipient);
  }
}

class EmailNotificationFactory extends NotificationFactory {
  createNotifier(): Notifier {
    return new EmailNotifier(process.env.SMTP_HOST ?? 'smtp.local', 'noreply@example.com');
  }
}

class SmsNotificationFactory extends NotificationFactory {
  createNotifier(): Notifier {
    return new SmsNotifier(process.env.TWILIO_SID ?? 'dev-sid');
  }
}

const factory: NotificationFactory = process.env.NOTIFY_BY === 'sms'
  ? new SmsNotificationFactory()
  : new EmailNotificationFactory();

await factory.notifyUser('Your order has shipped!', 'user@example.com');

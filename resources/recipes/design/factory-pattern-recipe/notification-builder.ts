// Factory + Builder — factory picks the class, builder configures it (TypeScript)
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

class PushNotifier implements Notifier {
  constructor(private fcmKey: string) {}
  async send(message: string, recipient: string): Promise<void> {
    console.log(`Push to ${recipient}: ${message}`);
  }
}

// Wraps any Notifier with timeout, retry, and priority policies
class ResilientNotifier implements Notifier {
  constructor(
    private inner: Notifier,
    private timeout: number,
    private retries: number,
    private priority: string,
  ) {}
  async send(message: string, recipient: string): Promise<void> {
    for (let attempt = 0; attempt <= this.retries; attempt++) {
      try {
        return await this.inner.send(message, recipient);
      } catch {
        if (attempt === this.retries) throw new Error('Send failed');
      }
    }
  }
}

class NotificationBuilder {
  private channel: 'email' | 'sms' | 'push' = 'email';
  private timeout = 30;
  private retries = 3;
  private priority: 'low' | 'normal' | 'high' = 'normal';

  withChannel(channel: 'email' | 'sms' | 'push'): this { this.channel = channel; return this; }
  withTimeout(seconds: number): this { this.timeout = seconds; return this; }
  withRetries(count: number): this { this.retries = count; return this; }
  withPriority(priority: 'low' | 'normal' | 'high'): this { this.priority = priority; return this; }

  build(): Notifier {
    const base = this.channel === 'email'
      ? new EmailNotifier(process.env.SMTP_HOST ?? 'smtp.local', 'noreply@example.com')
      : this.channel === 'sms'
      ? new SmsNotifier(process.env.TWILIO_SID ?? 'dev-sid')
      : new PushNotifier(process.env.FCM_KEY ?? 'dev-key');

    return new ResilientNotifier(base, this.timeout, this.retries, this.priority);
  }
}

const notifier = new NotificationBuilder()
  .withChannel('sms')
  .withTimeout(10)
  .withRetries(5)
  .withPriority('high')
  .build();

await notifier.send('Server down!', 'admin@example.com');

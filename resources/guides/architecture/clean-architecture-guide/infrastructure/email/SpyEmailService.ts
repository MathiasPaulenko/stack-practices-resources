import { EmailService } from '../../domain/services/EmailService';

// Adapter: test double for the EmailService port.
// Records what would have been sent instead of calling SendGrid.
export class SpyEmailService implements EmailService {
  readonly sentEmails: string[] = [];

  async sendWelcome(emailAddress: string): Promise<void> {
    this.sentEmails.push(emailAddress);
  }
}

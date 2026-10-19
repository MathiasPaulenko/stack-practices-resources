// Port: outbound notification channel. The domain defines what it needs;
// an adapter in infrastructure provides the implementation.
export interface EmailService {
  sendWelcome(emailAddress: string): Promise<void>;
}

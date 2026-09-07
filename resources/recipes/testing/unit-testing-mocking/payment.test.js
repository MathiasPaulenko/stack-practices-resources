// payment.test.js — Jest 29.x mock examples
import { processPayment } from './payment';
import { sendEmail } from './email';

jest.mock('./email');

test('sends receipt email after successful payment', async () => {
  sendEmail.mockResolvedValue({ messageId: '123' });

  await processPayment({ amount: 100, userId: 'u1' });

  expect(sendEmail).toHaveBeenCalledWith(
    expect.objectContaining({
      to: 'user@example.com',
      subject: 'Payment received',
    })
  );
});

test('handles email service failure gracefully', async () => {
  sendEmail.mockRejectedValue(new Error('SMTP down'));

  const result = await processPayment({ amount: 100, userId: 'u1' });

  expect(result.emailSent).toBe(false);
  expect(result.paymentId).toBeDefined();
});

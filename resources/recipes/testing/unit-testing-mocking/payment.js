// payment.js — Payment processor with email dependency
export async function processPayment({ amount, userId }) {
  const paymentId = `pay_${Date.now()}`;
  let emailSent = false;

  try {
    await sendEmail({
      to: 'user@example.com',
      subject: 'Payment received',
      body: `Payment of $${amount} processed for ${userId}.`,
    });
    emailSent = true;
  } catch (err) {
    // Email failure should not block payment
    console.error('Email send failed:', err.message);
  }

  return { paymentId, emailSent, amount, userId };
}

import { sendEmail } from './email.js';

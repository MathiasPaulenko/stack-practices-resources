// email/EmailSender.ts
import * as fs from 'fs/promises';
import nodemailer from 'nodemailer';
import { compileTemplate, WelcomeData } from './EmailRenderer';

const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST,
  port: Number(process.env.SMTP_PORT),
  secure: true,
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,
  },
});

export async function sendWelcomeEmail(
  to: string,
  data: WelcomeData
): Promise<void> {
  const mjmlSource = await fs.readFile('./welcome.mjml', 'utf8');
  const { html, errors } = await compileTemplate(mjmlSource, data);

  if (errors.length > 0) {
    console.warn('MJML compilation warnings:', errors);
  }

  await transporter.sendMail({
    from: '"StackPractices" <noreply@example.com>',
    to,
    subject: 'Welcome to StackPractices',
    html,
    text: `Welcome ${data.name}! Visit: ${data.dashboardUrl}`,
  });
}

// Example usage
if (require.main === module) {
  sendWelcomeEmail('user@example.com', {
    name: 'Mathias',
    dashboardUrl: 'https://app.example.com/dashboard',
  })
    .then(() => console.log('Email sent'))
    .catch((err) => console.error('Failed:', err));
}

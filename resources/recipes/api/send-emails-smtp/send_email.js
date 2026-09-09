const nodemailer = require('nodemailer');
const path = require('path');

/**
 * SMTP sender with TLS, templates, attachments, and rate limiting.
 */
class SmtpSender {
  constructor(host, port, user, password, rateLimitMs = 100) {
    this.transporter = nodemailer.createTransport({
      host,
      port,
      secure: false,
      auth: { user, pass: password },
      tls: { rejectUnauthorized: true },
    });
    this.rateLimitMs = rateLimitMs;
    this._lastSend = 0;
  }

  async _throttle() {
    const elapsed = Date.now() - this._lastSend;
    if (elapsed < this.rateLimitMs) {
      await new Promise((r) => setTimeout(r, this.rateLimitMs - elapsed));
    }
    this._lastSend = Date.now();
  }

  async send(to, subject, text, html = null, attachments = []) {
    await this._throttle();
    await this.transporter.sendMail({
      from: this.transporter.options.auth.user,
      to,
      subject,
      text,
      html,
      attachments: attachments.map((file) => ({
        path: file,
        filename: path.basename(file),
      })),
    });
  }

  async sendTemplate(to, subject, templateText, templateHtml, context) {
    const text = templateText.replace(/\$\{(\w+)\}/g, (_, k) => context[k] ?? '');
    const html = templateHtml
      ? templateHtml.replace(/\$\{(\w+)\}/g, (_, k) => context[k] ?? '')
      : null;
    await this.send(to, subject, text, html);
  }
}

module.exports = { SmtpSender };

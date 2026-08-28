# Email Templates with MJML — Companion Resources

Runnable examples for the [Build Responsive Email Templates with MJML](https://stackpractices.com/recipes/email-templates-mjml/) recipe.

## Files

| File | Description |
|------|-------------|
| `welcome.mjml` | Basic welcome email template with Handlebars variables |
| `EmailRenderer.ts` | MJML compilation + Handlebars rendering pipeline |
| `EmailSender.ts` | Nodemailer SMTP sender with multipart/alternative |
| `Button.mjml` | Reusable button component for `mj-include` |
| `dark-mode.mjml` | Dark mode template with `prefers-color-scheme` media query |
| `package.json` | Dependencies: mjml, handlebars, nodemailer, typescript |
| `tsconfig.json` | TypeScript strict configuration |

## Quick Start

```bash
npm install
npm run build

# Set SMTP env vars
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=465
export SMTP_USER=your@gmail.com
export SMTP_PASS=your-app-password

# Send a test email
npm run send
```

## Testing Without SMTP

Use [Ethereal](https://ethereal.email/) for local testing:

```typescript
const transporter = nodemailer.createTransport({
  host: 'smtp.ethereal.email',
  port: 587,
  auth: {
    user: 'test@ethereal.email',
    pass: 'generated-password',
  },
});
```

## Key Points

- Always send `multipart/alternative` with HTML and plain text.
- Keep email width under 600px and size under 102KB.
- Test in Gmail, Outlook, and Apple Mail before sending.
- Escape user input with Handlebars' default HTML escaping.
- Use system fonts (Arial, Georgia, Verdana); web fonts fail in most clients.

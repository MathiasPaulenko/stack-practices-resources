# Send Transactional Emails with SMTP — Companion Resources

Production-ready SMTP email sending in Python, Node.js, and Java with TLS, templates,
attachments, and rate limiting.

## Files

| File | Language | Description |
| --- | --- | --- |
| `send_email.py` | Python | `SmtpSender` class with `smtplib`, templates, attachments, rate limiting |
| `send_email.js` | JavaScript | `SmtpSender` class with `nodemailer`, templates, rate limiting |
| `SmtpSender.java` | Java | `SmtpSender` class with Jakarta Mail, templates, attachments, rate limiting |
| `test_send_email.py` | Python | Unit tests for message building, templates, rate limiting, and sending |

## Requirements

### Python

```bash
pip install pytest
```

### Node.js

```bash
npm install nodemailer
```

### Java

```bash
# Jakarta Mail (jakarta.mail-api 2.1 + eclipse-angus/mail)
# Maven:
#   <dependency>
#     <groupId>jakarta.mail</groupId>
#     <artifactId>jakarta.mail-api</artifactId>
#     <version>2.1.3</version>
#   </dependency>
#   <dependency>
#     <groupId>org.eclipse.angus</groupId>
#     <artifactId>jakarta.mail</artifactId>
#     <version>2.0.3</version>
#   </dependency>
```

## Running Tests

```bash
# Python tests
cd resources/recipes/api/send-emails-smtp
python -m pytest test_send_email.py -v
```

## Key Features

- TLS via STARTTLS (port 587) or implicit TLS (port 465)
- Plain text + HTML multipart messages
- File attachments with automatic MIME type detection
- Template substitution with context variables
- Rate limiting to stay under provider limits
- Bounce and retry handling patterns

## See Also

- [Full recipe](https://stackpractices.com/recipes/send-emails-smtp/)
- [Receta en español](https://stackpractices.com/es/recipes/send-emails-smtp/)

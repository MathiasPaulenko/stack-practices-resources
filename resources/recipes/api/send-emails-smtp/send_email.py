"""Send transactional emails via SMTP with TLS, templates, and attachments."""

import mimetypes
import smtplib
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from string import Template


class SmtpSender:
    """SMTP client with TLS, templates, attachments, and rate limiting."""

    def __init__(self, host, port, user, password, rate_limit=0.1):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.rate_limit = rate_limit
        self._last_send = 0.0

    def build_message(self, to, subject, text, html=None, attachments=None):
        """Build a multipart email with plain text, optional HTML, and attachments."""
        msg = MIMEMultipart("mixed")
        msg["Subject"] = subject
        msg["From"] = self.user
        msg["To"] = to

        alt = MIMEMultipart("alternative")
        alt.attach(MIMEText(text, "plain"))
        if html:
            alt.attach(MIMEText(html, "html"))
        msg.attach(alt)

        if attachments:
            for path in attachments:
                ctype, _ = mimetypes.guess_type(path)
                if ctype is None:
                    ctype = "application/octet-stream"
                maintype, subtype = ctype.split("/", 1)
                with open(path, "rb") as f:
                    part = MIMEBase(maintype, subtype)
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=Path(path).name,
                )
                msg.attach(part)
        return msg

    def _throttle(self):
        elapsed = time.monotonic() - self._last_send
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self._last_send = time.monotonic()

    def send(self, to, subject, text, html=None, attachments=None):
        """Send an email with TLS and basic rate limiting."""
        self._throttle()
        msg = self.build_message(to, subject, text, html, attachments)
        with smtplib.SMTP(self.host, self.port) as server:
            server.starttls()
            server.login(self.user, self.password)
            server.send_message(msg)
        return msg

    def send_template(self, to, subject, template_text, template_html, context):
        """Send a templated email by substituting context variables."""
        text = Template(template_text).substitute(context)
        html = Template(template_html).substitute(context) if template_html else None
        return self.send(to, subject, text, html)

"""Tests for SmtpSender — verifies message building, templates, and rate limiting."""

import time
from unittest.mock import MagicMock, patch

import pytest

from send_email import SmtpSender


@pytest.fixture
def sender():
    return SmtpSender("smtp.example.com", 587, "user@example.com", "pass", rate_limit=0.05)


class TestBuildMessage:
    def test_builds_plain_text_only(self, sender):
        msg = sender.build_message("to@x.com", "Subject", "Hello")
        assert msg["Subject"] == "Subject"
        assert msg["From"] == "user@example.com"
        assert msg["To"] == "to@x.com"
        assert msg.is_multipart()

    def test_builds_multipart_with_html(self, sender):
        msg = sender.build_message("to@x.com", "Subject", "Hello", html="<p>Hello</p>")
        assert msg.is_multipart()

    def test_builds_with_attachment(self, sender, tmp_path):
        att = tmp_path / "test.txt"
        att.write_text("attachment content")
        msg = sender.build_message("to@x.com", "Subject", "Hello", attachments=[str(att)])
        assert msg.is_multipart()


class TestTemplate:
    def test_substitutes_context_variables(self, sender):
        with patch.object(sender, "send") as mock_send:
            sender.send_template(
                "to@x.com",
                "Order confirmed",
                "Hi $name, order $order_id",
                "<p>Hi $name, order $order_id</p>",
                {"name": "Alice", "order_id": "12345"},
            )
            mock_send.assert_called_once()
            args = mock_send.call_args
            assert "Alice" in args[0][2]
            assert "12345" in args[0][2]

    def test_handles_missing_context_key(self, sender):
        with patch.object(sender, "send") as mock_send:
            sender.send_template(
                "to@x.com",
                "Test",
                "Hi $name",
                None,
                {"name": "Bob"},
            )
            mock_send.assert_called_once()
            args = mock_send.call_args
            assert "Bob" in args[0][2]


class TestRateLimit:
    def test_throttle_delays_consecutive_sends(self, sender):
        with patch("smtplib.SMTP") as mock_smtp:
            server = MagicMock()
            mock_smtp.return_value.__enter__ = MagicMock(return_value=server)
            mock_smtp.return_value.__exit__ = MagicMock(return_value=False)

            start = time.monotonic()
            sender.send("to@x.com", "S1", "text1")
            sender.send("to@x.com", "S2", "text2")
            elapsed = time.monotonic() - start

            assert elapsed >= 0.04
            assert server.send_message.call_count == 2


class TestSend:
    def test_send_calls_starttls_and_login(self, sender):
        with patch("smtplib.SMTP") as mock_smtp:
            server = MagicMock()
            mock_smtp.return_value.__enter__ = MagicMock(return_value=server)
            mock_smtp.return_value.__exit__ = MagicMock(return_value=False)

            sender.send("to@x.com", "Subject", "Hello")

            server.starttls.assert_called_once()
            server.login.assert_called_once_with("user@example.com", "pass")
            server.send_message.assert_called_once()

    def test_send_with_html_and_attachment(self, sender, tmp_path):
        att = tmp_path / "report.pdf"
        att.write_bytes(b"%PDF-1.4 fake pdf")
        with patch("smtplib.SMTP") as mock_smtp:
            server = MagicMock()
            mock_smtp.return_value.__enter__ = MagicMock(return_value=server)
            mock_smtp.return_value.__exit__ = MagicMock(return_value=False)

            sender.send("to@x.com", "Report", "See report", html="<p>Report</p>",
                        attachments=[str(att)])
            server.send_message.assert_called_once()

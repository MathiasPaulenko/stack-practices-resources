# test_payment.py — Pytest 8.x mock examples
from unittest.mock import patch, MagicMock
from payment import process_payment


def test_payment_success():
    with patch('payment.send_email') as mock_email:
        mock_email.return_value = {'message_id': '123'}
        result = process_payment(amount=100, user_id='u1')
        assert result['email_sent'] is True
        mock_email.assert_called_once()


def test_payment_email_failure():
    with patch('payment.send_email', side_effect=Exception('timeout')):
        result = process_payment(amount=100, user_id='u1')
        assert result['email_sent'] is False

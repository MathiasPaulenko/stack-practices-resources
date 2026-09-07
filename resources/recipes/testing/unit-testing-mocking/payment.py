# payment.py — Payment processor with email dependency
from email_service import send_email


def process_payment(amount, user_id):
    payment_id = f"pay_{int(time.time() * 1000)}"
    email_sent = False

    try:
        send_email(
            to="user@example.com",
            subject="Payment received",
            body=f"Payment of ${amount} processed for {user_id}.",
        )
        email_sent = True
    except Exception as err:
        # Email failure should not block payment
        print(f"Email send failed: {err}")

    return {"payment_id": payment_id, "email_sent": email_sent, "amount": amount, "user_id": user_id}

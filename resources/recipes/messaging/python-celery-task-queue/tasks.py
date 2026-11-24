# tasks.py — task definitions: retries, chain targets and a chord callback.
import logging
import time

from celery import chord, group

from celery_app import app

logger = logging.getLogger(__name__)


@app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def send_email(self, to: str, subject: str, body: str):
    """Send an email; transient failures retry with exponential backoff."""
    try:
        smtp = connect_smtp()  # noqa: F821 — plug in your SMTP client
        smtp.sendmail(to, subject, body)
        logger.info("Email sent to %s", to)
        return {'status': 'sent', 'to': to}
    except Exception as exc:
        # autoretry_for already retries transient errors; this branch only
        # runs for non-transient failures.
        logger.error("Failed to send email to %s: %s", to, exc)
        raise


@app.task
def generate_report(report_type: str, params: dict) -> dict:
    """Simulate a slow report job."""
    time.sleep(5)
    return {
        'reportType': report_type,
        'params': params,
        'url': f'https://reports.example.com/{report_type}/{params["id"]}.pdf',
    }


@app.task
def send_report_email(report: dict, to: str, subject: str):
    """Chain target: takes the previous task's result as its first arg."""
    body = f"Your {report['reportType']} report is ready: {report['url']}"
    return send_email.delay(to, subject, body).get()


@app.task
def summarize_reports(results: list, to_email: str):
    """Chord callback: must be a registered task to have a .s() signature."""
    summary = f"Generated {len(results)} reports:\n"
    for r in results:
        summary += f"  - {r['reportType']}: {r['url']}\n"
    send_email.delay(to_email, 'Report Summary', summary)
    return {'sent': True, 'count': len(results)}


def run_chord(report_requests):
    header = group(
        generate_report.s(r['type'], r['params']) for r in report_requests
    )
    return chord(header)(summarize_reports.s('admin@example.com'))

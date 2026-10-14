"""Minimal in-app scheduler with the `schedule` library.

Install: pip install schedule
Run:     python schedule_example.py
"""
import time

import schedule


def job() -> None:
    print("Running scheduled task...")


# Every 10 minutes
schedule.every(10).minutes.do(job)

# Every day at 9:30 AM
schedule.every().day.at("09:30").do(job)

# Every Monday
schedule.every().monday.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

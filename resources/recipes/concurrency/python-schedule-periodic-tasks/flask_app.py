from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)
scheduler = BackgroundScheduler()


def health_check():
    print(f"Scheduler running: {scheduler.running}")


scheduler.add_job(health_check, "interval", seconds=60, id="health_check")
scheduler.start()
atexit.register(scheduler.shutdown)


@app.route("/health")
def health():
    return {"status": "healthy" if scheduler.running else "unhealthy"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

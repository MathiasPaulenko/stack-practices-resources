import azure.functions as func
import logging

app = func.FunctionApp()


def run_cleanup() -> None:
    """Placeholder for real cleanup logic."""
    pass


@app.timer_trigger(schedule="0 0 2 * * *", arg_name="timer",
                   run_on_startup=False)
def daily_cleanup(timer: func.TimerRequest) -> None:
    if timer.past_due:
        logging.warning("Timer is past due — running catch-up execution")
    logging.info("Daily cleanup started")
    run_cleanup()

import azure.functions as func
import logging

app = func.FunctionApp()

@app.schedule(schedule="0 0 */6 * * *", arg_name="timer", run_on_startup=False)
def cleanup_timer(timer: func.TimerRequest) -> None:
    logging.info(f"Timer triggered at: {timer.schedule_status}")
    # Run cleanup logic every 6 hours
    cleanup_expired_sessions()

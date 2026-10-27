import azure.functions as func
import json

app = func.FunctionApp()

@app.service_bus_queue_trigger(
    arg_name="msg",
    queue_name="orders",
    connection="ServiceBusConnection",
)
def process_order_message(msg: func.ServiceBusMessage) -> None:
    order = json.loads(msg.get_body().decode('utf-8'))
    process_order(order)

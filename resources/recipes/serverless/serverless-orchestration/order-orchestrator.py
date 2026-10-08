# Azure Durable Functions — order orchestrator (Python v2 programming model)
# Requires: pip install azure-functions azure-functions-durable

import azure.functions as func
import azure.durable_functions as df

myApp = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@myApp.route(route="orchestrators/{functionName}")
@myApp.durable_client_input(client_name="client")
async def http_start(req: func.HttpRequest, client):
    instance_id = await client.start_new(req.route_params["functionName"], None, None)
    return client.create_check_status_response(req, instance_id)


@myApp.orchestration_trigger(context_name="context")
def order_orchestrator(context: df.DurableOrchestrationContext):
    order = context.get_input()

    try:
        yield context.call_activity("validate_order", order)
        yield context.call_activity("check_inventory", order["items"])
        yield context.call_activity("process_payment", order)

        # Fan-out/fan-in for parallel tasks
        tasks = [
            context.call_activity("send_email", order),
            context.call_activity("update_analytics", order),
        ]
        yield context.task_all(tasks)

        yield context.call_activity("schedule_shipment", order)
        return {"status": "completed"}

    except Exception as e:
        if "PaymentFailed" in str(e):
            yield context.call_activity("release_inventory", order)
        raise

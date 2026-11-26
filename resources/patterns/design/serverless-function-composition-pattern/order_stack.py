"""CDK stack: order-processing state machine (validate -> pay -> branch).

Payment failure routes to a refund compensation step, then Fail.
Retries live on the tasks (retry_on_service_exceptions), not on the
state machine — StateMachine has no retry_on_failure prop.
"""

from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as lambda_,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
)
from constructs import Construct


class OrderProcessingStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        def fn(name: str, handler: str, seconds: int) -> lambda_.Function:
            return lambda_.Function(
                self,
                name,
                runtime=lambda_.Runtime.PYTHON_3_12,
                handler=handler,
                code=lambda_.Code.from_asset("lambda"),
                timeout=Duration.seconds(seconds),
            )

        validate_task = tasks.LambdaInvoke(
            self, "ValidateOrderTask",
            lambda_function=fn("ValidateOrder", "steps.validate", 30),
            output_path="$.Payload",
        )
        payment_task = tasks.LambdaInvoke(
            self, "ProcessPaymentTask",
            lambda_function=fn("ProcessPayment", "steps.process_payment", 60),
            output_path="$.Payload",
            retry_on_service_exceptions=True,
        )
        inventory_task = tasks.LambdaInvoke(
            self, "ReserveInventoryTask",
            lambda_function=fn("ReserveInventory", "steps.reserve_inventory", 30),
            output_path="$.Payload",
        )
        notify_task = tasks.LambdaInvoke(
            self, "SendNotificationTask",
            lambda_function=fn("SendNotification", "steps.send_notification", 15),
            output_path="$.Payload",
        )
        refund_task = tasks.LambdaInvoke(
            self, "RefundPaymentTask",
            lambda_function=fn("RefundPayment", "steps.refund_payment", 60),
            output_path="$.Payload",
        )

        definition = (
            validate_task
            .next(payment_task)
            .next(
                sfn.Choice(self, "PaymentResult")
                .when(
                    sfn.Condition.string_equals("$.paymentStatus", "SUCCESS"),
                    inventory_task.next(notify_task),
                )
                .when(
                    sfn.Condition.string_equals("$.paymentStatus", "FAILED"),
                    refund_task.next(
                        sfn.Fail(
                            self, "OrderFailed",
                            error="PaymentFailed",
                            cause="Payment processing failed",
                        )
                    ),
                )
                .otherwise(sfn.Fail(self, "UnknownPaymentStatus"))
            )
        )

        sfn.StateMachine(
            self, "OrderProcessingStateMachine",
            definition=definition,
            timeout=Duration.minutes(5),
        )

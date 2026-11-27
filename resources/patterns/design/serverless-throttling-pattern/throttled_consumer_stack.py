from aws_cdk import (
    Stack,
    aws_sqs as sqs,
    aws_lambda as lambda_,
    aws_lambda_event_sources as events,
    Duration,
)
from constructs import Construct


class ThrottledConsumerStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        dlq = sqs.Queue(self, "DeadLetterQueue",
            retention_period=Duration.days(14),
        )

        queue = sqs.Queue(self, "ThrottledQueue",
            visibility_timeout=Duration.seconds(300),
            receive_message_wait_time=Duration.seconds(20),
            dead_letter_queue=sqs.DeadLetterQueue(
                max_receive_count=5,
                queue=dlq,
            ),
        )

        consumer = lambda_.Function(self, "ThrottledConsumer",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="sqs_consumer.handler",
            code=lambda_.Code.from_asset("lambda"),
            timeout=Duration.seconds(60),
            reserved_concurrent_executions=10,
            environment={"QUEUE_URL": queue.queue_url},
        )

        consumer.add_event_source(events.SqsEventSource(
            queue,
            batch_size=5,
            max_batching_window=Duration.seconds(30),
            report_batch_item_failures=True,
        ))

        queue.grant_consume_messages(consumer)

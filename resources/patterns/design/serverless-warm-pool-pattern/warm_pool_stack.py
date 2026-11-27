"""CDK stack for the serverless warm pool pattern.

An EventBridge rule invokes a small warmup function every 5 minutes. The
warmup function sends N concurrent async pings to the API function, which
keeps N execution environments alive between traffic bursts.
"""
from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as lambda_,
    aws_events as events,
    aws_events_targets as targets,
)
from constructs import Construct


class WarmPoolStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # The function to keep warm
        api_function = lambda_.Function(
            self, "ApiFunction",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="api.handler",
            code=lambda_.Code.from_asset("lambda/api"),
            timeout=Duration.seconds(30),
            reserved_concurrent_executions=5,  # Limit warm pool size
        )

        # Warmup function that sends pings
        warmup_function = lambda_.Function(
            self, "WarmupFunction",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="warmup.handler",
            code=lambda_.Code.from_asset("lambda/warmup"),
            timeout=Duration.seconds(30),
        )

        # Grant warmup function permission to invoke API function
        api_function.grant_invoke(warmup_function)

        # Schedule warmup every 5 minutes
        warmup_rule = events.Rule(
            self, "WarmupSchedule",
            schedule=events.Schedule.rate(Duration.minutes(5)),
        )
        warmup_rule.add_target(targets.LambdaFunction(warmup_function))

        # Pass the API function name as environment variable
        warmup_function.add_environment(
            "TARGET_FUNCTION", api_function.function_name)
        warmup_function.add_environment("WARM_COUNT", "5")

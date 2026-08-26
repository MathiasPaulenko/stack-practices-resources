"""Support chatbot using the OpenAI Assistants API.

Run: python chatbot.py

Requires: pip install openai
Set: OPENAI_API_KEY environment variable
"""
import json
import os
import time

from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def get_order_status(order_id: str) -> str:
    """Mock function — replace with your real backend call."""
    return f"Order {order_id} is shipped and arriving tomorrow."


def create_assistant() -> str:
    assistant = client.beta.assistants.create(
        name="Support Bot",
        instructions=(
            "You are a support agent. Answer questions from the user's knowledge base. "
            "If you need order data, call get_order_status. Use only the data provided."
        ),
        model="gpt-4o-mini",
        tools=[
            {"type": "file_search"},
            {
                "type": "function",
                "function": {
                    "name": "get_order_status",
                    "description": "Get the status of a customer order",
                    "parameters": {
                        "type": "object",
                        "properties": {"order_id": {"type": "string"}},
                        "required": ["order_id"],
                    },
                },
            },
        ],
        tool_resources={"file_search": {"vector_store_ids": ["vs_..."]}},
    )
    return assistant.id


def run_conversation(assistant_id: str, user_message: str) -> str:
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id, assistant_id=assistant_id
    )

    while run.status in ("queued", "in_progress", "requires_action"):
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id, run_id=run.id
        )

        if run.status == "requires_action":
            outputs = []
            for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                if tool_call.function.name == "get_order_status":
                    args = json.loads(tool_call.function.arguments)
                    result = get_order_status(args["order_id"])
                    outputs.append(
                        {"tool_call_id": tool_call.id, "output": result}
                    )
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id, run_id=run.id, tool_outputs=outputs
            )

    if run.status in ("failed", "expired", "cancelled"):
        return f"Run failed with status: {run.status}"

    messages = client.beta.threads.messages.list(
        thread_id=thread.id, order="desc", limit=1
    )
    return messages.data[0].content[0].text.value


if __name__ == "__main__":
    assistant_id = create_assistant()
    reply = run_conversation(
        assistant_id, "What is the status of order ORD-9981?"
    )
    print(reply)

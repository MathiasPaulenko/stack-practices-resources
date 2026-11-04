"""Two-step function calling loop (tool -> result -> final answer).

Requires OPENAI_API_KEY. Handles parallel tool_calls as a list.
"""
import json

from openai import OpenAI

client = OpenAI()

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city. Use when the user asks about weather, temperature, or forecast.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name, e.g. 'Tokyo'"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["city"],
            },
        },
    }
]


def get_weather(city: str, unit: str = "celsius") -> dict:
    """Stub implementation - replace with a real weather API call."""
    return {"city": city, "temperature": 21, "unit": unit, "conditions": "clear"}


def ask(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]
    first = client.chat.completions.create(model="gpt-4o", messages=messages, tools=TOOLS)
    assistant_msg = first.choices[0].message

    if not assistant_msg.tool_calls:
        return assistant_msg.content

    messages.append(assistant_msg)
    for tool_call in assistant_msg.tool_calls:
        args = json.loads(tool_call.function.arguments)
        result = get_weather(**args)
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result),
            }
        )

    second = client.chat.completions.create(model="gpt-4o", messages=messages, tools=TOOLS)
    return second.choices[0].message.content


if __name__ == "__main__":
    print(ask("What's the weather in Tokyo?"))

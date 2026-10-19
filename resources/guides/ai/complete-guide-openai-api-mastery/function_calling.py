"""Full tool-call loop with iteration cap and argument validation."""
import json

from openai import OpenAI

MAX_TOOL_ROUNDS = 5

client = OpenAI()

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name, e.g. 'Madrid, Spain'",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit",
                    },
                },
                "required": ["location"],
            },
        },
    }
]


def get_weather(location: str, unit: str = "celsius") -> str:
    # Simulated API call
    return f"Weather in {location}: 22°{unit[0].upper()}, sunny"


FUNCTION_MAP = {"get_weather": get_weather}


def run(user_prompt: str) -> str:
    messages = [{"role": "user", "content": user_prompt}]

    for _ in range(MAX_TOOL_ROUNDS):
        response = client.chat.completions.create(
            model="gpt-4o", messages=messages, tools=TOOLS
        )
        tool_calls = response.choices[0].message.tool_calls

        if not tool_calls:
            return response.choices[0].message.content

        messages.append(response.choices[0].message)
        for call in tool_calls:
            try:
                args = json.loads(call.function.arguments)
                result = FUNCTION_MAP[call.function.name](**args)
            except (KeyError, TypeError, json.JSONDecodeError) as exc:
                result = f"Tool error: {exc}"

            messages.append(
                {"role": "tool", "tool_call_id": call.id, "content": result}
            )

    return "Stopped after max tool rounds."


if __name__ == "__main__":
    print(run("What's the weather in Madrid?"))

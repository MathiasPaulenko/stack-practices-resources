"""Responses API basics: create, chaining, flattened function tools."""
import json

from openai import OpenAI

client = OpenAI()


def basic_response() -> None:
    response = client.responses.create(
        model="gpt-4o",
        input="Explain Python decorators in 2 sentences.",
    )
    print(response.output_text)
    print(f"Tokens used: {response.usage.total_tokens}")


def multi_turn() -> None:
    first = client.responses.create(
        model="gpt-4o",
        input="You are a Python expert. What is a decorator?",
    )
    follow_up = client.responses.create(
        model="gpt-4o",
        previous_response_id=first.id,
        input="Show me an example.",
    )
    print(follow_up.output_text)


def get_weather(location: str, unit: str = "celsius") -> str:
    # Simulated API call
    return f"Weather in {location}: 22°{unit[0].upper()}, sunny"


def function_calling() -> None:
    tools = [
        {
            "type": "function",
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name, e.g. 'Madrid, Spain'",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
            "strict": True,
        }
    ]

    response = client.responses.create(
        model="gpt-4o",
        input="What's the weather in Madrid?",
        tools=tools,
    )

    for item in response.output:
        if item.type == "function_call":
            result = get_weather(**json.loads(item.arguments))
            follow = client.responses.create(
                model="gpt-4o",
                previous_response_id=response.id,
                input=[
                    {
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": result,
                    }
                ],
            )
            print(follow.output_text)


if __name__ == "__main__":
    basic_response()
    # multi_turn()
    # function_calling()

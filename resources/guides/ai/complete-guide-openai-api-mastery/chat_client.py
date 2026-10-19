"""Chat completions: single call and managed multi-turn history."""
from openai import OpenAI

client = OpenAI()


def basic_completion() -> None:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Explain Python decorators in 2 sentences."},
        ],
        temperature=0.7,
        max_tokens=200,
    )
    print(response.choices[0].message.content)
    print(f"Tokens used: {response.usage.total_tokens}")


def multi_turn() -> None:
    conversation = [
        {"role": "system", "content": "You are a Python expert."},
        {"role": "user", "content": "What is a decorator?"},
    ]
    response = client.chat.completions.create(model="gpt-4o", messages=conversation)

    conversation.append(
        {"role": "assistant", "content": response.choices[0].message.content}
    )
    conversation.append({"role": "user", "content": "Show me an example."})

    response = client.chat.completions.create(model="gpt-4o", messages=conversation)
    print(response.choices[0].message.content)


if __name__ == "__main__":
    basic_completion()
    # multi_turn()

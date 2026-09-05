"""Ollama Python client."""

from ollama import Client

client = Client(host="http://localhost:11434")

response = client.chat(
    model="llama3.1:8b",
    messages=[
        {"role": "system", "content": "You are a Python expert."},
        {"role": "user", "content": "Write a decorator that logs calls."},
    ],
)
print(response["message"]["content"])

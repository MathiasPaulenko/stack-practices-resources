"""OpenAI-compatible client for vLLM."""

from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="dummy",
)

response = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain Docker containers."},
    ],
    temperature=0.7,
    max_tokens=500,
)

print(response.choices[0].message.content)

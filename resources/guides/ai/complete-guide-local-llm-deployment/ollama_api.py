"""Ollama API server client."""

import requests

OLLAMA_URL = "http://localhost:11434"


def chat(model: str, message: str, system: str = "You are a helpful assistant.") -> str:
    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": message},
            ],
            "stream": False,
        },
    )
    result = response.json()
    return result["message"]["content"]


if __name__ == "__main__":
    print(chat("llama3.1:8b", "Explain Python decorators."))

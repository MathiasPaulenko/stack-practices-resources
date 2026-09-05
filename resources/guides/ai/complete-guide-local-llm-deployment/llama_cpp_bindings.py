"""llama.cpp Python bindings."""

from llama_cpp import Llama

llm = Llama(
    model_path="llama-3.1-8b-instruct-q4_k_m.gguf",
    n_ctx=8192,
    n_gpu_layers=35,
    n_threads=8,
    verbose=False,
)

response = llm(
    "Explain Python decorators with examples.",
    max_tokens=500,
    temperature=0.7,
    stop=["\n\n\n"],
)
print(response["choices"][0]["text"])

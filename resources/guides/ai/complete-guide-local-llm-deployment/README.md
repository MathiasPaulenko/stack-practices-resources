# Local LLM Deployment — Companion

Runnable examples for the StackPractices guide
[Local LLM Deployment: Ollama, vLLM & llama.cpp](https://stackpractices.com/guides/complete-guide-local-llm-deployment/).

## Files

| File | Language | Description |
|------|----------|-------------|
| `ollama_api.py` | Python | Ollama HTTP API client |
| `ollama_client.py` | Python | Ollama Python SDK client |
| `Modelfile` | Dockerfile | Custom Ollama model definition |
| `vllm_serve.sh` | Bash | vLLM server startup script |
| `vllm_client.py` | Python | OpenAI-compatible vLLM client |
| `llama_cpp_build.sh` | Bash | llama.cpp build and run script |
| `llama_cpp_bindings.py` | Python | llama.cpp Python bindings |
| `estimate_vram.py` | Python | VRAM calculator for model sizing |
| `benchmark.py` | Python | Inference benchmarking tool |
| `Dockerfile` | Dockerfile | vLLM Docker image |
| `docker-compose.yml` | YAML | Production Docker Compose with health checks |

## Quick start

### Ollama

```bash
ollama pull llama3.1:8b
python ollama_api.py
```

### vLLM

```bash
pip install vllm
bash vllm_serve.sh
python vllm_client.py
```

### llama.cpp

```bash
bash llama_cpp_build.sh
python llama_cpp_bindings.py
```

### Docker

```bash
export HUGGING_FACE_HUB_TOKEN=your_token
docker compose up -d
docker exec -it ollama ollama pull llama3.1:8b
```

### Benchmark

```bash
python benchmark.py
```

## Source

- [Guide (EN)](https://stackpractices.com/guides/complete-guide-local-llm-deployment/)
- [Guide (ES)](https://stackpractices.com/es/guides/complete-guide-local-llm-deployment/)

# Despliegue Local de LLM — Companion

Ejemplos ejecutables para la guía de StackPractices
[Despliegue Local de LLM: Ollama, vLLM y llama.cpp](https://stackpractices.com/es/guides/complete-guide-local-llm-deployment/).

## Archivos

| Archivo | Lenguaje | Descripción |
|---------|----------|-------------|
| `ollama_api.py` | Python | Cliente HTTP API de Ollama |
| `ollama_client.py` | Python | Cliente SDK Python de Ollama |
| `Modelfile` | Dockerfile | Definición de modelo custom de Ollama |
| `vllm_serve.sh` | Bash | Script de inicio de server vLLM |
| `vllm_client.py` | Python | Cliente vLLM compatible con OpenAI |
| `llama_cpp_build.sh` | Bash | Script de build y run de llama.cpp |
| `llama_cpp_bindings.py` | Python | Bindings de Python de llama.cpp |
| `estimate_vram.py` | Python | Calculadora de VRAM para model sizing |
| `benchmark.py` | Python | Herramienta de benchmarking de inferencia |
| `Dockerfile` | Dockerfile | Imagen Docker de vLLM |
| `docker-compose.yml` | YAML | Docker Compose de producción con health checks |

## Inicio rápido

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

## Fuente

- [Guía (EN)](https://stackpractices.com/guides/complete-guide-local-llm-deployment/)
- [Guía (ES)](https://stackpractices.com/es/guides/complete-guide-local-llm-deployment/)

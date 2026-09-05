#!/bin/bash
# vLLM serving with performance tuning

pip install vllm

python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-3.1-8B-Instruct \
    --port 8000 \
    --tensor-parallel-size 1 \
    --gpu-memory-utilization 0.9 \
    --max-model-len 8192

# Performance tuning version:
# python -m vllm.entrypoints.openai.api_server \
#     --model meta-llama/Llama-3.1-8B-Instruct \
#     --port 8000 \
#     --tensor-parallel-size 2 \
#     --gpu-memory-utilization 0.95 \
#     --max-model-len 16384 \
#     --enable-chunked-prefill \
#     --enable-prefix-caching

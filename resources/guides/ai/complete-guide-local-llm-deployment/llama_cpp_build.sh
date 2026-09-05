#!/bin/bash
# Build and run llama.cpp

git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

# CPU only
make

# CUDA build
# make GGML_CUDA=1

# Download a GGUF model
wget https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct-GGUF/resolve/main/llama-3.1-8b-instruct-q4_k_m.gguf

# Run inference
./llama-cli -m llama-3.1-8b-instruct-q4_k_m.gguf -p "Explain Python GIL" -n 200

# Run as server with flash attention
./llama-server -m llama-3.1-8b-instruct-q4_k_m.gguf --port 8080 --ctx-size 8192 -fa

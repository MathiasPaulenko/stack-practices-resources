"""Estimate VRAM requirements for LLM inference."""


def estimate_vram(params_billion: float, quantization: str = "q4") -> float:
    bytes_per_param = {
        "fp16": 2.0,
        "q8": 1.0,
        "q6": 0.75,
        "q5": 0.625,
        "q4": 0.5,
        "q3": 0.375,
        "q2": 0.25,
    }
    bpp = bytes_per_param.get(quantization, 2.0)
    weights_gb = params_billion * bpp
    kv_cache_gb = weights_gb * 0.15
    overhead_gb = 1.0
    return weights_gb + kv_cache_gb + overhead_gb


if __name__ == "__main__":
    for name, params, quant in [
        ("Llama 3.1 8B", 8, "q4"),
        ("Llama 3.1 8B", 8, "fp16"),
        ("Llama 3.1 70B", 70, "q4"),
        ("Mistral 7B", 7, "q4"),
        ("Qwen 2.5 14B", 14, "q4"),
    ]:
        vram = estimate_vram(params, quant)
        print(f"{name} ({quant}): {vram:.1f} GB VRAM")

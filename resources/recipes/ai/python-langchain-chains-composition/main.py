"""Entry point — runs every chain variant from chains.py.

Set OPENAI_API_KEY before running:  export OPENAI_API_KEY=sk-...
"""

import chains
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
strong_model = ChatOpenAI(model="gpt-4o", temperature=0)

print("=== Basic chain ===")
print(chains.basic_chain(model).invoke({"topic": "vector databases"}))

print("\n=== Summarize then translate ===")
print(
    chains.summarize_then_translate_chain(model).invoke(
        {"text": "LangChain is a framework for building applications powered by LLMs..."}
    )
)

print("\n=== Parallel analysis ===")
print(
    chains.parallel_analysis_chain(model).invoke(
        {"text": "Our new product is amazing and uses cutting-edge AI!"}
    )
)

print("\n=== Custom components ===")
print(
    chains.custom_components_chain(model).invoke(
        {"text": "Vector databases enable semantic search over embeddings..."}
    )
)

print("\n=== Resilient chain (retry + fallback) ===")
print(chains.resilient_chain(model, strong_model).invoke({"topic": "Kubernetes probes"}))

print("\n=== Routing chain ===")
print(
    chains.routing_chain(model).invoke(
        {"text": "This technical guide covers database internals..."}
    )
)

print("\n=== Batch ===")
for r in chains.basic_chain(model).batch(
    [{"topic": "Redis caching"}, {"topic": "PostgreSQL indexing"}]
):
    print(r)
    print("---")

# Compara similitud semántica con embeddings de OpenAI

Código ejecutable que acompaña a la receta de StackPractices
[Compara similitud semántica con embeddings de OpenAI](https://stackpractices.com/es/recipes/python-openai-embeddings-cosine/).

## Contenido

- `similarity_search.py` — helpers de embeddings (individual, batch,
  reintentos con backoff), funciones de similitud coseno,
  `SimilaritySearchIndex` y `find_duplicates` por umbral.
- `main.py` — demo que compara dos textos, busca en un índice pequeño,
  imprime una matriz de similitud por pares y detecta casi duplicados.
- `requirements.txt` — dependencias fijadas (`openai`, `numpy`).

## Uso

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python main.py
```

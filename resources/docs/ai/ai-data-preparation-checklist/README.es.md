# Checklist de Preparación de Datos para IA — Scripts Compañeros

Scripts para preparar datos para sistemas LLM y RAG, complementarios del
[Checklist de Preparación de Datos para IA](https://stackpractices.com/es/docs/ai-data-preparation-checklist/).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `clean_text.py` | Elimina HTML, normaliza espacios, quita contenido repetitivo |
| `detect_pii.py` | Detecta y redacta PII (email, teléfono, SSN, tarjeta de crédito, IP) |
| `find_duplicates.py` | Detección de duplicados exactos y aproximados con TF-IDF y similitud coseno |
| `chunk_documents.py` | Divide documentos en fragmentos con metadatos usando LangChain |
| `generate_embeddings.py` | Genera embeddings en lotes con limitación de tasa |
| `test_retrieval.py` | Prueba la calidad de recuperación con métrica de tasa de acierto |

## Requisitos

```bash
pip install scikit-learn langchain openai
```

Configura la variable de entorno `OPENAI_API_KEY` antes de ejecutar
`generate_embeddings.py`.

## Uso

Cada script es independiente y ejecutable. Ejecuta cualquier script
directamente para ver una demostración con datos de ejemplo:

```bash
python clean_text.py
python detect_pii.py
python find_duplicates.py
python chunk_documents.py
python test_retrieval.py
```

Para `generate_embeddings.py`, proporciona tus propios fragmentos y
configura la clave de API.

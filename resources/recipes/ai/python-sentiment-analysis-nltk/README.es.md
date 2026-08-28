# Análisis de Sentimiento con Python y NLTK — Recursos Companion

Ejemplos ejecutables para la receta [Análisis de Sentimiento con Python y NLTK](https://stackpractices.com/es/recipes/python-sentiment-analysis-nltk/).

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `sentiment_basic.py` | Scoring básico de sentimiento con VADER |
| `classify_sentiment.py` | Clasifica texto en etiquetas positivo/negativo/neutral |
| `csv_batch.py` | Procesamiento en lote de sentimiento desde CSV |
| `custom_lexicon.py` | Personaliza el léxico de VADER con palabras de dominio |
| `sentiment_over_time.py` | Trackea tendencias de sentimiento en el tiempo |
| `requirements.txt` | Dependencias de Python (nltk) |

## Inicio Rápido

```bash
pip install -r requirements.txt
python sentiment_basic.py
python classify_sentiment.py
python custom_lexicon.py
python sentiment_over_time.py
```

Para procesamiento CSV, crea un `reviews.csv` con una columna `review`:

```bash
python csv_batch.py
# Output: scored.csv con columnas sentiment y compound
```

## Puntos Clave

- Usa el score `compound` para clasificar (rango -1 a +1).
- Thresholds por defecto: +0.05 para positivo, -0.05 para negativo.
- Customiza el léxico con palabras de tu dominio para mejor accuracy.
- VADER es solo inglés; para español usa `pysentimiento`.
- Puntúa documentos largos párrafo por párrafo, no como un todo.

# Generación de Imágenes — Recursos Complementarios

Helpers ejecutables para la [receta image-generation](https://stackpractices.com/es/recipes/image-generation/).

## Archivos

- `batch_generate.py` — renderiza las plantillas de prompts para un tema,
  calcula la clave de caché (`modelo + seed + prompt`) usada para deduplicar
  generaciones e imprime un plan en seco. Con `--call-api` llama de verdad a la
  API de imágenes de OpenAI (requiere `pip install openai requests` y
  `OPENAI_API_KEY`).
- `prompt_templates.json` — set de plantillas (hero, thumbnail, icon) con
  placeholders `{theme}` y tamaños objetivo.

## Ejecutar

```bash
python batch_generate.py "auriculares inalambricos"            # dry run, sin API key
python batch_generate.py "auriculares inalambricos" --call-api # generación real
```

El dry run muestra los tres prompts que se enviarían, la clave de caché para
deduplicar cada uno y el nombre de archivo de salida. Volver a correr con el
mismo tema produce las mismas claves — así funciona el cacheo por hash de
prompt de la receta.

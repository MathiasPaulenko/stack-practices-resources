# Compresión Gzip y Brotli — Recursos Complementarios

Ejemplos ejecutables de la receta [Comprimir y Descomprimir Archivos con Gzip y Brotli](https://stackpractices.com/es/recipes/compression-gzip/) en StackPractices.

## Archivos

| Archivo | Qué muestra |
|---|---|
| `gzip_streaming.py` | Compresión/descompresión Gzip en streaming con verificación SHA256 |
| `compress-brotli.js` | Pipelines Brotli/Gzip en Node.js + middleware `smartCompression()` de negociación de contenido |
| `precompress.sh` | Pre-compresión Bash de assets estáticos (`.gz` + `.br`) para Nginx |
| `ratio_benchmark.py` | Benchmark de ratios: JSON/HTML/logs vs aleatorio vs payloads pequeños |

## Ejecutar

```bash
python gzip_streaming.py      # comprimir + restaurar + verificar SHA256
node compress-brotli.js       # salida del pipeline gz + br con ratios
python ratio_benchmark.py     # por qué importan los umbrales (¡lo aleatorio crece!)
./precompress.sh dist/        # emite archivo.gz + archivo.br junto a cada asset
```

## Notas

- `smartCompression()` es middleware de Express — negocia `br`/`gzip` desde `Accept-Encoding` y establece `Vary: Accept-Encoding` para que los caches mantengan separadas las variantes.
- `ratio_benchmark.py` hace concreto el caso del umbral: los payloads por debajo de ~1KB y los datos ya aleatorios quedan *más grandes* al comprimirlos.
- Brotli requiere `pip install brotli` para el benchmark de Python; Node ≥11.7 incluye `zlib.createBrotliCompress` de serie.

Artículo original (ES): <https://stackpractices.com/es/recipes/compression-gzip/>

# Procesar Archivos Grandes con Streams — Ejemplos de Código

Código complementario de [Procesar Archivos Grandes con Streams](https://stackpractices.com/es/recipes/stream-processing/) en StackPractices.

## Archivos

| Archivo | Descripción |
|---|---|
| `python_reader.py` | Lector CSV mínimo línea a línea con `open()` (Python) |
| `nodejs_reader.js` | Stream de lectura mínimo con eventos `data` (Node.js) |
| `FileProcessor.java` | Procesador de líneas mínimo con `BufferedReader` (Java) |
| `etl_pipeline.py` | Pipeline ETL CSV → JSONL con seguimiento de progreso y renombrado atómico |
| `process_large_file.js` | `pipeline()` + `Transform` con manejo de backpressure (Node.js) |
| `ParallelStreamProcessor.java` | Procesamiento paralelo por lotes con thread pool (Java) |
| `fifo_pipeline.sh` | Streaming entre procesos con pipe nombrado FIFO (Bash) |

Cada ejemplo lee un trozo a la vez, así que la memoria se mantiene plana sin importar el tamaño del archivo. Las salidas se escriben a un `.tmp` y se renombran atómicamente para no corromper datos ante un fallo.

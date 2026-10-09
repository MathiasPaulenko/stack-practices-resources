# Leer Archivos Grandes en Node.js con Streams — Recursos complementarios

Archivos complementarios de [Leer Archivos Grandes en Node.js con Streams](https://stackpractices.com/es/recipes/nodejs-read-large-file-stream/) en StackPractices.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `csv-to-jsonl.js` | Pipeline completo: leer CSV → parsear con buffer de resto → filtrar → escribir JSONL vía `stream/promises` |
| `memory-compare.js` | Comparación de heap: `fs.readFile` vs conteo de líneas con stream sobre el mismo archivo |

## Cómo usarlo

1. `node csv-to-jsonl.js` — genera `sample.csv` (10k filas) si no se indica uno, escribe `output.jsonl`.
2. `node memory-compare.js big.log` — muestra el delta de heap de ambos enfoques. Genera antes un archivo de prueba: `node -e "require('fs').writeFileSync('big.log', 'x\n'.repeat(5e6))"`.

Sin dependencias — solo Node.js 18+.
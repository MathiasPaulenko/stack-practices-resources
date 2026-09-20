# Puente Batch-Streaming — Ejemplos Companion

Ejemplos ejecutables del [patrón Puente Batch-Streaming](https://stackpractices.com/es/patterns/batch-to-streaming-bridge-pattern/): cómo ETL batch y streaming en tiempo real escriben en un mismo data lake particionado, y cómo la capa de servicio los fusiona.

Sin servicios externos — los ejemplos simulan la arquitectura en memoria para que la semántica (layout de particiones, alineación de esquema, dedup) sea fácil de ver y testear.

## Qué contiene

| Fichero | Propósito |
| --- | --- |
| `bridge.py` / `bridge.js` | El patrón: productores de esquema compartido, lago particionado, capa speed, dedup en capa de servicio, consumidor unificado |
| `test_bridge.py` | Suite pytest (7 tests) |
| `bridge.test.js` | Suite `node:test` (7 tests) |

## Conceptos cubiertos

- **Esquema compartido** — `BatchProducer` y `StreamingProducer` normalizan ambas fuentes al mismo registro (email en minúsculas, `is_active` derivado, `source` etiquetado).
- **Layout de particiones** — cada registro aterriza bajo `year=/month=/day=/hour=`; el segmento de hora es lo que rompe las implementaciones reales.
- **Dedup en capa de servicio** — semántica `ROW_NUMBER()`: prefiere streaming (más fresco), cae a batch.
- **Capa speed** — lookup por clave para el estado más fresco, en lugar de re-consumir el stream.
- **Fusión selectiva** — los campos streaming sobrescriben batch solo cuando existen, para que actualizaciones parciales no borren campos.

## Ejecutar

```bash
node bridge.js        # demo JS
python bridge.py      # demo Python

node --test bridge.test.js   # tests JS
python -m pytest test_bridge.py -v   # tests Python
```

Cero dependencias más allá de pytest para la suite de tests.

# Matriz de Selección de Modelos de IA — Archivos Complementarios

Archivos independientes de la [Matriz de Selección de Modelos de IA](https://stackpractices.com/es/docs/ai-model-selection-matrix/) de StackPractices. Copia lo que necesites; cada archivo funciona por su cuenta.

## Archivos

| Archivo | Qué es |
|---|---|
| `model-pricing-comparison.csv` | Nueve modelos actuales lado a lado: precio de entrada/salida por 1K tokens, ventana de contexto, soporte multimodal. |
| `cost-per-1000-queries.csv` | La misma carga (1500 tokens de entrada + 500 de salida por consulta) costeada en los nueve modelos — por consulta, por 1K consultas y al mes con 10K consultas/día. |
| `weighted-scorecard-template.md` | La scorecard ponderada de decisión: criterios, pesos sugeridos, un ejemplo relleno y cómo calcular el ganador. |
| `model-selection-checklist.md` | El checklist previo al compromiso: carga, benchmark propio, scorecard, TCO, latencia, fallback, cadencia de re-evaluación. |

## Quick start

1. Actualiza `model-pricing-comparison.csv` con los precios vigentes del proveedor — estas filas son una foto.
2. Corre tu propio benchmark (50–100 inputs de producción) sobre los 2–3 candidatos principales.
3. Rellena la scorecard con pesos que reflejen tu funcionalidad, no promedios genéricos.
4. Recorre el checklist antes de comprometerte.

## Notas

- Los precios se mueven rápido — verifícalos con las páginas de precios de los proveedores antes de cerrar.
- La scorecard no decide por ti; deja las compensaciones a la vista.

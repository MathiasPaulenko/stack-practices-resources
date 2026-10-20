# Plantilla de Estrategia de Pruebas — Recursos Complementarios

Archivos descargables del artículo [Plantilla de Estrategia de Pruebas](https://stackpractices.com/es/docs/test-strategy-document-template/).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `test-strategy-template.md` | Plantilla en blanco de 12 secciones: objetivos, pirámide, alcance, entornos, herramientas, gates de CI, datos, política flaky, métricas, riesgos, roles, ciclo de revisión |
| `test-strategy-payments-example.md` | Ejemplo rellenado para un microservicio de pagos: gates de cobertura más estrictos, porción de contract tests, riesgos específicos de Stripe |

## Cómo usarlo

1. Copia `test-strategy-template.md` en tu repo como `TEST_STRATEGY.md`.
2. Rellena primero la tabla de alcance: fuerza la conversación de prioridades con tu tech lead y PM.
3. Ajusta los porcentajes de la pirámide a tu dominio y deja el porqué por escrito en la justificación.
4. Conecta los gates de cobertura al CI antes de publicar el documento.
5. Usa `test-strategy-payments-example.md` como referencia de cómo un servicio crítico se desvía de los valores por defecto.

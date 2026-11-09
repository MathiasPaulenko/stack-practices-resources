# Plantilla de línea de tiempo de deprecación — Archivos complementarios

Archivos rellenables de la guía de StackPractices:
[Plantilla de línea de tiempo de deprecación](https://stackpractices.com/es/docs/deprecation-timeline-template/)

| Archivo | Qué es |
|---------|--------|
| `deprecation-timeline-template.md` | La plantilla en blanco: cópiala a la documentación de tu repo y rellena los huecos |
| `filled-example.md` | La misma plantilla completada para un escenario real: payments-api v1 → v2 con cláusulas contractuales de preaviso |
| `migration-tracker.csv` | Hoja de seguimiento de consumidores: estado, último contacto y nivel de riesgo por consumidor |
| `express-deprecation-headers.js` | Middleware de Express que añade las cabeceras `Deprecation` (RFC 9745) y `Sunset` (RFC 8594), más un handler de 410 Gone |
| `nginx-deprecation-headers.conf` | Las mismas cabeceras en configuración nginx, incluido el bloque de 410 posterior al corte |

## Inicio rápido

1. Copia `deprecation-timeline-template.md` a tu proyecto y rellena cada `______`.
2. Registra a los consumidores en `migration-tracker.csv` y actualízala cada semana.
3. Cuando llegue el hito del aviso suave, conecta el middleware de cabeceras en las rutas deprecadas para que los clientes reciban avisos legibles por máquina.
4. El día del corte, sustituye el bloque de proxy por el handler de 410 (o el bloque comentado de nginx).

El formato de fecha HTTP importa: `Sunset` espera una HTTP-date como
`Thu, 15 Oct 2027 00:00:00 GMT`, no una cadena ISO.

# Pronóstico de Capacidad — Recursos complementarios

Archivos complementarios de la [Plantilla de Pronóstico de Capacidad](https://stackpractices.com/es/docs/capacity-planning-forecast-template/) en StackPractices.com.

## Qué incluye

| Archivo | Formato | Descripción |
|---------|---------|-------------|
| `capacity-forecast-template.md` | Markdown | El pronóstico rellenable de 9 secciones: estado actual, suposiciones de crecimiento, proyecciones de tráfico, pronóstico de recursos, plan de escalado, proyección de costes, evaluación de riesgos, acciones y apéndice |
| `capacity-dashboard-example.txt` | Texto | Un pronóstico completado como dashboard — muestra cómo la proyección marca el primer cuello de botella (conexiones BD en octubre, disco en noviembre, CPU en el pico estacional) con acciones fechadas |
| `capacity-projection.csv` | CSV | La misma proyección a 6 meses en formato hoja de cálculo — impórtala en Sheets/Excel y sustituye tus propios números |

## Inicio rápido

### 1. Copia la plantilla

Lleva `capacity-forecast-template.md` a tu wiki o repo, junto a la infraestructura que describe.

### 2. Rellena primero el estado actual

Extrae los picos (no las medias) de los últimos 30 días de tu monitoreo. Acuerda qué significa "lleno" por recurso antes de proyectar — 70% de CPU en una base de datos es muy distinto de 90% en un nivel web sin estado.

### 3. Proyecta y encuentra el cuello de botella

Aplica tu tasa de crecimiento a cada recurso de la sección 4. El primer recurso en tocar su límite marca tu fecha límite de escalado; programa cada acción antes de esa fecha menos el tiempo de compra/despliegue.

### 4. Revisa trimestralmente

Guarda versiones fechadas de cada pronóstico y registra proyectado vs real — esa carpeta se convierte en tu dataset de precisión de pronósticos.

## Fórmulas útiles

- Crecimiento mensual compuesto: `(fin / inicio)^(1/meses) - 1`
- Runway: `(límite - pico_actual) / crecimiento_mensual`
- Proyección de picos: pronostica picos p95 de hora punta, no medias diarias (el ratio pico/media suele ser 1.5x–3x en servicios web)

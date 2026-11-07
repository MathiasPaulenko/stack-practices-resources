# Plantilla de Documentación de API de Componentes — Kit Complementario

Archivos complementarios de la [Plantilla de Documentación de API de Componentes](https://stackpractices.com/es/docs/component-api-documentation-template/) en StackPractices.

## Contenido

| Archivo | Qué es |
|---------|--------|
| `component-api-doc.md` | La plantilla Markdown rellenable: resumen, tabla de props, tipos TypeScript, detalle de props, eventos, slots, métodos, accesibilidad, variantes, qué hacer y qué no, pruebas, guía de migración. |
| `docgen_drift_check.py` | Chequeo de deriva para CI: compara la salida de `react-docgen` con los props documentados en un archivo Markdown. Sale con error cuando difieren. |
| `props-table.csv` | La tabla de props del Button como CSV — impórtala en una hoja de cálculo o pégala en documentos que no aceptan tablas Markdown. |
| `storybook-autodocs.mdx` | Página mínima de autodocs de Storybook que renderiza tablas de props generadas junto a la parte narrativa escrita a mano. |

## Inicio rápido

```bash
# 1. Genera la salida de docgen para tu componente
npx react-docgen src/components/Button/Button.tsx --pretty > docgen.json

# 2. Rellena component-api-doc.md para el componente

# 3. Verifica que la doc coincide con el código (en CI)
python docgen_drift_check.py docgen.json component-api-doc.md
```

El chequeo de deriva compara el conjunto de props que `react-docgen` encontró en el código fuente con los props de la tabla `## Props` del documento. Cualquier prop presente en un solo lado falla el chequeo — que es justo lo que quieres que haga un PR cuando alguien cambia el componente y olvida la documentación.

## Notas

- `docgen_drift_check.py` lee la tabla de props por convención: filas bajo `## Props` cuya primera celda es el nombre del prop. Ajusta `PROPS_HEADING` si tu plantilla usa otro encabezado.
- Todo funciona sin dependencias (solo stdlib para el script).

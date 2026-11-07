# Patrón Composite para Árboles UI — Recursos Complementarios

Ejemplos ejecutables de la guía del [Patrón Composite para Árboles de Componentes UI en React](https://stackpractices.com/es/patterns/composite-pattern-ui/) en StackPractices.

## Archivos

| Archivo | Qué muestra |
|---|---|
| `ui-node.tsx` | La unión discriminada `UINode` + el renderer recursivo `<Node>` para árboles de formulario |
| `form-tree.json` | El mismo árbol como datos planos — envíalo por POST, versiónalo, renderízalo |
| `nav-tree.tsx` | Segundo dominio: un menú de navegación anidado renderizado de la misma forma |
| `serialization.test.mjs` | Tests de ida y vuelta + seguridad — ejecútalo con `node serialization.test.mjs` |

## Notas

- Solo los miembros compuestos de la unión llevan `children` — la variante "segura": una hoja no puede recibir hijos por error.
- `serialization.test.mjs` verifica los dos invariantes que promete el patrón: el árbol sobrevive intacto a `JSON.parse(JSON.stringify(t))` y las hojas nunca llevan un campo `children`.
- Para usar `ui-node.tsx`/`nav-tree.tsx`, cópialos a un proyecto React + TypeScript; son componentes función sin dependencias más allá de React.

Artículo original (ES): <https://stackpractices.com/es/patterns/composite-pattern-ui/>

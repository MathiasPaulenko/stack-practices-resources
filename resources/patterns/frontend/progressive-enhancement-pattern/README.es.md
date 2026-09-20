# Mejora Progresiva — Demo ejecutable

Código companion del patrón de StackPractices:
[Progressive Enhancement](https://stackpractices.com/es/patterns/progressive-enhancement-pattern/)

Una demo sin dependencias del enfoque por tres capas: una página HTML base que
funciona con JavaScript deshabilitado, una capa CSS para la presentación y una
capa JavaScript que añade validación en línea, envío asíncrono del formulario y
ordenación de tablas por clic solo tras pasar la detección de características.

## Ejecutar la demo

```bash
# cualquier servidor estático sirve; no hay paso de build
python -m http.server 8080
# abre http://localhost:8080
```

Para verificar la base, deshabilita JavaScript en DevTools y recarga: el
formulario sigue enviando y la tabla sigue renderizando.

## Ejecutar los tests

```bash
npm test
```

`validation.test.mjs` cubre las reglas de validación compartidas de
`validation.mjs` con `node:test`, sin dependencias.

## Archivos

| Archivo | Rol |
|---|---|
| `index.html` | Página base: formulario, nav y tabla que funcionan sin JS |
| `styles.css` | Capa de presentación; las reglas `.js` solo aplican con JS |
| `feature-detect.js` | Comprobaciones de capacidad (`fetch`, `IntersectionObserver`, etc.) |
| `enhance.js` | Capa de mejora: validación en línea, envío asíncrono, ordenación |
| `validation.mjs` | Reglas de validación compartidas, funciones puras |
| `validation.test.mjs` | Cobertura `node:test` de las reglas |

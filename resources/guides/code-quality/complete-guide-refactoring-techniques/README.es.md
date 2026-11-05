# Técnicas de Refactoring — Ejemplos ejecutables

Código compañero de la guía [Técnicas de Refactoring: Guía Completa](https://stackpractices.com/es/guides/complete-guide-refactoring-techniques/).

`refactoring_examples.js` contiene la función desastrosa `processOrder` y su versión refactorizada lado a lado: guard clauses, extract method, constantes con nombre y move function (la decisión de precio movida a `Customer`). Una prueba rápida al final verifica que ambas versiones producen el mismo total —esa equivalencia es el punto central del refactoring seguro.

## Ejecutar

```bash
node refactoring_examples.js
```

Salida esperada: `before: 99` y `after: 99`.

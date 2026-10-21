# Patrón State — Companion

Código de acompañamiento de la página del [Patrón State](https://stackpractices.com/es/patterns/state-pattern/).

## Resumen

El ejemplo del ciclo de vida de un pedido de la página del patrón, ejecutable en tres lenguajes: `pending -> paid -> shipped`, con `cancelled` alcanzable desde `pending` y `paid`. Cada estado es una clase que posee su comportamiento y decide las transiciones legales — sin un `switch` gigante en el contexto.

El archivo de Python incluye además la **variante dirigida por tabla** (dict `TRANSITIONS` + `InvalidTransition`) para máquinas con muchos estados y lógica por estado ligera.

## Estructura

```text
python/
└── state_pattern.py      # Implementación GoF + variante dirigida por tabla + demo de transición inválida
javascript/
└── state_pattern.js      # Implementación GoF con transiciones controladas por estado
java/
└── StatePatternDemo.java # Implementación GoF, demo autocontenida
```

## Requisitos

- Python 3.9+ (sin dependencias)
- Node.js 18+ (sin dependencias)
- JDK 17+

## Ejecutar

```bash
python python/state_pattern.py
node javascript/state_pattern.js
cd java && javac StatePatternDemo.java && java StatePatternDemo
```

Salida esperada (los tres lenguajes):

```text
Processing payment...
Shipping order...
Cannot cancel: already shipped
```

## Relacionado

- [Patrón State en StackPractices](https://stackpractices.com/es/patterns/state-pattern/) — explicación completa, compromisos, variante de tabla de transiciones y notas de testing

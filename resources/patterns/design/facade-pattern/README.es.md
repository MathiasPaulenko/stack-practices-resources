# Patrón Facade — Companion

Código de apoyo para la página del [Patrón Facade](https://stackpractices.com/es/patterns/facade-pattern/).

## Descripción

Dos ejemplos ejecutables en tres lenguajes. `VideoConverter` es el ejemplo canónico: un solo método esconde un pipeline de decoder, calculadora de bitrate, mezclador de audio y encoder. `CheckoutFacade` es la variante de producción: cinco servicios inyectados (inventario, precios, pagos, envíos y notificaciones) orquestados detrás de una única llamada `checkout()` con salidas tempranas ante fallos.

## Estructura

```text
python/
├── video_converter.py     # Facade canónico + demo de bypass al subsistema
└── checkout_facade.py     # Facade con servicios inyectados (dataclasses)
javascript/
├── video_converter.js     # Facade canónico + demo de bypass al subsistema
└── checkout_facade.js     # Facade con servicios inyectados (async)
java/
├── VideoConverter.java    # Facade canónico + demo de bypass al subsistema
└── CheckoutFacade.java    # Facade con servicios inyectados (records)
```

## Requisitos

- Python 3.9+ (sin dependencias)
- Node.js 18+ (sin dependencias)
- JDK 17+

## Ejecutar

```bash
python python/video_converter.py
python python/checkout_facade.py
node javascript/video_converter.js
node javascript/checkout_facade.js
javac java/VideoConverter.java && java -cp java VideoConverter
javac java/CheckoutFacade.java && java -cp java CheckoutFacade
```

Salida esperada: `Encoded to avi at 1024 kbps` para el conversor, y una traza paso a paso que termina en un `OrderResult` (`tx_123`, `TRK_456`) para el checkout.

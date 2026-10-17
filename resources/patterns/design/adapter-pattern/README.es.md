# Patrón Adapter — Companion

Código companion de la página del [Patrón Adapter](https://stackpractices.com/es/patterns/adapter-pattern/).

## Descripción

El ejemplo base del adapter de la página del patrón, ejecutable en tres lenguajes. `PrinterAdapter` envuelve una `OldPrinter` legacy detrás de la interfaz moderna `print()` — composición, no herencia. El archivo Python incluye además la variante bidireccional.

## Estructura

```text
python/
└── printer_adapter.py    # Adapter de objeto + BiDirectionalPrinterAdapter (variante two-way)
javascript/
└── printer_adapter.js    # Adapter de objeto
java/
└── PrinterAdapter.java   # Adapter de objeto que implementa la interfaz ModernPrinter
```

## Requisitos

- Python 3.9+ (sin dependencias)
- Node.js 18+ (sin dependencias)
- JDK 17+

## Ejecutar

```bash
python python/printer_adapter.py
node javascript/printer_adapter.js
javac java/PrinterAdapter.java && java -cp java PrinterAdapter
```

Salida esperada: `OldPrinter: Hello World` (más las líneas de la demo bidireccional en Python).

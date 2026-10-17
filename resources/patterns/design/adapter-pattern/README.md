# Adapter Pattern — Companion

Companion code for the [Adapter Pattern](https://stackpractices.com/patterns/adapter-pattern/) page.

## Overview

The base adapter example from the pattern page, runnable in three languages. `PrinterAdapter` wraps a legacy `OldPrinter` behind the modern `print()` interface — composition, not inheritance. The Python file also includes the two-way adapter variant.

## Structure

```text
python/
└── printer_adapter.py    # Object adapter + BiDirectionalPrinterAdapter (two-way variant)
javascript/
└── printer_adapter.js    # Object adapter
java/
└── PrinterAdapter.java   # Object adapter implementing a ModernPrinter interface
```

## Requirements

- Python 3.9+ (no dependencies)
- Node.js 18+ (no dependencies)
- JDK 17+

## Run

```bash
python python/printer_adapter.py
node javascript/printer_adapter.js
javac java/PrinterAdapter.java && java -cp java PrinterAdapter
```

Expected output: `OldPrinter: Hello World` (plus the two-way demo lines in Python).

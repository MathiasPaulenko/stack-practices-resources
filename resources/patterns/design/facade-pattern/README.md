# Facade Pattern — Companion

Companion code for the [Facade Pattern](https://stackpractices.com/patterns/facade-pattern/) page.

## Overview

Two runnable examples in three languages. `VideoConverter` is the canonical example: one method hides a pipeline of decoder, bitrate calculator, audio mixer, and encoder. `CheckoutFacade` is the production-style variant: five injected services (inventory, pricing, payment, shipping, notifications) orchestrated behind a single `checkout()` call with early exits on failure.

## Structure

```text
python/
├── video_converter.py     # Canonical facade + subsystem bypass demo
└── checkout_facade.py     # Facade with injected services (dataclasses)
javascript/
├── video_converter.js     # Canonical facade + subsystem bypass demo
└── checkout_facade.js     # Facade with injected services (async)
java/
├── VideoConverter.java    # Canonical facade + subsystem bypass demo
└── CheckoutFacade.java    # Facade with injected services (records)
```

## Requirements

- Python 3.9+ (no dependencies)
- Node.js 18+ (no dependencies)
- JDK 17+

## Run

```bash
python python/video_converter.py
python python/checkout_facade.py
node javascript/video_converter.js
node javascript/checkout_facade.js
javac java/VideoConverter.java && java -cp java VideoConverter
javac java/CheckoutFacade.java && java -cp java CheckoutFacade
```

Expected output: `Encoded to avi at 1024 kbps` for the converter, and a step-by-step trace ending in an `OrderResult` (`tx_123`, `TRK_456`) for the checkout.

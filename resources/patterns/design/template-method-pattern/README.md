# Template Method Pattern — Companion

Companion code for the [Template Method Pattern](https://stackpractices.com/patterns/template-method-pattern/) page.

## Overview

The data-import pipeline example from the pattern page, runnable in three languages. The base class `DataImporter` owns the algorithm skeleton — `fetch → parse → validate → save → onComplete` — and subclasses implement only the steps that vary (`fetch` and `parse`), with `onComplete` as an optional hook.

The Java version names the hook `onComplete` rather than `notify`: `Object.notify()` is final, and a method with that name will not compile.

## Structure

```text
python/
└── template_method.py        # ABC + @abstractmethod, hook override in JSONImporter
javascript/
└── template-method.js        # throws-in-base convention for abstract steps
java/
└── TemplateMethodDemo.java   # final template method, self-contained demo
```

## Requirements

- Python 3.9+ (no dependencies)
- Node.js 18+ (no dependencies)
- JDK 17+

## Run

```bash
python python/template_method.py
node javascript/template-method.js
cd java && javac TemplateMethodDemo.java && java TemplateMethodDemo
```

Expected output (all three languages):

```text
Saving: {id=1, format=csv, content=CSV content from users.csv}
Saving: {id=2, format=json, content=JSON content from users.json}
JSON import completed!
```

(Output format differs slightly per language.)

## Related

- [Template Method Pattern on StackPractices](https://stackpractices.com/patterns/template-method-pattern/) — full explanation, class diagram, variants, and the Template Method vs Strategy trade-off

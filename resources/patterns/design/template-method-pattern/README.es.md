# Patrón Template Method — Companion

Código companion de la página del [Patrón Template Method](https://stackpractices.com/es/patterns/template-method-pattern/).

## Resumen

El ejemplo del pipeline de importación de datos de la página del patrón, ejecutable en tres lenguajes. La clase base `DataImporter` controla el esqueleto del algoritmo — `fetch → parse → validate → save → onComplete` — y las subclases implementan solo los pasos que varían (`fetch` y `parse`), con `onComplete` como hook opcional.

La versión Java nombra el hook `onComplete` en lugar de `notify`: `Object.notify()` es final, y un método con ese nombre no compila.

## Estructura

```text
python/
└── template_method.py        # ABC + @abstractmethod, hook sobrescrito en JSONImporter
javascript/
└── template-method.js        # convención de lanzar en la base para pasos abstractos
java/
└── TemplateMethodDemo.java   # método template final, demo autocontenida
```

## Requisitos

- Python 3.9+ (sin dependencias)
- Node.js 18+ (sin dependencias)
- JDK 17+

## Ejecutar

```bash
python python/template_method.py
node javascript/template-method.js
cd java && javac TemplateMethodDemo.java && java TemplateMethodDemo
```

Salida esperada (los tres lenguajes):

```text
Saving: {id=1, format=csv, content=CSV content from users.csv}
Saving: {id=2, format=json, content=JSON content from users.json}
JSON import completed!
```

(El formato de salida varía ligeramente por lenguaje.)

## Relacionado

- [Patrón Template Method en StackPractices](https://stackpractices.com/es/patterns/template-method-pattern/) — explicación completa, diagrama de clases, variantes y el trade-off Template Method vs Strategy

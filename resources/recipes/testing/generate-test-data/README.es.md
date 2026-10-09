# Generar Datos de Test — Recursos complementarios

Archivos complementarios de [Generar Datos de Test (Faker + Factories)](https://stackpractices.com/es/recipes/generate-test-data/) en StackPractices.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `test_data.py` | Generadores Python: campos Faker, `UserFactory` de factory-boy, `ProductProvider` propio, estrategia Hypothesis |
| `test-data.mjs` | Generadores JavaScript: `@faker-js/faker` con semilla, factories `createUser`/`createOrder` con overrides |
| `TestDataGenerator.java` | Generadores Java: `createUser`/`createUsers` de DataFaker, provider `@MethodSource` de JUnit 5, nota de Instancio |
| `requirements.txt` | Dependencias Python |

## Cómo usarlo

1. Python: `pip install -r requirements.txt` y luego `python test_data.py`.
2. JavaScript: `npm install @faker-js/faker` y luego `node test-data.mjs`.
3. Java: añade `net.datafaker:datafaker` a tu build; `main()` imprime un usuario de ejemplo y un lote.

Siembra siempre el generador (`Faker.seed` / `faker.seed`) en el setup global de tests para que CI y local produzcan los mismos datos.
# Generate Test Data — Companion Resources

Companion files for [Generate Test Data (Faker + Factories)](https://stackpractices.com/recipes/generate-test-data/) on StackPractices.

## Files

| File | Purpose |
|------|---------|
| `test_data.py` | Python generators: Faker fields, factory-boy `UserFactory`, custom `ProductProvider`, Hypothesis strategy |
| `test-data.mjs` | JavaScript generators: seeded `@faker-js/faker`, `createUser`/`createOrder` factories with overrides |
| `TestDataGenerator.java` | Java generators: DataFaker `createUser`/`createUsers`, JUnit 5 `@MethodSource` email provider, Instancio note |
| `requirements.txt` | Python dependencies |

## How to use

1. Python: `pip install -r requirements.txt` then `python test_data.py`.
2. JavaScript: `npm install @faker-js/faker` then `node test-data.mjs`.
3. Java: add `net.datafaker:datafaker` to your build; `main()` prints a sample user and batch.

Always seed the generator (`Faker.seed` / `faker.seed`) in your global test setup so CI and local runs produce the same data.
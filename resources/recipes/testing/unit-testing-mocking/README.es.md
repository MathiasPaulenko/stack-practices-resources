# Escribir Unit Tests con Mocks y Stubs

Código complementario para [StackPractices: Unit Testing con Mocks](https://stackpractices.com/es/recipes/unit-testing-mocking/).

## Requisitos

- Node.js 20+ con Jest 29.x
- Python 3.10+ con Pytest 8.x
- Java 17+ con JUnit 5.x y Mockito 5.x

## Archivos

| Archivo | Lenguaje | Descripción |
| --------- | ----------- | ----------- |
| `payment.js` | JavaScript | Procesador de pagos con dependencia de email |
| `payment.test.js` | JavaScript | Ejemplos de mock con Jest 29.x (mockResolvedValue, mockRejectedValue) |
| `payment.py` | Python | Procesador de pagos con dependencia de email |
| `test_payment.py` | Python | Ejemplos de mock con Pytest 8.x (patch, side_effect) |
| `PaymentService.java` | Java | Servicio de pago con dependencia de email inyectada por constructor |
| `PaymentServiceTest.java` | Java | Ejemplos de stub con Mockito 5.x (mock, when, verify) |

## Uso

### JavaScript (Jest)

```bash
npm install jest
npx jest payment.test.js
```

### Python (Pytest)

```bash
pip install pytest
pytest test_payment.py
```

### Java (Mockito + JUnit 5)

```bash
# Requiere JUnit 5.x y Mockito 5.x en el classpath
javac -cp "junit-jupiter.jar:mockito-core.jar" PaymentServiceTest.java
java -jar junit-platform-console-standalone.jar -cp . -c PaymentServiceTest
```

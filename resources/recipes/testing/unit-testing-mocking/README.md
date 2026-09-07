# Write Unit Tests with Mocks and Stubs

Companion code for [StackPractices: Unit Testing with Mocks](https://stackpractices.com/recipes/unit-testing-mocking/).

## Requirements

- Node.js 20+ with Jest 29.x
- Python 3.10+ with Pytest 8.x
- Java 17+ with JUnit 5.x and Mockito 5.x

## Files

| File | Language | Description |
| ------ | ------------- | ----------- |
| `payment.js` | JavaScript | Payment processor with email dependency |
| `payment.test.js` | JavaScript | Jest 29.x mock examples (mockResolvedValue, mockRejectedValue) |
| `payment.py` | Python | Payment processor with email dependency |
| `test_payment.py` | Python | Pytest 8.x mock examples (patch, side_effect) |
| `PaymentService.java` | Java | Payment service with constructor-injected email dependency |
| `PaymentServiceTest.java` | Java | Mockito 5.x stub examples (mock, when, verify) |

## Usage

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
# Requires JUnit 5.x and Mockito 5.x on classpath
javac -cp "junit-jupiter.jar:mockito-core.jar" PaymentServiceTest.java
java -jar junit-platform-console-standalone.jar -cp . -c PaymentServiceTest
```

# Patrón Contract Testing — Código complementario

Artefactos ejecutables del [patrón Contract Testing](https://stackpractices.com/es/patterns/contract-testing-pattern/) en StackPractices.

## Archivos

| Archivo | Qué hace |
|---|---|
| `consumer.pact.test.js` | Test de consumidor con Pact (Jest) — registra interacciones, usa matchers y un provider state, escribe el archivo pact |
| `provider.verify.test.js` | Verificación del proveedor — reproduce los pacts contra la API real con `stateHandlers` para los provider states |
| `consumer_pact_test.py` | El mismo contrato de consumidor en pact-python / estilo pytest |
| `contract-tests.yml` | Workflow de GitHub Actions — el consumidor publica pacts al broker, el proveedor los verifica desde ahí |
| `can-i-deploy.sh` | Script de puerta de release — le pregunta al broker si una versión es segura para desplegar |

## Uso

```bash
# Lado del consumidor (Node)
npm i @pact-foundation/pact jest
npx jest consumer.pact.test.js          # escribe pacts/order-service-user-service.json

# Lado del proveedor: levanta la API en :3000, luego
npx jest provider.verify.test.js

# Consumidor en Python
pip install pact-python pytest
pytest consumer_pact_test.py

# Puerta de deploy
export PACT_BROKER_URL=... PACT_BROKER_TOKEN=... GIT_SHA=$(git rev-parse HEAD)
./can-i-deploy.sh order-service production
```

## Setup de provider states

El verificador llama a los `stateHandlers` (o a un endpoint `/pact-state-setup`) antes de cada reproducción para que el proveedor ponga su base de datos de test en la condición que el consumidor describió — p. ej. `a user with id 1 exists`.

## Relacionados

- Patrón: https://stackpractices.com/es/patterns/contract-testing-pattern/
- Receta (walkthrough de CI ejecutable): https://stackpractices.com/es/recipes/api-contract-testing/
- Docs de Pact: https://docs.pact.io/

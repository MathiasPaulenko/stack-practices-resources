# Pruebas de Contratos de API — Recursos complementarios

Archivos complementarios de la receta [Pruebas de Contratos de API con Consumer-Driven Contracts](https://stackpractices.com/es/recipes/api-contract-testing/) en StackPractices.com.

## Qué incluye

| Archivo | Formato | Descripción |
|---------|---------|-------------|
| `pact-consumer.test.js` | JavaScript | Test de consumidor con Pact V3 (HTTP) más un ejemplo asíncrono con `MessageConsumerPact` para contratos de eventos |
| `pact-provider.verify.test.js` | JavaScript | Configuración del `Verifier` del provider con `stateHandlers` que preparan datos para cada estado `given(...)` |
| `openapi-validate.py` | Python | Verificación provider-driven: valida la spec OpenAPI y después chequea una respuesta real contra ella |
| `contract-testing-ci.yml` | YAML | Pipeline de GitHub Actions: verificación de pacts en cada PR más un gate de despliegue `can-i-deploy` |

## Inicio rápido

### 1. Instala las dependencias

```bash
npm install --save-dev @pact-foundation/pact
pip install openapi-spec-validator openapi-core requests
```

### 2. Ejecuta el test de consumidor

```bash
npm test -- pact-consumer.test.js
```

Esto escribe los archivos pact en `pacts/`. Publícalos en tu Pact Broker con `pact-broker publish pacts/`.

### 3. Verifica el provider

Con el provider corriendo en el puerto 3000:

```bash
export PACT_BROKER_URL=https://tu-broker
export PACT_BROKER_TOKEN=...
export GIT_SHA=$(git rev-parse HEAD)
export GIT_BRANCH=$(git branch --show-current)

npm test -- pact-provider.verify.test.js
```

### 4. Protege el despliegue

Copia `contract-testing-ci.yml` en `.github/workflows/` y configura los secrets `PACT_BROKER_URL` y `PACT_BROKER_TOKEN`. `can-i-deploy` bloquea la publicación cuando un contrato de consumidor está sin verificar o falla para esa versión.

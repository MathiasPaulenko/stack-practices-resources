# Patrones de Resiliencia para Microservicios — ejemplos complementarios

Esta carpeta contiene ejemplos ejecutables de patrones de resiliencia para
la receta de StackPractices
[Patrones de Resiliencia para Microservicios](https://stackpractices.com/es/recipes/microservices-patterns/).

## Archivos

| Archivo | Descripción |
| --- | --- |
| `circuit_breaker.py` | Circuit breaker desde cero (stdlib): estados CLOSED → OPEN → HALF_OPEN |
| `retry_backoff.mjs` | `p-retry` con backoff exponencial y jitter sobre una llamada de pago |
| `saga.ts` | Orquestación de sagas: pasos con acciones de compensación en orden inverso |
| `package.json` | Dependencias y scripts de Node |
| `bulkhead.go` | Bulkhead con semáforos + `errgroup`: concurrencia acotada por dependencia |
| `go.mod` | Módulo Go para el ejemplo de bulkhead |
| `pom.xml` | Proyecto Maven para el ejemplo de Java |
| `src/main/java/ResilientPaymentClient.java` | Circuit breaker + retry + bulkhead + time limiter de Resilience4j |
| `deployment.yaml` | Deployment de Kubernetes con probes de liveness/readiness/startup |
| `health_probes.ts` | Endpoints Express que implementan los tres probes |

## Cómo ejecutar los ejemplos

### Python (solo stdlib)

```bash
python circuit_breaker.py
```

### Node.js / TypeScript

```bash
npm install
npm run retry    # necesita un endpoint del servicio de pagos
npm run saga     # conecta implementaciones de SagaStep
npm run probes   # endpoints de salud con Express
```

### Go

```bash
go mod tidy
go run bulkhead.go
```

### Java

```bash
mvn compile
# ResilientPaymentClient envuelve la llamada de pago con un circuit breaker
# (umbral de fallo del 50%, 30s abierto), 3 reintentos, un bulkhead de
# 10 llamadas y un límite de tiempo de 3s.
```

### Kubernetes

```bash
kubectl apply -f deployment.yaml
```

## Ver también

- [Patrón Circuit Breaker](https://stackpractices.com/es/recipes/circuit-breaker-pattern-recipe/)
- [Reintentos y Backoff](https://stackpractices.com/es/recipes/retry-backoff/)
- [Patrón Saga](https://stackpractices.com/es/recipes/saga-pattern/)

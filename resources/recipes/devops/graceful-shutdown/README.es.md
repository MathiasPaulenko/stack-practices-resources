# Implementar Graceful Shutdown y Reinicios sin Downtime

Código complementario para [StackPractices: Graceful Shutdown](https://stackpractices.com/es/recipes/graceful-shutdown/).

## Requisitos

- Python 3.12+ con Flask 3.x
- Node.js 20+
- Java 17+ con Spring Boot 3.x
- Go 1.22+
- Cluster de Kubernetes (para deployment.yaml)
- Nginx (para nginx.conf)
- vegeta (para pruebas de carga)

## Archivos

| Archivo | Lenguaje | Descripción |
| --------- | ----------- | ----------- |
| `app.py` | Python | App Flask 3.x con manejo de SIGTERM y drenado de ThreadPoolExecutor |
| `server.js` | JavaScript | Servidor HTTP Node 20+ con tracking de conexiones y timeout de force-close |
| `App.java` | Java | App Spring Boot 3.x con shutdown hook y config de graceful shutdown |
| `main.go` | Go | Servidor HTTP Go 1.22+ con context cancellation y cleanup de recursos |
| `deployment.yaml` | YAML | Deployment de Kubernetes con preStop hook y terminationGracePeriodSeconds |
| `nginx.conf` | Nginx | Config de upstream con health checks y slow_start para nuevas instancias |
| `test-graceful-shutdown.sh` | Bash | Script de test CI usando vegeta para prueba de carga con inyección de SIGTERM |

## Uso

### Python (Flask)

```bash
pip install flask
python app.py
```

### JavaScript (Node.js)

```bash
node server.js
```

### Java (Spring Boot)

```bash
mvn spring-boot:run
```

### Go

```bash
go run main.go
```

### Kubernetes

```bash
kubectl apply -f deployment.yaml
```

### Test CI

```bash
chmod +x test-graceful-shutdown.sh
./test-graceful-shutdown.sh
```

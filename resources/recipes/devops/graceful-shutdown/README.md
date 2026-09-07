# Implement Graceful Shutdown and Zero-Downtime Restarts

Companion code for [StackPractices: Graceful Shutdown](https://stackpractices.com/recipes/graceful-shutdown/).

## Requirements

- Python 3.12+ with Flask 3.x
- Node.js 20+
- Java 17+ with Spring Boot 3.x
- Go 1.22+
- Kubernetes cluster (for deployment.yaml)
- Nginx (for nginx.conf)
- vegeta (for load testing)

## Files

| File | Language | Description |
| ------ | ------------- | ----------- |
| `app.py` | Python | Flask 3.x app with SIGTERM handling and ThreadPoolExecutor drain |
| `server.js` | JavaScript | Node 20+ HTTP server with connection tracking and force-close timeout |
| `App.java` | Java | Spring Boot 3.x app with shutdown hook and graceful shutdown config |
| `main.go` | Go | Go 1.22+ HTTP server with context cancellation and resource cleanup |
| `deployment.yaml` | YAML | Kubernetes deployment with preStop hook and terminationGracePeriodSeconds |
| `nginx.conf` | Nginx | Upstream config with health checks and slow_start for new instances |
| `test-graceful-shutdown.sh` | Bash | CI test script using vegeta for load testing with SIGTERM injection |

## Usage

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

### CI Test

```bash
chmod +x test-graceful-shutdown.sh
./test-graceful-shutdown.sh
```

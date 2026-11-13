# Patrones concurrentes con goroutines y canales de Go — Código companion

Código companion ejecutable de la receta de StackPractices
[Patrones concurrentes con Go Goroutines y Channels](https://stackpractices.com/es/recipes/go-goroutines-channels-patterns/).

Cada archivo es un programa `package main` independiente que puedes ejecutar directamente:

```bash
go run 01-basic-goroutines.go
```

## Archivos

| Archivo | Patrón |
| --- | --- |
| `01-basic-goroutines.go` | Goroutines + canales con `sync.WaitGroup` y cierre de canal |
| `02-worker-pool.go` | Pool de trabajadores: N trabajadores leen tareas y escriben resultados |
| `03-fan-out-fan-in.go` | Fan-out a 4 trabajadores y fan-in que fusiona en un canal |
| `04-pipeline.go` | Pipeline de varias etapas: generar → filtrar → transformar → recoger |
| `05-context-timeout.go` | Cancelación con `context.WithTimeout` en el bucle del trabajador |
| `06-rate-limiting.go` | Limitación de frecuencia con `time.NewTicker` |
| `07-select-channels.go` | `select` multiplexando tick/boom/default |
| `08-errgroup.go` | Fan-out con manejo de errores usando `golang.org/x/sync/errgroup` |
| `09-bounded-semaphore.go` | Paralelismo acotado con un canal semáforo |
| `10-done-channel.go` | Cancelación con un canal `done` dedicado |
| `11-tee-channel.go` | `tee` genérico que divide un canal en dos |

## Requisitos

- Go 1.21 o posterior.
- `08-errgroup.go` necesita `golang.org/x/sync/errgroup`; ejecuta `go mod tidy` una vez para descargarlo.

## Notas

- `10-done-channel.go` es el patrón clásico de "señal de parada"; en código real prefiere `context.Context`, como en `05-context-timeout.go`.
- `07-select-channels.go` usa `time.NewTicker` con `defer ticker.Stop()` — evita `time.Tick` en programas de larga duración porque su ticker nunca puede detenerse.

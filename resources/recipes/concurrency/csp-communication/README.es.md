# Comunicación CSP — Canales, Select y Fan-out

Ejemplos ejecutables de la receta de StackPractices
[Coordinar Tareas Concurrentes con Canales CSP](https://stackpractices.com/es/recipes/csp-communication/).

CSP (Communicating Sequential Processes) reemplaza el estado mutable compartido
por paso de mensajes: las goroutines/tareas se comunican por canales en lugar
de locks. Estos ejemplos ejecutan los patrones de la receta de punta a punta.

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `pipeline.go` | Pipeline en Go (`generator` → `square` → consumidor) más workers fan-out/fan-in coordinados con `sync.WaitGroup` — el canal de resultados se cierra de forma segura cuando terminan todos los workers. |
| `select_timeout.go` | `select` multiplexando dos entradas, el truco del canal nil para desactivar casos cerrados, cancelación con `context.Context` y un caso de timeout. |
| `rust_mpsc.rs` | Productor/consumidor con `tokio::sync::mpsc` — el canal acotado te da backpressure gratis; `recv()` devuelve `None` cuando todos los emisores se sueltan. |
| `ts_pipeline.ts` | Generadores async de TypeScript como canales: un pipeline lineal más un fan-out sobre un iterador async compartido. |

## Ejecutar

```bash
go run pipeline.go
go run select_timeout.go

# Rust (necesita tokio = { version = "1", features = ["full"] } en Cargo.toml)
cargo run --bin rust_mpsc

# TypeScript
npx tsx ts_pipeline.ts
```

## Ideas clave

- El emisor cierra el canal; los receptores lo detectan con `range`/`ok`.
- `select` + `ctx.Done()` da a cada goroutine una salida limpia — sin fugas.
- Bufferea para las ráfagas, no "por si acaso": los canales sin buffer sacan a
  la luz bugs de coordinación temprano.
- Nunca cuentes receives a ciegas; usa `sync.WaitGroup` con un número fijo de
  workers.

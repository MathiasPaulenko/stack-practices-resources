# Patrón Context Object — Código complementario

Implementaciones ejecutables para el [artículo del patrón Context Object](https://stackpractices.com/es/patterns/context-object-pattern/) en StackPractices.

## Archivos

| Archivo | Lenguaje | Qué muestra |
|---------|----------|-------------|
| `context_object.py` | Python 3.10+ | dataclass `frozen` + `replace()` para copias inmutables |
| `context-object.js` | Node.js 18+ | contexto con `Object.freeze` construido en el handler |
| `ContextObjectDemo.java` | Java 11+ | contexto inmutable con builder |

## Ejecutar

```bash
python context_object.py     # → "context-object-pattern OK"
node context-object.js       # → "context-object-pattern OK"
javac ContextObjectDemo.java && java ContextObjectDemo   # → "context-object-pattern OK"
```

Cada demo construye un `RequestContext` una vez en el handler (el borde), lo pasa por la capa de servicio y devuelve un id de pedido — sin arrastrar metadatos de la petición por cada firma.

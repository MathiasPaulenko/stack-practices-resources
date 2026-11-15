# Patrón LLM Router — Código complementario

Implementaciones ejecutables del recurso [Patrón LLM Router](https://stackpractices.com/es/patterns/llm-router-pattern/) en StackPractices.

## Archivos

| Archivo | Qué muestra |
| --- | --- |
| `llm_router.py` | Demo autocontenida: clasificador de complejidad por reglas con confianza, enrutamiento de un disparo por tiers, y un `CascadeRouter` que empieza un tier abajo con confianza baja y escala por una puerta de calidad. Registra el coste enrutado contra una línea base de siempre-grande. Corre con Python 3 estándar — sin API keys. |
| `llm-router.js` | El mismo router + cascada en Node.js. |
| `LLMRouterCascade.java` | El mismo router + cascada en Java 17+ (`javac` + `java`, sin dependencias). |

## Inicio rápido

```bash
python llm_router.py
node llm-router.js
javac LLMRouterCascade.java && java LLMRouterCascade
```

Salida esperada: el router de un disparo envía consultas bajas a
`gpt-4o-mini` y medias a `gpt-4o` (~81 % más barato que siempre-grande).
La variante en cascada empieza las consultas borderline un tier abajo,
detecta las respuestas pobres y escala — misma calidad, tres llamadas
extra, ~83 % de ahorro. Todas las llamadas son mock, así que los
resultados son deterministas.

## Qué adaptar para producción

- Sustituye `mockGenerate` / `mock_generate` por llamadas reales a los
  proveedores; el contrato de enrutamiento (nivel + confianza → tier) no
  cambia.
- El clasificador por reglas es un suelo, no un techo — sube a
  clasificación por embeddings o LLM solo cuando el ahorro justifique la
  latencia añadida.
- Sesga los umbrales hacia el modelo mayor: enrutar de menos envía una
  respuesta errónea en silencio; enrutar de más solo cuesta más. Ante la
  duda, enruta arriba o usa la cascada.
- Conserva el rastreador de línea base — «coste vs. siempre-grande» es el
  número que justifica el router internamente, y no puedes afinar
  umbrales que no ves.

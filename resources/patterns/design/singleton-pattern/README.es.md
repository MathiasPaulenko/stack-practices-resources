# Patrón Singleton — ejemplos ejecutables

Complemento del artículo: https://stackpractices.com/es/patterns/singleton-pattern/

Cuatro formas de obtener exactamente una instancia, en varios lenguajes — cada archivo corre por sí solo e imprime el resultado de las aserciones.

| Archivo | Lenguaje | Enfoque |
|---------|----------|---------|
| `singleton.py` | Python | `__new__` protegido con `threading.Lock`, con la trampa del `__init__` reejecutado resuelta |
| `connection_pool.py` | Python | Singleton a nivel de módulo — la forma idiomática en Python |
| `Configuration.java` | Java | Enum singleton — thread-safe, inmune a serialización y reflexión |
| `CacheClient.java` | Java | Double-checked locking con `volatile` |
| `Registry.java` | Java | Idiom del holder de Bill Pugh + `readResolve()` para serialización |
| `registry.ts` | TypeScript | Registro con nombres / Multiton con `reset()` para tests |

## Ejecutar

```bash
python singleton.py            # Python 3.8+
python connection_pool.py

javac Configuration.java && java Configuration
javac CacheClient.java && java CacheClient
javac Registry.java && java Registry

npx ts-node registry.ts        # o: npx tsc registry.ts && node registry.js
```

## ¿Cuál usar?

- **Java**: enum primero (inmune a todo), Bill Pugh si necesitas una clase normal, DCL solo para init lazy configurable — nunca sin `volatile`.
- **Python**: instancia a nivel de módulo; evita `__new__` salvo que no quede otra — y si lo usas, protégelo con lock y guarda `__init__`.
- **TypeScript/Node**: una instancia exportada del módulo ya es un singleton; usa un registro cuando necesites instancias con nombre o resets en tests.
- **Todo lo testeable**: salta el patrón e inyecta la dependencia — vincúlala como singleton en el contenedor DI.

EN: [README.md](README.md)

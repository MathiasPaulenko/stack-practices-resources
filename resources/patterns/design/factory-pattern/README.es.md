# Patrón Factory — Ejemplos de Código

Ejemplos ejecutables del [artículo del Patrón Factory](https://stackpractices.com/es/patterns/factory-pattern/) en StackPractices.

Dos ejemplos por lenguaje:

1. **Fábrica de notificaciones** — la forma canónica: una interfaz de producto, productos concretos y una fábrica basada en registro. Los canales nuevos se añaden con `register()` en lugar de editar la fábrica.
2. **Fábrica de conexiones a bases de datos** — una variante estilo producción donde los productos llevan su propia configuración y un `Map` de creadores enruta la petición. La misma estructura que hay detrás de la carga de drivers y los sistemas de plugins.

## Archivos

| Lenguaje | Canónico | Aplicado |
| --- | --- | --- |
| Python | `python/notification_factory.py` | `python/database_factory.py` |
| JavaScript | `javascript/notification_factory.js` | `javascript/database_factory.js` |
| Java | `java/NotificationFactory.java` | `java/DatabaseFactory.java` |

## Ejecutar

```bash
python python/notification_factory.py
python python/database_factory.py

node javascript/notification_factory.js
node javascript/database_factory.js

javac java/NotificationFactory.java java/DatabaseFactory.java
java -cp java NotificationFactory
java -cp java DatabaseFactory
```

Cada ejemplo corre de forma independiente, sin dependencias de terceros.

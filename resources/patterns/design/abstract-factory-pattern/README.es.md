# Patrón Abstract Factory

Código complementario del patrón [Patrón Abstract Factory](https://stackpractices.com/es/patterns/abstract-factory-pattern/).

## Contenido

| Archivo | Qué es |
|---------|--------|
| `abstract_factory.py` | Familias de productos (`Light`/`Dark` Button+Checkbox) más un `FactoryRegistry` para selección de familia en runtime |
| `ui_factory.js` | Interfaces JavaScript, `LightUIFactory`, y un proxy `LazyUIFactory` que difiere la instanciación al primer uso |
| `UIFactory.java` | Interfaces Java, `LightUIFactory` y `FactoryLoader` para carga basada en configuración vía reflexión |

## Cómo usarlo

- Python: `python abstract_factory.py` — sin dependencias fuera de la stdlib.
- JavaScript: `node ui_factory.js`.
- Java: compila y conecta vía `FactoryLoader.loadFactory("LightUIFactory")` o instancia directamente.

Cada archivo replica una sección de la página del patrón: implementación base, selección por registro, proxy lazy y carga por reflexión.

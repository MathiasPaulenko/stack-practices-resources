# Patrón Repository — Recurso Companion

Código companion del patrón de StackPractices [Patrón Repository](https://stackpractices.com/es/patterns/repository-pattern/).

## Contenidos

- `user_repository.py` — Implementación en Python con interfaz abstracta, repositorio en memoria y servicio de dominio.
- `user_repository.js` — Implementación en JavaScript con la misma estructura.
- `UserRepository.java` — Implementación en Java con interfaz y repositorio en memoria.
- `test_repository.py` — Tests con Pytest cubriendo CRUD, filtrado y lógica del servicio.
- `meta.json` — Metadata del recurso.

## Ejecutar los tests

```bash
pip install pytest
pytest test_repository.py -v
```

## Conceptos clave

- **Interfaz de repositorio**: contrato abstracto que todas las implementaciones deben satisfacer.
- **Repositorio en memoria**: tests rápidos y determinísticos sin base de datos.
- **Servicio de dominio**: depende de la interfaz, no de la clase concreta.
- **Aggregate root**: los repositorios son por aggregate, no por entidad.

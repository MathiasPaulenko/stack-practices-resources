# Patrón Model-View-Presenter — Código complementario

Implementación ejecutable y sin dependencias del [patrón Model-View-Presenter](https://stackpractices.com/es/patterns/model-view-presenter-pattern/): un `UserDetailPresenter` contiene toda la lógica de pantalla y habla solo con una `UserDetailView` abstracta, así que los tests pueden reemplazar la GUI por una `FakeView` que registra cada llamada.

## Archivos

| Archivo | Stack | Tests |
|---------|-------|-------|
| `mvp.py` | Python stdlib (`abc`, `dataclasses`, `unittest`) | 5 casos unittest |
| `mvp.mjs` | Node.js (`node:test`, `node:assert`) | 5 casos con `node --test` |

## Ejecutar

```bash
# Python — suite de tests
python -m unittest mvp -v

# Node — suite de tests
node --test mvp.mjs
```

## Qué cubren los tests

- El camino feliz: `onLoadClicked` llega a `showUser` con los datos correctos.
- La rama de no-encontrado muestra `showError`, no una excepción.
- La entrada inválida se rechaza antes de tocar el repositorio.
- `showLoading`/`hideLoading` envuelven la búsqueda en el orden correcto.
- `hideLoading` se ejecuta igual en caso de error — la costura `finally` que las UIs reales suelen filtrar.

## Por qué una view falsa en vez de un test de UI

La fake implementa la misma interfaz que la pantalla, así que el registro de aserciones lee como lo que el usuario habría visto. Lo único que queda sin testear es el cableado — qué Activity o componente instancia el Presenter — y eso corresponde a un pequeño test de integración.

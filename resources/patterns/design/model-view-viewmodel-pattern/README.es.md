# Patrón Model-View-ViewModel (MVVM) — Recursos Companion

Ejemplos de código companion para el [Patrón MVVM](https://stackpractices.com/es/patterns/model-view-viewmodel-pattern/) en StackPractices.

## Contenidos

| Archivo | Lenguaje | Descripción |
|---------|----------|-------------|
| `python_mvvm.py` | Python | Implementación MVVM completa con TodoApp (Model, ViewModel, View) |
| `test_python_mvvm.py` | Python | Tests unitarios para TodoViewModel (pytest) |
| `JavaMVVM.java` | Java | Implementación MVVM completa con TodoApp |
| `javascript_mvvm.js` | JavaScript | Implementación MVVM completa con TodoApp |
| `test_javascript_mvvm.js` | JavaScript | Tests unitarios para TodoViewModel (Node.js assert) |

## Cómo ejecutar los ejemplos

### Python

```bash
python python_mvvm.py            # Ejecutar la TodoApp
pytest test_python_mvvm.py -v    # Ejecutar tests unitarios
```

### Java

```bash
javac JavaMVVM.java
java JavaMVVM
```

### JavaScript

```bash
node javascript_mvvm.js           # Ejecutar la TodoApp
node test_javascript_mvvm.js      # Ejecutar tests unitarios
```

## Arquitectura

```
Model (TodoRepository)  →  ViewModel (TodoViewModel)  ↔  View (TodoConsoleView)
     datos + lógica           estado observable              UI declarativa
                               + comandos                    se suscribe al VM
```

El ViewModel es framework-agnostic — podés testearlo unitariamente sin browser, dispositivo ni DOM.

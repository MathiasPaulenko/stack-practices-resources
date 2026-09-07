# Model-View-ViewModel (MVVM) Pattern — Companion Resources

Companion code examples for the [MVVM Pattern](https://stackpractices.com/patterns/model-view-viewmodel-pattern/) on StackPractices.

## Contents

| File | Language | Description |
|------|----------|-------------|
| `python_mvvm.py` | Python | Full MVVM implementation with TodoApp (Model, ViewModel, View) |
| `test_python_mvvm.py` | Python | Unit tests for TodoViewModel (pytest) |
| `JavaMVVM.java` | Java | Full MVVM implementation with TodoApp |
| `javascript_mvvm.js` | JavaScript | Full MVVM implementation with TodoApp |
| `test_javascript_mvvm.js` | JavaScript | Unit tests for TodoViewModel (Node.js assert) |

## Running the Examples

### Python

```bash
python python_mvvm.py            # Run the TodoApp
pytest test_python_mvvm.py -v    # Run unit tests
```

### Java

```bash
javac JavaMVVM.java
java JavaMVVM
```

### JavaScript

```bash
node javascript_mvvm.js           # Run the TodoApp
node test_javascript_mvvm.js      # Run unit tests
```

## Architecture

```
Model (TodoRepository)  →  ViewModel (TodoViewModel)  ↔  View (TodoConsoleView)
     data + logic              observable state              declarative UI
                                + commands                   subscribes to VM
```

The ViewModel is framework-agnostic — you can unit test it without a browser, device, or DOM.

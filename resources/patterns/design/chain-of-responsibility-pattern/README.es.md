# Patrón Chain of Responsibility

Código ejecutable complementario del patrón de StackPractices
[Patrón Chain of Responsibility](https://stackpractices.com/es/patterns/chain-of-responsibility-pattern/).

## Archivos

| Archivo | Qué muestra |
| --- | --- |
| `src/chain.py` | Python: `Handler` ABC + `AuthHandler`/`RateLimitHandler`/`DataHandler` con encadenamiento fluido `set_next`. |
| `src/chain.js` | JavaScript: la misma cadena con `setNext` y reenvío vía `super.handle`. |
| `src/Chain.java` | Java: `Handler`/`passToNext` con demo `main`. |

## Uso

```bash
python src/chain.py   # Procesada / 401 Unauthorized
node src/chain.js     # misma salida
javac src/Chain.java && java -cp src Chain
```

## Relacionados

- Página del patrón (ES): <https://stackpractices.com/es/patterns/chain-of-responsibility-pattern/>
- Página del patrón (EN): <https://stackpractices.com/patterns/chain-of-responsibility-pattern/>
- Variante middleware: <https://stackpractices.com/es/patterns/chain-of-responsibility-middleware/>

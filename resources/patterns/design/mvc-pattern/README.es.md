# Patrón MVC — Código complementario

Implementaciones Modelo-Vista-Controlador ejecutables. Fuente:
<https://stackpractices.com/es/patterns/mvc-pattern/>

## Archivos

| Archivo | Lenguaje | Qué muestra |
| --- | --- | --- |
| `mvc.py` | Python | MVC mínimo de 3 clases con un controlador que orquesta modelo + vista |
| `mvc.js` | JavaScript | La misma estructura en JS plano |
| `UserMvc.java` | Java | La misma estructura en un solo archivo (`javac UserMvc.java && java UserMvc`) |
| `dashboard.ts` | TypeScript | Caso real: el modelo notifica a sus suscriptores y la vista se re-renderiza sola — lo que hace que MVC merezca la pena |

## Ejecutar

```bash
python mvc.py
node mvc.js
javac UserMvc.java && java UserMvc
```

`dashboard.ts` apunta a una página del navegador (`document.getElementById("dashboard")`);
compila con `tsc --strict --lib es2020,dom dashboard.ts` o inclúyelo en tu bundler.

## Notas

- Mantén el modelo ignorante de las vistas — notifica, no sabe quién lo pinta.
- Las mutaciones pasan por el controlador; las vistas son de solo lectura sobre el modelo.

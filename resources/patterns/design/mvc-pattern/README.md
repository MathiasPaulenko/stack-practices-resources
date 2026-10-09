# MVC Pattern — Companion Code

Runnable Model-View-Controller implementations. Source:
<https://stackpractices.com/patterns/mvc-pattern/>

## Files

| File | Language | What it shows |
| --- | --- | --- |
| `mvc.py` | Python | Minimal 3-class MVC with a controller driving model + view |
| `mvc.js` | JavaScript | Same structure in vanilla JS |
| `UserMvc.java` | Java | Same structure, single-file runnable (`javac UserMvc.java && java UserMvc`) |
| `dashboard.ts` | TypeScript | Real case: model notifies subscribers so the view re-renders itself — the part that makes MVC worth it |

## Run

```bash
python mvc.py
node mvc.js
javac UserMvc.java && java UserMvc
```

`dashboard.ts` targets a browser page (`document.getElementById("dashboard")`);
compile with `tsc --strict --lib es2020,dom dashboard.ts` or drop it into any
bundler setup.

## Notes

- Keep the model ignorant of views — it notifies, it doesn't know.
- Mutations go through the controller; views are read-only on the model.

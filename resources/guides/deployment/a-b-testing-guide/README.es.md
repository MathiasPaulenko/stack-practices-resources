# Guía de A/B Testing: Diseño, Estadística y Errores

Recursos complementarios de la guía [Guía de A/B Testing: Diseño, Estadística y Errores](https://stackpractices.com/es/guides/a-b-testing-guide/).

## Contenido

| Archivo | Qué es |
|---------|--------|
| `sample_size.py` | Calculadora de tamaño de muestra para un test de dos proporciones (scipy): entran tasa baseline, MDE, alpha y potencia; sale el número de usuarios por grupo |
| `assignment.py` | Asignación determinista de usuarios por hash MD5 — el mismo usuario cae siempre en el mismo grupo, independiente entre experimentos |
| `analyze.py` | Análisis con z-test de dos proporciones (statsmodels): tasas, lift relativo, p-value y flag de significancia |
| `hypothesis-template.md` | Plantilla de pre-registro: hipótesis falsificable más checklist previo al lanzamiento (métrica primaria, guardrails, MDE, duración) |

## Cómo usarlo

Ejecuta `sample_size.py` antes de lanzar un test para comprobar que tu tráfico alcanza la muestra requerida. Usa `assignment.py` como función de bucketing (con un ID de usuario estable, nunca una cookie) y `analyze.py` en la fecha de fin pre-comprometida, no antes. Rellena `hypothesis-template.md` y archívalo en tu registro de experimentos antes de mirar ningún dato.

Requiere `scipy` y `statsmodels` (`pip install scipy statsmodels`).

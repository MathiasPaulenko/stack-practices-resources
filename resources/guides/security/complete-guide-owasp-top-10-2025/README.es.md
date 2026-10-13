# OWASP Top 10 2025 — Archivos complementarios

Mitigaciones ejecutables para las categorías de la guía
[Guía completa del OWASP Top 10 2025](https://stackpractices.com/es/guides/complete-guide-owasp-top-10-2025/).

## Archivos

| Archivo | Categoría | Qué hace |
| --- | --- | --- |
| `ssrf_protection.py` | A01 (SSRF dentro de control de acceso) | `SSRFProtector` valida URLs del usuario por esquema, puerto e **IP resuelta** — se comprueba la respuesta DNS, no el texto de la URL. Las redirecciones se revalidan salto a salto. |
| `access_control.py` | A01 Broken Access Control | Decoradores `require_ownership` / `require_role` que imponen autorización horizontal y vertical del lado del servidor, con adaptador para FastAPI. |
| `security_logging.py` | A09 Logging & Alerting | `SecurityLogger` emite eventos JSON estructurados y dispara alertas por ráfagas de logins fallidos por IP y por denegaciones en rutas de administración. |
| `fail_closed.py` | A10 Mishandling of Exceptional Conditions | `transfer_funds` atómica con un gestor de contexto `transaction` que hace rollback: los fallos esperados lanzan errores tipados, los inesperados propagan — nada falla abierto. |
| `test_mitigations.py` | todas | Suite de pytest que ejercita cada control. |

## Ejecutar

```bash
pip install pytest requests
pytest test_mitigations.py
```

## Notas

- El protector SSRF bloquea rangos privados/link-local **tras la resolución DNS** — validar el texto del hostname no sirve cuando `evil.com` resuelve a `169.254.169.254`.
- `access_control.py` es agnóstico de framework; el adaptador comentado para FastAPI muestra cómo integrarlo con `Depends`.
- En 2025, SSRF ya no es una categoría propia del OWASP — está dentro de A01 Broken Access Control.
